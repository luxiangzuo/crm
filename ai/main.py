# ai/main.py
from fastapi import APIRouter, Body
from ai.generate_sales_reply import generate_sales_reply_from_email
from hubspot.hubspot_note_writer import write_note  # ✅ 只用这个！

from fastapi import APIRouter, Body
from hubspot.hubspot_contact_editor import update_contact_fields

from hubspot.hubspot_contact_creator import router as create_router



router = APIRouter()

@router.post("/hubspot/ai_followup_note")
def ai_followup_note(data: dict = Body(...)):
    contact_id = data.get("contact_id")
    email = data.get("email")
    name = data.get("first_name", "there")

    if not contact_id or not email:
        return {"error": "缺少 contact_id 或 email"}

    try:
        followup_text = generate_sales_reply_from_email(name, email)
    except Exception as e:
        return {"error": "生成内容失败", "detail": str(e)}

    try:
        result = write_note(contact_id, followup_text)
    except Exception as e:
        return {"error": "写入 HubSpot Note 失败", "detail": str(e)}

    return {"✅ Note 写入成功": result}






@router.patch("/hubspot/update_contact")
def update_contact(data: dict = Body(...)):
    contact_id = data.get("contact_id")
    properties = data.get("properties")

    if not contact_id or not isinstance(properties, dict):
        return {"error": "缺少 contact_id 或属性不合法"}

    try:
        result = update_contact_fields(contact_id, properties)
    except Exception as e:
        return {"error": "更新联系人失败", "detail": str(e)}

    return {"✅ 联系人更新成功": result}



router.include_router(create_router)