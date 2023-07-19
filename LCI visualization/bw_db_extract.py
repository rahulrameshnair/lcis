import brightway2 as bw
import bw2data as bd

'''
Documentation
A brightway database and an exchange is passed as input arguments. Then, the functions below returns the different non-activity specific details of these exchanges

'''


def extract_details (name_selected_database, exchange_name, exchange_type):
    #function to return name of the activity it belongs to, reference product, location and unit of an exchange
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