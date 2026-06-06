import os
from dotenv import load_dotenv
import yaml

load_dotenv()

with open("static/prompt.yaml", encoding="utf-8") as f:
    prompts = yaml.safe_load(f)

class Config:
    # lay API
    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
    NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
    # ten model
    NVIDIA_MODEL_NAME = "meta/llama-3.1-70b-instruct"
    NVIDIA_MODEL_EMBEDDING = "llama-nemotron-embed-vl-1b-v2"

class Prompt:
    SUMMARIZE_SINGLE_PROMPT = prompts["summarize_single_prompt"]
    SUMMARIZE_TOTAL_PROMPT = prompts["summarize_total_prompt"]
    RETRIEVE_PROMPT = prompts["retrieve_prompt"]
