# Template for Life cycle inventory (LCI) in ALICIA

## LCI Structure 🌿

Each project is represented by a parent folder of the same name. This folder hosts the project-specific files and a documentation called "readme" that briefly explains the project. The file structure is as follows:
- ../module-name/
    - LCI-name: 
        - dataset.xlsx and dataset.csv
        - dataset_properties.csv
        - network.graphml
        - environment.yml
        - metadata.md
        - source/^*^
    - readme.md^*^
    - glossary.md^*^

**Note:**  Items marked with ^*^ are non-mandatory in the initial stages and are meant for the final publicaiton of the datasets.

## Definitions 📚

Module - refers to a self-contained standardiszed part or a group of parts or systems of an aircraft. E.g: LH~2~ storage tank, landing gears. Modules can also refer to the procedure concerning aircraft operations, maintenance or service as defined by chapters (00 to 18) of Air Transportation Association (ATA)
- Dataset: LCI inventory data collected for a module in the form of a brightway database.
- Dataset properties: An overview of the information contained within the dataset, and the dependencies on external datasets/databases.
- Network: LCI represented as an interconnected network for visualization, analysis and the study of its dynamics, if necessary. The network inherits all information contained within the parent dataset
- Environment: It is the configuration file containing the information on the  packages and dependencies/libraries to re-create the environment in which the dataset was created.
- Metadata: Is the structred collection of data about the dataset to enable accessibility, interoperability and reusability of the LCI database.
Project specific:
- Readme: Contains general information regarding the modules and/or the parent project under study.
- Glossary: list of terms, definitions and terminologies used within the datsets. The preliminary assumption here is that the general (non-project/non-aviation specific) terms used throughout the dataset adheres to the best practcices in life cycle assessment as indicated [here](/documentation/life_cycle_terminology.pdf)
- Sources contains the raw data of the dataset in a format compatible for sharing between LCA software, and for integration with other appplications.

## Schematic represenation of the database structure
![Database structure](/documentation/database_template.png)

## Schema for naming and comments

The naming convention for the module and the LCI follows a prefix_yyyymmdd scheme, where prefix is the module name followed by the date in the ISO 8601 scheme. For comments of flows within a database, citations of research documents and/data should only be provided in the format of DOI or PIDs.

## Versioning of the dataset

All datasets that undergoes changes in the form of updates or revisions are versioned according to the following format. Error corrections and/or recitifications are not classified as changes and does not deem a separate version. The versioning will follow the semantic convention of  **major.minor.patch** syntax, starting from 1.0.0. Updating 'patch' values 
- 'patch': constitute changes in properties of individual properties (unit, amount, citations etc. ) of activities or exchanges
- 'minor': encompasses addition, removal or overhauls (changes in forumlaes or references to existing parameters) of exchanges (technosphere, production or biosphere) pertaining to one or more activities.
- 'major': includes the addition, removal or overhauls of parameters (project, database and activity-level), activities; using different versions of background databases.

## File formats 📀

- Dataset is saved as .xlsx and .csv files in the schema defined by Brightway. Both formats can be directly imported into brightway. xlsx provides better human readability, while csv provides the benefits of version and change tracking via git.
- Dataset properties are saved in csv format. This is meant for programattic usages (such as database linkings) within brightway.
- The network is stored using the graphMl format. There is no custom syntax unlike other network graphs. It is based on xml and utilizes the standard xml library present in python. This network should be, theoretically, easily mutable for integration with CPACS
- The conda environment is stored in the yml format
- Text documents such as metadata, readme and glossary are stored in mardown format (.md). This provides version tracking, text formatting and interoperability between various text parsers.
- JSON or JSON-LD is proposed as the method for sharing dataset source. This is also under implementation in Brightway. It would preserve the data structure present with the python dictionaries and -LD would also enable the preservation of relationships present within the linked data. JSON-LD is already supported by openLCA.

## How to? 🙋‍♀️

### Exporting the dataset and network

The dataset, properties and the metadata can be exported by running the jupyter notebook [export_lci](/export/export_lci.ipynb). While the network diagram can be created by running the notebook [LCI_network_diagram](/network/LCI_network_diagram.ipynb). The sample template for creating the dataset folder (as indicated in [LCI structure](#lci-structure-🌿)) is provided [here](/export/templates/datasets/).

### Creating the environment.yml file
This file contains the entire information concerning the environment in which the brightway code and datasets were created and executed to achieve the results of LCIA results. It can be performed as follows

```
conda activate [environment_name]
conda env export > environment.yml
#the file is stored in the directory shown in the terminal
```
### Cloning the environment from yml file

```
#navigate to the location where the yml file is stored
cd /path/to/your/folder 

#create the environment using the file
conda env create --file environment.yml 

#activate the environment
conda activate name_of_the_env 
```

## Details about framework used in life cycle assessment in ALICIA
- Ecoinvent cutoff 3.9.1
- Biosphere3
- brightway2 2.4.2
    - bw2analyzer 0.10
    - bw2calc 1.8.1 
    - bw2data 3.6.5
    - bw2io 0.8.8
    - bw2parameters 0.7
    - bw_migrations 0.1

## References
Helmholtz Metadata Collaboration (https://helmholtz-metadaten.de/en)
Danish e-infrastructure consortium (https://www.howtofair.dk/)
Brightway documentation (https://docs.brightway.dev/)
