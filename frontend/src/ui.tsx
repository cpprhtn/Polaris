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
import { FilterNode } from "./nodes/FilterNode";
import "reactflow/dist/style.css";

const gridSize = 20;
const proOptions = { hideAttribution: true };

const nodeTypes = {
  Input: InputNode,
  Filter: FilterNode,
  Output: OutputNode,
  text: TextNode,
};

type NodeType = keyof typeof nodeTypes;

export const PipelineUI: React.FC = () => {
  const reactFlowWrapper = useRef<HTMLDivElement | null>(null);
  const [reactFlowInstance, setReactFlowInstance] =
    useState<ReactFlowInstance | null>(null);

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
                case "Input":
                  return "#0041d0";
                case "Output":
                  return "#ff0072";
                case "text":
                  return "#ff8400";
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
