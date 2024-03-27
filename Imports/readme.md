## Documentation

To avoid inconsistencies the brightway database should have the activities and exchanges in the following hirearchy. The activity contains the process name. The exchanges in this activity are three kinds 1) production, 2) technosphere inputs and 3) biosphere outputs. For example, a demo is shown below.

        Activity: {'database': 'materials2', 'code': '421695138c4741af8deeb228ed68b13d', 'location': 'GLO', 'name': 'Pyrolytic carbon', 'reference product': 'Pyrolytic carbon', 'unit': 'kilogram', 'type': 'process'} 

	      Exchange {'output': ('materials2', '421695138c4741af8deeb228ed68b13d'), 'input': ('materials2', '421695138c4741af8deeb228ed68b13d'), 'amount': 0.65, 'type': 'production'} 

	      Exchange {'output': ('materials2', '421695138c4741af8deeb228ed68b13d'), 'input': ('cutoff391', 'e77669e3f0e8d2473070ea895c442edb'), 'amount': 1, 'type': 'technosphere'} 

          Exchange {'output': ('materials2', '421695138c4741af8deeb228ed68b13d'), 'input': ('biosphere3', 'f9749677-9c9f-4678-ab55-c607dfdc2cb9'), 'amount': 0.35, 'type': 'biosphere'} 
 
This would correspond to an excel schema as shown in the file **excel_template2023.xlsx**

## Environment

In all the 