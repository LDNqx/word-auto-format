from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from style.parser import parse_style_rule
from fastapi.middleware.cors import CORSMiddleware
from semantic.classifier import classify_paragraphs
from semantic.style_mapper import map_roles_to_styles
import traceback

app = FastAPI()

class StyleRequest(BaseModel):
    rule_text: str

class ParagraphsRequest(BaseModel):
    paragraphs: list[dict]

class ApplyStyleRequest(BaseModel):
    """完整排版请求"""
    paragraphs: list[dict]
    rule_text: str

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8080",
        "http://localhost:8080",
        "https://word-auto-format.pages.dev",
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parse-style")
def parse_style(req: StyleRequest):
    result = parse_style_rule(req.rule_text)
    print("AI解析排版要求:", result)
    return result

@app.post("/classify")
async def classify_paragraphs_api(request: ParagraphsRequest):
    try:
        print("=" * 50)
        print("收到分类请求，段落数量:", len(request.paragraphs))
        print("段落内容预览:", request.paragraphs[:2] if len(request.paragraphs) > 0 else "空")
        print("=" * 50)
        
        # 调用核心分类函数
        classified_result = classify_paragraphs(request.paragraphs)
        
        print("分类成功，返回结果")
        return classified_result
        
    except Exception as e:
        # 打印完整的错误堆栈
        print("=" * 50)
        print("❌ 分类失败，详细错误:")
        print(traceback.format_exc())
        print("=" * 50)
        raise HTTPException(status_code=500, detail=f"语义分类失败：{str(e)}")


@app.post("/apply-style")
async def apply_style_api(request: ApplyStyleRequest):
    """
    完整的排版流程：
    1. 解析用户排版规则
    2. 对段落进行语义分类
    3. 将语义角色映射到样式
    4. 返回带样式的段落列表供前端应用
    """
    try:
        print("=" * 50)
        print("🚀 开始完整排版流程")
        print(f"段落数量: {len(request.paragraphs)}")
        print(f"排版规则: {request.rule_text[:100]}...")
        print("=" * 50)
        
        # 步骤1: 解析排版规则
        print("📋 步骤1: 解析排版规则...")
        style_config = parse_style_rule(request.rule_text)
        print(f"✅ 解析完成，共 {len(style_config.styles)} 个样式规则")
        
        # 步骤2: 语义分类
        print("🔍 步骤2: 语义分类...")
        classified_result = classify_paragraphs(request.paragraphs)
        classified_paragraphs = classified_result["classified_paragraphs"]
        print(f"✅ 分类完成，共 {len(classified_paragraphs)} 个段落")
        
        # 步骤3: 映射样式
        print("🎨 步骤3: 映射样式...")
        styled_paragraphs = map_roles_to_styles(classified_paragraphs, style_config)
        
        # 统计有样式的段落数量
        styled_count = sum(1 for p in styled_paragraphs if p.get("style"))
        print(f"✅ 映射完成，{styled_count}/{len(styled_paragraphs)} 个段落有样式")
        
        print("=" * 50)
        print("🎉 排版流程完成")
        print("=" * 50)
        
        return {
            "success": True,
            "paragraphs": styled_paragraphs,
            "style_config": style_config.model_dump(),
            "statistics": {
                "total": len(styled_paragraphs),
                "styled": styled_count,
                "unstyled": len(styled_paragraphs) - styled_count
            }
        }
        
    except Exception as e:
        print("=" * 50)
        print("❌ 排版流程失败:")
        print(traceback.format_exc())
        print("=" * 50)
        raise HTTPException(status_code=500, detail=f"排版失败：{str(e)}")