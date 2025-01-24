# Data Warehouse for Crashes in Chicago

This project is a comprehensive data warehouse implementation and analysis of traffic incidents in Chicago, aimed at supporting decision-making for an insurance company. It involves the creation of a data warehouse, data processing with SSIS, and analytical queries to extract insights from crash data.

## Project Overview

The project consists of two major phases:
1. **Part 1**: Creating and populating a data warehouse, cleaning data, and answering analytical questions using SSIS.
2. **Part 2**: Building a datacube and performing advanced analyses using MDX queries and dashboards.

### Dataset
The dataset contains traffic incidents in Chicago between January 2014 and January 2019, including:
- **Crashes.csv**: Details about incidents and their causes.
- **People.csv**: Information about individuals involved in incidents.
- **Vehicles.csv**: Data about vehicles in crashes.

Source: [Traffic Crashes Chicago on Kaggle](https://www.kaggle.com/datasets/isadoraamorim/trafficcrasheschicago)

---

## Group Assignments

This project is completed by **Group 16**, focusing on specific tasks assigned from the project guidelines:

### Part 1 Assignments
1. **Data Understanding**: Analyzed the relationships between the data files and identified missing values and potential enhancements.
2. **Data Cleaning**: Addressed missing data and integrated additional spatial information.
3. **DW Schema**: Designed and created a schema simulating an insurance company's data warehouse.
4. **Data Preparation**: Prepared separate files for each table in the data warehouse.
5. **Data Uploading**: Populated the database using Python scripts.
6. **SSIS Data Uploading**: Created a new set of tables (e.g., `TABLE_NAME_SSIS`) and used SSIS to populate them with 10% of the data.
7. **SSIS Analytical Queries**:
   - **Query 6b**: Showed all participants ordered by total damage costs for each vehicle type.
   - **Query 7b**: Calculated the percentage of damage costs by time of day across months.
   - **Query 8b**: Displayed crash damage costs for each vehicle type and weather condition.
   - **Query 9b**: Defined an interesting query based on insights gathered (details in the report).

### Part 2 Assignments
1. **Datacube Creation**: Built a datacube with appropriate hierarchies and measures.
2. **MDX Queries**: Completed four marked assignments, including:
   - Monthly damage costs by location.
   - Yearly average damage costs per person.
   - Quarterly analysis of vehicle involvement and damage costs.
   - Interesting query revealing non-trivial facts from the data.
3. **Dashboards**:
   - Geographical distribution of total damage costs by vehicle category.
   - Additional visualizations focusing on streets and people involved.

---

## Technologies Used

- **SQL Server**: For data warehouse implementation and querying.
- **SSIS**: For ETL processes and analytical queries.
- **Python**: For data preparation and database population.
- **Power BI / Tableau**: For creating interactive dashboards.

---

## File Structure

- `scripts/`: Python scripts for data cleaning, preparation, and uploading.
- `ssis/`: SSIS packages for ETL and analytical queries.
- `dashboards/`: Screenshots and files for dashboards created in Part 2.
- `report/`: Detailed project reports for both parts.

---

## Results

Key insights extracted include:
- Patterns in crash causes and their impact on damage costs.
- Time-based trends in vehicle involvement and crash severity.
- Geographical hot spots for high damage costs.
- Insights into vehicle types and weather conditions affecting crash outcomes.

---

## Contributing

Contributions are welcome! Feel free to fork this repository, create issues, or submit pull requests to improve the project.

## License

This project is licensed under the MIT License.

---

*Note: This project is for educational purposes as part of the LDS course.*
