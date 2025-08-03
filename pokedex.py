def analyse_pokemon(query,move_type = None):
    
    print(f"Analyzing {query} against {move_type}-type move")

    import requests

    from termcolor import colored

    import pprint

    from IPython.display import Image, display

    pokemon_number = None
    pokemon_name = None

    # Use identifier directly from Flask form
    pokemon_identifier = query
    
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_identifier}")
    
    if response.status_code == 200:
        pokemon_forms = response.json()

        pokemon_full_data = response.json()

        sprite = pokemon_full_data['sprites']['front_default']
        display(Image(url=sprite,width = 200))


        pokemon_name = pokemon_full_data['name']
        print(colored(pokemon_name.title(),attrs=["bold"]))

        #Types
        pokemon_type_1 = pokemon_full_data['types'][0]['type']['name']

        try:
            pokemon_type_2 = pokemon_full_data['types'][1]['type']['name']
        except IndexError: 
            pokemon_type_2 = False

        if pokemon_type_2:
            print(pokemon_type_1.title(), " / ", pokemon_type_2.title())

        else:
            print(pokemon_type_1.title())


        # Game title
        def get_game_title(pokemon_number):
            pokemon_forms = requests.get(f"https://pokeapi.co/api/v2/pokemon-form/{pokemon_number}/").json()

            pokemon_version = pokemon_forms['version_group']['name']

            if pokemon_version is None:
                return 'Game title not found'

            list_of_words = pokemon_version.split('-')

            num_of_words = len(list_of_words)

            if num_of_words == 2:
                return(list_of_words[0].title() + " and " + list_of_words[1].title())
            
            elif num_of_words == 4:
                return(list_of_words[0].title() + ' ' + list_of_words[1].title() + " and " + list_of_words[2].title() + ' ' + list_of_words[3].title())

            return 'Game title not found'
        
        game_title = get_game_title(pokemon_identifier)

        print()
        print(colored("Game introduced:",attrs=["bold"]))
        print(get_game_title(pokemon_identifier))


        # Stats
        pokemon_stats = pokemon_full_data['stats']
        pokemon_hp = pokemon_full_data['stats'][0]['base_stat']
        pokemon_attack = pokemon_full_data['stats'][1]['base_stat']
        pokemon_defence = pokemon_full_data['stats'][2]['base_stat']
        pokemon_sp_attack = pokemon_full_data['stats'][3]['base_stat']
        pokemon_sp_defence = pokemon_full_data['stats'][4]['base_stat']
        pokemon_speed = pokemon_full_data['stats'][5]['base_stat']

        print()
        print(colored("Stats: ",attrs=["bold"]))
        print("HP:", pokemon_hp)
        print("Attack:", pokemon_attack)
        print("Defence:", pokemon_defence)
        print("Special attack:", pokemon_sp_attack)
        print("Speed:", pokemon_speed)
        print()


        # Pulling all types from PokeAPI
        type_API = requests.get(f"https://pokeapi.co/api/v2/type/").json()
        all_types = type_API['results'] # all_types is a LIST
        type_names = [type_info['name'] for type_info in all_types]


        # Pokemon's types
        pokemon_type_1 = pokemon_full_data['types'][0]['type']['name'] if pokemon_full_data['types'] else "No types found"
        try:
            pokemon_type_2 = pokemon_full_data['types'][1]['type']['name']
        except IndexError: 
            pokemon_type_2 = False
        try:
            t2_url = pokemon_full_data['types'][1]['type']['url']
        except IndexError: 
            t2_url = False


        # Pokemon's type 1 data
        t1_url = pokemon_full_data['types'][0]['type']['url']
        t1_api = requests.get(t1_url).json()
        t1_damage_relations = t1_api['damage_relations']
        t1_double_damage_to = t1_damage_relations['double_damage_to']
        t1_damage_profile = {
            "double_damage_from": [entry['name'] for entry in t1_damage_relations['double_damage_from']],
            "double_damage_to": [entry['name'] for entry in t1_damage_relations['double_damage_to']],
            "half_damage_from": [entry['name'] for entry in t1_damage_relations['half_damage_from']],
            "half_damage_to": [entry['name'] for entry in t1_damage_relations['half_damage_to']],
            "no_damage_from": [entry['name'] for entry in t1_damage_relations['no_damage_from']],
            "no_damage_to": [entry['name'] for entry in t1_damage_relations['no_damage_to']],
        }
        print()


        # Pokemon's type 2 data
        t2_damage_profile = None # Resets the memory (otherwise last stored t2 will be run even if none exists)
        if t2_url:
            t2_api = requests.get(t2_url).json()
            t2_damage_relations = t2_api['damage_relations']
            t2_damage_profile = {
            "double_damage_from": [entry['name'] for entry in t2_damage_relations['double_damage_from']],
            "double_damage_to": [entry['name'] for entry in t2_damage_relations['double_damage_to']],
            "half_damage_from": [entry['name'] for entry in t2_damage_relations['half_damage_from']],
            "half_damage_to": [entry['name'] for entry in t2_damage_relations['half_damage_to']],
            "no_damage_from": [entry['name'] for entry in t2_damage_relations['no_damage_from']],
            "no_damage_to": [entry['name'] for entry in t2_damage_relations['no_damage_to']],
        }
        print()

        offensive_profiles = {}

        # Type 1 offensive profile
        offensive_profiles[pokemon_type_1.title()] = {
        "2x": sorted([item.title() for item in t1_damage_profile['double_damage_to']]) if t1_damage_profile['double_damage_to'] else ["None"],
        "0.5x": sorted([item.title() for item in t1_damage_profile['half_damage_to']]) if t1_damage_profile['half_damage_to'] else ["None"],
        "0x": sorted([item.title() for item in t1_damage_profile['no_damage_to']]) if t1_damage_profile['no_damage_to'] else ["None"]
}

        # Type 2 offensive profile (if available)
        if t2_damage_profile:
            offensive_profiles[pokemon_type_2.title()] = {
                "2x": sorted([item.title() for item in t2_damage_profile['double_damage_to']]) if t2_damage_profile['double_damage_to'] else ["None"],
                "0.5x": sorted([item.title() for item in t2_damage_profile['half_damage_to']]) if t2_damage_profile['half_damage_to'] else ["None"],
                "0x": sorted([item.title() for item in t2_damage_profile['no_damage_to']]) if t2_damage_profile['no_damage_to'] else ["None"]
            }



        # Defending vs a specific type
        
        multiplier = None

        if move_type:

            print(colored("Defending against a specific type:",attrs=["bold"]))
            type_api = requests.get(f"https://pokeapi.co/api/v2/type/{(move_type)}").json()
            relations = type_api['damage_relations']
            damage_profile = {
                "double_damage_from": [entry['name'] for entry in relations['double_damage_from']],
                "double_damage_to": [entry['name'] for entry in relations['double_damage_to']],
                "half_damage_from": [entry['name'] for entry in relations['half_damage_from']],
                "half_damage_to": [entry['name'] for entry in relations['half_damage_to']],
                "no_damage_from": [entry['name'] for entry in relations['no_damage_from']],
                "no_damage_to": [entry['name'] for entry in relations['no_damage_to']],
            }

            # Calculating move effectiveness v Pokemon
            multiplier = 1.0
            # Check against type 1
            if pokemon_type_1:
                if pokemon_type_1 in damage_profile['double_damage_to']:
                    multiplier *= 2
                elif pokemon_type_1 in damage_profile['half_damage_to']:
                    multiplier *= 0.5
                elif pokemon_type_1 in damage_profile['no_damage_to']:
                    multiplier *= 0

            # Check against type 2 (if it exists)
            if pokemon_type_2:
                if pokemon_type_2 in damage_profile['double_damage_to']:
                    multiplier *= 2
                elif pokemon_type_2 in damage_profile['half_damage_to']:
                    multiplier *= 0.5
                elif pokemon_type_2 in damage_profile['no_damage_to']:
                    multiplier *= 0


        return {
            "name": pokemon_name.title(),
            "types": [pokemon_type_1.title(), pokemon_type_2.title()] if pokemon_type_2 else [pokemon_type_1.title()],
            "game_title": game_title,
            "sprite_url": sprite,
            "stats": {
                "HP": pokemon_hp,
                "Attack": pokemon_attack,
                "Defense": pokemon_defence,
                "Special Attack": pokemon_sp_attack,
                "Speed": pokemon_speed
            },
            "offensive_profiles": offensive_profiles,
            "defensive_effectiveness": {
                "selected_type": move_type.title() if move_type else None,
                "move_type_effectiveness": f"{multiplier}x damage" if multiplier is not None else "N/A",
            }
        }
    
    else:
        print(f"Error fetching data: {response.status_code}")
        pokemon_forms = None
