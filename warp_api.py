from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from report_generation_final import process_transcript
import json

app = FastAPI()

def llm_process(text: str) -> dict:

    bert_model_name = "d4data/biomedical-ner-all"
    ollama_model = "phi4:latest"
    output_json = process_transcript(text, bert_model_name, ollama_model)
    
    return output_json

@app.post("/process-file/")
async def process_file(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    result = llm_process(text)
    return JSONResponse(content=result)
