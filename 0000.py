from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client()

print("Avalible Models")
for m in client.models.list():
    if "gemini" in m.name:
        print(m.name)

"""
Avalible Models
models/gemini-2.5-flash
models/gemini-2.5-pro
models/gemini-2.5-flash-lite
models/gemini-2.5-flash-image
models/gemini-3.1-flash-lite
models/gemini-3-pro-image
models/gemini-3.1-flash-image
models/gemini-3.1-flash-lite-image
models/gemini-nano-banana-2.1
models/gemini-3.5-flash
models/gemini-3.5-flash-lite
models/gemini-omni-flash-preview
models/gemini-3.6-flash
models/gemini-3.7-flash
models/gemini-3.8-flash
models/gemini-4-argon
models/gemini-4-carbon
models/gemini-4-hydrogen
models/gemini-4-neon
models/gemini-embedding-001
models/gemini-embedding-2
"""