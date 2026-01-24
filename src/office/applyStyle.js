// src/office/applyStyle.js

/**
 * 样式字段 → Office JS 应用函数 的声明式映射表
 * 只放 Office JS 真正支持、且是“样式级”的能力
 */
const STYLE_APPLIERS = {
  /* ===== 基础字形字体类 ===== */

  font: (para, value) => {
    para.font.name = value;
  },

  size: (para, value) => {
    para.font.size = value;
  },

  bold: (para, value) => {
    para.font.bold = value;
  },

  italic: (para, value) => {
    para.font.italic = value;
  },

  /* ===== 对齐方式类 ===== */

  align: (para, value) => {
    const ALIGN_MAP = {
      center: Word.Alignment.centered,
      left: Word.Alignment.left,
      right: Word.Alignment.right,
      justify: Word.Alignment.justified,
    };

    if (ALIGN_MAP[value]) {
      para.alignment = ALIGN_MAP[value];
    }
  },

  /* ===== 行 / 段间距类 ===== */

  line_spacing: (para, value) => {
    para.lineSpacing = value;
  },

  space_before: (para, value) => {
    para.spaceBefore = value;
  },

  space_after: (para, value) => {
    para.spaceAfter = value;
  },

  /* ===== 缩进类 ===== */

  first_line_indent: (para, value) => {
    para.firstLineIndent = value;
  },

  hanging_indent: (para, value) => {
    para.leftIndent = value;
    para.firstLineIndent = -value;
  },

  /* ===== 特殊标注类 ===== */

  superscript: (para, value) => {
    para.font.superscript = value;
  },

  /* ===== 布局类 ===== */

  page_break_before: (para, value) => {
    if (value === true) {
      para.insertBreak(Word.BreakType.page, Word.InsertLocation.before);
    }
  },
};

/**
 * 通用样式应用器
 * @param {Word.Paragraph} para
 * @param {Object} style
 */
function applyStyleToParagraph(para, style) {
  Object.entries(style).forEach(([key, value]) => {
    // null / undefined 一律跳过
    if (value === undefined || value === null) return;

    const applier = STYLE_APPLIERS[key];
    if (!applier) {
      console.warn(`⚠️ 不支持的样式字段: ${key}`);
      return;
    }

    try {
      applier(para, value);
    } catch (err) {
      console.error(`❌ 应用样式失败: ${key}`, err);
    }
  });
}

/**
 * 将样式应用到 Word 文档的段落
 * @param {Array} styledParagraphs - [{ pid, style }]
 */
export async function applyStylesToDocument(styledParagraphs) {
  return Word.run(async (context) => {
    const body = context.document.body;
    const paragraphs = body.paragraphs;

    paragraphs.load("items");
    await context.sync();

    console.log(`📝 开始应用样式，共 ${paragraphs.items.length} 个段落`);

    let appliedCount = 0;
    let skippedCount = 0;

    styledParagraphs.forEach(({ pid, style }) => {
      // pid 校验（你原来的逻辑，完全保留）
      if (pid < 0 || pid >= paragraphs.items.length) {
        console.warn(`⚠️ 段落ID ${pid} 超出范围`);
        skippedCount++;
        return;
      }

      // 无样式直接跳过
      if (!style || Object.keys(style).length === 0) {
        skippedCount++;
        return;
      }

      const para = paragraphs.items[pid];

      // 核心：统一样式应用入口
      applyStyleToParagraph(para, style);
      appliedCount++;
    });

    await context.sync();

    console.log(`✅ 样式应用完成！`);
    console.log(`   - 成功应用: ${appliedCount} 个段落`);
    console.log(`   - 跳过: ${skippedCount} 个段落`);

    return {
      success: true,
      applied: appliedCount,
      skipped: skippedCount,
      total: styledParagraphs.length,
    };
  });
}

/**
 * 清除文档所有格式（保持简单直观）
 */
export async function clearAllFormatting() {
  return Word.run(async (context) => {
    const body = context.document.body;
    const paragraphs = body.paragraphs;

    paragraphs.load("items");
    await context.sync();

    paragraphs.items.forEach((para) => {
      para.font.name = "宋体";
      para.font.size = 12;
      para.font.bold = false;
      para.font.italic = false;
      para.alignment = Word.Alignment.left;
      para.firstLineIndent = 0;
      para.spaceBefore = 0;
      para.spaceAfter = 0;
    });

    await context.sync();
    console.log("✅ 已清除所有格式");
  });
}
