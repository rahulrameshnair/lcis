# metadata.py

"""
Module for editing, changing and converting the metadata file and database properties associated with a LCI dataset.
"""
import pandas as pd
from bw2data.parameters import ActivityParameter, DatabaseParameter, ProjectParameter
import bw2data as bw
import brightway2
import csv
import uuid
from datetime import datetime, timezone


class Metadata:
    """
    To handle all the additional user-generated metadata that is associatted with a dataset.

    Methods available:
    excel_to_md(file_path, output_file)
    """

    @staticmethod
    def excel_to_csv(excel_file_path, csv_file_path):
        """
        Convert the metadata Excel file to a CSV (comma separated) file using pandas.

        Args:
        excel_file_path (str): The path to the metadata excel file.
        csv_file_path (str): The path where the CSV file should be saved.
        """

        df = pd.read_excel(excel_file_path)
        # Save the dataframe to a CSV file
        df.to_csv(csv_file_path, index=False)

        print(f"File converted and saved as {csv_file_path}")

    def excel_to_md(self, file_path, output_file):
        """
        Converts metadata file present in xlsx format to an unformatted markdown file.
        Args:
        file_path (str): path to the excel file that needs to be converted
        output_file (str): name of the desired output markdown file

        Returns:
        a success message if file conversion has taken place.

        """
        # Read the Excel file into a dictionary of DataFrames, with sheet names as keys
        try:
            xls = pd.ExcelFile(file_path)
            sheet_names = xls.sheet_names
        except Exception as e:
            print(f"An error occurred: {e}")
            exit(1)

        # Write the Markdown content to the output Markdown file
        with open(output_file, "w") as md_file:
            for sheet_name in sheet_names:
                df = xls.parse(sheet_name)
                markdown_table = df.to_markdown(index=False)
                md_file.write(f"# {sheet_name}\n")  # Use the sheet name as a heading
                md_file.write(markdown_table)
                md_file.write("\n\n")

        print(f"Excel file converted to Markdown and saved as '{output_file}'.")


class Dbprops:
    """
    To handle the properties of an LCI database that is present in a project

    Methods:
    gen_info()
    db_dependencies(dictionary)
    csv(csv_file, database_properties)

    """

    def __init__(self, project_name, database_name):
        bw.projects.set_current(project_name)
        self.database = bw.Database(database_name)
        self.dataset_name = database_name

    def gen_info(self):
        """
        To extract the general information pertaining to a brightway database such as total no. of atcivities, exchanges, and so on

        Returns:
        db_props (dict): properties of the database with 'property name and value as a key:value pair
        """
        db_props = {}
        # counters for all properties
        total_exchanges = 0
        total_biosphere_flows = 0
        total_technosphere_flows = 0
        total_production_flows = 0

        for activity in self.database:
            total_exchanges += len(activity.exchanges())
            total_biosphere_flows += len(activity.biosphere())
            total_technosphere_flows += len(activity.technosphere())
            total_production_flows += len(activity.production())

        db_props["Total Project Parameters"] = len(ProjectParameter.select())
        db_props["Total Database Parameters"] = len(DatabaseParameter.select())
        db_props["Total Activity Parameters"] = len(ActivityParameter.select())
        db_props["Total Activities"] = len(self.database)
        db_props["Total Exchanges"] = total_exchanges
        db_props["Total Biosphere flows"] = total_biosphere_flows
        db_props["Total Technosphere flows"] = total_technosphere_flows
        db_props["Total Reference products"] = total_production_flows

        return db_props

    def identifying_info(self, schema_version, dataset_version):
        """
        To generate the identifying information concerning the datasets such as name, version, unique dataset identifier etc.
        Args:
            schema_version (str): the schema version of the LCI
            dataset_version (str): the version of the dataset defined according to the LCI schema
        Returns:
            idf_props (dict): propertie of the dataset in key:value pairs
        """
        timestamp = datetime.now(timezone.utc)
        dataset_time = timestamp.strftime(
            "%Y%m%d-%H%M%S"
        )  # formatting the time of the dataset in the form of yyyymmdd-hhmmss
        text_for_udi = (
            self.dataset_name + schema_version + dataset_version + dataset_time
        )
        udi = uuid.uuid5(
            uuid.NAMESPACE_X500, text_for_udi
        )  # creates an unique dataset identifier (UDI)
        dataset_udi = str(udi).replace(
            "-", ""
        )  # removes the - in the generated unique dataset identifier
        software_version = brightway2.__version__
        bw_version = "Brightway " + ".".join(
            map(str, software_version)
        )  # converts the version tuple to the format 0.0.0
        idf_props = {
            "Dataset Name": self.dataset_name,
            "Schema Version": schema_version,
            "Dataset Version": dataset_version,
            "Software": bw_version,
            "Export Time": dataset_time,
            "Unique Dataset Identifier": dataset_udi,
        }

        return idf_props

    def db_dependencies(self):
        """
        To find out the dependencies of the selected dataset in a project.

        Args: self
        Returns (list): The name of all the database dependencies
        """
        database_dependencies = []
        for activity in self.database:
            for exchange in activity.exchanges():
                if "database" in exchange:
                    db_value = exchange["database"]
                    if db_value not in database_dependencies:
                        database_dependencies.append(db_value)
        return database_dependencies

    # @staticmethod
    # def db_dependencies (dictionary, dependencies=[]):
    #     """
    #     Find the names of all the databases that the selcted database depends on. In other words, the database dependencies of the LCI

    #     Args:
    #     dictionary  (dict): the dictionary contanining all the activities and their details, usually the second element of the LCI list
    #     dependencies=[]: null list passed on to recursively save the dependent databases.

    #     Return:
    #     dependencies (dict): properties of the database
    #     """
    #     for key, value in dictionary.items():
    #         # print (key, value)
    #         if key == 'database':
    #             dependencies.append(value) if value not in dependencies else dependencies
    #             # print (key, value)
    #         elif isinstance (value, dict): # assuming we have reached the nested dict containing info of an activity or exchange
    #             db_props.db_dependencies(value)
    #             # print (value)
    #         elif isinstance (value, list): #assuming we have reached the nested exchange list within an activity
    #             for exchange in value:
    #                 db_props.db_dependencies(exchange)
    #     return (dependencies)

    @staticmethod
    def csv(csv_file, database_properties):
        """
        Generates the csv file of the database properties

        Args:
        csv_file (str): name of the desired output csv file
        database_properties (dict): the properties of the LCI database that has to be converted to csv file

        Prints:
        A success message after the creation of the csv file.
        """
        # Write the dictionary to a CSV file
        with open(csv_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # Write the header
            writer.writerow(["Property", "Value"])

            # Write the dictionary data
            for key, value in database_properties.items():
                if isinstance(value, list):
                    value = ", ".join(
                        value
                    )  # Join the list into a comma-separated string
                writer.writerow([key, value])
        print(
            f"The database properties file have been successfully created as '{csv_file}'."
        )
