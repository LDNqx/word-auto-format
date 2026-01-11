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
  
// 统一请求地址为后端实际运行的地址（127.0.0.1:8000）
export async function classifyParagraphs(paragraphs) {
  const res = await fetch("http://127.0.0.1:8000/classify", {  // 修正地址
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({
          paragraphs
      })
  });

  if (!res.ok) {
      // 捕获后端返回的错误详情（需后端配合返回）
      const errorDetail = await res.text();
      throw new Error(`AI 语义解析失败: ${errorDetail}`);
  }

  return await res.json();
}
  