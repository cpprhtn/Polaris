import React from "react";
import { Position } from "reactflow";
import BaseNode from "./BaseNode";

// CustomNode2용 props 타입 정의
interface CustomNode2Props {
  id: string;
  data: {
    [key: string]: any;
  };
}

// 입력과 출력 핸들이 모두 있는 사용자 정의 노드 2
export const CustomNode1: React.FC<CustomNode2Props> = ({ id, data }) => {
  // param1 필드 하나만 입력으로 구성
  const inputs = [
    {
      key: "param1",
      label: "Param",
      type: "text", // 텍스트 입력 필드
    },
  ];

  // 입력 (왼쪽) + 출력 (오른쪽) 핸들 구성
  const handles = [
    {
      type: "source",
      position: Position.Right,
      id: `${id}-output`, // 출력 핸들
    },
    {
      type: "target",
      position: Position.Left,
      id: `${id}-input`, // 입력 핸들
    },
  ];

  return (
    <BaseNode
      id={id}
      data={data}
      title="Custom Node 1"
      inputs={inputs}
      handles={handles}
    />
  );
};
