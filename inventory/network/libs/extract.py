#extract.py
'''
Module for extracting and organizing data from exchanges within an activity present in the brightway database

'''
import brightway2 as bw
import bw2data as bd

def extract_details (name_selected_database, exchange_name, exchange_type):
    """
    A function to return specific parameters such as name, unit, location etc. of an exchange 
    (biosphere, technosphere or production) belonging to an activity
    """
    if exchange_type == 'biosphere':
        selected_database = bw.Database(name_selected_database)
        name = selected_database.get(exchange_name)['name']
        #since some biosphere categories are tuples containing multiple element, we need a for loop to extract all category values
        categories =''
        for item in selected_database.get(exchange_name)['categories']:
            categories = categories + ', ' + item
        unit = selected_database.get(exchange_name)['unit']
        return selected_database, name, categories, unit
    else:
        selected_database = bw.Database(name_selected_database)
        name = selected_database.get(exchange_name)['name']
        reference_product = selected_database.get(exchange_name)['reference product']
        location = selected_database.get(exchange_name)['location']
        unit = selected_database.get(exchange_name)['unit']
        return selected_database, name, reference_product, location, unit #returning the results as a tuple

def extract_all_details(name_selected_database, exchange_name):
    """
    A function to return all the details concerning an exchange that belongs to an activity
    in a dictionary format.
    """
    selected_database = bw.Database(name_selected_database)
    details = selected_database.get(exchange_name).as_dict()
    return details

def organize_all_details(details_of_exchange, exchange_dict, key_names, exchange_type ):
    """
    organize_all details (#details of exchange extracted from 'input' or 'output' tuples of the exchange (a), 
    #dictionary containing all exchange details in the activity (b), #name of keys to be added from (b) to (a) )
    """
    for key in key_names:
        details_of_exchange[key] = exchange_dict[key]
    organized_details = details_of_exchange
    if exchange_type == 'biosphere':
        #convert category tuple with in the biosphere exchange to a string with the format of "primary category:: others" such as "air::urban air close to ground"
        categories = f"{details_of_exchange['categories'][0]}::{' '.join(map(str, details_of_exchange['categories'][1:]))}"
        organized_details['categories'] = categories
           
    return organized_details

def classify_exchanges(exchange_dict, exchange_type):
    """
    Classifies the exchanges within an activity based on its type.

    Args:
        exchange_dict (dictionary): the dictionary of information of an exchange within an activity
        exchange_type (string): the type of the exchange (usua;;y technosphere, production, or biosphere)

    Returns:
        exchange_database (string): name of the database from which exchange is taken
        exchange_code (int): the code of this exchange within this database
    """
    if exchange_type == 'technosphere' or exchange_type == 'biosphere':
        exchange_db, exchange_code = exchange_dict['input'][0], exchange_dict['input'][1]
    elif exchange_type == 'production':
        exchange_db, exchange_code = exchange_dict['output'][0], exchange_dict['output'][1]
    return (exchange_db, exchange_code)

def update_exchange_details(exchange_details, list_of_keys):
    updated_exchange_details = {}
    for key in list_of_keys:
        updated_exchange_details [key] = exchange_details[key]
    return (updated_exchange_details)
