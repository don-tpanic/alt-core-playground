"""Response models for the prompts."""

from pydantic import BaseModel, Field


class SummarizeMethods(BaseModel):
    """Output for summarize_methods prompt."""

    methods: str = Field(description="Summary of the paper's methods in sentence form")


class KGAsText(BaseModel):
    """Output for convert_kg_to_text prompt."""

    results: str = Field(
        description="Brief paragraph describing the results of main study/experiment"
    )


class KGNode(BaseModel):
    """Represents a node in the knowledge graph."""

    id: int = Field(description="Unique identifier for the node")
    label: str = Field(description="Text label describing the node's content")


class KGEdge(BaseModel):
    """Represents an edge in the knowledge graph."""

    source: int = Field(description="ID of the source node")
    target: int = Field(description="ID of the target node")
    relation: str = Field(description="Text describing the relationship between nodes")


class KGExperiment(BaseModel):
    """Represents a single experiment with its nodes and edges."""

    experiment_name: str = Field(description="Name of the experiment")
    nodes: list[KGNode] = Field(description="List of nodes in this experiment")
    edges: list[KGEdge] = Field(description="List of edges connecting the nodes")


class InitialKG(BaseModel):
    """Output for create_initial_kg prompt."""

    knowledge_graph: list[KGExperiment] = Field(
        description="List of experiments with their graph structures"
    )

    def to_dict_format(self) -> dict:
        """Format InitialKG into the required dictionary format.

        Returns:
            dict: Formatted knowledge graph with experiment_N keys
        """
        formatted_kg = {}

        for i, experiment in enumerate(self.knowledge_graph, 1):
            formatted_kg[f"experiment_{i}"] = {
                "nodes": [{"id": node.id, "label": node.label} for node in experiment.nodes],
                "edges": [
                    {"source": edge.source, "target": edge.target, "relation": edge.relation}
                    for edge in experiment.edges
                ],
            }

        return formatted_kg


class SemanticNode(BaseModel):
    """Represents a node in a semantic group."""

    id: int = Field(description="Unique identifier for the node")
    label: str = Field(description="Text label describing the node's content")
    level: int = Field(description="Granularity level of the node")


class SemanticGroup(BaseModel):
    """Represents a semantic group of nodes."""

    group_name: str = Field(description="Name of the semantic group")
    nodes: list[SemanticNode] = Field(description="List of nodes in this semantic group")


class ExperimentSemanticGroups(BaseModel):
    """Represents a semantic group of nodes."""

    experiment_name: str = Field(description="Name of the experiment")
    semantic_groups: list[SemanticGroup] = Field(
        description="List of semantic groups with group name and nodes"
    )


class IdentifiedSemanticGroups(BaseModel):
    """Output for identify_semantic_groups prompt."""

    experiment_semantic_groups: list[ExperimentSemanticGroups] = Field(
        description=("List of semantic groups with experiment name and nodes")
    )

    def to_dict_format(self) -> dict:
        """Format IdentifiedSemanticGroups into the required dictionary format.

        Returns:
            dict: Formatted semantic groups with experiment_N keys
        """
        formatted_groups = {}

        for i, experiment in enumerate(self.experiment_semantic_groups, 1):
            experiment_groups = {}
            for semantic_group in experiment.semantic_groups:
                experiment_groups[semantic_group.group_name] = [
                    {"id": node.id, "label": node.label, "level": node.level}
                    for node in semantic_group.nodes
                ]
            formatted_groups[f"experiment_{i}"] = experiment_groups

        return formatted_groups
