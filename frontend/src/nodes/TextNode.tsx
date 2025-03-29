import React from "react";
import { Position } from "reactflow";
import BaseNode from "./BaseNode";

// TextNode가 받는 props 타입 정의
interface TextNodeProps {
  id: string;
  data: {
    [key: string]: any;
  };
}

// 단순 텍스트 노드 컴포넌트
export const TextNode: React.FC<TextNodeProps> = ({ id, data }) => {
  // BaseNode에서 사용할 입력 필드 설정
  const inputs = [
    {
      key: "text",
      label: "Text",
      type: "textarea", // 여러 줄 입력을 위한 필드
    },
  ];

  // 출력 핸들 (오른쪽)
  const handles = [
    {
      type: "source", // 이 노드는 데이터를 외부로 출력함
      position: Position.Right,
      id: `${id}-output`,
    },
  ];

  return (
    <BaseNode
      id={id}
      data={data}
      title="Text"
      inputs={inputs}
      handles={handles}
    />
  );
};
