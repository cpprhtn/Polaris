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
        <DraggableNode type="customInput" label="Input" />
        <DraggableNode type="filter" label="Filter" />
        <DraggableNode type="customOutput" label="Output" />
        <DraggableNode type="text" label="Text" />
        <DraggableNode type="customnode1" label="Custom" />
        <DraggableNode type="customnode2" label="General" />
        <DraggableNode type="customnode3" label="Setting" />
        <DraggableNode type="customnode4" label="Attribute" />
        <DraggableNode type="customnode5" label="Parameter" />
      </div>
    </div>
  );
};
