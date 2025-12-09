import React from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

interface Props {
  value: string;
}

export const LatexPreview: React.FC<Props> = ({ value }) => {
  const content = value.trim() || "在这里实时预览 LaTeX 表达式（支持 $a^2 + b^2 = c^2$ 等）。";

  return (
    <div className="latex-preview">
      <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
        {content}
      </ReactMarkdown>
    </div>
  );
};
