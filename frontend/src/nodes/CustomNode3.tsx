import React from "react";
import { Position } from "reactflow";
import BaseNode from "./BaseNode";

// CustomNode3용 props 타입 정의
interface CustomNode3Props {
  id: string;
  data: {
    [key: string]: any;
  };
}

// 설정 값을 선택받고, 입출력 연결이 가능한 사용자 정의 노드 3
export const CustomNode3: React.FC<CustomNode3Props> = ({ id, data }) => {
  // select 필드 하나 ("A", "B", "C" 중 선택)
  const inputs = [
    {
      key: "setting",
      label: "Setting",
      type: "select",
      options: ["A", "B", "C"],
    },
  ];

  // 입출력 핸들 구성
  const handles = [
    {
      type: "source",
      position: Position.Right,
      id: `${id}-result`, // 출력 핸들
    },
    {
      type: "target",
      position: Position.Left,
      id: `${id}-config`, // 입력 핸들
    },
  ];

  return (
    <BaseNode
      id={id}
      data={data}
      title="Custom Node 3"
      inputs={inputs}
      handles={handles}
    />
  );
};
