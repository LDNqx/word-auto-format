// src/office/applyStyle.js

export async function applyStyles(paragraphRoles, styleConfig) {
    await Word.run(async (context) => {
      const paragraphs = context.document.body.paragraphs;
      paragraphs.load("items");
  
      await context.sync();
  
      paragraphs.items.forEach((para, index) => {
        const roleInfo = paragraphRoles[index];
        if (!roleInfo) return;
  
        const styleKey = roleInfo.style_key;
        const style = styleConfig.styles[styleKey];
        if (!style) return;
  
        const font = para.font;
  
        if (style.font) font.name = style.font;
        if (style.size) font.size = style.size;
        if (style.bold !== null && style.bold !== undefined)
          font.bold = style.bold;
  
        if (style.align) {
          para.alignment =
            style.align === "center"
              ? Word.Alignment.center
              : style.align === "right"
              ? Word.Alignment.right
              : Word.Alignment.left;
        }
  
        if (style.first_line_indent !== null && style.first_line_indent !== undefined) {
          para.firstLineIndent = style.first_line_indent;
        }
      });
  
      await context.sync();
    });
  }
  