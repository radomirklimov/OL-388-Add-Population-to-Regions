import csv
from openpyxl import load_workbook

proposal_file = "location_proposals.csv"
reference_file = "reference_file.xlsx"

# Load Excel workbook
wb = load_workbook(reference_file, read_only=True, data_only=True)
ws = wb.active

# Build city -> population lookup from Excel
reference_population = {}

for row in ws.iter_rows(values_only=True):
    if row[6] is None or row[22] is None:
        continue

    name = str(row[6]).strip()
    level = str(row[1]).strip()

    if level in ("5", "6"):
        reference_population[name] = int(row[22])

wb.close()


# Read proposal file
population_lookup = {}
seen = set()
allCities = 0
notFound = 0
nullPopulation = 0

with open(proposal_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        if row["country"] != "DE":
            continue

        placeString = row["places"]

        if placeString in seen:
            continue

        places = [p.strip() for p in placeString.split(";")]
        allCities += len(places)

        total_population = 0

        for p in places:
            population = reference_population.get(p)

            if population == 0:
                nullPopulation += 1
                continue

            if population is None:
                notFound += 1
                print(f"WARN: no population of {p} found")
                continue

            total_population += population

        if total_population != 0:
            population_lookup[placeString] = total_population
            seen.add(placeString)

for city, population in population_lookup.items():
    print(f"{city}: {population}")

print()
print(f"Number of all cities: {allCities}")
print()
print(f"Number of cities whose population couldn't be found: {notFound}")
print()
print(f"Number of cities whose population was 0 in reference_file: {nullPopulation}")

















# import csv
# from openpyxl import load_workbook

# proposal_file = "location_proposals.csv"
# reference_file = "reference_file.xlsx"

# # Load Excel workbook
# wb = load_workbook(reference_file, read_only=True, data_only=True)
# ws = wb.active

# # Build lookup: city name -> population
# population_lookup = dict()
# seen = set()
# nullPopulation = 0 

# def find_population(city_name):
#     for row in ws.iter_rows(values_only=True):
#         if row[6] is None or row[22] is None:
#             continue

#         name = str(row[6]).strip()
#         level = str(row[1]).strip()

#         if name == city_name and level in ("5", "6"):
#             return int(row[22])

#     return None  # not found

# # Read proposal file
# with open(proposal_file, newline="", encoding="utf-8") as f:
#     reader = csv.DictReader(f)

#     for row in reader:
#         placeString = row["places"]
#         if placeString in seen:
#             continue
#         places = [p.strip() for p in placeString.split(";")]

#         total_population = 0
#         for p in places:
#             population = find_population(p)

#             if population is None:
#                 print(f"WARN: no population of {p} found")
#                 continue

#             if population == 0:
#                 nullPopulation += 1

#             total_population += population

#         population_lookup[placeString] = total_population
#         seen.add(placeString)

# print(f"Number of cities whose population couldn't be found: {nullPopulation}")
# for city, population in population_lookup.items():
#     print(f"{city}: {population}")
# wb.close()








# # file_path = "location_proposals.csv"
# # base_url = "https://www.gemeindeverzeichnis.de/api/gemeinden"
# base_url1 = "http://api.geonames.org/searchJSON?q="
# base_url2 = "&country=DE&username=radomyrklymov"


# seen = set()
# last_request_time = 0

# nullPopulation = 0

# with open(file_path, mode="r", encoding="utf-8") as file:
#     reader = csv.DictReader(file)

#     for row in reader:
#         place = row["places"]

#         # Split on ';' if there are multiple places
#         places = [p.strip() for p in place.split(";")]

#         total_population = 0
#         for p in places:
#             # Cool-down: max 60 requests/minute
#             elapsed = time.time() - last_request_time
#             if elapsed < 1:
#                 time.sleep(1 - elapsed)

#             response = requests.get(base_url1 + p + base_url2)
#             response.raise_for_status()

#             data = response.json()

#             # total_population += data["results"][0]["population_total"]

#             if not data["geonames"]:
#                 print(f"WARN: no population of {p} found")
#                 continue

#             if data["geonames"][0]["population"] == 0:
#                 nullPopulation += 1
#                 print(nullPopulation)

#             total_population += data["geonames"][0]["population"]

#             # Respect rate limit
#             time.sleep(1)

#         key = (place, total_population)
#         if key in seen:
#             continue

#         seen.add(key)
#         print(f"{place}: {total_population}") 
