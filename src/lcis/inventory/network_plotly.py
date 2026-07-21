"""Optional Plotly notebook previews for LCIS inventory networks.

This module is intentionally separate from the GraphML exporter. GraphML remains
the primary network export format, while these helpers provide a lightweight
interactive preview for Jupyter notebooks when Plotly is installed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PlotlyNetworkConfig:
    """Configuration for Plotly network previews."""
    """
    The preview is meant for quick visual inspection, not for replacing
    Cytoscape or other external graph tools. The layout seed keeps notebook
    previews reproducible across runs, while the visual settings control only
    the Plotly rendering and do not affect GraphML export.
    """

    layout_seed: int = 42
    node_size: int = 12
    edge_width: float = 1.5
    show_edge_hover: bool = True


def build_plotly_network_graph(
    project_name: str,
    database_name: str,
    key_config: Any | None = None,
    *,
    drop_incompatible_attributes: bool = True,
):
    """Build the cleaned NetworkX graph used for a Plotly notebook preview."""
    """
    This function mirrors the existing network export preparation but stops
    before writing GraphML. It selects the Brightway project/database, builds
    the LCIS network, normalizes node attributes, and optionally removes values
    that are incompatible with common graph serialization workflows.
    """

    import bw2data as bw
    import networkx as nx

    from lcis.inventory import lci as inventory
    from lcis.inventory.lci_network import (
        NetworkKeyConfig,
        _drop_incompatible_node_attributes,
    )

    key_config = key_config or NetworkKeyConfig()

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
    return network_graph


def network_to_plotly_figure(graph, config: PlotlyNetworkConfig | None = None):
    """Convert a NetworkX graph into a Plotly figure for notebook display."""
    """
    Plotly and NetworkX are imported inside this function so LCIS remains
    import-safe when optional plotting dependencies are not installed. The
    figure uses the graph's existing node and edge attributes for hover text
    and styling where possible.
    """

    config = config or PlotlyNetworkConfig()
    go = _require_plotly()

    import networkx as nx

    positions = nx.spring_layout(graph, seed=config.layout_seed)
    edge_traces = _edge_traces(graph, positions, go, config)
    node_trace = _node_trace(graph, positions, go, config)

    figure = go.Figure(data=[*edge_traces, node_trace])
    figure.update_layout(
        showlegend=False,
        hovermode="closest",
        margin={"b": 20, "l": 5, "r": 5, "t": 20},
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
    )
    return figure


def plot_network(
    project_name: str,
    database_name: str,
    key_config: Any | None = None,
    config: PlotlyNetworkConfig | None = None,
):
    """Build and return a Plotly preview figure for a Brightway database."""
    """
    This is the convenience function intended for notebooks. It keeps the
    notebook cell small by combining graph construction and Plotly conversion,
    while leaving the GraphML export workflow untouched.
    """

    _require_plotly()
    graph = build_plotly_network_graph(
        project_name,
        database_name,
        key_config=key_config,
    )
    return network_to_plotly_figure(graph, config=config)


def _require_plotly():
    try:
        import plotly.graph_objects as go
    except ModuleNotFoundError as error:
        raise ModuleNotFoundError(
            "Install plotly to use LCIS notebook network previews."
        ) from error
    return go


def _edge_traces(graph, positions, go, config: PlotlyNetworkConfig) -> list[Any]:
    edge_points_by_color: dict[str, dict[str, list[Any]]] = {}
    edge_hover_x: list[float] = []
    edge_hover_y: list[float] = []
    edge_hover_text: list[str] = []

    for source, target, attributes in graph.edges(data=True):
        x0, y0 = positions[source]
        x1, y1 = positions[target]
        color = str(attributes.get("color", "#9ca3af"))
        points = edge_points_by_color.setdefault(color, {"x": [], "y": []})
        points["x"].extend([x0, x1, None])
        points["y"].extend([y0, y1, None])

        if config.show_edge_hover:
            edge_hover_x.append((x0 + x1) / 2)
            edge_hover_y.append((y0 + y1) / 2)
            edge_hover_text.append(_format_edge_hover(source, target, attributes))

    traces = [
        go.Scatter(
            x=points["x"],
            y=points["y"],
            mode="lines",
            line={"width": config.edge_width, "color": color},
            hoverinfo="none",
        )
        for color, points in edge_points_by_color.items()
    ]

    if config.show_edge_hover and edge_hover_text:
        traces.append(
            go.Scatter(
                x=edge_hover_x,
                y=edge_hover_y,
                mode="markers",
                marker={"size": 8, "color": "rgba(0,0,0,0)"},
                text=edge_hover_text,
                hoverinfo="text",
            )
        )

    return traces


def _node_trace(graph, positions, go, config: PlotlyNetworkConfig):
    node_x: list[float] = []
    node_y: list[float] = []
    node_color: list[str] = []
    node_text: list[str] = []

    for node, attributes in graph.nodes(data=True):
        x, y = positions[node]
        node_x.append(x)
        node_y.append(y)
        node_color.append(str(attributes.get("color", "#6b7280")))
        node_text.append(_format_node_hover(node, attributes))

    return go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        marker={
            "size": config.node_size,
            "color": node_color,
            "line": {"width": 1, "color": "#111827"},
        },
        text=node_text,
        hoverinfo="text",
    )


def _format_node_hover(node: Any, attributes: dict[str, Any]) -> str:
    lines = [f"<b>{node}</b>"]
    for key, value in attributes.items():
        lines.append(f"{key}: {value}")
    return "<br>".join(lines)


def _format_edge_hover(source: Any, target: Any, attributes: dict[str, Any]) -> str:
    lines = [f"<b>{source} -> {target}</b>"]
    for key, value in attributes.items():
        lines.append(f"{key}: {value}")
    return "<br>".join(lines)


__all__ = [
    "PlotlyNetworkConfig",
    "build_plotly_network_graph",
    "network_to_plotly_figure",
    "plot_network",
]
