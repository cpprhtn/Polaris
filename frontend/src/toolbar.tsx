import React from "react";
import { DraggableNode } from "./draggableNode";

export const PipelineToolbar: React.FC = () => {
  return (
    <div
      style={{
        padding: "10px",
        backgroundImage:
          "radial-gradient(circle, rgba(0, 0, 0, 0.5) 0.5px, transparent 1px)",
        backgroundSize: "10px 10px",
        borderRadius: "4px",
      }}
    >
      <div
        style={{
          marginTop: "10px",
          display: "flex",
          flexWrap: "wrap",
          gap: "10px",
          marginBottom: "10px",
        }}
      >
        <DraggableNode type="Input" label="Input" />
        <DraggableNode type="Filter" label="Filter" />
        <DraggableNode type="Output" label="Output" />
        <DraggableNode type="text" label="Text" />
      </div>
    </div>
  );
};
