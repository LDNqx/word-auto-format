// src/office/word.js

export async function getDocumentParagraphs() {
  return Word.run(async (context) => {
    const body = context.document.body;
    const paragraphs = body.paragraphs;

    paragraphs.load("items/text");
    await context.sync();

    const result = paragraphs.items.map((p, index) => ({
      pid: index,
      text: p.text.trim()
    })).filter(p => p.text.length > 0);

    return result;
  });
}
