# backend/schemas/style_schema.py

from typing import Optional, Dict
from pydantic import BaseModel, Field


class StyleItem(BaseModel):
    font: Optional[str] = Field(default=None)
    size: Optional[float] = Field(default=None)
    bold: Optional[bool] = Field(default=None)
    align: Optional[str] = Field(default=None)
    first_line_indent: Optional[float] = Field(default=None)


class StyleMeta(BaseModel):
    unit: str = "pt"
    indent_unit: str = "pt"


class StyleSchema(BaseModel):
    meta: StyleMeta
    styles: Dict[str, StyleItem]
