from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
#from report_generation_final import process_transcript
import json

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
def llm_process(text: str) -> dict:

    # bert_model_name = "d4data/biomedical-ner-all"
    # ollama_model = "phi4:latest"
    # output_json = process_transcript(text, bert_model_name, ollama_model)
    # return output_json
    test = {
          "patient_info": {
            'NAME': 'ANONIMIZED',
            'SEX': 'FEMALE',
            'AGE': '28',
            'DATE': '15 JAN 2025',
            'UHID.NO': '',
            'REF. By': 'OBSTETRICS DEPARTMENT',
            'OTHER': {"EXAMINATION":"GRAV IDU TERUS","LMP":"15/11/2024","D":"7 WEEKS 3 DAYS", "EDD":"22/08/2025"}
          },
          "findings": ["The grav id uterus shows a smooth walled gestation al sac",
            "A fetal pole is seen with cardiac activity appreciated",
          "Decidual reaction is noted to be good",
          "CRL measures 3 mm, suggesting an estimated gestational age of approximately 5 weeks 6 days",
          "A tiny blood collection is observed just above the internal os, measuring 5.9 x 2.8 mm"
          ],
          "comments": ["Early intrauterine pregnancy estimated at about 5 weeks and 6 days. The presence of delayed conception is noted, with further examination planned for UIGDD on 30 August 2025"]
        }
    return test

@app.post("/process-file/")
async def process_file(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    result = llm_process(text)
    return JSONResponse(content=result)
