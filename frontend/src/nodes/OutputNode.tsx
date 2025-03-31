import React from "react";
import { Position } from "reactflow";
import BaseNode from "./BaseNode";

interface OutputNodeProps {
  id: string;
  data: {
    [key: string]: any;
  };
}

export const OutputNode: React.FC<OutputNodeProps> = ({ id, data }) => {
  const inputs = [
    {
      key: "fileName",
      label: "File Name",
      type: "text",
    },
    {
      key: "format",
      label: "Format",
      type: "select",
      options: ["CSV", "Parquet"],
    },
  ];

  const handles = [
    {
      type: "target",
      position: Position.Left,
      id: `${id}-value`,
    },
  ];

  return (
    <BaseNode
      id={id}
      data={data}
      title="Output"
      inputs={inputs}
      handles={handles}
    />
  );
};
