import csv
import os

input_file = "location_proposals_with_population.csv"
output_dir = "city_batches"
batch_size = 15

missing_cities = []

with open(input_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        population = row.get("population", "").strip()

        # Missing or zero population
        if not population or population == "0":
            name = row.get("places", "").strip()
            country = row.get("country", "").strip()

            if name:
                missing_cities.append((name, country))

# Remove duplicates and sort
missing_cities = sorted(set(missing_cities))

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Write batches
num_files = 0
for i in range(0, len(missing_cities), batch_size):
    batch = missing_cities[i:i + batch_size]
    num_files += 1

    output_file = os.path.join(
        output_dir,
        f"cities_batch_{num_files:03d}.txt"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        for name, country in batch:
            f.write(f"{country},{name}\n")

print(f"Found {len(missing_cities)} cities without population.")
print(f"Created {num_files} batch files in '{output_dir}'.")






# import csv

# input_file = "location_proposals_with_population.csv"
# output_file = "cities_without_population.txt"

# missing_cities = []

# with open(input_file, newline="", encoding="utf-8") as f:
#     reader = csv.DictReader(f)

#     for row in reader:
#         population = row.get("population", "").strip()

#         # Missing or zero population
#         if not population or population == "0":
#             name = row.get("places", "").strip()
#             country = row.get("country", "").strip()

#             if name:
#                 missing_cities.append((name, country))

# # Remove duplicates and sort
# missing_cities = sorted(set(missing_cities))

# # Save names with country
# with open(output_file, "w", encoding="utf-8") as f:
#     for name, country in missing_cities:
#         f.write(f"{name}; {country}\n")

# print(f"Found {len(missing_cities)} cities without population.")
# print(f"Saved to {output_file}")