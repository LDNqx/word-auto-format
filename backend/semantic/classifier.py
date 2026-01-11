# backend/semantic/classifier.py
def classify_paragraphs(paragraphs: list[dict]) -> dict:
    """
    语义分类核心函数：识别每个段落的角色（标题/摘要/正文等）
    参数：paragraphs - 前端传的段落列表，格式 [{pid: int, text: str}, ...]
    返回：分类结果，格式 {"classified_paragraphs": [{pid, text, role}, ...]}
    """
    classified = []
    for para in paragraphs:
        text = para.get("text", "").strip()
        pid = para.get("pid", 0)
        role = "UNKNOWN"  # 默认未知角色

        # 简单规则匹配（后续替换为AI/LLM解析）
        if "摘要" in text:
            role = "CN_ABSTRACT_TITLE"
        elif "Abstract" in text:
            role = "EN_ABSTRACT"
        elif text.startswith(("一、", "（一）", "1.")):
            role = "HEADING_1"
        elif text.startswith(("二、", "（二）", "2.")):
            role = "HEADING_2"
        elif "参考文献" in text:
            role = "REFERENCES"
        elif "致谢" in text:
            role = "ACKNOWLEDGEMENTS"

        classified.append({
            "pid": pid,
            "text": text,
            "role": role
        })
    return {"classified_paragraphs": classified}