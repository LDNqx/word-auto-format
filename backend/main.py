from fastapi import FastAPI
from pydantic import BaseModel
from style.parser import parse_style_rule

app = FastAPI()

class StyleRequest(BaseModel):
    rule_text: str

@app.post("/parse-style")
def parse_style(req: StyleRequest):
    result = parse_style_rule(req.rule_text)
    print(result)
    return result
