#!/usr/bin/env python

import json
import os
from pprint import pprint

import psycopg2
import psycopg2.extras
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

POSTGRES_URL = os.getenv("POSTGRES_URL")

GREEN = "\033[92m"
ENDC = "\033[0m"


def read_json(path):
    with open(path, "r") as f:
        return json.loads(f.read())


def main():
    print(f"{GREEN}READING CONSTANT DATA{ENDC}")
    API_URL = os.getenv("OPEN_DOTA_API_BASE_URL")
    heroes_url = f"{API_URL}/constants/heroes"
    items_url = f"{API_URL}/constants/items"

    heroes_response = requests.get(heroes_url)
    items_response = requests.get(items_url)

    heroes = heroes_response.json()
    items = items_response.json()

    aliases = read_json("src/constant_data/aliases.json")

    all_heroes = []
    for hero_id, hero_obj in heroes.items():
        all_heroes.append(
            {
                "id": int(hero_id),
                "name": hero_obj["name"],
                "localized_name": hero_obj["localized_name"],
                "primary_attr": hero_obj["primary_attr"],
                "roles": hero_obj["roles"],
                "img": hero_obj["img"],
            }
        )

    all_aliases = []
    for alias_obj in aliases:
        for alias in alias_obj["aliases"]:
            all_aliases.append(
                {"hero_id": alias_obj["id"], "alias": alias.lower()})

    all_items = []
    for item_name, item_data in items.items():
        display_name = item_data.get("dname") or item_name.replace("_", " ")
        new_item = {"id": item_data["id"], "item_name": display_name.lower()}
        all_items.append(new_item)

    conn = psycopg2.connect(POSTGRES_URL)
    conn.autocommit = True

    with conn.cursor() as cursor:
        # Run rebuild_constants.sql
        print(f"{GREEN}RUNNING rebuild_constants.sql{ENDC}")
        with open("scripts/rebuild_constants.sql", "r") as sql_file:
            sql_statements = sql_file.read()
            cursor.execute(sql_statements)

        print(f"{GREEN}SEEDING HEROES{ENDC}")
        psycopg2.extras.execute_batch(
            cursor,
            """
            INSERT INTO heroes VALUES (
                %(id)s,
                %(name)s,
                %(localized_name)s,
                %(primary_attr)s,
                %(roles)s,
                %(img)s
            ) ON CONFLICT DO NOTHING;
            """,
            all_heroes,
        )

        print(f"{GREEN}SEEDING ALIASES{ENDC}")
        psycopg2.extras.execute_batch(
            cursor,
            """
            INSERT INTO hero_aliases (hero_id, alias) VALUES (
                %(hero_id)s,
                %(alias)s
            ) ON CONFLICT DO NOTHING;
            """,
            all_aliases,
        )

        print(f"{GREEN}SEEDING ITEMS{ENDC}")
        psycopg2.extras.execute_batch(
            cursor,
            """
            INSERT INTO items VALUES (
                %(id)s,
                %(item_name)s
            ) ON CONFLICT DO NOTHING;
            """,
            all_items,
        )

    print(f"{GREEN}DONE{ENDC}")


if __name__ == "__main__":
    main()
