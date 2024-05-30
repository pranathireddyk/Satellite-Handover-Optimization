import csv
from pyorbital.orbital import Orbital
import datetime

# Define the list of NOAA satellite names
noaa_satellites = [
    'NOAA 1',
    'NOAA 2',
    'NOAA 3',
    'NOAA 4',
    'NOAA 5',
    'NOAA 6',
    'NOAA 7',
    'NOAA 8',
    'NOAA 9',
    'NOAA 10',
    'NOAA 11',
    'NOAA 12',
    'NOAA 13',
    'NOAA 14',
    'NOAA 15',
    'NOAA 16',
    'NOAA 17',
    'NOAA 18',
    'NOAA 19',
    'NOAA 20',
]

# Load the TLE data from the text file
tle_data = {}

with open('tle.txt', 'r') as tle_file:
    lines = tle_file.readlines()
    i = 0
    while i < len(lines):
        sat_name = lines[i].strip()
        tle_line1 = lines[i + 1].strip()
        tle_line2 = lines[i + 2].strip()
        tle_data[sat_name] = (tle_line1, tle_line2)
        i += 3

# Get the current time
current_time = datetime.datetime.utcnow()

# Create a dataset for the past 24 hours with the same timestamps
dataset = []

for i in range(24 * 60):  # 24 hours * 60 minutes
    data_point = {'Time': current_time}

    for sat_name in noaa_satellites:
        try:
            tle_lines = tle_data.get(sat_name)
            if tle_lines:
                sat = Orbital(sat_name, line1=tle_lines[0], line2=tle_lines[1])
                position = sat.get_lonlatalt(current_time)
                data_point[sat_name] = {
                    'Longitude': position[0],
                    'Latitude': position[1],
                    'Altitude': position[2],
                }
            else:
                print(f"No TLE data found for {sat_name}. Skipping...")
        except ValueError as e:
            print(f"Error fetching data for {sat_name}: {e}. Skipping...")

    dataset.append(data_point)
    current_time -= datetime.timedelta(minutes=1)  # Move back one minute

# Save the dataset to a CSV file
csv_filename = 'noaa_satellite_data.csv'

with open(csv_filename, mode='w', newline='') as csv_file:
    fieldnames = ['Time'] + noaa_satellites
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for data_point in dataset:
        writer.writerow(data_point)

print(f'Data has been saved to {csv_filename}.')
