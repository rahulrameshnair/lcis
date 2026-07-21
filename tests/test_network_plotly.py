import pytest


nx = pytest.importorskip("networkx")


def _sample_lci_database():
    return [
        {
            "Project Parameters": [],
            "Database Parameters": [],
            "Activity Parameters": [],
        },
        {
            "Activity A": {
                "name": "Activity A",
                "database": "demo_db",
                "location": "GLO",
                "unit": "kilogram",
                "exchanges": [
                    {
                        "type": "production",
                        "reference product": "Product A",
                        "amount": 1.0,
                        "unit": "kilogram",
                    },
                    {
                        "type": "technosphere",
                        "reference product": "Input B",
                        "amount": 2.0,
                        "unit": "kilogram",
                    },
                    {
                        "type": "biosphere",
                        "name": "CO2",
                        "amount": 3.0,
                        "unit": "kilogram",
                    },
                ],
            }
        },
    ]


def test_activity_metadata_is_keyed_by_activity_node_id():
    from lcis.inventory.lci import LCI

    graph, node_attributes = LCI.network(_sample_lci_database())

    assert "Activity - Activity A" in graph.nodes
    assert "Activity - Activity A" in node_attributes
    assert "Activity A" not in node_attributes

    nx.set_node_attributes(graph, node_attributes)

    activity_attributes = graph.nodes["Activity - Activity A"]
    assert activity_attributes["name"] == "Activity A"
    assert activity_attributes["location"] == "GLO"


def test_network_to_plotly_figure_returns_node_and_edge_traces():
    pytest.importorskip("plotly")

    from lcis.inventory.network_plotly import network_to_plotly_figure

    graph = nx.DiGraph()
    graph.add_node("Activity - Activity A", color="blue", name="Activity A")
    graph.add_node("Product A")
    graph.add_edge(
        "Activity - Activity A",
        "Product A",
        color="black",
        amount=1.0,
        unit="kilogram",
    )

    figure = network_to_plotly_figure(graph)

    assert len(figure.data) >= 2
    assert any(trace.mode == "markers" for trace in figure.data)
    assert any(trace.mode == "lines" for trace in figure.data)
