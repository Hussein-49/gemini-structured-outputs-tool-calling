from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# 1. تعريف شكل المخرجات المطلوبة بصرامة
class AnalysisResult(BaseModel):
    summary: str = Field(description="ملخص دقيق في جملة أو جملتين فقط.")
    key_points: list[str] = Field(description="أهم النقاط الواردة صراحة في النص.")
    missing_info: list[str] = Field(description="أي معلومات أو تفاصيل غير مذكورة في النص وتم السؤال عنها أو يتوقعها القارئ.")
    is_fully_supported: bool = Field(description="True فقط إذا كانت كل النقاط مستخلصة مباشرة من النص دون افتراض.")

# 2. كتابة System Prompt منظم ومقسم
def load_prompt_file(file_path:Path):
    if not file_path.exists():
        raise FileNotFoundError(f"ملف الـ System Prompt غير موجود: {file_path}")

    content = file_path.read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError(f"ملف الـ System Prompt فارغ: {file_path}")

    return content

# افترض أن الملف system_prompt.xml موجود في نفس مجلد السكريبت
prompt_path = Path(__file__).resolve().parent / "System_Instruction.xml"
system_instruction = load_prompt_file(prompt_path)

load_dotenv()
client = genai.Client()

sample_text = """
أطلقنا تحديثاً جديداً يضيف ميزة "التذكير الذكي بالمواعيد" داخل التطبيق.
الميزة بتحلل المواعيد المكتوبة في ملاحظات المستخدم وتقترح تنبيهات تلقائية قبل الموعد بوقت كافٍ، مع إرسال إشعار فوري عند قرب الموعد.
التحديث متاح حالياً للنسخة التجريبية فقط لبعض المستخدمين.
"""

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=f"<input_text>\n{sample_text.strip()}\n</input_text>",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=AnalysisResult,
        temperature=0.1
    )
)

print(response.text)