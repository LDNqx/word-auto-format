// src/office/applyStyle.js

/**
 * 将样式应用到Word文档的段落
 * @param {Array} styledParagraphs - 带样式信息的段落数组
 */
export async function applyStylesToDocument(styledParagraphs) {
  return Word.run(async (context) => {
    const body = context.document.body;
    const paragraphs = body.paragraphs;
    
    // 加载段落
    paragraphs.load("items");
    await context.sync();
    
    console.log(`📝 开始应用样式，共 ${paragraphs.items.length} 个段落`);
    
    let appliedCount = 0;
    let skippedCount = 0;
    
    // 遍历每个段落并应用样式
    styledParagraphs.forEach((paraData) => {
      const { pid, style } = paraData;
      
      // 确保pid在范围内
      if (pid < 0 || pid >= paragraphs.items.length) {
        console.warn(`⚠️  段落ID ${pid} 超出范围`);
        skippedCount++;
        return;
      }
      
      const para = paragraphs.items[pid];
      
      // 如果没有样式配置，跳过
      if (!style || Object.keys(style).length === 0) {
        skippedCount++;
        return;
      }
      
      // 应用字体样式
      if (style.font) {
        para.font.name = style.font;
      }
      
      // 应用字号
      if (style.size) {
        para.font.size = style.size;
      }
      
      // 应用加粗
      if (style.bold !== undefined && style.bold !== null) {
        para.font.bold = style.bold;
      }
      
      // 应用对齐方式
      if (style.align) {
        switch (style.align) {
          case "center":
            para.alignment = Word.Alignment.centered;
            break;
          case "right":
            para.alignment = Word.Alignment.right;
            break;
          case "left":
            para.alignment = Word.Alignment.left;
            break;
          case "justify":
            para.alignment = Word.Alignment.justified;
            break;
        }
      }
      
      // 应用首行缩进
      if (style.first_line_indent !== undefined && style.first_line_indent !== null) {
        para.firstLineIndent = style.first_line_indent;
      }
      
      appliedCount++;
    });
    
    // 同步所有更改到Word文档
    await context.sync();
    
    console.log(`✅ 样式应用完成！`);
    console.log(`   - 成功应用: ${appliedCount} 个段落`);
    console.log(`   - 跳过: ${skippedCount} 个段落`);
    
    return {
      success: true,
      applied: appliedCount,
      skipped: skippedCount,
      total: styledParagraphs.length
    };
  });
}


/**
 * 清除文档所有格式（可选功能）
 */
export async function clearAllFormatting() {
  return Word.run(async (context) => {
    const body = context.document.body;
    const paragraphs = body.paragraphs;
    
    paragraphs.load("items");
    await context.sync();
    
    paragraphs.items.forEach((para) => {
      // 重置为默认样式
      para.font.name = "宋体";
      para.font.size = 12;
      para.font.bold = false;
      para.alignment = Word.Alignment.left;
      para.firstLineIndent = 0;
    });
    
    await context.sync();
    
    console.log("✅ 已清除所有格式");
  });
}