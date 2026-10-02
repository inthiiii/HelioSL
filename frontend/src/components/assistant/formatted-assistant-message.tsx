interface FormattedAssistantMessageProps {
  content: string;
}


type MessageBlock =
  | {
      type: "heading";
      text: string;
    }
  | {
      type: "paragraph";
      text: string;
    }
  | {
      type: "bullets";
      items: string[];
    }
  | {
      type: "numbers";
      items: string[];
    };


function parseMessage(content: string): MessageBlock[] {
  const blocks: MessageBlock[] = [];
  let paragraph: string[] = [];
  let listType: "bullets" | "numbers" | null = null;
  let listItems: string[] = [];

  function flushParagraph() {
    if (paragraph.length) {
      blocks.push({
        type: "paragraph",
        text: paragraph.join(" "),
      });
      paragraph = [];
    }
  }

  function flushList() {
    if (listType && listItems.length) {
      blocks.push({
        type: listType,
        items: listItems,
      });
      listType = null;
      listItems = [];
    }
  }

  for (const rawLine of content.split(/\r?\n/)) {
    const line = rawLine.trim();

    if (!line) {
      flushParagraph();
      flushList();
      continue;
    }

    const markdownHeading = line.match(
      /^#{1,6}\s+(.+)$/
    );

    if (markdownHeading) {
      flushParagraph();
      flushList();
      blocks.push({
        type: "heading",
        text: markdownHeading[1],
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

    const shortSectionHeading = (
      line.endsWith(":")
      && line.length <= 80
    );

    if (shortSectionHeading) {
      flushParagraph();
      blocks.push({
        type: "heading",
        text: line.slice(0, -1),
      });
      continue;
    }

    paragraph.push(line);
  }

  flushParagraph();
  flushList();

  return blocks;
}


export function FormattedAssistantMessage({
  content,
}: FormattedAssistantMessageProps) {
  const blocks = parseMessage(content);

  return (
    <div className="space-y-3">
      {blocks.map((block, index) => {
        if (block.type === "heading") {
          return (
            <h3
              className="pt-1 text-sm font-semibold text-white"
              key={`${index}-${block.text}`}
            >
              {block.text}
            </h3>
          );
        }

        if (block.type === "bullets") {
          return (
            <ul
              className="list-disc space-y-1 pl-5 text-sm leading-6 text-neutral-200"
              key={`${index}-bullets`}
            >
              {block.items.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          );
        }

        if (block.type === "numbers") {
          return (
            <ol
              className="list-decimal space-y-1 pl-5 text-sm leading-6 text-neutral-200"
              key={`${index}-numbers`}
            >
              {block.items.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ol>
          );
        }

        return (
          <p
            className="text-sm leading-6 text-neutral-200"
            key={`${index}-${block.text}`}
          >
            {block.text}
          </p>
        );
      })}
    </div>
  );
}
