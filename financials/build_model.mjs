import fs from 'node:fs/promises';
import path from 'node:path';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const root = path.resolve(import.meta.dirname, '../..');
const outDir = path.join(root, 'outputs', '01a127c8-5515-7cc1-b08b-37f95a321ae6');
await fs.mkdir(outDir, {recursive:true});
const wb = Workbook.create();
const summary = wb.worksheets.add('Summary');
const a = wb.worksheets.add('Assumptions');
const f = wb.worksheets.add('Forecast');
for (const s of [summary,a,f]) s.showGridLines=false;
const navy='#263139', amber='#FFB900', pale='#FFF2CF', dark='#202020', green='#228052';
const basic=s=>{s.getRange('A1:Z32').format.font={name:'Arial',size:10,color:dark};s.getRange('A:A').format.columnWidth=30;s.getRange('B:Z').format.columnWidth=14;s.getRange('A1:Z32').format.rowHeight=21;};
for(const s of [summary,a,f]) basic(s);

// Editable, dated plan and cost drivers.
a.getRange('A2').values=[['Crankshaft plan and voice assumptions']];
a.getRange('A2').format.font={name:'Arial',size:15,bold:true,color:dark};
a.getRange('A3:J3').values=[['Plan','Fee / month','Vehicles','New listings','Clips','AI minutes','Listing labor','Video labor','Tools and QA','Account mix']];
a.getRange('A3:J3').format={fill:navy,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'}};
a.getRange('A4:J6').values=[
  ['Launch',795,30,20,10,750,260,100,95,0.50],
  ['Growth',1295,60,40,25,1500,450,250,145,0.35],
  ['Scale',1995,100,70,50,2500,760,500,225,0.15],
];
a.getRange('B4:J6').format.fill=pale;
a.getRange('B4:J6').format.font={name:'Arial',size:10,color:'#1562A3'};
a.getRange('J4:J6').setNumberFormat('0%');
a.getRange('B4:B6').setNumberFormat('$#,##0');
a.getRange('G4:I6').setNumberFormat('$#,##0');
a.getRange('A9:B24').values=[
  ['Voice usage overage revenue (fixed zero)',0],
  ['New accounts / month, months 1–3',1],
  ['New accounts / month, months 4–12',2],
  ['New accounts / month, months 13–24',3],
  ['Monthly account churn',0.02],
  ['Expected use of included AI minutes',0.18],
  ['30k-token decisions / call (internal)',1],
  ['AI minutes / call (internal)',3],
  ['Input tokens / decision',24000],
  ['Output tokens / decision',6000],
  ['Audio input price / 1M tokens',32],
  ['Audio output price / 1M tokens',64],
  ['SignalWire transport allowance / AI min',0.05],
  ['Monthly fixed operating cost',8000],
  ['Acquisition cost / new account',500],
  ['Opening cash',50000],
];
a.getRange('B9:B24').format.fill=pale;
a.getRange('B9:B24').format.font={name:'Arial',size:10,color:'#1562A3'};
a.getRange('B13:B14').setNumberFormat('0%');
a.getRange('B19:B21').setNumberFormat('$0.00');a.getRange('B22:B24').setNumberFormat('$#,##0');
a.getRange('A26:A30').values=[['Plan mix check'],['Token cost / decision'],['Weighted plan fee'],['Weighted included AI minutes'],['Weighted listing, video and tools cost']];
a.getRange('B26:B30').formulas=[
  ['=SUM(J4:J6)'],
  ['=(B17*B19+B18*B20)/1000000'],
  ['=SUMPRODUCT(B4:B6,J4:J6)'],
  ['=SUMPRODUCT(F4:F6,J4:J6)'],
  ['=SUMPRODUCT(G4:G6,J4:J6)+SUMPRODUCT(H4:H6,J4:J6)+SUMPRODUCT(I4:I6,J4:J6)'],
];
a.getRange('B26').setNumberFormat('0%');a.getRange('B27:B28').setNumberFormat('$#,##0.00');a.getRange('B30').setNumberFormat('$#,##0');
a.getRange('D9').values=[['Proposed Crankshaft price and volume assumptions. See Business-Model.md.']];
a.getRange('D10').values=[['30,000 total measured tokens per decision; modality split still requires usage-log validation.']];
a.getRange('D11').values=[['OpenAI pricing: https://developers.openai.com/api/docs/pricing']];
a.getRange('D12').values=[['SignalWire pricing: https://signalwire.com/pricing']];
a.getRange('D13').values=[['18% expected usage = 1.5 listing-sourced calls × 3 AI minutes ÷ 25 included minutes.']];
a.getRange('D9:D13').format.columnWidth=70;
a.getRange('D9:D13').format.font={name:'Arial',size:10,color:'#595959'};

// One 24-month build. Fractional accounts are forecast expectations, not literal customers.
f.getRange('A2').values=[['24-month operating forecast (USD)']];
f.getRange('A2').format.font={name:'Arial',size:15,bold:true,color:dark};
const labels=[
  'Month','Opening accounts','New accounts','Account churn','Closing accounts','Average billable accounts',
  'Weighted monthly plan fee','Subscription revenue','Included AI minutes / account','AI verifier minutes used',
  'Minutes above plan for upgrade','Usage overage revenue (zero)','Total revenue','Internal voice cost / AI minute','Voice token + telecom cost',
  'Listing, video and tools cost','Total direct cost','Gross profit','Fixed operating cost','Acquisition cost',
  'Operating profit','Ending cash'
];
f.getRange('A3:A24').values=labels.map(x=>[x]);
f.getRange('A3:Y3').format={fill:navy,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'}};
f.getRange('A15:Y15').format.fill='#FFF3D4';
f.getRange('A20:Y20').format.fill='#E9EFEA';
f.getRange('A23:Y24').format.fill='#E5EEF1';
f.getRange('B:Y').format.columnWidth=13;
f.freezePanes.freezeRows(3);f.freezePanes.freezeColumns(1);
const cols=Array.from({length:24},(_,i)=>{let n=i+2,s='';while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26)}return s});
for(let i=0;i<24;i++){
  const c=cols[i],p=i?cols[i-1]:null;
  f.getRange(`${c}3`).values=[[new Date(Date.UTC(2026,9+i,1))]];
  f.getRange(`${c}3`).setNumberFormat('mmm-yy');
  const addRow=i<3?10:i<12?11:12;
  const formulas=[
    i?`=${p}7`:'=0',
    `=Assumptions!$B$${addRow}`,
    `=${c}4*Assumptions!$B$13`,
    `=${c}4+${c}5-${c}6`,
    `=AVERAGE(${c}4,${c}7)`,
    '=Assumptions!$B$28',
    `=${c}8*${c}9`,
    '=Assumptions!$B$29',
    `=${c}8*${c}11*Assumptions!$B$14`,
    `=MAX(0,${c}12-${c}8*${c}11)`,
    '=Assumptions!$B$9',
    `=${c}10+${c}14`,
    '=Assumptions!$B$27*Assumptions!$B$15/Assumptions!$B$16+Assumptions!$B$21',
    `=${c}12*${c}16`,
    `=${c}8*Assumptions!$B$30`,
    `=${c}17+${c}18`,
    `=${c}15-${c}19`,
    '=Assumptions!$B$22',
    `=${c}5*Assumptions!$B$23`,
    `=${c}20-${c}21-${c}22`,
    i?`=${p}24+${c}23`:`=Assumptions!$B$24+${c}23`,
  ];
  f.getRange(`${c}4:${c}24`).formulas=formulas.map(x=>[x]);
}
f.getRange('B4:Y8').setNumberFormat('#,##0.0');
f.getRange('B9:Y10').setNumberFormat('$#,##0');
f.getRange('B11:Y13').setNumberFormat('#,##0.0');
f.getRange('B14:Y15').setNumberFormat('$#,##0');
f.getRange('B16:Y16').setNumberFormat('$0.00');
f.getRange('B17:Y24').setNumberFormat('$#,##0;($#,##0);-');

