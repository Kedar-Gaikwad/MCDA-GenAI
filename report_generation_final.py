import torch
import re
import json
from ollama import chat
from ollama import ChatResponse
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

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

# Function to preprocess transcript text
def preprocess_text(text, is_cased_model=False):
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize spaces
    if not is_cased_model:
        text = text.lower()  # Convert to lowercase only for uncased models
    return text

# Extract entities using MedBERT
def extract_entities_with_bert(text, model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)

    # Preprocess the text based on whether the model is cased
    is_cased = "cased" in model_name.lower()
    text = preprocess_text(text, is_cased_model=is_cased)
    
    # Perform NER and print raw output for debugging
    raw_entities = nlp(text)
    # print(f"Raw NER output from {model_name}: {raw_entities}")
    
    # Post-process entities into a structured format
    extracted_entities = []
    current_entity = ""
    current_label = ""
    
    for entity in raw_entities:
        word = entity['word'].replace("##", "")  # Handle subword tokens
        if entity['entity'].startswith('B-'):
            if current_entity:
                extracted_entities.append({"entity": current_entity, "label": current_label})
            current_entity = word
            current_label = entity['entity'][2:]  # Remove 'B-' prefix
        elif entity['entity'].startswith('I-') and current_label == entity['entity'][2:]:
            current_entity += " " + word
        else:
            if current_entity:
                extracted_entities.append({"entity": current_entity, "label": current_label})
            current_entity = ""
            current_label = ""

    if current_entity:
        extracted_entities.append({"entity": current_entity, "label": current_label})

    extracted_entities = [entitie for entitie in extracted_entities if len(entitie['entity']) > 2]

    return extracted_entities

# Generate report using LLM
def generate_ollama_json(query, model_name, entities):

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
    'OTHER': {}},
    "FINDINGS":[],
    "Comments":[]}
    """
    prompt += "If a field of patient_info is unknown, please enter unknown\n"
    prompt += "FINDINGS and COMMENTS are lists containing multiple strings\n"
    if entities is not None:
        prompt += f"Extracted entities by BERT model for reference only: {entities}.\n\n"
    prompt += "Do not give me any output that does not conform to JSON format\n"
    response: ChatResponse = chat(model=model_name, messages=[
      {
        'role': 'user',
        'content': prompt,
      },
    ])

    return response.message.content


# Main pipeline to process transcript, extract entities, and generate report
def process_transcript(content, bert_model_name, ollama_model_name):
    
    # Step 1: Extract entities using BERT-based model
    entities = extract_entities_with_bert(content, bert_model_name)
    # print(f"Extracted entities using {bert_model_name}: {entities}")

    # Step 2: Generate structured report using Ollama
    output = generate_ollama_json(content, ollama_model_name, entities)
    output_json = json.loads(output.replace("```", '')\
                         .replace("json", '').replace("```", '').strip().replace("\n", ''))
    return output_json
    

if __name__ == '__main__':
    
    # Medbert model -- ClinicalBERT-NER, Fine-tuned for clinical NER, 
    bert_model_name = "d4data/biomedical-ner-all"

    # Generation model
    ollama_model = "phi4:latest"

    # Read the transcript file
    transcript_file = "./anonymized/5.wav.txt"  # Adjust path to your transcript file
    with open(transcript_file, "r", encoding="utf-8") as file:
        content = file.read()
    print(f"Processing transcript: {content}")  # Debug: Show the input

    # Run the pipeline
    output_json = process_transcript(content, bert_model_name, ollama_model)

    with open("./output_json/output.json", "w", encoding="utf-8") as json_file:
        json.dump(output_json, json_file, ensure_ascii=False, indent=4)

    print(f"Generated report in output_file")
    





