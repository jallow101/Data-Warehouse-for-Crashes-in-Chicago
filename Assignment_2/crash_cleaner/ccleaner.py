import sys
sys.path.append("../packages/crashFunctions/")  # Ensure the path is correct
from crashFunctions import create_unique_address_column, create_unique_address_dict, calculate_average_lat_long, fill_missing_lat_long, fill_missing_location, fix_report_type, fix_most_severe_injury

sys.path.append("../packages/main/")  # Ensure the path is correct
from main import read_csv, write_csv


def main():
  
    path = "../Data/"
    output_file = path + "cleaned/crash_cleaned.csv"

    data, header = read_csv(path + "Crashes.csv", True)
    print(len(data))

    ##create the unique address column
    data = create_unique_address_column(data)

    # Create a dictionary of unique addresses
    unique_address_dict = create_unique_address_dict(data, "UNIQUE_ADDRESS")

    # Calculate the average latitude and longitude for each unique address
    average_lat_lon = calculate_average_lat_long(unique_address_dict)

    # Fill missing values and get count of filled records
    data, filled_count = fill_missing_lat_long(data, average_lat_lon, "UNIQUE_ADDRESS")

    #######################################
    #        Round 2 - fill by Beat       #
    #######################################

    # Create a dictionary of unique addresses
    unique_address_dict_beat = create_unique_address_dict(data, "UNIQUE_ADDRESS_BEAT")

    # Calculate the average latitude and longitude for each unique address
    average_lat_lon = calculate_average_lat_long(unique_address_dict_beat)

    # Fill missing values and get count of filled records
    data, filled_count = fill_missing_lat_long(data, average_lat_lon, "UNIQUE_ADDRESS_BEAT")

    data = fill_missing_location(data)

    ############################################
    #           Report Type  Functions         #
    #         THE...................END        #
    ############################################
    data = fix_report_type(data)

    data = fix_most_severe_injury(data)

    #data = remove_null(data)

    write_csv(output_file, data)

    
if __name__ == "__main__":
    main()