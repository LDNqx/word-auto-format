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
