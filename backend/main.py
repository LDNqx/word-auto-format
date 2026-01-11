from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from style.parser import parse_style_rule
from fastapi.middleware.cors import CORSMiddleware
from semantic.classifier import classify_paragraphs

app = FastAPI()

class StyleRequest(BaseModel):
    rule_text: str

class ParagraphsRequest(BaseModel):
    paragraphs: list[dict]

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # 本地前端服务（8080端口）
        "http://127.0.0.1:8080",
        "http://localhost:8080",
        # Word加载项的在线域名（报错里的origin）
        "https://word-auto-format.pages.dev",
        # 兼容其他可能的本地调试源
        "http://127.0.0.1:5500",
        "http://localhost:5500"],  # 允许前端5500端口访问
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法（GET/POST等）
    allow_headers=["*"],  # 允许所有请求头
)

@app.post("/parse-style")
def parse_style(req: StyleRequest):
    result = parse_style_rule(req.rule_text)
    print("AI解析排版要求:", result)
    return result

@app.post("/classify")
async def classify_paragraphs_api(request: ParagraphsRequest):
    try:
        # 调用semantic/classifier.py中的核心分类函数
        classified_result = classify_paragraphs(request.paragraphs)
        return classified_result
    except Exception as e:
        # 捕获异常并返回500错误（方便调试）
        raise HTTPException(status_code=500, detail=f"语义分类失败：{str(e)}")