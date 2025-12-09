import React from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

interface KeyStepSegment {
  type: "normal" | "key";
  text: string;
  id?: string;
  theorem?: string;
}

function parseKeySteps(text: string): KeyStepSegment[] {
  const segments: KeyStepSegment[] = [];
  const startTag = "[[KEY_STEP";
  const endTag = "[[/KEY_STEP]]";

  let remaining = text;
  while (true) {
    const startIdx = remaining.indexOf(startTag);
    if (startIdx === -1) {
      if (remaining) {
        segments.push({ type: "normal", text: remaining });
      }
      break;
    }

    if (startIdx > 0) {
      segments.push({ type: "normal", text: remaining.slice(0, startIdx) });
    }

    const endIdx = remaining.indexOf(endTag, startIdx);
    if (endIdx === -1) {
      // Malformed; treat the rest as normal text
      segments.push({ type: "normal", text: remaining.slice(startIdx) });
      break;
    }

    const tagAndContent = remaining.slice(startIdx, endIdx + endTag.length);
    const headerEnd = tagAndContent.indexOf("]]");
    const header = tagAndContent.slice(startTag.length, headerEnd).trim();
    const body = tagAndContent.slice(headerEnd + 2, -endTag.length);

    const idMatch = header.match(/id=([^\s]+)(\s|$)/);
    const theoremMatch = header.match(/theorem="([^"]*)"/);

    segments.push({
      type: "key",
      text: body,
      id: idMatch?.[1],
      theorem: theoremMatch?.[1],
    });

    remaining = remaining.slice(endIdx + endTag.length);
  }

  return segments;
}

interface Props {
  text: string;
}

export const KeyStepRenderer: React.FC<Props> = ({ text }) => {
  const segments = parseKeySteps(text);

  return (
    <>
      {segments.map((seg, idx) => {
        if (seg.type === "normal") {
          return (
            <ReactMarkdown
              key={idx}
              remarkPlugins={[remarkMath]}
              rehypePlugins={[rehypeKatex]}
            >
              {seg.text}
            </ReactMarkdown>
          );
        }
        const title = seg.theorem
          ? `关键步骤${seg.id ? ` #${seg.id}` : ""}: ${seg.theorem}`
          : seg.id
          ? `关键步骤 #${seg.id}`
          : "关键步骤";
        return (
          <div
            key={idx}
            className="key-step"
            title={title}
          >
            <ReactMarkdown
              remarkPlugins={[remarkMath]}
              rehypePlugins={[rehypeKatex]}
            >
              {seg.text}
            </ReactMarkdown>
          </div>
        );
      })}
    </>
  );
};
