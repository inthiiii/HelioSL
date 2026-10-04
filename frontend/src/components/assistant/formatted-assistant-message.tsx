import type { ReactNode } from "react";


interface FormattedAssistantMessageProps {
  content: string;
}


type MessageBlock =
  | { type: "heading"; text: string }
  | { type: "paragraph"; text: string }
  | { type: "bullets"; items: string[] }
  | { type: "numbers"; items: string[] };


function cleanLine(value: string): string {
  return value
    .trim()
    .replace(/\s*[=_-]{4,}\s*$/, "")
    .trim();
}


function unwrapBold(value: string): string {
  const match = value.match(/^(?:\*\*|__)(.+)(?:\*\*|__)$/);
  return match ? match[1].trim() : value;
}


function parseMessage(content: string): MessageBlock[] {
  const blocks: MessageBlock[] = [];
  let paragraph: string[] = [];
  let listType: "bullets" | "numbers" | null = null;
  let listItems: string[] = [];

  function flushParagraph() {
    if (paragraph.length) {
      blocks.push({ type: "paragraph", text: paragraph.join(" ") });
      paragraph = [];
    }
  }

  function flushList() {
    if (listType && listItems.length) {
      blocks.push({ type: listType, items: listItems });
      listType = null;
      listItems = [];
    }
  }

  for (const rawLine of content.split(/\r?\n/)) {
    const line = cleanLine(rawLine);

    if (!line) {
      flushParagraph();
      flushList();
      continue;
    }

    const markdownHeading = line.match(/^#{1,6}\s+(.+)$/);
    const boldHeading = line.match(/^(?:\*\*|__)(.+)(?:\*\*|__)$/);

    if (markdownHeading || (boldHeading && line.length <= 100)) {
      flushParagraph();
      flushList();
      blocks.push({
        type: "heading",
        text: unwrapBold(markdownHeading?.[1] ?? line),
      });
      continue;
    }

    const bullet = line.match(/^[-*]\s+(.+)$/);
    if (bullet) {
      flushParagraph();
      if (listType !== "bullets") {
        flushList();
        listType = "bullets";
      }
      listItems.push(bullet[1]);
      continue;
    }

    const numbered = line.match(/^\d+[.)]\s+(.+)$/);
    if (numbered) {
      flushParagraph();
      if (listType !== "numbers") {
        flushList();
        listType = "numbers";
      }
      listItems.push(numbered[1]);
      continue;
    }

    flushList();

    if (line.endsWith(":") && line.length <= 80) {
      flushParagraph();
      blocks.push({ type: "heading", text: unwrapBold(line.slice(0, -1)) });
      continue;
    }

    paragraph.push(line);
  }

  flushParagraph();
  flushList();
  return blocks;
}


function formatInline(text: string): ReactNode[] {
  const tokens = text.split(/(\*\*.+?\*\*|__.+?__|`.+?`)/g);

  return tokens.filter(Boolean).map((token, index) => {
    if ((token.startsWith("**") && token.endsWith("**"))
      || (token.startsWith("__") && token.endsWith("__"))) {
      return (
        <strong key={`${index}-${token}`} className="font-semibold text-white">
          {token.slice(2, -2)}
        </strong>
      );
    }

    if (token.startsWith("`") && token.endsWith("`")) {
      return (
        <code key={`${index}-${token}`} className="rounded bg-black/30 px-1.5 py-0.5 font-mono text-xs text-emerald-200">
          {token.slice(1, -1)}
        </code>
      );
    }

    return token;
  });
}


export function FormattedAssistantMessage({ content }: FormattedAssistantMessageProps) {
  const blocks = parseMessage(content);

  return (
    <div className="space-y-3">
      {blocks.map((block, index) => {
        if (block.type === "heading") {
          return <h3 className="pt-1 text-sm font-semibold text-white" key={`${index}-${block.text}`}>{formatInline(block.text)}</h3>;
        }

        if (block.type === "bullets") {
          return (
            <ul className="list-disc space-y-1 pl-5 text-sm leading-6 text-neutral-200" key={`${index}-bullets`}>
              {block.items.map((item, itemIndex) => <li key={`${itemIndex}-${item}`}>{formatInline(item)}</li>)}
            </ul>
          );
        }

        if (block.type === "numbers") {
          return (
            <ol className="list-decimal space-y-1 pl-5 text-sm leading-6 text-neutral-200" key={`${index}-numbers`}>
              {block.items.map((item, itemIndex) => <li key={`${itemIndex}-${item}`}>{formatInline(item)}</li>)}
            </ol>
          );
        }

        return <p className="text-sm leading-6 text-neutral-200" key={`${index}-${block.text}`}>{formatInline(block.text)}</p>;
      })}
    </div>
  );
}
