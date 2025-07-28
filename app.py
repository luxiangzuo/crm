# filename: app.py
from fastapi import FastAPI
from ai.main import router as ai_router
from hubspot.hubspot_oauth_server import hubspot_callback
from hubspot.hubspot_contact_tools import router as contact_tools_router

app = FastAPI()




app.include_router(contact_tools_router)

# 注册 AI 自动跟进路由
app.include_router(ai_router)

# 注册 HubSpot OAuth 回调（GET）
app.add_api_route("/hubspot/oauth/callback", hubspot_callback, methods=["GET"])
