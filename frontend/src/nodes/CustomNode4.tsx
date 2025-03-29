import React from "react";
import { Position } from "reactflow";
import BaseNode from "./BaseNode";

// CustomNode4용 props 타입 정의
interface CustomNode4Props {
  id: string;
  data: {
    [key: string]: any;
  };
}

// 속성(Attribute) 입력 및 출력이 가능한 사용자 정의 노드 4
export const CustomNode4: React.FC<CustomNode4Props> = ({ id, data }) => {
  // BaseNode에 전달할 입력 필드 구성
  const inputs = [
    {
      key: "inputName",
      label: "Attribute",
      type: "text",
    },
    {
      key: "inputType",
      label: "Type",
      type: "select",
      options: ["Text", "File"],
    },
  ];

  // 출력 핸들 하나 (오른쪽)
  const handles = [
    {
      type: "source",
      position: Position.Right,
      id: `${id}-value`,
    },
  ];

  return (
    <BaseNode
      id={id}
      data={data}
      title="CustomNode 4"
      inputs={inputs}
      handles={handles}
    />
  );
};
