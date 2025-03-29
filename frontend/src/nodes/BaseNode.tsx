import React, { useState, useEffect, useRef } from "react";
import { Handle, Position, useUpdateNodeInternals } from "reactflow";
import TextareaAutosize from "react-textarea-autosize";

// === 타입 정의 ===
type InputField = {
  key: string;
  label: string;
  type: "text" | "number" | "select" | "textarea";
  options?: string[];
};

type HandleConfig = {
  id: string;
  type: "source" | "target";
  position: Position;
  style?: React.CSSProperties;
};

type BaseNodeProps = {
  id: string;
  title: string;
  data: {
    text?: string;
    [key: string]: any;
  };
  inputs: InputField[];
  handles: HandleConfig[];
};

const BaseNode: React.FC<BaseNodeProps> = ({
  id,
  data,
  title,
  inputs,
  handles,
}) => {
  const [text, setText] = useState(() => {
    return typeof data.text === "object" && data.text !== null ? data.text : {};
  });
  const [patternMatches, setPatternMatches] = useState<string[]>([]);
  const updateNodeInternals = useUpdateNodeInternals();
  const nodeRef = useRef<HTMLDivElement | null>(null);

  const findHandlePatterns = (text: string): string[] => {
    const regex = /\{\{(.+?)\}\}/g;
    const matches: string[] = [];
    let match: RegExpExecArray | null;
    while ((match = regex.exec(text)) !== null) {
      matches.push(match[1]);
    }
    return matches;
  };

  useEffect(() => {
    const matches = findHandlePatterns(text);

    // 상태 비교: 값이 진짜 바뀌었을 때만 setState
    setPatternMatches((prevMatches) => {
      const changed =
        matches.length !== prevMatches.length ||
        matches.some((m, i) => m !== prevMatches[i]);

      if (changed) {
        return matches;
      }
      return prevMatches;
    });

    updateNodeInternals(id);

    const nodeElement = nodeRef.current;
    if (nodeElement) {
      const textareaElement = nodeElement.querySelector("textarea");
      if (textareaElement instanceof HTMLElement) {
        const { offsetHeight } = textareaElement;
        nodeElement.style.height = `${offsetHeight + 50}px`;
      }
    }
  }, [text, id, updateNodeInternals]);

  const handleChange = (e: React.ChangeEvent<any>, key: string) => {
    setText(e.target.value);
  };

  return (
    <div
      ref={nodeRef}
      style={{
        position: "relative",
        width: 200,
        height: 100,
        border: "1px solid blue",
        padding: 10,
        borderRadius: 5,
        backgroundColor: "#6CB4EE",
      }}
    >
      <div
        style={{ marginBottom: 10, textAlign: "center", fontWeight: "bold" }}
      >
        <span>{title}</span>
      </div>
      <div>
        {inputs
          .filter((input) => !input.condition || input.condition(data)) // ✅ 조건 렌더링
          .map((input) => (
            <label
              key={input.key}
              style={{ marginBottom: 5, display: "flex", alignItems: "center" }}
            >
              {input.label}:
              {input.type === "select" ? (
                <select
                  value={text[input.key as keyof typeof text]}
                  onChange={(e) => handleChange(e, input.key)}
                  style={{ marginLeft: 20 }}
                >
                  {input.options?.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              ) : input.type === "textarea" ? (
                <TextareaAutosize
                  value={text}
                  minRows={2}
                  maxRows={16}
                  onChange={(e) => handleChange(e, input.key)}
                  style={{ width: "100%" }}
                />
              ) : (
                <input
                  type={input.type}
                  value={text[input.key as keyof typeof text]}
                  onChange={(e) => handleChange(e, input.key)}
                  style={{ marginLeft: 10, width: "calc(100% - 60px)" }}
                />
              )}
            </label>
          ))}
      </div>

      {handles.map((handle) => (
        <Handle
          key={handle.id}
          type={handle.type}
          position={handle.position}
          id={handle.id}
          style={handle.style}
        />
      ))}

      {patternMatches.map((match, index) => (
        <Handle
          key={`left-handle-${index}`}
          type="target"
          position={Position.Left}
          id={`${id}-target-${index}`}
          name={match}
          style={{
            background: "#555",
            top: `${(index + 1) * (100 / (patternMatches.length + 1))}%`,
          }}
        />
      ))}
    </div>
  );
};

export default BaseNode;
