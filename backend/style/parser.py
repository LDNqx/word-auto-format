import json
from openai import OpenAI
from pydantic import ValidationError

from style.prompt import SYSTEM_PROMPT
from schemas.style_schema import StyleSchema


class StyleParseError(Exception):
    """排版规则解析失败"""
    pass


def parse_style_rule(user_input: str) -> StyleSchema:
    """
    调用 AI 解析用户输入的排版要求，返回 StyleSchema
    """
    # 1. 初始化 OpenAI 客户端（你已有可复用配置也可以抽出去）
    client = OpenAI(
        api_key="b025252e-4bdb-4957-84a7-011fd94077f5",
        base_url="https://ark.cn-beijing.volces.com/api/v3"
    )

    # 2. 构造 prompt
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    # 3. 调用模型
    try:
        response = client.chat.completions.create(
            model="doubao-seed-1-6-flash-250828",
            messages=messages,
            temperature=0,
            response_format={"type": "json_object"},
            top_p=1.0
        )
    except Exception as e:
        raise StyleParseError(f"AI 调用失败: {e}")

    # 4. 解析返回内容
    try:
        raw_content = response.choices[0].message.content
        data = json.loads(raw_content)
    except Exception as e:
        raise StyleParseError(f"AI 返回结果不是合法 JSON: {e}")

    # 5. 使用 StyleSchema 校验
    try:
        style_schema = StyleSchema.model_validate(data)
    except ValidationError as e:
        raise StyleParseError(f"排版规则结构不合法: {e}")

    return style_schema
