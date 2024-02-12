# Life cycle inventory databases
import os, sys
# Add the parent directory of export to the Python path
working_dir = os.getcwd()
parent_dir = os.path.join(os.getcwd(), os.pardir)
p_parent_dir = os.path.join(parent_dir, os.pardir) 
print(p_parent_dir)
sys.path.append(os.path.abspath(p_parent_dir))


import bw2data as bw
from bw2data.parameters import ActivityParameter, DatabaseParameter, ProjectParameter
from .inventory.network.libs import extract
import pprint
import networkx as nx

class LCI:

    def __init__(self, project_name, database_name) -> None:
        bw.projects.set_current(project_name)
        self.database = bw.Database(database_name)
        self.lci_db_list = []
    
    def LCI_database_list(self, keys_biosphere, keys_technosphere, keys_production):
        LCI_database_list = [] #list of dictionaries to store the life cycle inventory

        
        parameters={} #to store the final parameters dict
        project_parameter_details, activity_parameter_details, database_parameter_details = [], [], []
        
        #Storing project parameters as a list of dictionary items
        for parameter in ProjectParameter.select():
            
            parameter_dict = {'name':parameter.name, 
                            'amount': parameter.amount,
                            'formula': parameter.formula}
            project_parameter_details.append(parameter_dict)
        
        #stores project parameters as a list of dictionaries with the key 'Project Parameters'
        parameters['Project Parameters'] = project_parameter_details

        #Storing database parameters as a list of dictionary items

        for parameter in DatabaseParameter.select():
            
            parameter_dict = {'name':parameter.name, 
                            'amount': parameter.amount,
                            'formula': parameter.formula,
                            'database':parameter.database}
            database_parameter_details.append(parameter_dict)
        parameters['Database Parameters'] = database_parameter_details

        #Storing activity parameters as a list of dictionary items

        for parameter in ActivityParameter.select():
            
            parameter_dict = {'name':parameter.name, 
                            'amount': parameter.amount,
                            'formula': parameter.formula,
                            'database':parameter.database}
            activity_parameter_details.append(parameter_dict)
        parameters['Activity Parameters'] = activity_parameter_details
        LCI_database_list = [parameters]
        activities_dict = {}
        for activity in self.database:
            key = activity['name']
            activities_dict[key]=activity.as_dict()
            exchanges_list=[]

            for exchange in activity.exchanges():
                exchange_dict = exchange.as_dict()
                # print (exchange_dict)
                if exchange_dict.get('name') is not None:
                    # print (exchange_dict)
                    del exchange_dict['input']
                    del exchange_dict['output']
                    # print(exchange_dict)
                    exchanges_list.append(exchange_dict)
                # pprint.pprint (exchanges_list)
                    
                else:
                    exchange_db, exchange_code = extract.classify_exchanges (exchange.as_dict(), exchange_dict['type'])
                    # print(exchange_dict)
                    # print(exchange_db, exchange_code, "\n")
                    exchange_details = extract.extract_all_details(exchange_db, exchange_code)
                    if exchange_dict['type'] == 'biosphere':
                        updated_exchange_details = extract.update_exchange_details(exchange_details, keys_biosphere)
                    elif exchange_dict['type'] == 'technosphere':
                        updated_exchange_details = extract.update_exchange_details(exchange_details, keys_technosphere)
                    elif exchange_dict['type'] == 'production':
                        updated_exchange_details = extract.update_exchange_details(exchange_details, keys_production)

                    updated_exchange_details['amount']=exchange_dict['amount']
                    updated_exchange_details['type']=exchange_dict['type']
                    updated_exchange_details['formula'] = exchange_dict['formula'] if exchange_dict.get('formula') is not None else None
                    # print(exchange_dict)
                    # print(updated_exchange_details, "\n")
                    exchanges_list.append(updated_exchange_details)
            activities_dict[key]['exchanges'] = exchanges_list
        
        LCI_database_list = [parameters, activities_dict]
        self.lci_db_list = LCI_database_list
        return (LCI_database_list)
    @staticmethod
    def lci_key_search(node_attributes):
        """
        Checks for keys that are present with in the nested node_attributes dictionary (created from the LCI) that contains values with incompatible dataypes (other than str, int, bool, and float).

        Args:
        node_attributes (dict): attributes of nodes created from the lci database

        Return:
        keys_to_remove (list): keys carrying the values with incompatible datypes
        datatypes_keys (list): datatypes of the above-mentioned keys
        keys_values_types (dict): key, values and their corresponding datatypes
        """ 
        keys_to_remove=[]
        datatypes_keys=[]
        key_values_types ={}
        for key in node_attributes:
            # print (key)
            for key2 in node_attributes[key]:
                # print ('\t', key2, '->', type(node_attributes[key][key2]))
                key_values_types [key]= tuple([key2, str(type(node_attributes[key][key2]))])
                if not isinstance(node_attributes[key][key2], (str, int, float, bool)) and key2 not in keys_to_remove:
                    keys_to_remove.append(key2)
                    datatypes_keys.append(type(node_attributes[key][key2]))
        return (keys_to_remove, datatypes_keys, key_values_types)
    
    @staticmethod
    def lci_recursive_search(lcidict_to_search):
        #Include a generalized recursive search of the lci inventory here rather than in the jupyter notebook [TO-DO]
        pass

    @staticmethod
    def network(lci_db_list):
        """
        Creates a network and the corresponding node attributes from an inventory passed on as list

        Args:
        lci_db_list (list): the life cycle inventory (returned by LCI.LCI_database_list)

        Returns:
        network_graph (class): the network graph generated from the life cycle inventory
        node_attributes (dict): the attributes of the all the nodes present in the network
        
        """
        # Define styling scheme for the network

        #--------------------------
        #Colors for nodes and edges
        activity_node_color = "blue"
        production_node_color = 'black'
        production_edge_color = 'black'
        technosphere_node_color = 'purple'
        technosphere_edge_color = 'purple'
        biosphere_node_color ='green'
        biosphere_edge_color = 'green'

        #line types for nodes and edges
        production_line_style='Solid'
        technosphere_line_style='Dash'
        biosphere_line_style='Dots'

        # node widths and heights
        parent_activity_width = 26
        production_node_width = 22
        technosphere_node_width = 20
        biosphere_node_width = 20
        #----------------------------

        network_graph = nx.DiGraph()
        node_attributes = {}
        activities_dict = lci_db_list[1] # Here, pos 0 is taken by parameters dict and 1 is taken by activities dict. Change, if required.
        for activity in activities_dict:
            activity_info = {}
            for key_in_activity in activities_dict[activity]:
                if key_in_activity != 'exchanges':
                    activity_info[key_in_activity] = activities_dict[activity][key_in_activity]
            activity_name = 'Activity - ' + str(activity_info['name'])
            network_graph.add_node(activity_name, color=activity_node_color, width=parent_activity_width)
            node_attributes[activity_info['name']] = activity_info

            exchanges = activities_dict[activity]['exchanges']
            #print (exchanges)
            for ex in exchanges:
                # print(ex)
                if ex['type'] == 'production':
                    network_graph.add_node(ex['reference product'], color=production_node_color, width = production_node_width)
                    network_graph.add_edge(activity_name, ex['reference product'], color=production_edge_color, line_type=production_line_style, arrows=True)
                    node_attributes[ex['reference product']] = ex
                elif ex['type'] == 'technosphere':
                    network_graph.add_node(ex['reference product'], color=technosphere_node_color, width = technosphere_node_width)
                    network_graph.add_edge(ex['reference product'], activity_name, color=production_edge_color, line_type=production_line_style, arrows=True)
                    node_attributes[ex['reference product']] = ex
                else:
                    network_graph.add_node(ex['name'], color=biosphere_node_color, width = biosphere_node_width)
                    network_graph.add_edge(activity_name, ex['name'], color=biosphere_edge_color, line_type=biosphere_line_style, arrows=True)
                    node_attributes[ex['name']] = ex
                
        return (network_graph, node_attributes)