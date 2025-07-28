# filename: api/hubspot_contact_tools.py

from fastapi import APIRouter
import requests
from .hubspot_oauth_server import get_valid_access_token

router = APIRouter()

# ✅ 1. 获取简化联系人列表
@router.get("/hubspot/list_contacts_simple")
def list_contacts_simple():
    try:
        access_token = get_valid_access_token()
    except Exception as e:
        return {"error": "token 获取失败", "detail": str(e)}

    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return {"error": "获取联系人失败", "detail": resp.text}

    data = resp.json()
    simplified = []
    for item in data.get("results", []):
        props = item.get("properties", {})
        simplified.append({
            "id": item.get("id"),
            "email": props.get("email"),
            "firstname": props.get("firstname"),
            "lastname": props.get("lastname")
        })

    return {"contacts": simplified}


# ✅ 2. 获取当前 token 的 scopes
@router.get("/hubspot/get_token_scopes")
def get_token_scopes():
    try:
        access_token = get_valid_access_token()
    except Exception as e:
        return {"error": "token 获取失败", "detail": str(e)}

    url = "https://api.hubapi.com/oauth/v1/access-tokens/" + access_token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return {"error": "获取 scopes 失败", "detail": resp.text}

    return resp.json()


# ✅ 3. 列出联系人所有字段（标准 + 自定义）
@router.get("/hubspot/list_contact_fields")
def list_contact_fields():
    try:
        access_token = get_valid_access_token()
    except Exception as e:
        return {"error": "token 获取失败", "detail": str(e)}

    url = "https://api.hubapi.com/crm/v3/properties/contacts"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return {"error": "获取字段失败", "detail": resp.text}

    results = resp.json().get("results", [])
    return [
        {
            "name": prop.get("name"),
            "label": prop.get("label"),
            "fieldType": prop.get("fieldType"),
            "type": prop.get("type")
        }
        for prop in results
    ]
