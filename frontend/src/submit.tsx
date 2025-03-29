import React from "react";
import axios from "axios";
import { useStore } from "./store";
import { Node, Edge } from "reactflow";

export const SubmitButton: React.FC = () => {
  const nodes: Node[] = useStore((state) => state.nodes);
  const edges: Edge[] = useStore((state) => state.edges);

  const handleSubmit = async () => {
    try {
      console.log("Nodes:", nodes);
      console.log("Edges:", edges);

      const response = await axios.post(
        "http://127.0.0.1:8000/pipelines/parse",
        {
          nodes,
          edges,
        }
      );

      const { num_nodes, num_edges, is_dag } = response.data as {
        num_nodes: number;
        num_edges: number;
        is_dag: boolean;
      };

      const isDagText = is_dag ? "yes" : "no";
      alert(
        `Number of nodes: ${num_nodes}, Number of edges: ${num_edges}, Is DAG: ${isDagText}`
      );
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while processing the pipeline.");
    }
  };

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        backgroundImage:
          "radial-gradient(circle, rgba(0, 0, 0, 0.5) 0.5px, transparent 1px)",
        backgroundSize: "10px 10px",
        height: "10.2vh",
        border: "0.5px solid black",
      }}
    >
      <button
        type="button"
        onClick={handleSubmit}
        style={{
          backgroundColor: "#0564b5",
          color: "white",
          padding: "10px 32px",
          fontSize: "15px",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
          transition: "background-color 0.3s",
        }}
        onMouseEnter={(e) =>
          ((e.target as HTMLButtonElement).style.backgroundColor = "#45a049")
        }
        onMouseLeave={(e) =>
          ((e.target as HTMLButtonElement).style.backgroundColor = "#0564b5")
        }
      >
        Submit
      </button>
    </div>
  );
};
