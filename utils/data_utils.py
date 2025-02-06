import csv

from models.venue import Venue
from models.locations import Locations



def is_duplicate_venue(name: str, seen_names: set) -> bool:
    """
    Verifica se o item já foi visto anteriormente.
    """
    return name in seen_names


def is_complete_venue(item: dict, required_keys: list) -> bool:
    """
    Verifica se todos os campos necessários estão presentes.
    """
    return all(key in item and item[key] for key in required_keys)


def save_venues_to_csv(venues: list, filename: str):
    if not venues:
        print("No locations to save.")
        return

    # Use field names from the Locations model
    fieldnames = list(Locations.model_fields.keys())

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(venues)
    print(f"Saved {len(venues)} locations to '{filename}'.")
