import pytest
from fastapi.testclient import TestClient

from main import Edge, Node, app, check_if_dag

client = TestClient(app)

@pytest.fixture
def nodes_and_edges_no_cycle() -> tuple[list[Node], list[Edge]]:
    """순환 없는 DAG 테스트에 사용할 예시 데이터"""
    nodes = [Node(id="1"), Node(id="2"), Node(id="3")]
    edges = [Edge(source="1", target="2"), Edge(source="2", target="3")]
    return nodes, edges

@pytest.fixture
def nodes_and_edges_with_cycle() -> tuple[list[Node], list[Edge]]:
    """순환이 있는 DAG 테스트에 사용할 예시 데이터"""
    nodes = [Node(id="1"), Node(id="2"), Node(id="3")]
    edges = [Edge(source="1", target="2"), Edge(source="2", target="3"), Edge(source="3", target="1")]
    return nodes, edges

@pytest.fixture
def empty_nodes_and_edges() -> tuple[list[Node], list[Edge]]:
    """노드와 엣지가 비어 있는 DAG 테스트에 사용할 예시 데이터"""
    return [], []

@pytest.fixture
def nodes_and_no_edges() -> tuple[list[Node], list[Edge]]:
    """엣지가 없는 경우 DAG 테스트에 사용할 예시 데이터"""
    nodes = [Node(id="1"), Node(id="2"), Node(id="3")]
    return nodes, []

# 테스트 함수에서 fixture를 사용하여 데이터 전달
def test_check_if_dag_no_cycle(nodes_and_edges_no_cycle: tuple[list[Node], list[Edge]]) -> None:
    """순환 없는 DAG 테스트"""
    nodes, edges = nodes_and_edges_no_cycle
    assert check_if_dag(nodes, edges) is True

def test_check_if_dag_with_cycle(nodes_and_edges_with_cycle: tuple[list[Node], list[Edge]]) -> None:
    """순환이 있는 경우 (DAG가 아님)"""
    nodes, edges = nodes_and_edges_with_cycle
    assert check_if_dag(nodes, edges) is False

def test_check_if_dag_no_nodes(empty_nodes_and_edges: tuple[list[Node], list[Edge]]) -> None:
    """노드가 없는 경우 (DAG로 간주)"""
    nodes, edges = empty_nodes_and_edges
    assert check_if_dag(nodes, edges) is True

def test_check_if_dag_no_edges(nodes_and_no_edges: tuple[list[Node], list[Edge]]) -> None:
    """엣지가 없는 경우 (DAG로 간주)"""
    nodes, edges = nodes_and_no_edges
    assert check_if_dag(nodes, edges) is True

def test_parse_pipeline_endpoint() -> None:
    """FastAPI 엔드포인트 테스트"""
    payload = {
        "nodes": [{"id": "1"}, {"id": "2"}, {"id": "3"}],
        "edges": [{"source": "1", "target": "2"}, {"source": "2", "target": "3"}]
    }
    response = client.post("/pipelines/parse", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["num_nodes"] == 3
    assert data["num_edges"] == 2
    assert data["is_dag"] is True
