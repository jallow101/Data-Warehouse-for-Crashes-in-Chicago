# DSS_Crashlytics_Data_Warehouse
## STEPS
* Donwload the Datasets from ====> (vehicles, crashes, people)
* Move to the Data folder
* Required Packages 
* Install dot-env
* pip install python-dotenv

# Order of execution
* cd into Assinment 2 
* run missingValues.py
* cd into Assinment 2 
* cd into assignment 4
* run dimensiions.py
* cd into assignment 5 
* run the populate_db.py script
* * Remeber the fact table (damage_to_user) should be last imported table. 
# The current alrogithm import dimension in ascending order based on filename
* Comment the fact table in the dimensions list  e.g #"Damage_to_User" to import others and later reverse the provesudre to populate the fact table.
* * You can also modify to always import the fact table last

# ##############################################################################
#                               ___^^^^^^^^^^___                               #
#                                   (')   (')                                  #
#                                       V                                      #
#                                      ~~~                                     #
#                                      < >                                     #
#                                      """                                     #
#                                                                              #
# ##############################################################################