import React from "react";
import { Position } from "reactflow";
import BaseNode from "./BaseNode";

interface TextNodeProps {
  id: string;
  data: {
    [key: string]: any;
  };
}

export const TextNode: React.FC<TextNodeProps> = ({ id, data }) => {
  const inputs = [
    {
      key: "text",
      label: "Text",
      type: "textarea",
    },
  ];

  const handles = [
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
      title="Text"
      inputs={inputs}
      handles={handles}
    />
  );
};
