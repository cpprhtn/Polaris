import React from "react";
import { Position } from "reactflow";
import BaseNode from "./BaseNode";

interface FilterNodeProps {
  id: string;
  data: {
    [key: string]: any;
  };
}

export const FilterNode: React.FC<FilterNodeProps> = ({ id, data }) => {
  const inputs = [
    {
      key: "column",
      label: "Column",
      type: "text",
    },
    {
      key: "operator",
      label: "Operator",
      type: "select",
      options: ["==", "!=", ">", "<", ">=", "<="],
    },
    {
      key: "value",
      label: "Value",
      type: "text",
    },
  ];

  const handles = [
    {
      type: "target",
      position: Position.Left,
      id: `${id}-input`,
    },
    {
      type: "source",
      position: Position.Right,
      id: `${id}-output`,
    },
  ];

  return (
    <BaseNode
      id={id}
      data={data}
      title="Filter"
      inputs={inputs}
      handles={handles}
    />
  );
};
