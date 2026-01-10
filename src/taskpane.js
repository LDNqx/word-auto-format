import { parseStyleRule } from "./api/aiService.js";

Office.onReady(() => {
  document
    .getElementById("parseRule")
    .addEventListener("click", onParseRule);
});

async function onParseRule() {
  const ruleText = document.getElementById("ruleInput").value.trim();

  if (!ruleText) {
    console.log('111')
    alert("请输入排版要求");
    return;
  }

  try {
    const result = await parseStyleRule(ruleText);
    document.getElementById("output").textContent =
      JSON.stringify(result, null, 2);
  } catch (err) {
    console.error(err);
    alert("解析失败，请查看控制台");
  }
}

import { getDocumentParagraphs } from "./office/word.js";
import { classifyParagraphs } from "./api/aiService.js";

async function runSemanticAnalysis() {
  try {
    const paragraphs = await getDocumentParagraphs();
    console.log("读取到段落：", paragraphs);

    const semanticResult = await classifyParagraphs(paragraphs);
    console.log("AI 语义标注结果：", semanticResult);

  } catch (err) {
    console.error(err);
  }
}

Office.onReady(() => {
  document.getElementById("analyzeBtn").onclick = runSemanticAnalysis;
});
