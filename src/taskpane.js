import { parseStyleRule, classifyParagraphs, applyStyleToDocument } from "./api/aiService.js";
import { getDocumentParagraphs } from "./office/word.js";
import { applyStylesToDocument, clearAllFormatting } from "./office/applyStyle.js";

Office.onReady(async (info) => {
  if (info.host === Office.HostType.Word) {
    // 绑定按钮事件
    document.getElementById("parseRule").addEventListener("click", onParseRule);
    document.getElementById("analyzeBtn").addEventListener("click", runSemanticAnalysis);
    document.getElementById("applyBtn").addEventListener("click", applyFormatting);
    document.getElementById("clearBtn").addEventListener("click", showClearConfirm);
    
    // 绑定模态框按钮
    document.getElementById("cancelBtn").addEventListener("click", hideClearConfirm);
    document.getElementById("confirmBtn").addEventListener("click", confirmClearFormatting);
    
    // 点击模态框外部关闭
    document.getElementById("confirmModal").addEventListener("click", (e) => {
      if (e.target.id === "confirmModal") {
        hideClearConfirm();
      }
    });
    
    console.log("✅ Word 加载项初始化完成");
  }
});

/**
 * 解析排版规则（测试用）
 */
async function onParseRule() {
  console.log("🔵 onParseRule 函数被调用");
  
  const ruleText = document.getElementById("ruleInput").value.trim();
  console.log("📝 规则文本:", ruleText);

  if (!ruleText) {
    showMessage("请输入排版要求", "error");
    return;
  }

  try {
    showMessage("正在解析排版规则...", "info");
    console.log("📡 准备调用 parseStyleRule...");
    const result = await parseStyleRule(ruleText);
    console.log("✅ 后端返回:", result);
    
    document.getElementById("output").textContent = JSON.stringify(result, null, 2);
    showMessage("解析成功！", "success");
  } catch (err) {
    showMessage("解析失败: " + err.message, "error");
    console.error(err);
  }
}

/**
 * 执行语义分析（测试用）
 */
async function runSemanticAnalysis() {
  console.log("🔵 runSemanticAnalysis 函数被调用");
  
  try {
    showMessage("正在读取文档段落...", "info");
    console.log("📖 准备读取段落...");
    const paragraphs = await getDocumentParagraphs();
    console.log("✅ 读取到段落：", paragraphs);

    showMessage(`正在分析 ${paragraphs.length} 个段落...`, "info");
    console.log("📡 准备调用 classifyParagraphs...");
    const semanticResult = await classifyParagraphs(paragraphs);
    console.log("✅ AI 语义标注结果：", semanticResult);
    
    document.getElementById("output").textContent = 
      JSON.stringify(semanticResult, null, 2);
    showMessage("语义分析完成！", "success");
  } catch (err) {
    showMessage("分析失败: " + err.message, "error");
    console.error(err);
  }
}

/**
 * 应用格式（核心功能）
 */
async function applyFormatting() {
  const ruleText = document.getElementById("ruleInput").value.trim();

  if (!ruleText) {
    showMessage("请先输入排版要求", "error");
    return;
  }

  try {
    // 步骤1: 读取文档段落
    showMessage("📖 正在读取文档...", "info");
    const paragraphs = await getDocumentParagraphs();
    console.log(`读取到 ${paragraphs.length} 个段落`);
    
    if (paragraphs.length === 0) {
      showMessage("文档中没有段落", "error");
      return;
    }

    // 步骤2: 调用后端完整流程
    showMessage(`🤖 正在分析和处理 ${paragraphs.length} 个段落...`, "info");
    const result = await applyStyleToDocument(paragraphs, ruleText);
    
    console.log("后端返回结果：", result);

    // 步骤3: 应用样式到Word文档
    showMessage("🎨 正在应用样式到文档...", "info");
    const applyResult = await applyStylesToDocument(result.paragraphs);
    
    // 显示结果
    const stats = result.statistics;
    const message = `
✅ 排版完成！
━━━━━━━━━━━━━━━━
📊 统计信息：
   • 总段落数: ${stats.total}
   • 已应用样式: ${stats.styled}
   • 未应用样式: ${stats.unstyled}
━━━━━━━━━━━━━━━━
    `.trim();
    
    document.getElementById("output").textContent = message;
    showMessage("排版成功！", "success");
    
  } catch (err) {
    showMessage("排版失败: " + err.message, "error");
    console.error("详细错误:", err);
  }
}

/**
 * 显示清除格式确认对话框
 */
function showClearConfirm() {
  document.getElementById("confirmModal").style.display = "block";
}

/**
 * 隐藏清除格式确认对话框
 */
function hideClearConfirm() {
  document.getElementById("confirmModal").style.display = "none";
}

/**
 * 确认清除所有格式
 */
async function confirmClearFormatting() {
  hideClearConfirm();
  
  try {
    showMessage("正在清除格式...", "info");
    await clearAllFormatting();
    showMessage("格式已清除", "success");
  } catch (err) {
    showMessage("清除失败: " + err.message, "error");
    console.error(err);
  }
}

/**
 * 显示消息提示
 */
function showMessage(text, type = "info") {
  console.log(`[${type.toUpperCase()}] ${text}`);
  
  // 可选：在界面上显示消息
  const outputEl = document.getElementById("output");
  if (outputEl) {
    const timestamp = new Date().toLocaleTimeString();
    const prefix = type === "error" ? "❌" : type === "success" ? "✅" : "ℹ️";
    outputEl.textContent = `${prefix} [${timestamp}] ${text}`;
  }
}