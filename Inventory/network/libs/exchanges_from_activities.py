import brightway2 as bw
import bw2data as bd


"""
Documentation
The purpose of this function is to invoke information of exchanges from within the new activities created in a database. New activities have their exchanges saved in a tuple format within dictionary. An example is as shown below for the activity called pyrolytic carbon in a database called materials2

Activity details:
 {'database': 'materials2', 'code': '421695138c4741af8deeb228ed68b13d', 'location': 'GLO', 'name': 'Pyrolytic carbon', 'reference product': 'Pyrolytic carbon', 'unit': 'kilogram', 'type': 'process'} activity details end 

Details of exchanges within this actvity:

{'output': ('materials2', '421695138c4741af8deeb228ed68b13d'), 'input': ('materials2', '421695138c4741af8deeb228ed68b13d'), 'amount': 0.65, 'type': 'production'}
{'output': ('materials2', '421695138c4741af8deeb228ed68b13d'), 'input': ('cutoff391', 'e77669e3f0e8d2473070ea895c442edb'), 'amount': 1, 'type': 'technosphere'}
{'output': ('materials2', '421695138c4741af8deeb228ed68b13d'), 'input': ('biosphere3', 'f9749677-9c9f-4678-ab55-c607dfdc2cb9'), 'amount': 0.35, 'type': 'biosphere'}

To get details about an exchange in such as activity, we pass the database name and activity key from the required exchange to this function. This function returns the name, unit and location

"""


def invoke_exchanges(database_name, exchange_key):
    """
    Retrieve and return basic details about an exchange from a specified brightway database.

    Args:
        database_name (str): The name of the database from which to retrieve exchange details.
        exchange_key (str): The unique key identifying the exchange within the database.

    Returns:
        exchange_name (str): name of the exchange
        exchange_unit (str): unit of the exchange
        exchange_location (str): region of this exchange

    Examples:
        >>> invoke_exchanges('materials2', '421695138c4741af8deeb228ed68b13d')
        ('Pyrolytic carbon', 'kilogram', 'GLO')
    """
    db_name = bw.Database(database_name)
    exchange_name = db_name.get(exchange_key)["name"]
    exchange_unit = db_name.get(exchange_key)["unit"]
    exchange_location = db_name.get(exchange_key)["location"]
    return (exchange_name, exchange_unit, exchange_location)
