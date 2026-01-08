from fastapi import FastAPI
from pydantic import BaseModel
from style.parser import parse_style_rule
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class StyleRequest(BaseModel):
    rule_text: str

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # 允许前端5500端口访问
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法（GET/POST等）
    allow_headers=["*"],  # 允许所有请求头
)

@app.post("/parse-style")
def parse_style(req: StyleRequest):
    result = parse_style_rule(req.rule_text)
    print("AI解析排版要求:", result)
    return result
