import csv

log_file = "non_population_cities.log"
switzerland_file = "population_switzerland_1.csv"

# Read cities from the log file
missing_cities = set()

with open(log_file, encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if line.startswith("City without population: CH: "):
            city = line.replace("City without population: CH: ", "")
            missing_cities.add(city)

print(f"Cities in log: {len(missing_cities)}")

# Find matches in the Swiss CSV
found = []
not_found = []

with open(switzerland_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    swiss_cities = {row["Schweizer Städte"].strip() for row in reader}

for city in missing_cities:
    if city in swiss_cities:
        found.append(city)
    else:
        not_found.append(city)

print(f"Found in Switzerland CSV: {len(found)}")
print(f"Not found: {len(not_found)}")

if found:
    print("\nFound:")
    for city in sorted(found):
        print(city)

if not_found:
    print("\nNot found:")
    for city in sorted(not_found):
        print(city) 
