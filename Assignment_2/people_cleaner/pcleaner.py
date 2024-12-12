import sys
sys.path.append("../packages/custom/")  # Ensure the path is correct
from custom import hi, calculate_median_mode_values, fill_and_clean_people_data, create_age_group, remove_duplicate_person_id

sys.path.append("../packages/main/")  # Ensure the path is correct
from main import read_csv, write_csv

def main():
    path = "../Data/"
    output_file = path + "cleaned/people_cleaned.csv"

    # Read the data
    rows = read_csv(path+ "people.csv")

    # Calculate median and mode values
    medians, modes = calculate_median_mode_values(rows)

    # Fill and clean the data
    cleaned_data = fill_and_clean_people_data(rows, medians, modes)
    
    cleaned_data = create_age_group(cleaned_data)
    cleaned_data = remove_duplicate_person_id(cleaned_data)
    write_csv(output_file, cleaned_data)

if __name__ == "__main__":
    main()
