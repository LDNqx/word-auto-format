# backend/semantic/style_mapper.py
"""
将语义角色映射到样式配置
"""

from typing import List, Dict, Any
from schemas.style_schema import StyleSchema

# 语义角色到样式key的映射表
ROLE_TO_STYLE_KEY = {
    # 题目
    "CN_TITLE": "CN_TITLE",
    "EN_TITLE": "EN_TITLE",
    
    # 目录
    "TOC_TITLE": "TOC_TITLE",
    "TOC_ITEM": "TOC_ITEM",
    
    # 中文摘要
    "CN_ABSTRACT_TITLE": "CN_ABSTRACT_TITLE",
    "CN_ABSTRACT_BODY": "CN_ABSTRACT_BODY",
    "CN_KEYWORDS_TITLE": "CN_KEYWORDS_TITLE",
    "CN_KEYWORDS": "CN_KEYWORDS",
    
    # 英文摘要
    "EN_ABSTRACT_TITLE": "EN_ABSTRACT_TITLE",
    "EN_ABSTRACT_BODY": "EN_ABSTRACT_BODY",
    "EN_KEYWORDS_TITLE": "EN_KEYWORDS_TITLE",
    "EN_KEYWORDS": "EN_KEYWORDS",
    
    # 正文标题
    "HEADING_1": "HEADING_1",
    "HEADING_2": "HEADING_2",
    "HEADING_3": "HEADING_3",
    "HEADING_4": "HEADING_4",
    "HEADING_5": "HEADING_5",
    
    # 正文
    "BODY_TEXT": "BODY_TEXT",
    
    # 参考文献
    "REFERENCE_TITLE": "REFERENCE_TITLE",
    "REFERENCE_CN_ITEM": "REFERENCE_ITEM",
    "REFERENCE_EN_ITEM": "REFERENCE_ITEM",
    
    # 致谢
    "ACKNOWLEDGEMENT_TITLE": "ACK_TITLE",
    "ACKNOWLEDGEMENT_TEXT": "ACK_BODY",
    
    # 附录
    "APPENDIX_TITLE": "APPENDIX_TITLE",
    "APPENDIX_TEXT": "APPENDIX_BODY",
    
    # 图表公式
    "FIGURE_TITLE": "FIGURE_TITLE",
    "TABLE_TITLE": "TABLE_TITLE",
    "TABLE_TEXT": "TABLE_TEXT",
    "FORMULA": "FORMULA",
    "FORMULA_NUMBER": "FORMULA_NUMBER",
    
    # 注释
    "FOOTNOTE_CN": "FOOTNOTE_CN",
    "FOOTNOTE_EN": "FOOTNOTE_EN",
}


def map_roles_to_styles(
    classified_paragraphs: List[Dict[str, Any]], 
    style_config: StyleSchema
) -> List[Dict[str, Any]]:
    """
    将语义角色映射到具体样式
    
    Args:
        classified_paragraphs: AI分类结果，格式: [{"pid": 0, "text": "...", "role": "..."}]
        style_config: 样式配置对象
        
    Returns:
        带样式信息的段落列表: [{"pid": 0, "text": "...", "role": "...", "style": {...}}]
    """
    result = []
    
    for para in classified_paragraphs:
        pid = para["pid"]
        text = para["text"]
        role = para["role"]
        
        # 获取样式key
        style_key = ROLE_TO_STYLE_KEY.get(role)
        
        # 从样式配置中获取具体样式
        style = None
        if style_key and style_key in style_config.styles:
            style_item = style_config.styles[style_key]
            # 转换为字典格式
            style = {
                "font": style_item.font,
                "size": style_item.size,
                "bold": style_item.bold,
                "align": style_item.align,
                "first_line_indent": style_item.first_line_indent
            }
            # 移除None值
            style = {k: v for k, v in style.items() if v is not None}
        
        result.append({
            "pid": pid,
            "text": text,
            "role": role,
            "style_key": style_key,
            "style": style
        })
    
    return result