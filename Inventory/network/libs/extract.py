# extract.py
"""
Module for extracting and organizing data from exchanges within an activity present in the brightway dataset

"""
import brightway2 as bw
import bw2data as bd


class Extract_from_lci:

    def extract_details(self, name_selected_database, exchange_name, exchange_type):
        """
        A function to return specific parameters such as name, unit, location etc. of an exchange
        (biosphere, technosphere or production) belonging to an activity
        """
        """
        Retrieves specific parameters such as name, unit, location etc. of an exchange (biosphere, technosphere, or production)
        from the specified database based on the exchange type.

        Args:
            name_selected_database (str): The name of the database to search within.
            exchange_name (str): The identifier of the exchange within the database.
            exchange_type (str): The type of exchange ('biosphere', 'technosphere', or 'production').

        Returns:
            tuple: Depending on the exchange type, returns different tuples:
                - For biosphere: (selected_database, name, categories, unit)
                - For others: (selected_database, name, reference product, location, unit)
        """
        if exchange_type == "biosphere":
            selected_database = bw.Database(name_selected_database)
            name = selected_database.get(exchange_name)["name"]
            # since some biosphere categories are tuples containing multiple element, we need a for loop to extract all category values
            categories = ""
            for item in selected_database.get(exchange_name)["categories"]:
                categories = categories + ", " + item
            unit = selected_database.get(exchange_name)["unit"]
            return selected_database, name, categories, unit
        else:
            selected_database = bw.Database(name_selected_database)
            name = selected_database.get(exchange_name)["name"]
            reference_product = selected_database.get(exchange_name)[
                "reference product"
            ]
            location = selected_database.get(exchange_name)["location"]
            unit = selected_database.get(exchange_name)["unit"]
            return (
                selected_database,
                name,
                reference_product,
                location,
                unit,
            )  # returning the results as a tuple

    def extract_all_details(self, name_selected_database, exchange_name):
        """
        Retrieves all details of a specified exchange in an activity in dictionary format.

        Args:
            name_selected_database (str): The name of the database where the exchange is stored.
            exchange_name (str): The identifier of the exchange within the database.

        Returns:
            details (dict): A dictionary containing all details of the exchange.
        """
        selected_database = bw.Database(name_selected_database)
        details = selected_database.get(exchange_name).as_dict()
        return details

    def organize_all_details(
        self, details_of_exchange, exchange_dict, key_names, exchange_type
    ):
        """
        Organizes and augments details of an exchange based on specified keys from an exchange dictionary.

        Args:
            details_of_exchange (dict): The initial exchange details.
            exchange_dict (dict): Dictionary containing all relevant exchange details.
            key_names (list): List of keys to add from exchange_dict to details_of_exchange.
            exchange_type (str): Type of exchange ('biosphere', 'technosphere', or 'production').

        Returns:
            dict: The updated and organized exchange details.
        """
        for key in key_names:
            details_of_exchange[key] = exchange_dict[key]
        organized_details = details_of_exchange
        if exchange_type == "biosphere":
            # convert category tuple with in the biosphere exchange to a string with the format of "primary category:: others" such as "air::urban air close to ground"
            categories = f"{details_of_exchange['categories'][0]}::{' '.join(map(str, details_of_exchange['categories'][1:]))}"
            organized_details["categories"] = categories

        return organized_details

    def classify_exchanges(self, exchange_dict, exchange_type):
        """
        Classifies the exchanges within an activity based on its type.

        Args:
            exchange_dict (dictionary): the dictionary of information of an exchange within an activity
            exchange_type (string): the type of the exchange (usua;;y technosphere, production, or biosphere)

        Returns:
            exchange_database (string): name of the database from which exchange is taken
            exchange_code (int): the code of this exchange within this database
        """
        if exchange_type == "technosphere" or exchange_type == "biosphere":
            exchange_db, exchange_code = (
                exchange_dict["input"][0],
                exchange_dict["input"][1],
            )
        elif exchange_type == "production":
            exchange_db, exchange_code = (
                exchange_dict["output"][0],
                exchange_dict["output"][1],
            )
        return (exchange_db, exchange_code)

    def update_exchange_details(self, exchange_details, specified_keys):
        """
        Updates exchange details based on a list of specified keys.

        Args:
            exchange_details (dict): The original exchange details.
            specified_keys (list): Keys to extract from the original details.

        Returns:
            dict: A dictionary containing updated details as specified by specified_keys.
        """
        updated_exchange_details = {}
        for key in specified_keys:
            updated_exchange_details[key] = exchange_details[key]
        return updated_exchange_details
