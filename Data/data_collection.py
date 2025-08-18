import sqlite3
import requests

# Create database
conn = sqlite3.connect('../pokemon_stats.db')
cursor = conn.cursor()

# Create table for ALL Pokemon data
cursor.execute('''
               CREATE TABLE IF NOT EXISTS all_pokemon_stats
               (
                   pokemon_id
                   INTEGER
                   PRIMARY
                   KEY,
                   pokemon_name
                   TEXT,
                   hp
                   INTEGER,
                   attack
                   INTEGER,
                   defense
                   INTEGER,
                   sp_attack
                   INTEGER,
                   sp_defense
                   INTEGER,
                   speed
                   INTEGER
               )
               ''')

pokemon_id = 1
while True:
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
        response.raise_for_status()

        pokemon_data = response.json()

        # Extract ALL stats
        stats = pokemon_data['stats']
        hp = stats[0]['base_stat']
        attack = stats[1]['base_stat']
        defense = stats[2]['base_stat']
        sp_attack = stats[3]['base_stat']
        sp_defense = stats[4]['base_stat']
        speed = stats[5]['base_stat']

        # Store ALL data for this Pokemon
        cursor.execute('''
        INSERT OR REPLACE INTO all_pokemon_stats VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (pokemon_id, pokemon_data['name'], hp, attack, defense,
              sp_attack, sp_defense, speed))

        print(f"Stored Pokemon #{pokemon_id}: {pokemon_data['name']}")
        pokemon_id += 1

    except requests.exceptions.HTTPError:
        print(f"No Pokemon found with ID {pokemon_id}")
        break

conn.commit()
conn.close()