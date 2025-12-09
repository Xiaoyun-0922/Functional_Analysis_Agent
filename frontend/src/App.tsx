import React, { useState } from "react";
import { KeyStepRenderer } from "./components/KeyStepRenderer";
import { LatexPreview } from "./components/LatexPreview";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

type ModelChoice = "deepseek-v3.2" | "gpt-5";

interface ChatSession {
  id: string;
  title: string;
  messages: ChatMessage[];
}

const App: React.FC = () => {
  const [model, setModel] = useState<ModelChoice>("deepseek-v3.2");
  const [input, setInput] = useState("");
  const [latex, setLatex] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Sessions (simple local history)
  const [sessions, setSessions] = useState<ChatSession[]>([{
    id: "session-1",
    title: "会话 1",
    messages: [],
  }]);
  const [activeSessionId, setActiveSessionId] = useState("session-1");

  const [inputMode, setInputMode] = useState<"text" | "image">("text");
  const [imageFile, setImageFile] = useState<File | null>(null);

  // Streaming state for the last assistant message
  const [streamIndex, setStreamIndex] = useState<number | null>(null);
  const [streamFull, setStreamFull] = useState("");
  const [streamVisible, setStreamVisible] = useState("");

  // Collapsed state for assistant messages' thinking/solution text
  const [collapsed, setCollapsed] = useState<Record<number, boolean>>({});

  const send = async () => {
    if (!input.trim() && !latex.trim()) return;
    setError(null);
    setLoading(true);

    const newMessages: ChatMessage[] = [
      ...messages,
      ...(input.trim()
        ? [{ role: "user" as const, content: input.trim() }]
        : []),
    ];

    setMessages(newMessages);
    setInput("");

    try {
      const res = await fetch("/api/functional-analysis/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: newMessages,
          latex: latex.trim() || null,
          model,
        }),
      });
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      const data = await res.json();
      const nextMessages = data.messages as ChatMessage[];
      setMessages(nextMessages);

      setSessions((prev) =>
        prev.map((s) =>
          s.id === activeSessionId ? { ...s, messages: nextMessages } : s
        )
      );

      // Prepare typewriter streaming for the last assistant message
      const lastAssistantIndex =
        [...nextMessages]
          .map((m, idx) => ({ ...m, idx }))
          .filter((m) => m.role === "assistant")
          .map((m) => m.idx)
          .pop() ?? null;

      if (lastAssistantIndex != null) {
        setStreamIndex(lastAssistantIndex);
        setStreamFull(nextMessages[lastAssistantIndex].content);
        setStreamVisible("");
      } else {
        setStreamIndex(null);
        setStreamFull("");
        setStreamVisible("");
      }
    } catch (e: any) {
      setError(e.message ?? String(e));
    } finally {
      setLoading(false);
    }
  };

  const toggleCollapsed = (idx: number) => {
    setCollapsed((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  const handleNewSession = () => {
    const id = `session-${sessions.length + 1}`;
    const next: ChatSession = { id, title: `会话 ${sessions.length + 1}`, messages: [] };
    setSessions((prev) => [...prev, next]);
    setActiveSessionId(id);
    setMessages([]);
    setCollapsed({});
    setStreamIndex(null);
    setStreamFull("");
    setStreamVisible("");
  };

  const handleSelectSession = (id: string) => {
    setActiveSessionId(id);
    const session = sessions.find((s) => s.id === id);
    setMessages(session?.messages ?? []);
    setCollapsed({});
    setStreamIndex(null);
    setStreamFull("");
    setStreamVisible("");
  };

  const handleCopy = (text: string) => {
    void navigator.clipboard.writeText(text);
  };

  const handleSendImage = async () => {
    if (!imageFile) return;
    setError(null);
    setLoading(true);

    const form = new FormData();
    form.append("file", imageFile);
    form.append("model", model);

    try {
      const res = await fetch("/api/functional-analysis/solve-image", {
        method: "POST",
        body: form,
      });
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      const data = await res.json();
      const nextMessages = data.messages as ChatMessage[];
      setMessages(nextMessages);
      setSessions((prev) =>
        prev.map((s) =>
          s.id === activeSessionId ? { ...s, messages: nextMessages } : s
        )
      );
    } catch (e: any) {
      setError(e.message ?? String(e));
    } finally {
      setLoading(false);
    }
  };

  // Typewriter effect for the last assistant message
  React.useEffect(() => {
    if (streamIndex == null || !streamFull) {
      return;
    }

    const currentIndex = streamIndex;
    setStreamVisible("");
    let i = 0;
    const step = Math.max(1, Math.floor(streamFull.length / 80));
    const id = window.setInterval(() => {
      i += step;
      if (i >= streamFull.length) {
        setStreamVisible(streamFull);
        setStreamIndex(null);
        if (currentIndex != null) {
          setCollapsed((prev) => ({ ...prev, [currentIndex]: true }));
        }
        window.clearInterval(id);
      } else {
        setStreamVisible(streamFull.slice(0, i));
      }
    }, 20);

    return () => window.clearInterval(id);
  }, [streamFull, streamIndex]);

  const onKeyDown: React.KeyboardEventHandler<HTMLTextAreaElement> = (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      void send();
    }
  };

  return (
    <div className="app-root">
      <header className="app-header">
        <h1>泛函分析问答与解题小助手</h1>
        <div className="controls">
          <div className="model-toggle">
            <button
              type="button"
              className={model === "deepseek-v3.2" ? "active" : ""}
              onClick={() => setModel("deepseek-v3.2")}
            >
              <div className="model-name">DeepSeek V3.2</div>
              <div className="model-desc">适合中文推理与解题</div>
            </button>
            <button
              type="button"
              className={model === "gpt-5" ? "active" : ""}
              onClick={() => setModel("gpt-5")}
            >
              <div className="model-name">GPT-5（XIAO_AI）</div>
              <div className="model-desc">英文与综合能力更强</div>
            </button>
          </div>
        </div>
      </header>

      <main className="app-main">
        <aside className="sidebar">
          <div className="sidebar-header">
            <span>历史会话</span>
            <button onClick={handleNewSession}>新建</button>
          </div>
          <ul className="session-list">
            {sessions.map((s) => (
              <li
                key={s.id}
                className={s.id === activeSessionId ? "session active" : "session"}
                onClick={() => handleSelectSession(s.id)}
              >
                {s.title}
              </li>
            ))}
          </ul>
        </aside>

        <section className="chat-pane">
          <div className="messages">
            {messages.map((m, idx) => {
              const isStreaming = streamIndex === idx && m.role === "assistant";
              const content = isStreaming ? streamVisible : m.content;
              const isCollapsed =
                m.role === "assistant" && collapsed[idx] && !isStreaming;
              return (
                <div
                  key={idx}
                  className={`msg msg-${m.role}`}
                >
                  <div className="msg-role">
                    {m.role === "user" ? "你" : "Agent"}
                  </div>
                  <div className="msg-content">
                    {isCollapsed ? (
                      <div
                        className="collapsed-hint"
                        onClick={() => toggleCollapsed(idx)}
                      >
                        思考过程已折叠，点击展开查看完整解答
                      </div>
                    ) : (
                      <KeyStepRenderer text={content} />
                    )}
                    {isStreaming && (
                      <span
                        className="thinking-spinner"
                        title="正在思考与检索课程材料的关键步骤，最终答案采用连贯证明风格。"
                      />
                    )}
                  </div>
                  {m.role === "assistant" && (
                    <button
                      className="copy-btn"
                      onClick={() => handleCopy(content)}
                    >
                      复制
                    </button>
                  )}
                </div>
              );
            })}
            {loading && <div className="msg msg-assistant">正在思考...</div>}
          </div>

          {error && <div className="error">Error: {error}</div>}
        </section>

        <section className="input-pane">
          <div className="mode-toggle">
            <button
              className={inputMode === "text" ? "active" : ""}
              onClick={() => setInputMode("text")}
            >
              文本 / LaTeX
            </button>
            <button
              className={inputMode === "image" ? "active" : ""}
              onClick={() => setInputMode("image")}
            >
              图片题目
            </button>
          </div>

          {inputMode === "text" ? (
            <>
              <div className="input-group">
                <label>题目 / 问题（支持 Ctrl+Enter 发送）</label>
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={onKeyDown}
                  rows={4}
                />
              </div>

              <div className="input-group">
                <label>LaTeX 输入（可选）</label>
                <textarea
                  value={latex}
                  onChange={(e) => setLatex(e.target.value)}
                  rows={4}
                />
                <LatexPreview value={latex} />
              </div>

              <div className="actions">
                <button
                  onClick={() => void send()}
                  disabled={loading}
                >
                  {loading ? "发送中..." : "发送"}
                </button>
              </div>
            </>
          ) : (
            <>
              <div className="input-group">
                <label>上传题目截图（图片）</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => setImageFile(e.target.files?.[0] ?? null)}
                />
              </div>
              <div className="actions">
                <button
                  onClick={() => void handleSendImage()}
                  disabled={loading || !imageFile}
                >
                  {loading ? "发送中..." : "发送图片"}
                </button>
              </div>
            </>
          )}
        </section>
      </main>
    </div>
  );
};

export default App;
