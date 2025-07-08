# Research Tree with requirements
# I want to build a research tree where you can see what buildings and research are required to unlock
# other buildings and research.
# The tree will be a directed acyclic graph (DAG) where each node is a building or research and the
# edges are the requirements to unlock them.
# The tree will be used to display the research and building options in the game.
# The tree will be built from the current level of each research currently researched by the user.
# Then I will add the requirement for these researches in a queue to be processed and added to the tree.
# Then after I drilled down the tree to the lowest level where no more requirements are found, I will
# add the researches and buildings that come after the current researches.


from pydantic import BaseModel

import spacegamebackend.application  # noqa: F401
from spacegamebackend.domain.models.research.research_template import ResearchTemplate
from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.domain.models.structure.structure_template import (
    StructureTemplate,
)
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.utils.int_to_roman import int_to_roman
from spacegamebackend.utils.research_requirement_component import ResearchRequirement
from spacegamebackend.utils.resource_requirement_component import ResourceRequirement
from spacegamebackend.utils.structure_requirement_component import StructureRequirement


class ResearchNode(BaseModel, frozen=True):
    node_type: str = "research"
    title: str
    type: ResearchType
    level: int
    status: str

    def __hash__(self) -> int:
        return hash((self.node_type, self.type, self.level))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ResearchNode):
            return NotImplemented
        return self.node_type == other.node_type and self.type == other.type and self.level == other.level


class StructureNode(BaseModel, frozen=True):
    node_type: str = "structure"
    title: str
    type: StructureType
    level: int
    status: str

    def __hash__(self) -> int:
        return hash((self.node_type, self.type, self.level))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StructureNode):
            return NotImplemented
        return self.node_type == other.node_type and self.type == other.type and self.level == other.level


Node = ResearchNode | StructureNode