summary.getRange('A2').values=[['Crankshaft operating model']];
summary.getRange('A2').format.font={name:'Arial',size:15,bold:true,color:dark};
summary.getRange('A4:D4').values=[['Metric','Year 1','Year 2','24 months']];
summary.getRange('A4:D4').format={fill:navy,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'}};
summary.getRange('A5:A11').values=[['Total revenue'],['Gross profit'],['Operating profit'],['Ending accounts'],['AI verifier minutes'],['Ending cash'],['Gross margin']];
summary.getRange('B5:D11').formulas=[
  ['=SUM(Forecast!B15:M15)','=SUM(Forecast!N15:Y15)','=SUM(Forecast!B15:Y15)'],
  ['=SUM(Forecast!B20:M20)','=SUM(Forecast!N20:Y20)','=SUM(Forecast!B20:Y20)'],
  ['=SUM(Forecast!B23:M23)','=SUM(Forecast!N23:Y23)','=SUM(Forecast!B23:Y23)'],
  ['=Forecast!M7','=Forecast!Y7','=Forecast!Y7'],
  ['=SUM(Forecast!B12:M12)','=SUM(Forecast!N12:Y12)','=SUM(Forecast!B12:Y12)'],
  ['=Forecast!M24','=Forecast!Y24','=Forecast!Y24'],
  ['=B6/B5','=C6/C5','=D6/D5'],
];
summary.getRange('A5:D5').format.fill='#FFF3D4';
summary.getRange('A7:D7').format.fill='#E5EEF1';
summary.getRange('A10:D10').format.fill='#E9EFEA';
summary.getRange('B5:D7').setNumberFormat('$#,##0;($#,##0);-');
summary.getRange('B8:D9').setNumberFormat('#,##0.0');
summary.getRange('B10:D10').setNumberFormat('$#,##0;($#,##0);-');
summary.getRange('B11:D11').setNumberFormat('0.0%');
summary.getRange('A14').values=[['Model basis']];
summary.getRange('A15').values=[['Accounts start at zero; new accounts bill for half of their first month. Churn applies to opening accounts.']];
summary.getRange('A16').values=[['Base forecast uses 18% of included AI minutes; full use is a downside stress with negative direct margin.']];
summary.getRange('A17').values=[['Internal costs include listing/video/tools, stress-case audio tokens, telecom, fixed cost and acquisition.']];
summary.getRange('A18').values=[['Cash assumes immediate collections and no tax, setup fees, capex, debt or working capital.']];
summary.getRange('A15:A18').format.columnWidth=95;
summary.getRange('A15:A18').format.font={name:'Arial',size:10,color:'#595959'};
summary.tabColor=navy;a.tabColor='#66512A';

// Exercise the plan-upgrade threshold, then restore the base input before export.
const baseOverage=f.getRange('B13').values[0][0];
a.getRange('B14').values=[[1.20]];
wb.recalculate();
const testedOverage=f.getRange('B13').values[0][0];
if(!(baseOverage===0 && testedOverage>0)) throw new Error('Upgrade threshold sensitivity did not recalculate');
if(f.getRange('B14').values[0][0]!==0) throw new Error('Minute excess must not generate usage revenue');
a.getRange('B14').values=[[0.18]];
wb.recalculate();
for(const [s,range,name] of [[summary,'A1:D18','summary'],[a,'A1:J30','assumptions'],[f,'A1:H24','forecast']]){
  const preview=await wb.render({sheetName:s.name,range,scale:1.5,format:'png'});
  await fs.writeFile(path.join(outDir,`${name}.png`),new Uint8Array(await preview.arrayBuffer()));
}
const check=await wb.inspect({kind:'table',range:'Summary!A4:D11',include:'values,formulas',tableMaxRows:12,tableMaxCols:5,maxChars:5000});
console.log(check.ndjson);
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},summary:'formula errors',maxChars:2000});
console.log(errors.ndjson);
const x=await SpreadsheetFile.exportXlsx(wb);
await x.save(path.join(outDir,'Crankshaft-24-Month-Model.xlsx'));
await fs.copyFile(path.join(outDir,'Crankshaft-24-Month-Model.xlsx'),path.join(import.meta.dirname,'Crankshaft-24-Month-Model.xlsx'));
console.log('Saved Crankshaft-24-Month-Model.xlsx');
