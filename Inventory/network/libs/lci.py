# Life cycle inventory databases
import os, sys

# Add the parent directory of export to the Python path
working_dir = os.getcwd()
# print (working_dir)

import bw2data as bw
from bw2data.parameters import ActivityParameter, DatabaseParameter, ProjectParameter
from .extract import Extract_from_lci as extract
import pprint
import networkx as nx


class LCI:

    def __init__(self, project_name, database_name) -> None:
        """
        Initializes the LCI class by setting the current project and selecting a database within Brightway2.

        Args:
            project_name (str): The name of the Brightway2 project to set as current.
            database_name (str): The name of the database to work with within the specified project.

        Returns:
            None
        """
        bw.projects.set_current(project_name)
        self.database = bw.Database(database_name)
        self.lci_dbs = []

    def database_list(self, keys_biosphere, keys_technosphere, keys_production):
        """
        Compiles a comprehensive list of the life cycle inventory (LCI) database, including project, database,
        and activity parameters. It also captures and organizes the exchanges related to each activity based on specified keys.

        Args:
            keys_biosphere (list): Keys specific to biosphere exchanges.
            keys_technosphere (list): Keys specific to technosphere exchanges.
            keys_production (list): Keys specific to production exchanges.

        Returns:
            lci_database (list): A list containing dictionaries of project parameters, database parameters, activity parameters,
            and detailed activity information including exchanges.
        """
        lci_database = []  # list of dictionaries to store the life cycle inventory

        parameters = {}  # to store the final parameters dict
        (
            project_parameter_details,
            activity_parameter_details,
            database_parameter_details,
        ) = ([], [], [])

        # Storing project parameters as a list of dictionary items
        for parameter in ProjectParameter.select():

            parameter_dict = {
                "name": parameter.name,
                "amount": parameter.amount,
                "formula": parameter.formula,
            }
            project_parameter_details.append(parameter_dict)

        # stores project parameters as a list of dictionaries with the key 'Project Parameters'
        parameters["Project Parameters"] = project_parameter_details

        # Storing database parameters as a list of dictionary items

        for parameter in DatabaseParameter.select():

            parameter_dict = {
                "name": parameter.name,
                "amount": parameter.amount,
                "formula": parameter.formula,
                "database": parameter.database,
            }
            database_parameter_details.append(parameter_dict)
        parameters["Database Parameters"] = database_parameter_details

        # Storing activity parameters as a list of dictionary items

        for parameter in ActivityParameter.select():

            parameter_dict = {
                "name": parameter.name,
                "amount": parameter.amount,
                "formula": parameter.formula,
                "database": parameter.database,
            }
            activity_parameter_details.append(parameter_dict)
        parameters["Activity Parameters"] = activity_parameter_details
        lci_database = [parameters]
        activities_dict = {}
        for activity in self.database:
            key = activity["name"]
            activities_dict[key] = activity.as_dict()
            exchanges_list = []

            for exchange in activity.exchanges():
                exchange_dict = exchange.as_dict()
                # print (exchange_dict)
                if exchange_dict.get("name") is not None:
                    # print (exchange_dict)
                    del exchange_dict["input"]
                    del exchange_dict["output"]
                    # print(exchange_dict)
                    exchanges_list.append(exchange_dict)
                # pprint.pprint (exchanges_list)

                else:
                    exchange_db, exchange_code = extract.classify_exchanges(
                        exchange.as_dict(), exchange_dict["type"]
                    )
                    # print(exchange_dict)
                    # print(exchange_db, exchange_code, "\n")
                    exchange_details = extract.extract_all_details(
                        exchange_db, exchange_code
                    )
                    if exchange_dict["type"] == "biosphere":
                        updated_exchange_details = extract.update_exchange_details(
                            exchange_details, keys_biosphere
                        )
                    elif exchange_dict["type"] == "technosphere":
                        updated_exchange_details = extract.update_exchange_details(
                            exchange_details, keys_technosphere
                        )
                    elif exchange_dict["type"] == "production":
                        updated_exchange_details = extract.update_exchange_details(
                            exchange_details, keys_production
                        )

                    updated_exchange_details["amount"] = exchange_dict["amount"]
                    updated_exchange_details["type"] = exchange_dict["type"]
                    updated_exchange_details["formula"] = (
                        exchange_dict["formula"]
                        if exchange_dict.get("formula") is not None
                        else None
                    )
                    # print(exchange_dict)
                    # print(updated_exchange_details, "\n")
                    exchanges_list.append(updated_exchange_details)
            activities_dict[key]["exchanges"] = exchanges_list

        lci_database = [parameters, activities_dict]
        self.lci_dbs = lci_database
        return lci_database

    @staticmethod
    def key_search(node_attributes):
        """
        Checks for keys that are present with in the nested node_attributes dictionary (created from the LCI) that contains values with incompatible dataypes (other than str, int, bool, and float).

        Args:
        node_attributes (dict): attributes of nodes created from the lci database

        Return:
        keys_to_remove (list): keys carrying the values with incompatible datypes
        datatypes_keys (list): datatypes of the above-mentioned keys
        keys_values_types (dict): key, values and their corresponding datatypes
        """
        keys_to_remove = []
        datatypes_keys = []
        key_values_types = {}
        for key in node_attributes:
            # print (key)
            for key2 in node_attributes[key]:
                # print ('\t', key2, '->', type(node_attributes[key][key2]))
                key_values_types[key] = tuple(
                    [key2, str(type(node_attributes[key][key2]))]
                )
                if (
                    not isinstance(node_attributes[key][key2], (str, int, float, bool))
                    and key2 not in keys_to_remove
                ):
                    keys_to_remove.append(key2)
                    datatypes_keys.append(type(node_attributes[key][key2]))
        return (keys_to_remove, datatypes_keys, key_values_types)

    @staticmethod
    def recursive_search(node_details):
        """
        Recursively searches and modifies node details to ensure compatibility for network graphing,
        such as converting tuples to strings and replacing None values with a string representation.

        Args:
            node_details (dict): The node details dictionary from the LCI data.

        Returns:
            node_details (dict): The modified node details dictionary after recursive processing.
        """
        for key, value in node_details.items():
            if key == "categories" and isinstance(value, tuple):
                node_details[key] = "::".join(value)
            if value is None:
                node_details[key] = "none"
            if isinstance(value, dict):
                LCI.recursive_search(value)
        return node_details

    @staticmethod
    def network(lci_database):
        """
        Creates a network and the corresponding node attributes from an inventory passed on as list

        Args:
        lci_database (list): the life cycle inventory (returned by LCI.lci_database)

        Returns:
        network_graph (class): the network graph generated from the life cycle inventory
        node_attributes (dict): the attributes of the all the nodes present in the network

        """

        # Define styling scheme for the network

        # --------------------------
        # Colors for nodes and edges
        activity_node_color = "blue"
        production_node_color = "black"
        production_edge_color = "black"
        technosphere_node_color = "purple"
        technosphere_edge_color = "purple"
        biosphere_node_color = "green"
        biosphere_edge_color = "green"

        # line types for nodes and edges
        production_line_style = "Solid"
        technosphere_line_style = "Dash"
        biosphere_line_style = "Dots"

        # node widths and heights
        parent_activity_width = 26
        production_node_width = 22
        technosphere_node_width = 20
        biosphere_node_width = 20
        # ----------------------------

        network_graph = nx.DiGraph()
        node_attributes = {}
        activities_dict = lci_database[
            1
        ]  # Here, pos 0 is taken by parameters dict and 1 is taken by activities dict. Change, if required.
        for activity in activities_dict:
            activity_info = {}
            for key_in_activity in activities_dict[activity]:
                if key_in_activity != "exchanges":
                    activity_info[key_in_activity] = activities_dict[activity][
                        key_in_activity
                    ]
            activity_name = "Activity - " + str(activity_info["name"])
            network_graph.add_node(
                activity_name, color=activity_node_color, width=parent_activity_width
            )
            node_attributes[activity_info["name"]] = activity_info

            exchanges = activities_dict[activity]["exchanges"]

            for ex in exchanges:
                if ex["type"] == "production":
                    network_graph.add_edge(
                        activity_name,
                        ex["reference product"],
                        color=production_edge_color,
                        line_type=production_line_style,
                        arrows=True,
                    )
                elif ex["type"] =="technosphere":
                    network_graph.add_edge(
                        ex["reference product"],
                        activity_name,
                        color=technosphere_edge_color,
                        line_type=technosphere_line_style,
                        arrows=True,
                    )
                elif ex["type"] == "biosphere":
                    
                    network_graph.add_edge(
                            activity_name,
                            ex["name"],
                            color=biosphere_edge_color,
                            line_type=biosphere_line_style,
                            arrows=True,
                    )


        return (network_graph, node_attributes)
