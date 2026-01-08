export async function parseStyleRule(ruleText) {
    const res = await fetch("http://127.0.0.1:8000/parse-style", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        rule_text: ruleText
      })
    });
  
    if (!res.ok) {
      throw new Error("后端解析失败");
    }
  
    return await res.json();
  }
  