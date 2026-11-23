from typing import Literal
from pydantic import BaseModel, ValidationError

# 1. تعريف الشكل المطلوب للمخرجات
class OrderExtraction(BaseModel):
    item_name: str
    quantity: int
    status: Literal["confirmed", "pending", "cancelled"]

def process_model_output(raw_json_form_llm:str) -> OrderExtraction | None:
    # 2. التحقق اثناء التشغيل (Runtime Validation)
    try:
        validated_data = OrderExtraction.model_validate_json(raw_json_form_llm)
        print("تم التحقق بنجاح: ", validated_data.model_dump())
        return validated_data

    except ValidationError as err:
        # بنلقط المشكلة بدل ما الكود يقع (مثلا الكمية رجعت نص او الحالة مش من ضمن القيم المسموحة)
        print("فشل التحقق اثناء التشغيل، تفاصيل الخطأ: ")
        print(err.json(indent=2))
        return None

# تجربة رقم 1: مخرجات مهيكلة ومطابقة للشروط
valid_response = '{"item_name": "Mechanical Keyboard", "quantity": 2, "status": "confirmed"}'
process_model_output(valid_response)

print("\n***********************************************\n")

# تجربة رقم 2: مخرجات فيها خلل
invalid_response = '{"item_name": "Mechanical Keyboard", "quantity": "two", "status": "shipped"}'
process_model_output(invalid_response)
