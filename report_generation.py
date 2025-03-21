import torch
import re
import json
from ollama import chat
from ollama import ChatResponse

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.cuda.empty_cache()

context = '''

Goal: Take anonymized audio notes and generate a structured report based on the extracted information. The content of the report should resemble clinical notes as closely as possible, containing patient information, FINDINGS, and comments.

You will be provided with the following examples:

Four anonymized clinical notes from sonography sessions
Corresponding anonymized audio notes (Note: Audio recordings may contain less information than the clinical notes).


anonymized audio note1: Early pregnancy LMP 4th October 2024 EDD 11th July 2025 D5 week 6 days Single intrauterine gestational sac is seen Fetal pole is not seen yet YAC sac seen Decidual reaction present No membrane separation is seen MHD 1.45 mm 1.45 cm Maturity 5 weeks 5 days Right over in normal Left over in odd scene History of removal noted

clinical note1: NAME:  DATE- 14 NOV 2024 SEX: FEMALE AGE: 31 YRS REF. BY:  UHID NO: 62576/ OP D EXAMINATION: GRAV IDU TERU S LMP- 04/10/2024 D- 5 W ks 6 Days EDD- 11/07/2025 FINDINGS:  The grav id uterus show' s smooth walled gestation al sac.  A yolk sac is seen. Foetal pole is not seen yet.  Decidual reaction seen.  No. membrane separation is seen.  MS D- 1.45 m D- 5 W ks 5 Days Right ovary normal.  Left ovary not seen. H/ O removal.  No aden ex al pathology seen.  No free fluid is seen in POD.  Comments: Early intra uterine pregnancy of age- 5 w ks 5 days

anonymized audio note2: liver is normal both kidney are normal in size and echo and both ureter are not dilated urinary bladder is well distended no calculus or mass seen uterus is normal in size the myometrial and endometrial echo are normal the endometrial cavity is empty ET 6 mm both ovaries are normal and minimal free fluid in lower abdomen

clinical note2: Name Date- 04 Dec 2024 Sex Female Age- 19 Yrs Ref. By Uni. ID- 86451/ IPD Examination: USG of Abdomen and Pelvis Findings:  The liver appears normal in size and echo. No focal or diffuse lesion is seen.  NoI HBR dilatation is seen. The portal and hepatic veins are normal.  The gall bladder is distended. No calculus or mass is seen. The wall thickness is normal.  CBD is of normal caliber.  Spleen is of normal size and echo. No focal or diffuse lesion seen.  Pancreas is normal in echo. The pancreatic duct is not dilated.  Both kidneys are normal in size and echo. The CM differentiation is preserved. No calculus or hydrone phrosis is seen. No perinephric pathology seen.  RK- 90 x 40 mm PT- 12 mm LK- 99 x 44 mm PT- 14 mm Both the ureters are not dilated.  Urinary bladder is well distended. No calculus or mass is seen.  Uterus is normal in size. The myometrial and endometrial echo are normal. The endometrial cavity is empty. ET- 6 mm.  Both ovaries are normal. No aden exal pathology is seen.  No lymph nodes seen. No obvious bowel lesion seen.  There is a minimal free fluid is seen in lower abdomen.  Comments:  Minimal free fluid in lower abdomen.  Clinical correlation and followup

anonymized audio note3:  Single live intrauterine fetus is seen in URTEX presentation. Fetal cardiac activity and movements are appreciated. FHR 136 per minute, LICAR is less, AFI 8.6 cm, placenta is posterior, left lateral, 3 vessel cord is seen. called a scene the PD 8.66 HC 32.7 AC 30.6 T FL 6.62 HL 6.07 average 35 plus 2 weight 2 4 6 9 color Doppler examination within normal limits mild oligohydronius

clinical note3: NAME:  DATE: 13 DEC 2024 SEX/ AGE: FEMALE/ 30 YRS REF. BY:  EXAM: OBSTETRICS USG LMP- 07/04/2024 D- 35 W KS 5 DAYS ED D- 12/01/2025 FINDINGS:  Single live intra ture r in e foe tus is seen in vertex presentation.  The foe tal cardiac activity and movements are appreciated. F HR- 136/ bpm.  Liquor is less. AFI- 8.6 cm.  Placenta is posterior, left lateral.  Three vessel cord is seen.  No obvious congenital anomalies are seen in the present foetal position.  Detection of anomalies depends upon the gestational age, foetal position.  amount of liquor and maternal abdominal wall thickness. Not all anomalies are detected on USG. Gender evaluation is not done as per the P CP ND T law.  The foetal parameters areas follows-  BPD 8.66 cm.  HC 32.70 cm.  AC 30.60 cm.  FL 6.62 cm.  HL 6.07 cm.  Average gestational age- 35 w ks 2 days EFB W- 2469 gm s± 10%  ART ER Y PI RI S/ D Umbilical 1.00 0.63 2.74 Right uter in e 0.61 0.40 1.67 Left uter in e 0.84 0.55 2.20 MCA 1.45 0.79 4.84 COMMENTS:  Single intra ture r in e foetus in vertex presentation with average gestational age of 35 w ks 2 days Less liquor.

anonymized audio note4:  Pelvic Ultrasound Examination Uterus is bulky, globular and shows adenomyotic changes Majors 8.5 x 6.34 x 5.7 cm Endometrial equal central and normal, ET 6.6 Both ovaries normal, no adenoxyl pathology, no free fluid is seen in pouch of Douglas Adenomyosis uterus

clinical note4: NAME SEX:  FEMALE DATE: 03 JAN 2024 REF. BY:  AGE: 22 YRS EXAMINATION: GRAV I DU TERU S UH ID NO: 80768/ OP D LMP- 15/11/2024 D- 7 W ks ED D- 22/08/2025 FINDINGS:  The gravid uterus shows smooth walled gestation al sac.  A foetal pole is seen.  Cardiac activity is appreciated.  Decidual reaction is good.  C RL- 3 mm D- 5 W ks 6 Days Tiny blood collection seen just above internal os, measuring 5.9 x 2.8 mm.  CER VIX- 4 cms No aden exal pathology seen.  No free fluid is seen in POD.  Comments:  Early intra uterine pregnancy of age- 5 W ks 6 Days Delayed conception. USG ED D- 30/08/2025 Tiny blood collection just above internal os.
'''


def generate_ollama_json(query, model_name):

    prompt = context
    prompt += f"\n\nTesting anonymized audio note: {query}\n\n"
    prompt += """Give me the corresponding report with JSON. The report should include the following fields:
    {"patient_info" :{'NAME': '',
    'DATE':'',
    'SEX':'',
    'AGE':'',
    'UHID.NO':'',
    'REF.By': '',
    'EXAMINATION': '',
    "FINDINGS":[],
    "Comments":[]
    'OTHER': {}}
    """
    prompt += "If a field of patient_info is unknown, please enter unknown\n"
    prompt += "FINDINGS and COMMENTS are lists containing multiple strings\n"
    prompt += "Do not give me any output that does not conform to JSON format\n"
    response: ChatResponse = chat(model=model_name, messages=[
      {
        'role': 'user',
        'content': prompt,
      },
    ])

    return response.message.content