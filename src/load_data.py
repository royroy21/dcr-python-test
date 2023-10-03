import requests

import settings
from db import Country, Region


class APIError(Exception):
    pass


class LoadData:

    def __init__(self):
        # Cache of regions
        self.regions = {}

    def get_data_from_api(self):
        response = requests.get(settings.COUNTRIES_URL)
        if not response.ok:
            raise APIError(
                "Problem getting data from %s", settings.COUNTRIES_URL,
            )
        return response.json()

    def add_country(self, data):
        region_name = data.get("region", "Unknown")
        region_id = self.get_region_id(region_name)

        country = Country()
        name = data["name"]
        found = country.get_by_name(name)
        if found:
            # TODO - maybe amend this so entries are updated not skipped?
            print(f"Skipping {name} as already exists.")
            return
        country.insert(
            name,
            data["alpha2Code"],
            data["alpha3Code"],
            data["population"],
            region_id,
            data["topLevelDomain"][0],
            data["capital"],
        )
        print(country.data)

    def get_region_id(self, region_name):
        if region_name not in self.regions:
            region = Region()
            region.get_or_create_by_name(region_name)
            self.regions[region.data["name"]] = region.data["id"]
        return self.regions[region_name]

    def run(self):
        data = self.get_data_from_api()
        for row in data:
            self.add_country(row)


if __name__ == "__main__":
    LoadData().run()
