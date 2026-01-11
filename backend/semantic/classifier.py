import json
from typing import List, Dict, Any
from openai import OpenAI
from pydantic import ValidationError

from semantic.prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from schemas.roles import SEMANTIC_STYLE_TARGETS  # 仅保留存在的导入

# 修正异常类名称，避免与style/parser.py冲突
class ClassificationError(Exception):
    """语义分类/AI调用相关异常"""
    pass

# 初始化OpenAI客户端（与style/parser.py保持一致）
client = OpenAI(
    api_key="b025252e-4bdb-4957-84a7-011fd94077f5",
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

def classify_paragraphs(paragraphs: List[Dict]) -> Dict[str, Any]:
    if not isinstance(paragraphs, list) or len(paragraphs) == 0:
        raise ClassificationError("传入的段落列表为空或格式非法")

    try:
        # 修正占位符为paragraphs_json
        paragraphs_str = json.dumps(paragraphs, ensure_ascii=False, indent=2)
        user_prompt = USER_PROMPT_TEMPLATE.format(paragraphs_json=paragraphs_str)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    except Exception as e:
        raise ClassificationError(f"构造提示词失败: {str(e)}")

    try:
        response = client.chat.completions.create(
            model="doubao-seed-1-6-flash-250828",
            messages=messages,
            temperature=0.0,
            top_p=1.0,
            response_format={"type": "json_object"},
            timeout=30
        )
    except Exception as e:
        raise ClassificationError(f"AI接口调用失败: {str(e)}")

    try:
        ai_raw_response = response.choices[0].message.content.strip()
        ai_result = json.loads(ai_raw_response)  # AI返回格式：{pid: 角色, ...}

        # 构造前端需要的结果格式
        final_result = {
            "classified_paragraphs": []
        }
        for para in paragraphs:
            pid = para["pid"]
            # 从AI结果中获取角色（AI返回的key是字符串类型的pid）
            role = ai_result.get(str(pid), "UNKNOWN")
            # 校验角色是否在允许的列表中（可选，增强健壮性）
            if role not in SEMANTIC_STYLE_TARGETS and role != "UNKNOWN":
                role = "UNKNOWN"
            final_result["classified_paragraphs"].append({
                "pid": pid,
                "text": para["text"],
                "role": role
            })

        return final_result

    except json.JSONDecodeError:
        raise ClassificationError("AI返回结果不是合法的JSON格式")
    except Exception as e:
        raise ClassificationError(f"解析AI返回结果失败: {str(e)}")