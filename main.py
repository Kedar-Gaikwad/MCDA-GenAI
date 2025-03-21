from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from report_generation import generate_ollama_json
import json

app = FastAPI()

def llm_process(text: str) -> dict:

    model_name = 'phi4:latest'

    output = generate_ollama_json(text, model_name)
    output_json = json.loads(output.replace("```", '')\
                            .replace("json", '').replace("```", '').strip().replace("\n", ''))
    return output_json

@app.post("/process-file/")
async def process_file(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    result = llm_process(text)
    return JSONResponse(content=result)
