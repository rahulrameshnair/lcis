# Changelog

All notable changes to this project will be documented in this file. The changelogs of individual versions can also be found inside their corresponding releases.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2] 2024-06-21

### Added
- authors.md
- citation.cff
- readme.md

### Changed
- license information
- gitignore
### Removed
- Icon

## [0.2.1] 2024-04-11

### Added

- version number has been declared for the export module within the __init__.py inside the libs folder. This version will match the tool version in git.
- added icon for the tool.
- added environment.yml file
- added MIT license
- template for metadata in /Inventory/export/templates
- template for excel import in /Imports/templates


### Changed
- updated variables inside database properties during export
- cleaned and rearranged the jupyter notebook export_lci.ipynb. 
- metadata file formats have been switched from markdown to csv for easier handling and uniformity.
- an excel_to_csv staticmethod has been declared for this new metadata files.
- the templates folder has been rearranged.
- updated README.md


### Removed

- removed the dependencies of the "database dependencies" section within the database properties.csv on the network diagram module. The new method is to use built-in brightway functions to search through the keys called "database".

## [0.1.1] - 2024-01-26

### Changed
- export_lci.ipynb has been moved to the\inventory folder and the notebook was also formatted for better readability.

- Functions inside the network\libs\extract.py were placed inside a class called extract_from_lci. This prevented the import error that was taking place when the functions inside extract.py were being invoked inside lci.py

- The lci.py from v0.1.0  file was renamed to lci_old.py for backup and future reference.

## [0.1.0] - 2024-01-26

### Added
- First working version of the ALICIA LCI schema
