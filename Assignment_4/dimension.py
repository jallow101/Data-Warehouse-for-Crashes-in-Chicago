import sys
sys.path.append("../packages/dimensionFunctions/")  # Ensure the path is correct
from dimensionFunctions import split_crash_data, create_date_dimension

sys.path.append("../packages/main/")  # Ensure the path is correct
from main import read_csv, write_csv


# Define columns to split
dimensions = [
    {
        "Injuries": ["INJURIES_ID","INJURY_CLASSIFICATION", "MOST_SEVERE_INJURY", "INJURIES_TOTAL", "INJURIES_FATAL", "INJURIES_INCAPACITATING", "INJURIES_NON_INCAPACITATING", "INJURIES_REPORTED_NOT_EVIDENT", "INJURIES_NO_INDICATION", "INJURIES_UNKNOWN"]
    },
    {
        "Crash": ["CRASH_ID","FIRST_CRASH_TYPE", "REPORT_TYPE", "CRASH_TYPE"]
    },
    {
        "Person": ["PERSON_ID","PERSON_TYPE", "CITY", "STATE", "SEX", "AGE","AGE_GROUP", "PHYSICAL_CONDITION", "SAFETY_EQUIPMENT", "AIRBAG_DEPLOYED", "EJECTION"]
    },
    {
        "Vehicle": ["VEHICLE_ID", "UNIT_TYPE", "MAKE", "MODEL", "LIC_PLATE_STATE", "VEHICLE_YEAR", "VEHICLE_DEFECT", "VEHICLE_TYPE", "VEHICLE_USE", "TRAVEL_DIRECTION", "MANEUVER", "OCCUPANT_CNT", "FIRST_CONTACT_POINT"]
    },
    {
        "Weather": ["WEATHER_ID","WEATHER_CONDITION", "LIGHTING_CONDITION"]
    },
    {
        "Cause": ["CAUSE_ID","BAC_RESULT", "DRIVER_ACTION", "DRIVER_VISION", "PRIM_CONTRIBUTORY_CAUSE", "SEC_CONTRIBUTORY_CAUSE"]
    },
    {
        "Geography": ["GEOGRAPHY_ID","POSTED_SPEED_LIMIT", "TRAFFIC_CONTROL_DEVICE", "DEVICE_CONDITION", "TRAFFICWAY_TYPE", "ALIGNMENT", "ROADWAY_SURFACE_COND", "ROAD_DEFECT", "STREET_NAME", "STREET_NO", "STREET_DIRECTION","BEAT_OF_OCCURRENCE", "LATITUDE", "LONGITUDE", "LOCATION"]
    },
    {
        "Damage_to_User": ["DATE_ID","CRASH_ID","VEHICLE_ID","INJURIES_ID","PERSON_ID","WEATHER_ID","CAUSE_ID", "GEOGRAPHY_ID","DAMAGE", "DAMAGE_CATEGORY", "NUM_UNITS","UNIT_NO"]
    },
    {   "Date": ["DATE_ID", "DATE","DATE_POLICE_NOTIFIED", "TIME", "YEAR", "MONTH","WEEK", "DAY", "HOUR", "QUARTER", "WEEKEND"]}
]

def main():
    path = "../Data/"
    merged_path = path + "merged/merged_data.csv"

    # Read the original dataset
    dataset = read_csv(merged_path)

    print("Initialization .... ...")
    #Associated_Merged_Data
    # Split the dataset into multiple files (Optional)
    
     # Split the dataset into multiple dimensions
    created_dimensions = split_crash_data(dataset, dimensions)

    # Write each dimension to a CSV file
    #print("Dimension to create =====> ", created_dimensions)
    for dimension, name in created_dimensions:
        if dimension:
            write_csv(path + "dimensions/" + name + ".csv", dimension, dimension[0].keys())
            print(f"Created dimension: {name}")

    # Create date dimension
    #date_dimension = create_date_dimension(dataset, "CRASH_DATE")
    #if date_dimension:
     #   write_csv(path + "dimensions/date_dimension.csv", date_dimension, date_dimension[0].keys())
      #  print("Created date dimension")

    #vehicle_dim, columns = read_csv('./Dimensions/new dims/Vehicle.csv')
    #vehicle_dim = remove_duplicate_id(vehicle_dim, "VEHICLE_ID")
    #vehicle = clean_vehicles(vehicle_dim)
    #write_csv('./Dimensions/new dims/Vehicle.csv', vehicle, columns)
    
    date_dimesnion =  create_date_dimension(dataset, "CRASH_DATE")
    #write_csv(path+"dimensions/date_dimension.csv", date_dimesnion)
    
if __name__ == "__main__":
    main()