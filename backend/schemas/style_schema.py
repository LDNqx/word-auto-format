from typing import Dict, Literal
from pydantic import BaseModel, Field


# =========================
# 单个样式定义
# =========================
class StyleItem(BaseModel):
    """
    描述一个 Word 段落样式的排版属性
    """
    font: str = Field(
        ...,
        description="字体名称，如：宋体、黑体、Times New Roman"
    )

    size: int = Field(
        ...,
        description="字号大小，单位 pt"
    )

    bold: bool = Field(
        False,
        description="是否加粗"
    )

    align: Literal["left", "center", "right"] = Field(
        "left",
        description="段落对齐方式"
    )

    first_line_indent: int = Field(
        0,
        description="首行缩进，单位 pt（如两字符=24pt）"
    )


# =========================
# 元信息
# =========================
class StyleMeta(BaseModel):
    """
    排版规则的元信息
    """
    unit: Literal["pt"] = Field(
        "pt",
        description="字号单位"
    )

    indent_unit: Literal["pt"] = Field(
        "pt",
        description="缩进单位"
    )


# =========================
# 排版规则总结构
# =========================
class StyleSchema(BaseModel):
    """
    AI 返回的完整排版规则结构
    """
    meta: StyleMeta
    styles: Dict[str, StyleItem]
