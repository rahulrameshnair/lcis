import brightway2 as bw
import bw2data as bd

"""
Used for printing all the activities and their corresponding exchanges in a database according to the way in which
they are stored within the brightway database.
"""


def print_all(selected_database):
    """
    Prints all activities and their corresponding exchanges from a selected Brightway database.

    Each activity and its exchanges are displayed in dictionary format, showcasing details such as linked database names,
    activity codes, and other pertinent information.

    Args:
        selected_database (Database): The Brightway database object from which to print activities and exchanges.

    Returns:
        None
    """
    for activity in selected_database:
        print("Activity:", activity.as_dict(), "\n")
        for exchange in activity.exchanges():
            print("\t", "Exchange", exchange.as_dict(), "\n")
        print("\n")


def print_classified(selected_database):
    """
    Classifies and prints activities and their exchanges from the selected database, distinguishing between intrinsic
    and imported activities. This function also counts and displays the number of technosphere, biosphere, and product flows
    associated with each activity.

    Intrinsic activities are defined as those native to the database, while imported activities are derived from other databases.

    There is another type of flow called "downstream consumers" in the activity browser. This just means that if the product from one of the activity (a1, say) is used as a technosphere input for the activity (a2, say).
    Then, a2 becomes the downstream consumer of a1. This is not classified here because it is a just an interdependency.

    Args:
        selected_database (Database): The Brightway database object to analyze and print information from.

    Returns:
        None
    """
    imported_activity_counter = 0
    intrinsic_activity_counter = 0
    total_activity_counter = 0

    print("The following activities are from the database:", selected_database, "\n")
    for activity in selected_database:
        # sets counters for technosphere, biosphere and product flows.
        technosphere_counter = 0
        biosphere_counter = 0
        product_counter = 0
        total_activity_counter = total_activity_counter + 1
        # intrinsic activities do not have the 'worksheet name' in the dictionary containing the details of activity. This 'worksheet name' contains the name of the database from which this activity was copied from.
        if "worksheet name" not in activity:

            intrinsic_activity_counter = intrinsic_activity_counter + 1

            for exchange in activity.exchanges():
                if exchange.as_dict()["type"] == "technosphere":
                    technosphere_counter = technosphere_counter + 1
                elif exchange.as_dict()["type"] == "biosphere":
                    biosphere_counter = biosphere_counter + 1
                elif exchange.as_dict()["type"] == "production":
                    product_counter = product_counter + 1

            print(
                "\t",
                str(total_activity_counter) + ".",
                activity,
                "Type: Intrinsic activity",
                " with",
                technosphere_counter,
                " technosphere flows",
                biosphere_counter,
                " biosphere flows",
                product_counter,
                " products",
                "\n",
            )
        else:

            imported_activity_counter = imported_activity_counter + 1
            name_database_dependecies = []
            name_database_dependecies.append(
                activity["worksheet name"]
            )  # to get the database from which the activity was imported
            for exchange in activity.exchanges():
                if exchange.as_dict()["type"] == "technosphere":
                    technosphere_counter = technosphere_counter + 1
                elif exchange.as_dict()["type"] == "biosphere":
                    biosphere_counter = biosphere_counter + 1
                elif exchange.as_dict()["type"] == "production":
                    product_counter = product_counter + 1
                    if exchange.as_dict()["input"][0] not in name_database_dependecies:
                        name_database_dependecies.append(
                            exchange.as_dict()["input"][0]
                        )  # to get the database from which this production exchange within the activity has been imported, if different from the database name of the imported activity
            print(
                "\t",
                str(total_activity_counter) + ".",
                activity,
                "Type: Imported activity",
                " with",
                technosphere_counter,
                " technosphere flows",
                biosphere_counter,
                " biosphere flows",
                product_counter,
                " products",
                "\n",
            )
    print(
        "In total, this database has ",
        imported_activity_counter,
        " imported activities and",
        intrinsic_activity_counter,
        " intrinsic activities",
    )
