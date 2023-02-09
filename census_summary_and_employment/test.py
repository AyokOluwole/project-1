# Import dependencies
import pandas as pd
import os

# Below are the ABSOLUTE paths to the csv files (since they are too big for git without large file handling)
    # PATHS WILL BE DIFFERENT FOR EACH COMPUTER

census_file_cd_csd = "C:/Users/kronh/OneDrive/Coding_bootcamp/project_1_datasources/2021_census_data_cd_cds/98-401-X2021005_English_CSV_data.csv"
employment_nums = "C:/Users/kronh/OneDrive/Coding_bootcamp/project_1_datasources/employment_by_occupation/14100389.csv"
wages = "C:/Users/kronh/OneDrive/Coding_bootcamp/project_1_datasources/wage_data_2021_by_region_and_job.csv"

# Reads census data by division and subdivision into a DataFrame
census_cd_csd_df = pd.read_csv(census_file_cd_csd, encoding='ISO-8859-1')

# Grabs data from Ontario only - regions with Alt Geo Codes starting with 35
census_cd_csd_df = census_cd_csd_df[census_cd_csd_df["ALT_GEO_CODE"].astype(str).str[:2] == '35']

### Creates a list of dictionaries with division codes tied to division names

# Makes a list for dictionaries of division codes and names in Ontario
divisions = []
# Loops through all the rows in the dataframe at the census division level
for index, row in census_cd_csd_df[census_cd_csd_df['GEO_LEVEL'] == 'Census division'].iterrows():
    # Gets the code and name for the census division
    code = row['ALT_GEO_CODE']
    name = row['GEO_NAME']
    # Creates a dictionary to hold the code and name
    dic = {'code': code, 'name': name}
    # Adds the dictionary to the list divisions if it's not already there
    if dic not in divisions:
        divisions.append(dic)

# Grabs the subset of data at the census subdivision level 
census_csd_df = census_cd_csd_df.loc[census_cd_csd_df['GEO_LEVEL'] == 'Census subdivision'].copy().reset_index(drop=True)

# Keeps a subset of columns
census_csd_df = census_csd_df[['ALT_GEO_CODE', 'GEO_NAME', 'CHARACTERISTIC_ID', 'CHARACTERISTIC_NAME', 'C1_COUNT_TOTAL']]

# Adds a column for census division code to the subdivision data, populates it, and resets the index
census_csd_df['Census division code'] = census_csd_df["ALT_GEO_CODE"].astype(str).str[:4]

# Renames the Geo name column
census_csd_df = census_csd_df.rename(columns={'GEO_NAME': "Census subdivision name", "ALT_GEO_CODE":"Census subdivision code"})

### Filter out unnecessary characteristics and put desired ones into columns

# Makes an empty list to hold dictionaries of values
characteristics_by_csd = []

# Series of each unique census subdivision code
subdivisions = census_csd_df.copy()['Census subdivision code'].unique()

# Iterates through the list of subdivisions
for subdivision in subdivisions:
    # Sets up a dictionary to go into the list and hold the characteristics of this subdivisioon
    characteristics = {'Census subdivision code': subdivision}
    # Grabs all the data pertaining to the given subdivision
    subdivision_data = census_csd_df.loc[census_csd_df['Census subdivision code'] == subdivision]
    # Iterates through the rows of the census dataframe
    for index, row in subdivision_data.iterrows():
        # Checks to see if the subdivision is equal to the one from the series
        if row['Census subdivision code'] == subdivision:
            # If they're the same, looks to see whether any of the desired characteristics are recorded and if so records them in the dictionary
            if int(row['CHARACTERISTIC_ID']) == 6:
                characteristics['Population density'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 1434:
                characteristics['Total households by #/room'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 1435:
                characteristics['1 or fewer per room'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 1436:
                characteristics['>1 per room'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 1437:
                characteristics['Total households by housing suitability'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 1438:
                characteristics['Suitable housing'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 1439:
                characteristics['Unsuitable housing'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 1465:
                characteristics['Total owned and rented households >0 income'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 1466:
                characteristics['<30 percent of income spent on shelter'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 1467:
                characteristics['>=30 percent of income spent on shelter'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 1468:
                characteristics['30 - <100 percent of income spent on shelter'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 2611:
                characteristics['Total commuting duration'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 2612:
                characteristics['Commute <15 min'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 2613:
                characteristics['Commute 15-29 min'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 2614:
                characteristics['Commute 30-44 min'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 2615:
                characteristics['Commute 45-59 min'] = row['C1_COUNT_TOTAL']
            elif int(row['CHARACTERISTIC_ID']) == 2616:
                characteristics['Commute >=60 min'] = row['C1_COUNT_TOTAL']
    print(f"census subdivision {subdivision} has been filled out")
    print(characteristics)
    characteristics_by_csd.append(characteristics)

print(len(characteristics))
print(len(subdivisions))