import sys
from datetime import datetime
sys.path.append("../packages/main/")  # Ensure the path is correct
from main import read_csv, write_csv, left_join, create_date_dimension

print("Merging data...")

crash_file = "../Data/cleaned/crash_cleaned.csv"
people_file = "../Data/cleaned/people_cleaned.csv"
vehicles_file = "../Data/cleaned/vehicle_cleaned.csv"

partial_merge = "../Data/merged/ppl_veh_crash_data.csv"
output_file = "../Data/merged/merged_data.csv"


# Leggere i file
crashes_data = read_csv(crash_file)
people_data = read_csv(people_file)
vehicles_data = read_csv(vehicles_file)


# Associare persone ai loro veicoli
#join_keys = 'RD_NO'  #  Usando VEHICLE_ID invece di UNIT_NO
people_vehicles_data = left_join(people_data, vehicles_data, 'Vehicle_ID')

write_csv(partial_merge, people_vehicles_data)
print(" People and Vehicles data saved to: people_vehicles_data.csv")

# Unire il risultato con Crashes
final_data = left_join(people_vehicles_data, crashes_data, 'RD_NO')
#print(" Merge + Crash data saved")
#write_csv(final_data, "./ppl_veh_crash_data.csv")

final_data1 = create_date_dimension(final_data, 'CRASH_DATE')
print(" Date Dimension Created")

# Scrivere il risultato su un file
write_csv(output_file, final_data1)

print(f"Dati uniti salvati in: {output_file}")         