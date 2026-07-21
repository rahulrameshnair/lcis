"""Create GraphML network exports from Brightway inventories."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class NetworkKeyConfig:
    """Keys copied from Brightway exchanges into the LCIS network model."""

    biosphere: list[str] = field(
        default_factory=lambda: ["name", "database", "unit", "categories"]
    )
    technosphere: list[str] = field(
        default_factory=lambda: [
            "name",
            "database",
            "location",
            "unit",
            "reference product",
        ]
    )
    production: list[str] = field(
        default_factory=lambda: [
            "name",
            "database",
            "location",
            "unit",
            "reference product",
        ]
    )


def _drop_incompatible_node_attributes(
    node_attributes: dict,
    keys_to_remove: Iterable[str],
) -> dict:
    cleaned = {}
    for node, attributes in node_attributes.items():
        cleaned[node] = {
            key: value
            for key, value in attributes.items()
            if key not in keys_to_remove
        }
    return cleaned


def export_network(
    project_name: str,
    database_name: str,
    output_path: str | Path | None = None,
    key_config: NetworkKeyConfig | None = None,
    *,
    drop_incompatible_attributes: bool = True,
) -> Path:
    """Export a Brightway inventory network as GraphML.

    Parameters
    ----------
    project_name:
        Brightway project name.
    database_name:
        Brightway database name inside the project.
    output_path:
        Destination GraphML path. Defaults to ``<database_name>.graphml``.
    key_config:
        Optional exchange-key configuration. Defaults match the original
        notebook workflow.
    drop_incompatible_attributes:
        If true, node attributes with GraphML-incompatible value types are
        removed, matching the original notebook's cleanup step.
    """

    import bw2data as bw
    import networkx as nx

    from lcis.inventory import lci as inventory

    key_config = key_config or NetworkKeyConfig()
    output_path = Path(output_path or f"{database_name}.graphml")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    bw.projects.set_current(project_name)
    bw.Database(database_name)

    lci_db = inventory.LCI(project_name, database_name)
    lci_list = lci_db.database_list(
        key_config.biosphere,
        key_config.technosphere,
        key_config.production,
    )

    network_graph, node_attributes = inventory.LCI.network(lci_list)
    updated_node_attributes = lci_db.recursive_search(node_attributes)

    keys_to_remove, _, _ = inventory.LCI.key_search(updated_node_attributes)
    if drop_incompatible_attributes and keys_to_remove:
        updated_node_attributes = _drop_incompatible_node_attributes(
            updated_node_attributes,
            keys_to_remove,
        )

    nx.set_node_attributes(network_graph, updated_node_attributes)
    nx.write_graphml(
        network_graph,
        output_path,
        named_key_ids=True,
        encoding="utf-8",
        prettyprint=True,
    )

    return output_path


__all__ = ["NetworkKeyConfig", "export_network"]
