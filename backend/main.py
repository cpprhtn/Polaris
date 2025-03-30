from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: str

class Edge(BaseModel):
    source: str
    target: str

class PipelineData(BaseModel):
    nodes: list[Node]
    edges: list[Edge]

def is_cyclic_util(
    v: int, 
    visited: dict[int, bool], 
    rec_stack: dict[int, bool], 
    graph: dict[int, list[int]]
) -> bool:
    visited[v] = True
    rec_stack[v] = True

    for neighbor in graph[v]:
        if not visited[neighbor]:
            if is_cyclic_util(neighbor, visited, rec_stack, graph):
                return True
        elif rec_stack[neighbor]:
            return True

    rec_stack[v] = False
    return False

def check_if_dag(nodes: list[Node], edges: list[Edge]) -> bool:
    graph: dict[int, list[int]] = {int(node.id): [] for node in nodes}  # str → int 변환
    for edge in edges:
        graph[int(edge.source)].append(int(edge.target))  # str → int 변환

    visited: dict[int, bool] = {int(node.id): False for node in nodes}  # str → int 변환
    rec_stack: dict[int, bool] = {int(node.id): False for node in nodes}

    for node in nodes:
        if not visited[int(node.id)]:
            if is_cyclic_util(int(node.id), visited, rec_stack, graph):
                return False

    return True  # 반환값 추가 (mypy 오류 해결)

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: PipelineData) -> dict:
    nodes = pipeline.nodes
    edges = pipeline.edges

    num_nodes = len(nodes)
    num_edges = len(edges)
    is_dag = check_if_dag(nodes, edges)

    print("Nodes:", nodes)
    print("Edges:", edges)

    return {'num_nodes': num_nodes, 'num_edges': num_edges, 'is_dag': is_dag}