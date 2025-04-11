import sqlite3

# Redefine data after kernel reset
activity_names = ["Culture & Historical Exploration", "Urban Entertainment & Nightlife", "Sports & Active Recreation", "Nature & Outdoor Adventure", "Relaxation & Wellness"]

raw_city_data = {
    "Istanbul": (41.0082, 28.9784, "Turkey"),
    "Moscow": (55.7558, 37.6173, "Russia"),
    "London": (51.5074, -0.1278, "United Kingdom"),
    "Saint Petersburg": (59.9343, 30.3351, "Russia"),
    "Berlin": (52.52, 13.405, "Germany"),
    "Madrid": (40.4168, -3.7038, "Spain"),
    "Rome": (41.9028, 12.4964, "Italy"),
    "Kyiv": (50.4501, 30.5236, "Ukraine"),
    "Bucharest": (44.4268, 26.1025, "Romania"),
    "Paris": (48.8566, 2.3522, "France"),
    "Belgrade": (44.8176, 20.4633, "Serbia"),
    "Hamburg": (53.5511, 9.9937, "Germany"),
    "Basel": (47.5596, 7.5886, "Switzerland"),
    "Geneva": (46.2044, 6.1432, "Switzerland"),
    "Warsaw": (52.2298, 21.0118, "Poland"),
    "Budapest": (47.4979, 19.0402, "Hungary"),
    "Vienna": (48.2082, 16.3738, "Austria"),
    "Munich": (48.1351, 11.582, "Germany"),
    "Milan": (45.4642, 9.19, "Italy"),
    "Prague": (50.0755, 14.4378, "Czech Republic"),
    "Sofia": (42.6977, 23.3219, "Bulgaria"),
    "Amsterdam": (52.3676, 4.9041, "Netherlands"),
    "Stuttgart": (48.7758, 9.1829, "Germany"),
    "Stockholm": (59.3293, 18.0686, "Sweden"),
    "Lisbon": (38.7169, -9.1395, "Portugal"),
    "Oslo": (59.9139, 10.7522, "Norway"),
    "Athens": (37.9838, 23.7275, "Greece"),
    "Copenhagen": (55.6761, 12.5683, "Denmark"),
    "Zürich": (47.3769, 8.5417, "Switzerland"),
    "Antwerp": (51.2194, 4.4025, "Belgium"),
    "Kraków": (50.0647, 19.945, "Poland"),
    "Minsk": (53.9, 27.5667, "Belarus"),
    "Tallinn": (59.437, 24.7535, "Estonia"),
    "Helsinki": (60.1699, 24.9384, "Finland"),
    "Chisinau": (47.0105, 28.8638, "Moldova"),
    "Belfast": (54.5973, -5.9301, "United Kingdom"),
    "Vilnius": (54.6892, 25.2798, "Lithuania"),
    "Riga": (56.946, 24.1059, "Latvia"),
    "Zagreb": (45.8131, 15.978, "Croatia"),
    "Sarajevo": (43.8486, 18.3564, "Bosnia and Herzegovina"),
    "Skopje": (41.9981, 21.4254, "North Macedonia"),
    "Tbilisi": (41.7151, 44.8271, "Georgia"),
    "Baku": (40.4093, 49.8671, "Azerbaijan"),
    "Dublin": (53.3498, -6.2603, "Ireland"),
    "Bristol": (51.4545, -2.5879, "United Kingdom"),
    "Cardiff": (51.4816, -3.1791, "United Kingdom"),
    "Manchester": (53.4808, -2.2426, "United Kingdom"),
    "Leeds": (53.8, -1.5491, "United Kingdom"),
    "Liverpool": (53.4084, -2.9916, "United Kingdom"),
    "Newcastle upon Tyne": (54.9783, -1.617, "United Kingdom"),
    "Sheffield": (53.3811, -1.4701, "United Kingdom"),
    "Nottingham": (52.9548, -1.1581, "United Kingdom"),
    "Leicester": (52.6369, -1.1398, "United Kingdom"),
    "Bradford": (53.7956, -1.7599, "United Kingdom"),
    "Coventry": (52.408, -1.5102, "United Kingdom"),
    "Birmingham": (52.4862, -1.8904, "United Kingdom"),
    "Glasgow": (55.8642, -4.2518, "United Kingdom"),
    "Edinburgh": (55.9533, -3.1883, "United Kingdom"),
    "Ljubljana": (46.0511, 14.5051, "Slovenia"),
    "Tirana": (41.3275, 19.8189, "Albania")
}

