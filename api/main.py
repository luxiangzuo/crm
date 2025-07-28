# api/main.py
from fastapi import FastAPI, Request
from ai.generate_sales_reply import generate_sales_reply_from_email
from ai.main import router

app = FastAPI()
app.include_router(router)
@app.get("/")
def home():
    return {"msg": "API is running."}

@app.post("/reply")
async def generate_reply(req: Request):
    data = await req.json()
    name = data.get("name", "Customer")
    email_text = data.get("email", "")

    reply = generate_sales_reply_from_email(name, email_text)
    return {"reply": reply}
