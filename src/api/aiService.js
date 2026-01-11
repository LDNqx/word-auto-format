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

// 统一请求地址为后端实际运行的地址（127.0.0.1:8000）
export async function classifyParagraphs(paragraphs) {
  const res = await fetch("http://127.0.0.1:8000/classify", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      paragraphs
    })
  });

  if (!res.ok) {
    const errorDetail = await res.text();
    throw new Error(`AI 语义解析失败: ${errorDetail}`);
  }

  return await res.json();
}

/**
 * 完整的排版流程API：解析规则 + 语义分析 + 样式映射
 */
export async function applyStyleToDocument(paragraphs, ruleText) {
  const res = await fetch("http://127.0.0.1:8000/apply-style", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      paragraphs,
      rule_text: ruleText
    })
  });

  if (!res.ok) {
    const errorDetail = await res.text();
    throw new Error(`应用样式失败: ${errorDetail}`);
  }

  return await res.json();
}