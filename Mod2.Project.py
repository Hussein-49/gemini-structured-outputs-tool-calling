from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError

load_dotenv()

# ---------------------------------------------------------
# الخطوة 1: تعريف الـ Schema (Structured Output / Tool Args)
# ---------------------------------------------------------
# هنا بنحدد شكل المدخلات اللي الأداة محتاجاها بدقة:
# السعر لازم يكون رقم موجب، ونسبة الخصم بين 0 و 100
class DiscountInput(BaseModel):
    original_price: float = Field(..., gt=0, description="السعر الأصلي للمنتج")
    discount_percent: float = Field(..., gt=0, description="نسبة الخصم من 0 إلى 100")


# ---------------------------------------------------------
# الخطوة 2: الدالة الفعلية اللي الكود بتاعك هينفذها
# ---------------------------------------------------------
def calculate_discount(original_price: float, discount_percent: float) -> dict:
    final_price = original_price - (original_price*(discount_percent/100))
    save_amount = original_price - final_price
    return {
        "original_price": original_price,
        "discount_persent": discount_percent,
        "save_amount": round(save_amount, 2),
        "final_price": round(final_price, 2)
    }

# ---------------------------------------------------------
# الخطوة 3: تعريف الأداة للموديل باستخدام JSON Schema من Pydantic
# ---------------------------------------------------------
discount_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="calculate_discount",
            description="تحسب السعر النهائي بعد الخصم وقيمة التوفير",
            parameters_json_schema=DiscountInput.model_json_schema()
        )
    ]
)

client = genai.Client()
user_prompt = "لو في كيبورد سعره 1500 جنيه وعليه خصم 20%، هيكون بكام بعد الخصم؟"

# ---------------------------------------------------------
# الخطوة 4: إرسال السؤال والأداة للموديل
# ---------------------------------------------------------
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=user_prompt,
    config=types.GenerateContentConfig(
        tools=[discount_tool],
        temperature=0 # تقليل العشوائية عشان الالتزام بالشكل يكون أعلى
    )
)

# ---------------------------------------------------------
# الخطوة 5: استقبال طلب الأداة + Runtime Validation + التنفيذ
# ---------------------------------------------------------
if response.function_calls:
    call = response.function_calls[0]
    print(f"الموديل قرر يستدعي أداة: {call.name}")
    print(f"البيانات اللي بعتها الموديل: {call.args}")

    if call.name == "calculate_discount":
        try:
            # التحقق أثناء التشغيل (Runtime Validation) باستخدام Pydantic
            validated_args = DiscountInput.model_validate(call.args)

            # تنفيذ الدالة الحقيقية في كودك بعد ما تأكدنا إن البيانات سليمة
            tool_output = calculate_discount(
                original_price=validated_args.original_price,
                discount_percent=validated_args.discount_percent
            )
            print("نتيجة التنفيذ الفعلي:", tool_output)

            # -------------------------------------------------
            # الخطوة 6: إرجاع نتيجة الأداة للموديل لصياغة الرد النهائي
            # -------------------------------------------------
            conversation = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=user_prompt)]
                ),
                response.candidates[0].content,
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=call.name,
                            response={"result": tool_output}
                        )
                    ]
                )
            ]

            final_response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=conversation,
                config=types.GenerateContentConfig(tools=[discount_tool])
            )
            print("\nالرد النهائي للمستخدم:\n", final_response.text)

        except ValidationError as e:
            # لو الموديل بعت بيانات مخالفة للـ Schema (مثلاً خصم 150% أو سعر سالب)
            print("فشل التحقق أثناء التشغيل (Runtime Validation):", e.json())
    else:
        print("الموديل رد مباشرة بدون أداة:\n", response.text)