def build_research_forest(
    research_levels: dict[ResearchType, int],
    structures_levels: dict[StructureType, int],
) -> tuple[
    list[Node],
    dict[
        Node,
        set[Node],
    ],
    dict[Node, int],
]:
    """Builds a research tree from the given researches and structures.
    The tree will be a directed acyclic graph (DAG) where each node is a building or research
    and the edges are the requirements to unlock them.
    The tree will be used to display the research and building options in the game.
    It can have multiple roots, as the user can have multiple researches and structures at different levels.

    Args:
        research_levels (dict[ResearchType, int]): The researches currently researched by the user,
            where the key is the research type and the value is the level.
        structures_levels (dict[StructureType, int]): The structures currently built by the user,
            where the key is the structure type and the value is the max level built anywhere in their Empire.
    """

    nodes: list[Node] = []
    edges: dict[
        Node,
        set[Node],
    ] = {}

    find_requirements: list[Node] = []

    for research_type, level in {
        research_type: research_levels.get(research_type, 0) for research_type in ResearchTemplate.research_templates
    }.items():
        r_node = ResearchNode(
            type=research_type,
            level=level + 1,
            status="unlockable",
            title=ResearchTemplate.get_research_template(research_type).title + " " + int_to_roman(level + 1),
        )
        if r_node not in nodes:
            nodes.append(r_node)
            find_requirements.append(r_node)

    for structure_type, level in {
        structure_type: structures_levels.get(structure_type, 0)
        for structure_type in StructureTemplate.structure_templates
    }.items():
        s_node = StructureNode(
            type=structure_type,
            level=level + 1,
            status="unlockable",
            title=StructureTemplate.get_structure_template(structure_type).title + " " + int_to_roman(level + 1),
        )
        if s_node not in nodes:
            nodes.append(s_node)
            find_requirements.append(s_node)

    while find_requirements:
        explore_node = find_requirements.pop(0)
        if isinstance(explore_node, ResearchNode):
            research_template = ResearchTemplate.get_research_template(explore_node.type)
            for component in research_template.scale(
                level=explore_node.level
            ).requirement_components.components.values():
                # TODO: refactor duplicate code
                if isinstance(component, ResearchRequirement):
                    new_node = ResearchNode(  # type: ignore[assignment]
                        type=component.research_type,
                        level=component.get_scaled_value(),
                        status=(
                            "unlocked"
                            if component.get_scaled_value() <= research_levels.get(component.research_type, 0)
                            else "unlockable"
                        ),
                        title=(
                            ResearchTemplate.get_research_template(component.research_type).title
                            + " "
                            + int_to_roman(component.get_scaled_value())
                        ),
                    )
                    if new_node.level < 1:
                        continue
                    edges.setdefault(explore_node, set()).add(new_node)
                    if new_node not in nodes:
                        nodes.append(new_node)
                        find_requirements.append(new_node)
                elif isinstance(component, StructureRequirement):
                    new_node = StructureNode(  # type: ignore[assignment]
                        type=component.structure_type,
                        level=component.get_scaled_value(),
                        status=(
                            "unlocked"
                            if component.get_scaled_value() <= structures_levels.get(component.structure_type, 0)
                            else "unlockable"
                        ),
                        title=(
                            StructureTemplate.get_structure_template(component.structure_type).title
                            + " "
                            + int_to_roman(component.get_scaled_value())
                        ),
                    )
                    if new_node.level < 1:
                        continue
                    edges.setdefault(explore_node, set()).add(new_node)
                    if new_node not in nodes:
                        nodes.append(new_node)
                        find_requirements.append(new_node)
                else:
                    continue
            prev_level = explore_node.level - 1
            if prev_level < 1:
                continue
            new_node = ResearchNode(
                type=research_template.research_type,
                level=prev_level,
                status=(
                    "unlocked"
                    if prev_level <= research_levels.get(research_template.research_type, 0)
                    else "unlockable"
                ),
                title=(research_template.title + " " + int_to_roman(prev_level)),
            )
            # edges.setdefault(explore_node, set()).add(new_node)
            if new_node not in nodes:
                nodes.append(new_node)
                find_requirements.append(new_node)
        elif isinstance(explore_node, StructureNode):
            structure_template = StructureTemplate.get_structure_template(explore_node.type)
            for component in structure_template.scale(
                level=explore_node.level
            ).requirement_components.components.values():
                if isinstance(component, ResearchRequirement):
                    new_node = ResearchNode(
                        type=component.research_type,
                        level=component.get_scaled_value(),
                        status=(
                            "unlocked"
                            if component.get_scaled_value() <= research_levels.get(component.research_type, 0)
                            else "unlockable"
                        ),
                        title=(
                            ResearchTemplate.get_research_template(component.research_type).title
                            + " "
                            + int_to_roman(component.get_scaled_value())
                        ),
                    )
                    if new_node.level < 1:
                        continue
                    edges.setdefault(explore_node, set()).add(new_node)
                    if new_node not in nodes:
                        nodes.append(new_node)
                        find_requirements.append(new_node)
                elif isinstance(component, StructureRequirement):
                    new_node = StructureNode(  # type: ignore[assignment]
                        type=component.structure_type,
                        level=component.get_scaled_value(),
                        status=(
                            "unlocked"
                            if component.get_scaled_value() <= structures_levels.get(component.structure_type, 0)
                            else "unlockable"
                        ),
                        title=(
                            StructureTemplate.get_structure_template(component.structure_type).title
                            + " "
                            + int_to_roman(component.get_scaled_value())
                        ),
                    )
                    if new_node.level < 1:
                        continue
                    edges.setdefault(explore_node, set()).add(new_node)
                    if new_node not in nodes:
                        nodes.append(new_node)
                        find_requirements.append(new_node)
                else:
                    continue
            prev_level = explore_node.level - 1
            if prev_level < 1:
                continue
            new_node = StructureNode(  # type: ignore[assignment]
                type=structure_template.structure_type,
                level=prev_level,
                status=(
                    "unlocked"
                    if prev_level <= structures_levels.get(structure_template.structure_type, 0)
                    else "unlockable"
                ),
                title=(structure_template.title + " " + int_to_roman(prev_level)),
            )
            # edges.setdefault(explore_node, set()).add(new_node)
            if new_node not in nodes:
                nodes.append(new_node)
                find_requirements.append(new_node)
        else:
            raise TypeError(f"Unknown type in research forest: {explore_node}")

    # go through all the nodes and calculate the longest path to each node with dfs into a new node_rank dict
    # calculate how many hops it takes to get to each node from the root nodes (
    # which are the nodes with no incoming edges)
    node_rank: dict[Node, int] = {}
    # edges are like what depends on each node, outgoing edges
    reverse_edges: dict[Node, set[Node]] = {}
    for node in nodes:
        if node not in edges:
            # If a node has no outgoing edges, it is a root node
            reverse_edges.setdefault(node, set())
            continue
        for dep in edges[node]:
            reverse_edges.setdefault(dep, set()).add(node)

    def dfs(node: Node, rank: int) -> None:
        if node in node_rank and node_rank[node] >= rank:
            return
        node_rank[node] = rank
        for dep in reverse_edges.get(node, []):
            dfs(dep, rank + 1)

    for node in nodes:
        if node not in node_rank:
            dfs(node, 0)

    return nodes, edges, node_rank


def calculate_total_resource_requirements(
    target_node: Node,
    research_levels: dict[ResearchType, int],
    structures_levels: dict[StructureType, int],
) -> dict[str, int]:
    nodes, edges, node_rank = build_research_forest(research_levels, structures_levels)
    visited = set()
    resource_totals: dict[str, int] = {}

    def collect_requirements(node: Node) -> None:
        if node in visited:
            return
        visited.add(node)
        # Get the template for the node
        template: ResearchTemplate | StructureTemplate
        if isinstance(node, ResearchNode):
            template = ResearchTemplate.get_research_template(node.type).scale(level=node.level)
        else:
            template = StructureTemplate.get_structure_template(node.type).scale(level=node.level)
        # Sum resource requirements
        # DEBUG: Print scaled requirements for this node
        print(f"Node: {node.title} (level {node.level})")

        for comp in template.requirement_components.components.values():
            if isinstance(comp, ResourceRequirement):
                print(f"  Requirement: {comp}")
                resource_totals[comp.resource_type] = (
                    resource_totals.get(comp.resource_type, 0) + comp.get_scaled_value()
                )
        # Recurse on dependencies
        for dep in edges.get(node, []):
            collect_requirements(dep)

    collect_requirements(target_node)
    return resource_totals


def main() -> None:
    target = StructureNode(
        type=StructureType.ORBITAL_GOVERNMENT_CENTER_T1,
        level=10,
        status="",
        title="",
    )

    structures_levels = {StructureType.ORBITAL_GOVERNMENT_CENTER_T1: 9}

    totals = calculate_total_resource_requirements(target, {}, structures_levels)

    print(totals)


if __name__ == "__main__":
    main()
