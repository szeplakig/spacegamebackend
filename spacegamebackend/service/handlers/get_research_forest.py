from pydantic import BaseModel

from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.utils.forest import Node, build_research_forest


class ResearchForestResponse(BaseModel):
    nodes: list[Node]
    edges: dict[int, set[int]]  # Maps source node index to a set of target node indices
    node_rank: dict[int, int]  # Maps node index to its rank in the forest


class GetResearchForestHandler:
    def __init__(
        self,
        user_research_repository: UserResearchRepository,
        user_structure_repository: UserStructureRepository,
    ) -> None:
        self.user_research_repository = user_research_repository
        self.user_structure_repository = user_structure_repository

    def handle(self, user_id: str) -> ResearchForestResponse:
        research_levels = self.user_research_repository.get_user_research(user_id=user_id)
        structure_levels = self.user_structure_repository.get_user_structure_levels(user_id=user_id)
        nodes, edges, node_rank = build_research_forest(research_levels, structure_levels)
        normalized_edges_with_node_index: dict[int, set[int]] = {
            nodes.index(source): {nodes.index(target) for target in targets} for source, targets in edges.items()
        }
        normalized_node_rank = {nodes.index(node): rank for node, rank in node_rank.items()}
        return ResearchForestResponse(
            nodes=nodes,
            edges=normalized_edges_with_node_index,
            node_rank=normalized_node_rank,
        )
