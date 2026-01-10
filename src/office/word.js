export async function extractParagraphsWithPid() {
    return Word.run(async (context) => {
      const paragraphs = context.document.body.paragraphs;
      paragraphs.load("items/text");
      await context.sync();
  
      const result = paragraphs.items.map((para, index) => ({
        pid: index,
        text: para.text.trim()
      }));
  
      return result;
    });
  }
  