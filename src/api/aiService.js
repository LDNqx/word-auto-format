export async function parseStyleRule(ruleText) {
    const res = await fetch("http://192.168.1.6:8000/parse-style", {
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
  
  export async function classifyParagraphs(paragraphs) {
    const res = await fetch("http://192.168.1.6:8000/classify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        paragraphs
      })
    });
  
    if (!res.ok) {
      throw new Error("AI 语义解析失败");
    }
  
    return await res.json();
  }
  