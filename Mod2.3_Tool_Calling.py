import json
from pydantic import BaseModel

# 1. الدالة الحقيقة اللي بتنفذ الشغل في الكود
def get_weather(city:str) -> str:
    # في الواقع هنا بنكلم API الطقس، بس هنحاكيها برقم ثابت
    fake_db = {"Alexandria": "22C, Sunny", "Cairo": "26C, Clear"}
    return fake_db.get(city, "Data Not available")

# 2. الاسكيما اللي بنوصف بيها مخرجات الاداه للموديل
class WeatherToolArgs(BaseModel):
    city:str

# 3. محاكاه لرد الموديل لما يقرر يستدعي الاداة (Structured Output)
llm_tool_call_response = '{"tool_name": "get_weather", "arguments": {"city": "Alexandria"}}'

# 4. دور الكود: فك الرد، التحقق من المدخلات، ثم التنفيذ
parsed_call = json.loads(llm_tool_call_response)

if parsed_call["tool_name"] == "get_weather":
    # التحقق اثناء التشغيل
    validated_args = WeatherToolArgs(**parsed_call["arguments"])
    # تنفيذ الدالة الحقيقية
    tool_result = get_weather(validated_args.city)
    print("Tool Result: ", tool_result)