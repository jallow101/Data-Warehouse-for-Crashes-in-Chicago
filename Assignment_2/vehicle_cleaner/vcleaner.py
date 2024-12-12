import sys
sys.path.append("../packages/vehicleFunctions/")  # Ensure the path is correct
from vehicleFunctions import clean_vehicle_data_exact

sys.path.append("../packages/main/")  # Ensure the path is correct
from main import read_csv, write_csv

def main():

    path = "../Data/"
    output_file = path + "cleaned/vehicle_cleaned.csv"

    # Read the data
    data = read_csv(path+ "Vehicles.csv")

    cleaned_data = clean_vehicle_data_exact(data)

    print(cleaned_data[0])
    write_csv(output_file, cleaned_data)

    
if __name__ == "__main__":
    main()