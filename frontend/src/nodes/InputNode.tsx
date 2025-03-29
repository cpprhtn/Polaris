import React from "react";
import { Position } from "reactflow";
import BaseNode from "./BaseNode";

export const InputNode: React.FC<{ id: string; data: any }> = ({
  id,
  data,
}) => {
  const inputs = [
    {
      key: "sourceType",
      label: "Source",
      type: "select",
      options: ["upload", "http", "s3", "gcs", "azure"],
    },
    {
      key: "url",
      label: "URL",
      type: "text",
      condition: (data: any) => data.sourceType && data.sourceType !== "upload",
    },
    {
      key: "file",
      label: "File",
      type: "file",
      condition: (data: any) => data.sourceType === "upload",
    },
  ];

  const handles = [
    { type: "source", position: Position.Right, id: `${id}-data` },
  ];

  return (
    <BaseNode
      id={id}
      data={data}
      title="Input"
      inputs={inputs}
      handles={handles}
    />
  );
};
