import unittest

from ml.vin_lookup import decode_vin


class VinLookupTests(unittest.TestCase):
    def test_identity_does_not_become_installed_options(self):
        response = {"Results": [{
            "VIN": "1HGCM82633A004352", "ModelYear": "2003", "Make": "HONDA",
            "Model": "Accord", "Trim": "EX", "ErrorCode": "0", "ErrorText": "0 - VIN decoded clean."
        }]}
        result = decode_vin("1hgcm82633a004352", 2003, lambda _: response)
        self.assertEqual(result["status"], "decoded")
        self.assertEqual(result["identity_candidates"]["Trim"], "EX")
        self.assertEqual(result["installed_options"], [])
        self.assertFalse(result["installed_options_verified"])
        self.assertIn("modelyear=2003", result["request_url"])

    def test_bad_vin_and_decoder_error_require_attention(self):
        with self.assertRaises(ValueError):
            decode_vin("not-a-vin")
        response = {"Results": [{"ErrorCode": "8", "ErrorText": "Invalid check digit"}]}
        result = decode_vin("1HGCM82633A004352", fetch_json=lambda _: response)
        self.assertEqual(result["status"], "review_required")


if __name__ == "__main__":
    unittest.main()
