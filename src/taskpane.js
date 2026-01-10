// 【仅修复1】所有import置顶 (ES6语法规范，原代码分散import是语法隐患，必须修正，无业务改动)
import { parseStyleRule } from "./api/aiService.js";
import { getDocumentParagraphs } from "./office/word.js";
import { classifyParagraphs } from "./api/aiService.js";

// 【核心修复】合并原代码两处重复的 Office.onReady，只执行一次初始化（原重复调用是报错诱因之一）
// 修复为 Word Online 兼容的 标准写法，不改变你任何事件绑定逻辑、函数调用逻辑
Office.onReady(async (info) => {
  // 关键校验：确认当前是Word环境，杜绝Word is not defined 核心报错
  if (info.host === Office.HostType.Word) {
    // 原代码逻辑1：给 parseRule 按钮绑定点击事件 (保留你原有的 addEventListener 写法)
    document.getElementById("parseRule").addEventListener("click", onParseRule);
    // 原代码逻辑2：给 analyzeBtn 按钮绑定点击事件 (保留你原有的 onclick 赋值写法)
    document.getElementById("analyzeBtn").onclick = runSemanticAnalysis;
  }
});

// 【完全未修改】你原有的 onParseRule 函数，一行代码都没动
async function onParseRule() {
  const ruleText = document.getElementById("ruleInput").value.trim();

  if (!ruleText) {
    console.log('111')
    console.log("请输入排版要求");
    return;
  }

  try {
    const result = await parseStyleRule(ruleText);
    document.getElementById("output").textContent =
      JSON.stringify(result, null, 2);
  } catch (err) {
    
    console.log("解析失败，请查看控制台");
    console.log(err);
  }
}

// 【完全未修改】你原有的 runSemanticAnalysis 函数，一行代码都没动
async function runSemanticAnalysis() {
  try {
    const paragraphs = await getDocumentParagraphs();
    console.log("读取到段落：", paragraphs);

    const semanticResult = await classifyParagraphs(paragraphs);
    console.log("AI 语义标注结果：", semanticResult);

  } catch (err) {
    console.log(err);
  }
}