custom_city_activities = {
	"Basel": {
		"Culture & Historical Exploration": ["Kunstmuseum", "Basel Minster"],
		"Urban Entertainment & Nightlife": ["Bar Rouge", "Atlantis Club"],
		"Nature & Outdoor Adventure": ["Rhine River Cruise", "Basel Zoo"]
	},
	"Geneva": {
		"Culture & Historical Exploration": ["Jet d'Eau", "Palais des Nations"],
		"Urban Entertainment & Nightlife": ["Rue de l'École-de-Médecine Bars", "Java Club"],
		"Nature & Outdoor Adventure": ["Lake Geneva Boat Tour", "Mont Salève Hike"]
	},
    "Istanbul": {
        "Culture & Historical Exploration": ["Hagia Sophia", "Topkapi Palace"],
        "Urban Entertainment & Nightlife": ["Taksim Square", "Kadikoy Bars"],
        "Nature & Outdoor Adventure": ["Bosphorus Cruise", "Princes' Islands Tour"]
    },
    "Moscow": {
        "Culture & Historical Exploration": ["Red Square", "The Kremlin"],
        "Urban Entertainment & Nightlife": ["Arbat Street", "Bolotnaya Naberezhnaya"],
        "Nature & Outdoor Adventure": ["Gorky Park Activities"]
    },
    "London": {
        "Culture & Historical Exploration": ["British Museum", "Tower of London"],
        "Urban Entertainment & Nightlife": ["Soho", "Camden Town"],
        "Nature & Outdoor Adventure": ["Thames River Kayaking"]
    },
    "Saint Petersburg": {
        "Culture & Historical Exploration": ["Hermitage Museum", "Peter and Paul Fortress"],
        "Urban Entertainment & Nightlife": ["Nevsky Prospect", "Rubinstein Street"],
        "Nature & Outdoor Adventure": ["Icebreaker Cruise on Neva River"]
    },
    "Berlin": {
        "Culture & Historical Exploration": ["Brandenburg Gate", "Museum Island"],
        "Urban Entertainment & Nightlife": ["Berghain", "Kreuzberg Bars"],
        "Nature & Outdoor Adventure": ["Spree River Boat Tour"]
    },
    "Madrid": {
        "Culture & Historical Exploration": ["Prado Museum", "Royal Palace of Madrid"],
        "Urban Entertainment & Nightlife": ["Gran Via", "Chueca District"],
        "Nature & Outdoor Adventure": ["Retiro Park Rowing"]
    },
    "Rome": {
        "Culture & Historical Exploration": ["Colosseum", "Vatican Museums"],
        "Urban Entertainment & Nightlife": ["Trastevere", "Campo de' Fiori"],
        "Nature & Outdoor Adventure": ["Gianicolo Hill Walk"]
    },
    "Kyiv": {
        "Culture & Historical Exploration": ["Saint Sophia's Cathedral", "Kyiv Pechersk Lavra"],
        "Urban Entertainment & Nightlife": ["Arena City", "Podil District"],
        "Nature & Outdoor Adventure": ["Dnipro River Cruise"]
    },
    "Bucharest": {
        "Culture & Historical Exploration": ["Palace of the Parliament", "Romanian Athenaeum"],
        "Urban Entertainment & Nightlife": ["Old Town Lipscani", "Control Club"],
        "Nature & Outdoor Adventure": ["Herăstrău Park Boating"]
    },
    "Paris": {
        "Culture & Historical Exploration": ["Louvre Museum", "Notre-Dame Cathedral"],
        "Urban Entertainment & Nightlife": ["Moulin Rouge", "Le Marais"],
        "Nature & Outdoor Adventure": ["Seine River Cruise", "Montmartre Walk"]
    },
    "Belgrade": {
        "Culture & Historical Exploration": ["Belgrade Fortress", "Nikola Tesla Museum"],
        "Urban Entertainment & Nightlife": ["Skadarlija", "Floating River Clubs"],
        "Nature & Outdoor Adventure": ["Ada Ciganlija Lake Activities"]
    },
    "Hamburg": {
        "Culture & Historical Exploration": ["Miniatur Wunderland", "Elbphilharmonie"],
        "Urban Entertainment & Nightlife": ["Reeperbahn", "Sternschanze"],
        "Nature & Outdoor Adventure": ["Harbor Boat Tour"]
    },
    "Warsaw": {
        "Culture & Historical Exploration": ["Royal Castle", "POLIN Museum"],
        "Urban Entertainment & Nightlife": ["Pawilony", "Nowy Świat Street"],
        "Nature & Outdoor Adventure": ["Vistula River Sports & Active Recreation"]
    },
    "Budapest": {
        "Culture & Historical Exploration": ["Buda Castle", "Hungarian Parliament"],
        "Urban Entertainment & Nightlife": ["Ruin Bars in District VII", "Gozsdu Courtyard"],
        "Nature & Outdoor Adventure": ["Thermal Baths", "Danube River Cruise"]
    },
    "Vienna": {
        "Culture & Historical Exploration": ["Schönbrunn Palace", "Belvedere Museum"],
        "Urban Entertainment & Nightlife": ["Bermuda Triangle", "Gürtel Urban Entertainment & Nightlife Mile"],
        "Nature & Outdoor Adventure": ["Danube Island Activities"]
    },
    "Munich": {
        "Culture & Historical Exploration": ["Nymphenburg Palace", "Deutsches Museum"],
        "Urban Entertainment & Nightlife": ["Schwabing", "Glockenbachviertel"],
        "Nature & Outdoor Adventure": ["English Garden Surfing"]
    },
    "Milan": {
        "Culture & Historical Exploration": ["Duomo di Milano", "Sforza Castle"],
        "Urban Entertainment & Nightlife": ["Navigli District", "Brera District"],
        "Nature & Outdoor Adventure": ["Parco Sempione Walks"]
    },
    "Prague": {
        "Culture & Historical Exploration": ["Prague Castle", "Charles Bridge"],
        "Urban Entertainment & Nightlife": ["Wenceslas Square", "Zizkov District"],
        "Nature & Outdoor Adventure": ["Vltava River Cruise"]
    },
    "Sofia": {
        "Culture & Historical Exploration": ["Alexander Nevsky Cathedral", "National Palace of Culture"],
        "Urban Entertainment & Nightlife": ["Vitosha Boulevard", "Studentski Grad"],
        "Nature & Outdoor Adventure": ["Vitosha Mountain Hiking"]
    },
    "Amsterdam": {
        "Culture & Historical Exploration": ["Rijksmuseum", "Van Gogh Museum"],
        "Urban Entertainment & Nightlife": ["Leidseplein", "Red Light District"],
        "Nature & Outdoor Adventure": ["Canal Kayaking"]
    },
    "Stuttgart": {
        "Culture & Historical Exploration": ["Mercedes-Benz Museum", "Staatsgalerie Stuttgart"],
        "Urban Entertainment & Nightlife": ["Theodor-Heuss-Straße", "Hans-im-Glück-Viertel"],
        "Nature & Outdoor Adventure": ["Killesberg Park Climbing Tower"]
    },
    "Stockholm": {
        "Culture & Historical Exploration": ["Vasa Museum", "Gamla Stan"],
        "Urban Entertainment & Nightlife": ["Södermalm", "Stureplan"],
        "Nature & Outdoor Adventure": ["Archipelago Kayaking"]
    },
    "Lisbon": {
        "Culture & Historical Exploration": ["Belém Tower", "Jerónimos Monastery"],
        "Urban Entertainment & Nightlife": ["Bairro Alto", "Cais do Sodré"],
        "Sports & Active Recreation": ["Carcavelos Sports & Active Recreation", "Costa da Caparica"],
        "Nature & Outdoor Adventure": ["Tram 28 Ride"]
    },
    "Oslo": {
        "Culture & Historical Exploration": ["Viking Ship Museum", "Oslo Opera House"],
        "Urban Entertainment & Nightlife": ["Grünerløkka", "Aker Brygge"],
        "Nature & Outdoor Adventure": ["Oslofjord Sailing"]
    },
    "Athens": {
        "Culture & Historical Exploration": ["Acropolis", "National Archaeological Museum"],
        "Urban Entertainment & Nightlife": ["Psiri", "Gazi District"],
        "Sports & Active Recreation": ["Vouliagmeni Sports & Active Recreation", "Alimos Sports & Active Recreation"],
        "Nature & Outdoor Adventure": ["Mount Lycabettus Hike"]
    },
    "Copenhagen": {
        "Culture & Historical Exploration": ["Tivoli Gardens", "The Little Mermaid"],
        "Urban Entertainment & Nightlife": ["Nyhavn", "Meatpacking District"],
        "Nature & Outdoor Adventure": ["Cycling Tours"]
    },
    "Zürich": {
        "Culture & Historical Exploration": ["Kunsthaus", "Swiss National Museum"],
        "Urban Entertainment & Nightlife": ["Plaza", "Kanzlei Club"],
        "Nature & Outdoor Adventure": ["Swimming in Lake Zurich", "Hike to Uetliberg"]
    },
    "Antwerp": {
        "Culture & Historical Exploration": ["Cathedral of Our Lady", "MAS Museum"],
        "Urban Entertainment & Nightlife": ["Het Zuid", "Eilandje"],
        "Nature & Outdoor Adventure": ["Scheldt River Cruise"]
    },
    "Kraków": {
        "Culture & Historical Exploration": ["Wawel Castle", "Main Market Square"],
        "Urban Entertainment & Nightlife": ["Kazimierz District", "Old Town Bars"],
        "Nature & Outdoor Adventure": ["Vistula River Walks"]
    },
    "Minsk": {
        "Culture & Historical Exploration": ["National Opera and Ballet Theatre", "Victory Square"],
        "Urban Entertainment & Nightlife": ["Zybitskaya Street", "Nemiga Clubs"],
        "Nature & Outdoor Adventure": ["Gorky Park Activities"]
    },
    "Tallinn": {
        "Culture & Historical Exploration": ["Toompea Castle", "Alexander Nevsky Cathedral"],
        "Urban Entertainment & Nightlife": ["Old Town Pubs", "Telliskivi Creative City"],
        "Nature & Outdoor Adventure": ["Seaside Promenade Walks"]
    },
    "Helsinki": {
        "Culture & Historical Exploration": ["Helsinki Cathedral", "Ateneum Art Museum"],
        "Urban Entertainment & Nightlife": ["Kallio District", "Punavuori Bars"],
        "Nature & Outdoor Adventure": ["Suomenlinna Island", "Baltic Sea Ferries"]
    },
    "Chisinau": {
        "Culture & Historical Exploration": ["Stefan Cel Mare Park", "National Museum of History"],
        "Urban Entertainment & Nightlife": ["Z Lounge", "Eli-Pili"],
        "Nature & Outdoor Adventure": ["Valea Morilor Lake Walk"]
    },
    "Belfast": {
        "Culture & Historical Exploration": ["Titanic Belfast", "Ulster Museum"],
        "Urban Entertainment & Nightlife": ["Cathedral Quarter", "Laverys Bar"],
        "Nature & Outdoor Adventure": ["Cave Hill Hike"]
    },
    "Vilnius": {
        "Culture & Historical Exploration": ["Gediminas Tower", "Vilnius Old Town"],
        "Urban Entertainment & Nightlife": ["Užupis Bars", "Vilniaus Street"],
        "Nature & Outdoor Adventure": ["Hot Air Balloon Ride"]
    },
    "Riga": {
        "Culture & Historical Exploration": ["House of the Blackheads", "Riga Cathedral"],
        "Urban Entertainment & Nightlife": ["Old Town Bars", "Miera Iela District"],
        "Nature & Outdoor Adventure": ["Daugava River Cruise"]
    },
    "Zagreb": {
        "Culture & Historical Exploration": ["Museum of Broken Relationships", "St. Mark's Church"],
        "Urban Entertainment & Nightlife": ["Tkalciceva Street", "Medika Club"],
        "Nature & Outdoor Adventure": ["Medvednica Mountain Hiking"]
    },
    "Sarajevo": {
        "Culture & Historical Exploration": ["Baščaršija", "Latin Bridge"],
        "Urban Entertainment & Nightlife": ["Ferhadija Street Bars", "Sloga Club"],
        "Nature & Outdoor Adventure": ["Cable Car to Trebević"]
    },
    "Skopje": {
        "Culture & Historical Exploration": ["Old Bazaar", "Skopje Fortress"],
        "Urban Entertainment & Nightlife": ["Debar Maalo", "Bohemian Street"],
        "Nature & Outdoor Adventure": ["Vodno Mountain Hike"]
    },
    "Tbilisi": {
        "Culture & Historical Exploration": ["Narikala Fortress", "Holy Trinity Cathedral"],
        "Urban Entertainment & Nightlife": ["Fabrika", "Rustaveli Avenue Bars"],
        "Nature & Outdoor Adventure": ["Sulfur Baths", "Mtatsminda Park"]
    },
    "Baku": {
        "Culture & Historical Exploration": ["Maiden Tower", "Heydar Aliyev Center"],
        "Urban Entertainment & Nightlife": ["Nizami Street", "Port Baku Clubs"],
        "Nature & Outdoor Adventure": ["Caspian Sea Boulevard Walks"],
        "Sports & Active Recreation": ["Shikhov Sports & Active Recreation", "Bilgah Sports & Active Recreation"]
    },
    "Dublin": {
        "Culture & Historical Exploration": ["Trinity College & Book of Kells", "Dublin Castle"],
        "Urban Entertainment & Nightlife": ["Temple Bar", "Camden Street"],
        "Nature & Outdoor Adventure": ["Phoenix Park Cycling"]
    },
    "Bristol": {
        "Culture & Historical Exploration": ["SS Great Britain", "Bristol Museum"],
        "Urban Entertainment & Nightlife": ["Stokes Croft", "Harbourside Bars"],
        "Nature & Outdoor Adventure": ["Clifton Suspension Bridge Walk"]
    },
    "Cardiff": {
        "Culture & Historical Exploration": ["Cardiff Castle", "National Museum Cardiff"],
        "Urban Entertainment & Nightlife": ["Mill Lane", "Womanby Street"],
        "Nature & Outdoor Adventure": ["Cardiff Bay Kayaking"]
    },
    "Manchester": {
        "Culture & Historical Exploration": ["Manchester Art Gallery", "Science and Industry Museum"],
        "Urban Entertainment & Nightlife": ["Northern Quarter", "Deansgate Locks"],
        "Nature & Outdoor Adventure": ["Canal Walks", "Heaton Park Boating"]
    },
    "Leeds": {
        "Culture & Historical Exploration": ["Royal Armouries Museum", "Kirkstall Abbey"],
        "Urban Entertainment & Nightlife": ["Call Lane", "Greek Street"],
        "Nature & Outdoor Adventure": ["Roundhay Park Activities"]
    },
    "Liverpool": {
        "Culture & Historical Exploration": ["The Beatles Story", "Liverpool Cathedral"],
        "Urban Entertainment & Nightlife": ["Mathew Street", "Concert Square"],
        "Nature & Outdoor Adventure": ["Mersey Ferry Ride"]
    },
    "Newcastle upon Tyne": {
        "Culture & Historical Exploration": ["BALTIC Centre", "St. Nicholas' Cathedral"],
        "Urban Entertainment & Nightlife": ["Bigg Market", "The Ouseburn"],
        "Nature & Outdoor Adventure": ["Tyne Bridge Walk"]
    },
    "Sheffield": {
        "Culture & Historical Exploration": ["Millennium Gallery", "Kelham Island Museum"],
        "Urban Entertainment & Nightlife": ["Division Street", "Ecclesall Road"],
        "Nature & Outdoor Adventure": ["Peak District Excursions"]
    },
    "Nottingham": {
        "Culture & Historical Exploration": ["Nottingham Castle", "Galleries of Justice Museum"],
        "Urban Entertainment & Nightlife": ["Hockley", "Lace Market"],
        "Nature & Outdoor Adventure": ["Sherwood Forest Trips"]
    },
    "Leicester": {
        "Culture & Historical Exploration": ["King Richard III Visitor Centre", "New Walk Museum"],
        "Urban Entertainment & Nightlife": ["Granby Street", "Highcross Area"],
        "Nature & Outdoor Adventure": ["Bradgate Park Hike"]
    },
    "Bradford": {
        "Culture & Historical Exploration": ["National Science and Media Museum", "Cartwright Hall"],
        "Urban Entertainment & Nightlife": ["Sunbridge Wells", "North Parade Bars"]
    },
    "Coventry": {
        "Culture & Historical Exploration": ["Coventry Cathedral", "Transport Museum"],
        "Urban Entertainment & Nightlife": ["FarGo Village", "City Centre Pubs"]
    },
    "Birmingham": {
        "Culture & Historical Exploration": ["Birmingham Museum & Art Gallery", "Library of Birmingham"],
        "Urban Entertainment & Nightlife": ["Broad Street", "Digbeth"],
        "Nature & Outdoor Adventure": ["Canal Network Tours"]
    },
    "Glasgow": {
        "Culture & Historical Exploration": ["Kelvingrove Art Gallery", "Glasgow Cathedral"],
        "Urban Entertainment & Nightlife": ["Sauchiehall Street", "Ashton Lane"],
        "Nature & Outdoor Adventure": ["Glasgow Green Walks"]
    },
    "Edinburgh": {
        "Culture & Historical Exploration": ["Edinburgh Castle", "National Museum of Scotland"],
        "Urban Entertainment & Nightlife": ["Grassmarket", "Cowgate"],
        "Nature & Outdoor Adventure": ["Arthur's Seat Hike"]
    },
    "Ljubljana": {
        "Culture & Historical Exploration": ["Ljubljana Castle", "National Gallery"],
        "Urban Entertainment & Nightlife": ["Metelkova", "Ljubljanica Riverside Bars"],
        "Nature & Outdoor Adventure": ["Tivoli Park Cycling"]
    },
    "Tirana": {
        "Culture & Historical Exploration": ["Et'hem Bey Mosque", "Bunk'Art Museum"],
        "Urban Entertainment & Nightlife": ["Blloku District", "Sky Club"],
        "Nature & Outdoor Adventure": ["Dajti Mountain Cable Car"]
    }
}

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS city_activities")
cursor.execute("DROP TABLE IF EXISTS activities")
cursor.execute("DROP TABLE IF EXISTS cities")

