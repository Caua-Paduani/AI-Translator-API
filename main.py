from openai import OpenAI
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
app = FastAPI()

client = OpenAI(
  api_key=OPENAI_API_KEY
)


response = client.responses.create(
  model="gpt-4o-mini",
  input="write a haiku about ai",
  store=True,
)


