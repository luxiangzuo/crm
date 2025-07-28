好的！你刚刚发的这段 `hubspot_oauth_server.py` 是一份很干净、功能明确的 **HubSpot OAuth 授权和 token 管理工具模块**。

妎妎来逐段给你 **详细拆解 + 中文注释讲解**，让你彻底明白：

---

# 🌐 脚本名称

```python
# filename: hubspot_oauth_server.py
```

---

## 🔧 导入模块

```python
from fastapi import Request
import requests, os, json
from datetime import datetime, timedelta
```

* `Request`: FastAPI 的请求对象，用于读取 URL 中的参数（如 code）
* `requests`: 用来调用 HubSpot 的 HTTP API
* `os`, `json`: 用于保存 token 文件
* `datetime`, `timedelta`: 用来判断 token 是否过期

---

## 🔐 配置参数（Client 信息 + token 路径）

```python
CLIENT_ID = "6d980ab9-5759-42a1-a7d4-cab1caa5e74b"
CLIENT_SECRET = "b26c391d-7db2-45fd-b657-6449132f34bb"
REDIRECT_URI = "http://localhost:8000/hubspot/oauth/callback"
TOKEN_PATH = os.path.join("data", "token.json")
```

* `CLIENT_ID / SECRET`: HubSpot 应用的身份凭证
* `REDIRECT_URI`: 授权完成后回调到你的 FastAPI 路径
* `TOKEN_PATH`: 本地 token 存储路径

---

## ✅ 核心函数 1：获取有效的 access\_token

```python
def get_valid_access_token():
```

### 👇逻辑分解

1. **读取本地 token 文件**，检查是否存在
2. 提取其中的字段：`access_token`、`refresh_token`、`expires_in`、`fetched_at`
3. 用 `fetched_at + expires_in` 计算是否已过期
4. 如果过期，则：

   * 用 `refresh_token` 自动刷新
   * 覆盖 `token.json`
5. 返回有效的 `access_token`

这是整个系统的“心脏”，你每次调用 HubSpot API 都依赖这个函数。

---

## ✅ 核心函数 2：处理 OAuth 回调

```python
async def hubspot_callback(request: Request):
```

这是你在完成 OAuth 登录后，HubSpot 回调你用的接口。

### 👇逻辑：

1. 从回调 URL 中提取 `code`
2. 用 `code + client_secret` 换取 access\_token
3. 把换到的 token 保存成 `token.json`
4. 添加一个 `fetched_at` 时间戳，方便后续判断是否过期

这个函数你在 `app.py` 里注册为：

```python
app.add_api_route("/hubspot/oauth/callback", hubspot_callback, methods=["GET"])
```

---

## ✅ 核心函数 3：手动刷新 token（调试用）

```python
def refresh_access_token_manual():
```

这个函数提供一个备用手段：如果你不想等 token 过期才刷新，就可以直接手动调用。

1. 从 `token.json` 里取出 `refresh_token`
2. 调用 HubSpot API 刷新 token
3. 保存新的 token 并更新 `fetched_at`

---

## ✅ 总结功能结构图：

```text
[用户点击授权] → [HubSpot 重定向回来带 code]
                            ↓
                 hubspot_callback(code) 
                            ↓
              POST 换 access_token + 保存
                            ↓
           get_valid_access_token() → 每次用时自动检测是否过期 → 自动 refresh
                            ↓
            其它模块直接调用这个函数获取 token 就行 ✅
```

---

## ✅ 你现在这个脚本支持的能力

| 能力           | 说明                             |
| ------------ | ------------------------------ |
| ✅ 自动刷新 token | 用于长期访问 HubSpot API             |
| ✅ 回调函数注册     | 正常接收 OAuth code 并换 token       |
| ✅ 可被其它接口调用   | 比如写 note、获取联系人都可用              |
| ✅ 支持本地存储     | 所有 token 存储在 `data/token.json` |

---


### ✅ 当前 FastAPI 应用能力汇总：

| 接口     | 路径                              | 功能描述                           |
| ------ | ------------------------------- | ------------------------------ |
| `GET`  | `/hubspot/list_contacts_simple` | ✅ 获取联系人列表（含ID、姓名、邮箱）           |
| `GET`  | `/hubspot/get_token_scopes`     | ✅ 查看当前 OAuth token 权限          |
| `GET`  | `/hubspot/list_contact_fields`  | ✅ 获取联系人字段名（准备“编辑联系人”用）         |
| `POST` | `/hubspot/ai_followup_note`     | ✅ 自动生成 AI 跟进内容并写入 HubSpot Note |
| `GET`  | `/hubspot/oauth/callback`       | 🔁 授权完成后的回调逻辑                  |



---

### 🧠 你可能在问：

> “那这些功能跟我一开始说的 *AI能操作HubSpot联系人* 有什么关系？”

答：你现在就是在 **一步步地构建这个 AI 能力链条**：

1. ✅ 获取联系人信息 → 供 AI 识别上下文和用户对象
2. ✅ 获取字段列表 → 知道可以“修改哪些内容”
3. ✅ 具备写入权限 → 能真正去 HubSpot 改变联系人
4. ✅ 用 AI 生成内容或判断 → 让自动化变得“有脑子”


