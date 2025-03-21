# Our algorithm

## technique
- In context learning (Give Eamples in prompt)
- Format Standardization (Output json)
- More test data (generated by GPT)
- Medical information injection (Explain medical terminology using MedBERT)

## install env

```bash
conda create -n Kedar_team python=3.9.20
conda activate Kedar_team
```

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

```bash
pip3 install -r requirements.txt
```

## Test our algorithm
- python report_generation_final.py
- check output at ./output_json/output.json

## Run back-end (only for UI link)
- pip install fastapi uvicorn python-multipart
- uvicorn warp_api:app --reload
- curl -X POST "http://127.0.0.1:8000/process-file/" -F "file=@anonymized/5.wav.txt"

# Testing log
## Model Testing 3/15
- Input 5.wav.txt
- Output markdown report and PDF report 

## Running models
- all code in generation.ipynb

## Have Tested
- **gpt-4o-mini**: Good, but not local running
- **llama3:8b**: Poor style, cost 1m21s
- **qwen2.5:7b**: Good, cost 1m39s
- **phi4:latest**: Good, cost 3m36s


## Model Testing 3/20

- Input 5.wav.txt
- Output json

## Running models
- all code in generation.ipynb

## Have Tested on 5.wav.txt, 6.wav.txt, 7.wav.txt
- **llama3:8b**: very Poor style
- **qwen2.5:7b**: Good
- **phi4:latest**: Good



