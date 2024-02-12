import brightway2 as bw
import bw2data as bd

"""
Used for printing all the activities and their corresponding exchanges in a database according to the way in which
they are stored within the brightway database.
"""
def print_all(selected_database):
    """
    To output all the activities and the corresponding exchanges from a selected brightway database. 
    The printing is done in dictionary format with all the details such as the linked database names, activity codes and so on.

    """
    for activity in selected_database:
        print ('Activity:', activity.as_dict(), '\n')
        for exchange in activity.exchanges():
            print('\t','Exchange', exchange.as_dict(), '\n')
        print('\n')

def print_classified(selected_database):
    """
    To classify and count those exchanges and activities intrinsic to the database and those that copied/imported from other databases. 
    This is because, in BW, copied activities have their exchanges stored in a dictionary format while intrinsic activities have their exchanges stored in dictionary form. 
    Within each such activities, the number of technosphere flows and biosphere flows are to be identified.
        There is another type of flow called "downstream consumers" in the activity browser. This just means that if the product from one of the activity (a1, say) is used as a technosphere input for the activity (a2, say). 
        Then, a2 becomes the downstream consumer of a1. This is not classified here because it is a just an interdependency.

    """
    imported_activity_counter = 0
    intrinsic_activity_counter = 0
    total_activity_counter = 0

    print ('The following activities are from the database:', selected_database, '\n')
    for activity in selected_database:
        #sets counters for technosphere, biosphere and product flows.
        technosphere_counter = 0
        biosphere_counter = 0
        product_counter = 0
        total_activity_counter = total_activity_counter + 1
        # intrinsic activities do not have the 'worksheet name' in the dictionary containing the details of activity. This 'worksheet name' contains the name of the database from which this activity was copied from.
        if 'worksheet name' not in activity:
          
            intrinsic_activity_counter = intrinsic_activity_counter + 1
            

            for exchange in activity.exchanges():
                if exchange.as_dict()['type'] == 'technosphere':
                    technosphere_counter = technosphere_counter+1
                elif exchange.as_dict()['type'] == 'biosphere':
                    biosphere_counter = biosphere_counter + 1
                elif exchange.as_dict()['type'] == 'production':
                    product_counter = product_counter + 1
                    
            
            print ('\t', str(total_activity_counter)+'.',  activity, "Type: Intrinsic activity", " with", technosphere_counter, " technosphere flows", biosphere_counter, " biosphere flows", product_counter, " products",  '\n')
        else:
            
            imported_activity_counter = imported_activity_counter + 1
            name_database_dependecies = []
            name_database_dependecies.append(activity['worksheet name']) #to get the database from which the activity was imported
            for exchange in activity.exchanges():
                if exchange.as_dict()['type'] == 'technosphere':
                    technosphere_counter = technosphere_counter+1
                elif exchange.as_dict()['type'] == 'biosphere':
                    biosphere_counter = biosphere_counter + 1
                elif exchange.as_dict()['type'] == 'production':
                    product_counter = product_counter + 1
                    if exchange.as_dict()['input'][0] not in name_database_dependecies:
                        name_database_dependecies.append(exchange.as_dict()['input'][0]) #to get the database from which this production exchange within the activity has been imported, if different from the database name of the imported activity
            print ('\t', str(total_activity_counter)+'.', activity, "Type: Imported activity", " with", technosphere_counter, " technosphere flows", biosphere_counter, " biosphere flows", product_counter, " products",  '\n')
    print ("In total, this database has ", imported_activity_counter, " imported activities and", intrinsic_activity_counter, " intrinsic activities")



