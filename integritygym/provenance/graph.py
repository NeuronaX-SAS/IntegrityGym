"""
IntegrityGym Multi-Agent Provenance Graph
Tracks strategy propagation, knowledge dissemination, and coordination dynamics across agent populations.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Set


@dataclass
class ProvenanceNode:
    node_id: str
    node_type: str  # 'AGENT', 'STRATEGY', 'ARTIFACT', 'SHARED_BUS'
    label: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    quarantined: bool = False


@dataclass
class ProvenanceEdge:
    source_id: str
    target_id: str
    relation: str  # 'DISCOVERED', 'BROADCAST_TO', 'CONSUMED_BY', 'EXPLOITED', 'PRODUCES', 'CONSUMES'
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class ProvenanceGraph:
    """Directed graph recording how techniques and artifacts spread across an agent swarm."""

    def __init__(self):
        self.nodes: Dict[str, ProvenanceNode] = {}
        self.edges: List[ProvenanceEdge] = []

    def add_node(self, node_id: str, node_type: str, label: str, metadata: Dict[str, Any] = None) -> None:
        if node_id not in self.nodes:
            self.nodes[node_id] = ProvenanceNode(
                node_id=node_id,
                node_type=node_type,
                label=label,
                metadata=metadata or {},
            )

    def add_agent(self, agent_id: str, label: str = None, metadata: Dict[str, Any] = None) -> None:
        self.add_node(
            node_id=agent_id,
            node_type="AGENT",
            label=label or agent_id,
            metadata=metadata or {},
        )

    def add_artifact(self, artifact_id: str, producer_id: str = None, artifact_type: str = "ARTIFACT", metadata: Dict[str, Any] = None) -> None:
        meta = metadata or {}
        if producer_id:
            meta["producer_id"] = producer_id
        meta["artifact_type"] = artifact_type
        self.add_node(
            node_id=artifact_id,
            node_type="ARTIFACT",
            label=artifact_id,
            metadata=meta,
        )

    def add_edge(self, source_id: str, target_id: str, relation: str, timestamp: str = None, metadata: Dict[str, Any] = None) -> None:
        import datetime
        ts = timestamp or datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.edges.append(
            ProvenanceEdge(
                source_id=source_id,
                target_id=target_id,
                relation=relation,
                timestamp=ts,
                metadata=metadata or {},
            )
        )

    def quarantine_agent(self, agent_id: str, reason: str = "") -> None:
        """Quarantine agent and any downstream tainted artifacts and agents."""
        if agent_id in self.nodes:
            self.nodes[agent_id].quarantined = True
            self.nodes[agent_id].metadata["quarantine_reason"] = reason

            tainted_artifacts = set()
            for e in self.edges:
                if e.source_id == agent_id and e.relation in ["PRODUCES", "EXPLOITED", "DISCOVERED"]:
                    tainted_artifacts.add(e.target_id)
                    if e.target_id in self.nodes:
                        self.nodes[e.target_id].quarantined = True

            for e in self.edges:
                if (e.source_id in tainted_artifacts or e.target_id in tainted_artifacts) and e.relation in ["CONSUMED_BY", "CONSUMES"]:
                    consumer_id = e.target_id if e.source_id in tainted_artifacts else e.source_id
                    if consumer_id in self.nodes:
                        self.nodes[consumer_id].quarantined = True

    def compute_propagation_metrics(self, strategy_id: str) -> Dict[str, Any]:
        """Calculates adoption velocity and reach of a specific strategy through the swarm."""
        adopters: Set[str] = set()
        for edge in self.edges:
            if edge.target_id == strategy_id and edge.relation == "DISCOVERED":
                adopters.add(edge.source_id)
            if edge.source_id == strategy_id and edge.relation == "CONSUMED_BY":
                adopters.add(edge.target_id)

        total_agents = sum(1 for n in self.nodes.values() if n.node_type == "AGENT")
        penetration = (len(adopters) / total_agents) if total_agents > 0 else 0.0

        return {
            "strategy_id": strategy_id,
            "total_adopters": len(adopters),
            "total_agents": total_agents,
            "swarm_penetration_rate": round(penetration, 3),
            "adopters": sorted(list(adopters)),
        }

    def export_json(self, output_path: str | Path) -> None:
        """Exports the graph structure for visualization and reporting."""
        data = {
            "nodes": [
                {
                    "id": n.node_id,
                    "type": n.node_type,
                    "label": n.label,
                    "metadata": n.metadata,
                }
                for n in self.nodes.values()
            ],
            "edges": [
                {
                    "source": e.source_id,
                    "target": e.target_id,
                    "relation": e.relation,
                    "timestamp": e.timestamp,
                    "metadata": e.metadata,
                }
                for e in self.edges
            ],
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def to_mermaid(self) -> str:
        """Renders the provenance graph as Mermaid markdown for documentation and reports."""
        lines = ["graph TD"]
        for node in self.nodes.values():
            if node.node_type == "AGENT":
                lines.append(f'    {node.node_id}["🤖 Agent: {node.label}"]')
            elif node.node_type == "SHARED_BUS":
                lines.append(f'    {node.node_id}["📡 Shared Bus: {node.label}"]')
            else:
                lines.append(f'    {node.node_id}["⚡ Artifact: {node.label}"]')

        for edge in self.edges:
            lines.append(f"    {edge.source_id} -->|{edge.relation}| {edge.target_id}")

        return "\n".join(lines)