cursor.execute('''
CREATE TABLE cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    latitude REAL,
    longitude REAL,
    country TEXT
)''')

cursor.execute('''
CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)''')

cursor.execute('''
CREATE TABLE city_activities (
    city_id INTEGER,
    activity_id INTEGER,
    description TEXT,
    FOREIGN KEY (city_id) REFERENCES cities(id),
    FOREIGN KEY (activity_id) REFERENCES activities(id)
)''')

activity_ids = {}
for name in activity_names:
    cursor.execute("INSERT INTO activities (name) VALUES (?)", (name,))
    activity_ids[name] = cursor.lastrowid

for city, (lat, lon, country) in raw_city_data.items():
    cursor.execute("INSERT INTO cities (name, latitude, longitude, country) VALUES (?, ?, ?, ?)",
                   (city, lat, lon, country))
    cursor.execute("SELECT id FROM cities WHERE name = ?", (city,))
    city_id = cursor.fetchone()[0]
    for activity in activity_names:
        cursor.execute("SELECT id FROM activities WHERE name = ?", (activity,))
        activity_id = cursor.fetchone()[0]
        if city in custom_city_activities and activity in custom_city_activities[city]:
            for desc in custom_city_activities[city][activity]:
                cursor.execute('''
                    INSERT INTO city_activities (city_id, activity_id, description)
                    VALUES (?, ?, ?)
                ''', (city_id, activity_id, desc))
        else:
            cursor.execute('''
                INSERT INTO city_activities (city_id, activity_id, description)
                VALUES (?, ?, NULL)
            ''', (city_id, activity_id))

conn.commit()
conn.close()
