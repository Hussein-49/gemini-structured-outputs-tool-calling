from Demos.rastest import usage
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# ربط الكود بحسابي باستخدام الـ API Key
client = genai.Client()

# ضبط التعليمات الاساسية (System Instructions) ودرجة الابداع (Temperature)
config = types.GenerateContentConfig(
    system_instruction="انت صديق مبرمج مصري شاطر، بتشرح ببساطة وبالعامية المصرية",
    temperature=0.7)

# ارسال رسالة المستخدم (User) مع تفعيل البث المباشر (Streaming)
response = client.models.generate_content_stream(
    model="gemini-3.5-flash-lite",
    contents="Tell me What is 'API' mean in 3 lines.",
    config=config)
#
print("Response: ")
last_chunk=None
for chunk in response:
    print(chunk.text, end="", flush=True)
    last_chunk=chunk

print("\n**************************************************************************************\n")

# فحص سبب توقف الرد واستهلاك التوكينز
if last_chunk:
    if last_chunk.candidates:
        print(f"Finish Reason: {last_chunk.candidates[0].finish_reason}")

    if last_chunk.usage_metadata:
        usage=last_chunk.usage_metadata
        print(f"Input Tokens: {usage.prompt_token_count}")
        print(f"Output Tokens: {usage.candidates_token_count}")
        print(f"Total Tokens: {usage.total_token_count}")

