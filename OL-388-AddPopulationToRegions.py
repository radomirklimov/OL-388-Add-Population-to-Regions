import csv
import requests
import time

file_path = "location_proposals.csv"
# base_url = "https://www.gemeindeverzeichnis.de/api/gemeinden"
base_url1 = "http://api.geonames.org/searchJSON?q="
base_url2 = "&country=DE&username=radomyrklymov"


seen = set()
last_request_time = 0

nullPopulation = 0

with open(file_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        place = row["places"]

        # Split on ';' if there are multiple places
        places = [p.strip() for p in place.split(";")]

        total_population = 0
        for p in places:
            # Cool-down: max 60 requests/minute
            elapsed = time.time() - last_request_time
            if elapsed < 1:
                time.sleep(1 - elapsed)

            response = requests.get(base_url1 + p + base_url2)
            response.raise_for_status()

            data = response.json()

            # total_population += data["results"][0]["population_total"]

            if not data["geonames"]:
                print(f"WARN: no population of {p} found")
                continue

            if data["geonames"][0]["population"] == 0:
                nullPopulation += 1
                print(nullPopulation)

            total_population += data["geonames"][0]["population"]

            # Respect rate limit
            time.sleep(1)

        key = (place, total_population)
        if key in seen:
            continue

        seen.add(key)
        print(f"{place}: {total_population}")