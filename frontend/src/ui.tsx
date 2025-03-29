import React, { useState, useRef, useCallback } from "react";
import ReactFlow, {
  Controls,
  Background,
  MiniMap,
  Node,
  Edge,
  ReactFlowInstance,
} from "reactflow";
import { useStore } from "./store";
import { InputNode } from "./nodes/inputNode";
import { OutputNode } from "./nodes/OutputNode";
import { TextNode } from "./nodes/textNode";
import { CustomNode1 } from "./nodes/CustomNode1";
import { CustomNode2 } from "./nodes/CustomNode2";
import { CustomNode3 } from "./nodes/CustomNode3";
import { CustomNode4 } from "./nodes/CustomNode4";
import { CustomNode5 } from "./nodes/CustomNode5";
import { FilterNode } from "./nodes/FilterNode";
import "reactflow/dist/style.css";

const gridSize = 20;
const proOptions = { hideAttribution: true };

const nodeTypes = {
  customInput: InputNode,
  filter: FilterNode,
  customOutput: OutputNode,
  text: TextNode,
  customnode1: CustomNode1,
  customnode2: CustomNode2,
  customnode3: CustomNode3,
  customnode4: CustomNode4,
  customnode5: CustomNode5,
};

type NodeType = keyof typeof nodeTypes;

export const PipelineUI: React.FC = () => {
  const reactFlowWrapper = useRef<HTMLDivElement | null>(null);
  const [reactFlowInstance, setReactFlowInstance] =
    useState<ReactFlowInstance | null>(null);

  // ✅ 상태를 개별로 가져와서 무한 루프 방지
  const nodes = useStore((state) => state.nodes);
  const edges = useStore((state) => state.edges);
  const getNodeID = useStore((state) => state.getNodeID);
  const addNode = useStore((state) => state.addNode);
  const onNodesChange = useStore((state) => state.onNodesChange);
  const onEdgesChange = useStore((state) => state.onEdgesChange);
  const onConnect = useStore((state) => state.onConnect);

  const getInitNodeData = (nodeID: string, type: string) => {
    return { id: nodeID, nodeType: type };
  };

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();

      const bounds = reactFlowWrapper.current?.getBoundingClientRect();
      const rawData = event.dataTransfer.getData("application/reactflow");

      if (!bounds || !rawData) return;

      const appData = JSON.parse(rawData);
      const type = appData?.nodeType as NodeType;
      if (!type) return;

      const position = reactFlowInstance?.project({
        x: event.clientX - bounds.left,
        y: event.clientY - bounds.top,
      });
      if (!position) return;

      const nodeID = getNodeID(type);
      const newNode: Node = {
        id: nodeID,
        type,
        position,
        data: getInitNodeData(nodeID, type),
      };

      addNode(newNode);
    },
    [reactFlowInstance, getNodeID, addNode]
  );

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  }, []);

  const getEdgeCenter = (edge: Edge) => {
    const sourceNode = nodes.find((node) => node.id === edge.source);
    const targetNode = nodes.find((node) => node.id === edge.target);

    if (!sourceNode || !targetNode) return { x: 0, y: 0 };

    const sourcePos = sourceNode.position;
    const targetPos = targetNode.position;

    return {
      x: (sourcePos.x + targetPos.x) / 2,
      y: (sourcePos.y + targetPos.y) / 2,
    };
  };

  return (
    <div
      ref={reactFlowWrapper}
      style={{
        width: "100vw",
        height: "75vh",
        backgroundColor: "#e3f0f3",
      }}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onDrop={onDrop}
        onDragOver={onDragOver}
        onInit={setReactFlowInstance}
        nodeTypes={nodeTypes}
        proOptions={proOptions}
        snapGrid={[gridSize, gridSize]}
        connectionLineType="smoothstep"
      >
        <Background color="#08191d" gap={gridSize} />
        <Controls />
        <div style={{ border: "0.5px solid black" }}>
          <MiniMap
            nodeColor={(node) => {
              switch (node.type) {
                case "customInput":
                  return "#0041d0";
                case "customOutput":
                  return "#ff0072";
                case "text":
                  return "#ff8400";
                case "customnode1":
                  return "#00b386";
                case "customnode2":
                  return "#9e00c5";
                case "customnode3":
                  return "#ff7e00";
                case "customnode4":
                  return "#b30000";
                case "customnode5":
                  return "yellow";
                default:
                  return "#888";
              }
            }}
          />
        </div>

        {edges.map((edge) => {
          const { x, y } = getEdgeCenter(edge);
          return (
            <div
              key={edge.id}
              style={{ position: "absolute", left: x, top: y }}
            />
          );
        })}
      </ReactFlow>
    </div>
  );
};
