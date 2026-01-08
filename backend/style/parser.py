from openai import OpenAI
from .prompt import SYSTEM_PROMPT

client = OpenAI(
    api_key="b025252e-4bdb-4957-84a7-011fd94077f5",
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

def parse_style_rule(rule_text: str) -> dict:
    response = client.chat.completions.create(
        model="doubao-seed-1-6-flash-250828",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": rule_text}
        ],
        temperature=0,
        response_format={"type": "json_object"},
        top_p=1.0
    )

    return response.choices[0].message.content
