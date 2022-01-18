import os
import psycopg2

# GETs rows given args from the web request
def get_rows(weapon, species, resident, points):

    # provides a mapping from query params to db syntax
    web_to_db_mapping = {
        'archery': 'Archery',
        'any-legal-weapon': 'Any Legal Weapon',
        'muzzleloader': 'Muzzleloader',
        'hams': 'H.a.m.s.',
        'general-deer': '%General Deer%',
        'mountain-goat': '%Mountain Goat%',
        'rocky-mountain-bighorn-sheep': '%Rocky Mountain Bighorn Sheep%',
        'desert-bighorn-sheep': '%Desert Bighorn Sheep%',
        'bison': '%Bison%',
        'cwmu-bull-moose': '%Cwmu Bull Moose%',
        'bull-moose': '%Bull Moose%',
        'cwmu-buck-pronghorn': '%Cwmu Buck Pronghorn%',
        'buck-pronghorn': '%Buck Pronghorn%',
        'cwmu-any-bull-elk': '%Cwmu Any Bull Elk%',
        'bull-elk': '%Bull Elk%',
        'cwmu-buck-deer': '%Cwmu Buck Deer%',
        'buck-deer': '%Buck Deer%',
        'true': True,
        'false': False,  
    }
    weapon = web_to_db_mapping.get(weapon)
    species = web_to_db_mapping.get(species)
    resident = web_to_db_mapping.get(resident)
    points = int(points)

    if weapon is None or species is None or resident is None:
        print(weapon, species, points)
        print('naughty naughty')
        return 'Invalid format for query params'
    
    # resident should be true or false, points should be valid integer

    DATABASE_URL = os.environ['DATABASE_URL']

    ## for local testing
    # DATABASE_URL = None
    conn = None
    if DATABASE_URL is not None:    
        conn = psycopg2.connect('DATABASE_URL', sslmode='require')
    else:
        conn = psycopg2.connect('postgres://postgres:admin@localHost:5432/postgres')

    try:
        cur = conn.cursor()

        if resident is True:
            cur.execute('''SELECT hunt_id, weapon, species, resident_points_guaranteed_to_draw, resident_permit_numbers, resident_odds
                           FROM hunting_odds_2021
                           WHERE weapon = %s and species like %s and resident_points_guaranteed_to_draw <= %s;''', (weapon, species, points))
        elif resident is False:
            cur.execute('''SELECT hunt_id, weapon, species, non_resident_points_guaranteed_to_draw, non_resident_permit_numbers, non_resident_odds
                           FROM hunting_odds_2021
                           WHERE weapon = %s and species like %s and non_resident_points_guaranteed_to_draw <= %s;''', (weapon, species, points))
        else:
            pass

        val = cur.fetchall()

        return val
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('db conn closed')

