# backend/semantic/classifier.py
import json
from typing import List, Dict, Any
from openai import OpenAI
from pydantic import ValidationError

# 导入自定义异常、提示词、角色Schema（按需）
from semantic.prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from schemas.roles import CLASSIFIED_PARAGRAPHS  # 若有角色校验Schema，需确保该文件存在
# from semantic.style_map import ROLE_MAPPING  # 若有角色映射表，按需导入

# 定义专属异常（对齐style/parser.py的异常风格）
class StyleParseError(Exception):
    """语义分类/AI调用相关异常"""
    pass

# 初始化OpenAI客户端（和style/parser.py保持一致的配置）
client = OpenAI(
    api_key="b025252e-4bdb-4957-84a7-011fd94077f5",  # 建议抽离到环境变量，和parser.py保持一致
    base_url="https://ark.cn-beijing.volces.com/api/v3"  # 火山方舟/其他AI平台地址
)

def classify_paragraphs(paragraphs: List[Dict]) -> Dict[str, Any]:
    """
    调用AI接口实现段落语义分类（参考style/parser.py逻辑）
    :param paragraphs: 前端传入的段落列表，格式 [{pid: int, text: str}, ...]
    :return: 结构化的分类结果，包含每个段落的角色信息
    """
    # 1. 校验入参合法性
    if not isinstance(paragraphs, list) or len(paragraphs) == 0:
        raise StyleParseError("传入的段落列表为空或格式非法")

    # 2. 构造AI请求的提示词（基于semantic/prompt.py）
    try:
        # 将段落列表转为JSON字符串，注入到用户提示词模板
        paragraphs_str = json.dumps(paragraphs, ensure_ascii=False, indent=2)
        user_prompt = USER_PROMPT_TEMPLATE.format(paragraphs=paragraphs_str)
        
        # 构造消息体（对齐style/parser.py的消息格式）
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    except Exception as e:
        raise StyleParseError(f"构造提示词失败: {str(e)}")

    # 3. 调用AI接口（和style/parser.py保持相同的调用参数）
    try:
        response = client.chat.completions.create(
            model="doubao-seed-1-6-flash-250828",  # 和parser.py使用的模型一致
            messages=messages,
            temperature=0.0,  # 分类任务用0温度，保证结果稳定
            top_p=1.0,
            response_format={"type": "json_object"},  # 强制返回JSON格式
            timeout=30  # 超时时间（对齐parser.py）
        )
    except Exception as e:
        raise StyleParseError(f"AI接口调用失败: {str(e)}")

    # 4. 解析AI返回结果
    try:
        # 提取AI返回的JSON字符串并解析
        ai_raw_response = response.choices[0].message.content.strip()
        ai_result = json.loads(ai_raw_response)
        
        # 5. 校验AI返回结果的Schema（若schemas/roles.py定义了校验模型）
        try:
            # 若ClassifiedParagraphs是Pydantic模型，校验结果合法性
            validated_result = ClassifiedParagraphs(**ai_result)
            # 转换为字典返回（兼容原有逻辑）
            classified_result = validated_result.model_dump()
        except (ImportError, ValidationError):
            # 若未定义Schema，直接使用原始解析结果（降级处理）
            classified_result = ai_result

        # 6. 兼容原始返回格式（保证前端能解析）
        # 确保返回结果包含classified_paragraphs字段，映射pid和role
        final_result = {
            "meta": {"status": "success", "unit": "pt"},
            "classified_paragraphs": []
        }
        # 对齐前端需要的格式：[{pid: x, text: x, role: x}, ...]
        for para in paragraphs:
            pid = para["pid"]
            # 从AI结果中匹配当前段落的角色（兼容AI返回的字段名）
            para_role = next(
                (item["role"] for item in classified_result.get("classified_paragraphs", []) if item["pid"] == pid),
                "UNKNOWN"  # 未匹配到则默认UNKNOWN
            )
            final_result["classified_paragraphs"].append({
                "pid": pid,
                "text": para["text"],
                "role": para_role
            })

        return final_result

    except json.JSONDecodeError:
        raise StyleParseError("AI返回结果不是合法的JSON格式")
    except Exception as e:
        raise StyleParseError(f"解析AI返回结果失败: {str(e)}")