import json
from typing import List, Dict, Any
from openai import OpenAI

from semantic.prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from schemas.roles import SEMANTIC_STYLE_TARGETS

class ClassificationError(Exception):
    """语义分类/AI调用相关异常"""
    pass

# 初始化OpenAI客户端
client = OpenAI(
    api_key="b025252e-4bdb-4957-84a7-011fd94077f5",
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

def classify_paragraphs(paragraphs: List[Dict]) -> Dict[str, Any]:
    """
    调用AI对段落进行语义分类
    
    Args:
        paragraphs: 段落列表，每个段落包含 pid 和 text
        
    Returns:
        分类结果，格式: {"classified_paragraphs": [{"pid": 0, "text": "...", "role": "..."}]}
    """
    # 1. 输入校验
    if not isinstance(paragraphs, list):
        raise ClassificationError(f"传入参数类型错误，期望 list，实际为 {type(paragraphs)}")
    
    if len(paragraphs) == 0:
        raise ClassificationError("传入的段落列表为空")
    
    # 2. 构造提示词
    try:
        paragraphs_str = json.dumps(paragraphs, ensure_ascii=False, indent=2)
        user_prompt = USER_PROMPT_TEMPLATE.format(paragraphs_json=paragraphs_str)
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        
        print(f"📝 准备调用AI，段落数量: {len(paragraphs)}")
        
    except Exception as e:
        raise ClassificationError(f"构造提示词失败: {str(e)}")
    
    # 3. 调用AI
    try:
        # 根据段落数量动态设置超时时间
        # 基础 60 秒 + 每 10 个段落额外 30 秒
        dynamic_timeout = 60 + (len(paragraphs) // 10) * 30
        print(f"⏱️  设置超时时间: {dynamic_timeout} 秒")
        
        response = client.chat.completions.create(
            model="doubao-seed-1-6-flash-250828",
            messages=messages,
            temperature=0.0,
            top_p=1.0,
            response_format={"type": "json_object"},
            timeout=dynamic_timeout
        )
        print("✅ AI 调用成功")
        
    except Exception as e:
        raise ClassificationError(f"AI接口调用失败: {str(e)}")
    
    # 4. 解析AI返回结果
    try:
        ai_raw_response = response.choices[0].message.content.strip()
        print(f"📄 AI 原始返回: {ai_raw_response[:200]}...")  # 只打印前200字符
        
        ai_result = json.loads(ai_raw_response)
        
        # 检查AI返回格式
        if not isinstance(ai_result, dict):
            raise ClassificationError(f"AI返回格式错误，期望对象，实际为 {type(ai_result)}")
        
    except json.JSONDecodeError as e:
        raise ClassificationError(f"AI返回结果不是合法的JSON: {str(e)}\n原始内容: {ai_raw_response[:500]}")
    except Exception as e:
        raise ClassificationError(f"解析AI返回结果失败: {str(e)}")
    
    # 5. 构造前端所需的结果格式
    try:
        final_result = {
            "classified_paragraphs": []
        }
        
        for para in paragraphs:
            pid = para.get("pid")
            text = para.get("text", "")
            
            if pid is None:
                print(f"⚠️  警告：段落缺少 pid 字段: {para}")
                continue
            
            # 从AI结果中获取角色（AI返回的key可能是字符串或整数）
            role = ai_result.get(str(pid)) or ai_result.get(pid) or "UNKNOWN"
            
            # 校验角色是否合法
            if role not in SEMANTIC_STYLE_TARGETS:
                print(f"⚠️  警告：AI返回了非法角色 '{role}' (pid={pid})，已重置为 UNKNOWN")
                role = "UNKNOWN"
            
            final_result["classified_paragraphs"].append({
                "pid": pid,
                "text": text,
                "role": role
            })
        
        print(f"✅ 分类完成，共处理 {len(final_result['classified_paragraphs'])} 个段落")
        return final_result
        
    except Exception as e:
        raise ClassificationError(f"构造最终结果失败: {str(e)}")