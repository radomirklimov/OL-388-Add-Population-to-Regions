import csv

result_file = "location_proposals_with_population.csv"

countries = {
    "DE": {"total": 0, "not_found": 0},
    "AT": {"total": 0, "not_found": 0},
    "CH": {"total": 0, "not_found": 0},
}

rows_without_population = 0
total_rows = 0

with open(result_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        total_rows += 1
        population = row["population"]
        if (
            population is None
            or str(population).strip() == ""
            or (str(population).isdigit() and int(population) == 0)
        ):
            rows_without_population += 1

        country = row["country"]

        if country not in countries:
            continue

        countries[country]["total"] += 1

        if (
            population is None
            or str(population).strip() == ""
            or (str(population).isdigit() and int(population) == 0)
        ):
            countries[country]["not_found"] += 1

print(f"Rows without population value: {rows_without_population} from {total_rows} total")
print()

for country, stats in countries.items():
    print(
        f"{country}: {stats['not_found']} not found from {stats['total']} total"
    )
            