import React from "react";
import { Position } from "reactflow";
import BaseNode from "./BaseNode";

// CustomNode5용 props 타입 정의
interface CustomNode5Props {
  id: string;
  data: {
    [key: string]: any;
  };
}

// 파라미터 및 값 설정이 가능한 사용자 정의 노드 5
export const CustomNode5: React.FC<CustomNode5Props> = ({ id, data }) => {
  // 입력 필드 구성: Param, Value
  const inputs = [
    {
      key: "parameter",
      label: "Param",
      type: "text",
    },
    {
      key: "value",
      label: "Value",
      type: "text",
    },
  ];

  // 입출력 핸들 구성
  const handles = [
    {
      type: "source",
      position: Position.Right,
      id: `${id}-output`,
    },
    {
      type: "target",
      position: Position.Left,
      id: `${id}-input`,
    },
  ];

  return (
    <BaseNode
      id={id}
      data={data}
      title="Custom Node 5"
      inputs={inputs}
      handles={handles}
    />
  );
};
