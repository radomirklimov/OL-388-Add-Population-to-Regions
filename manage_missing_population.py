import csv

result_file = "location_proposals_with_population.csv"

non_population_cities = []

with open(result_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        population = row["population"]
        if population is None or int(population) == 0:
            non_population_cities.append(f"{row['country']}: {row['places']}")

for city in non_population_cities:
    print(f"City without population: {city}")

print()
print(f"Total cities without population value: {len(non_population_cities)}")
             
