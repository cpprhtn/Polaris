import React from "react";
import { MdInput, MdCallMade } from "react-icons/md";
import { LuFileOutput } from "react-icons/lu";
import { CiText } from "react-icons/ci";
import { BiCustomize, BiAlignMiddle, BiAtom } from "react-icons/bi";
import { VscSymbolParameter } from "react-icons/vsc";
import { IoMdSettings } from "react-icons/io";

interface DraggableNodeProps {
  type: string;
  label: string;
}

export const DraggableNode: React.FC<DraggableNodeProps> = ({
  type,
  label,
}) => {
  const getIcon = (type: string): JSX.Element | null => {
    switch (type) {
      case "Input":
        return <MdInput />;
      case "Filter":
        return <MdInput />;
      case "Output":
        return <LuFileOutput />;
      case "text":
        return <CiText />;
      default:
        return null;
    }
  };

  const onDragStart = (
    event: React.DragEvent<HTMLDivElement>,
    nodeType: string
  ) => {
    const appData = { nodeType };
    event.currentTarget.style.cursor = "grabbing";
    event.dataTransfer.setData(
      "application/reactflow",
      JSON.stringify(appData)
    );
    event.dataTransfer.effectAllowed = "move";
  };

  return (
    <div
      className={type}
      onDragStart={(event) => onDragStart(event, type)}
      onDragEnd={(event) => {
        (event.target as HTMLDivElement).style.cursor = "grab";
      }}
      style={{
        cursor: "grab",
        minWidth: "80px",
        height: "60px",
        display: "flex",
        alignItems: "center",
        borderRadius: "8px",
        backgroundColor: "#0564b5",
        justifyContent: "center",
        flexDirection: "column",
        position: "relative",
      }}
      draggable
    >
      <div style={{ position: "absolute", top: 5, color: "white" }}>
        {getIcon(type)}
      </div>
      <br />
      <span style={{ color: "#fff" }}>{label}</span>
    </div>
  );
};
