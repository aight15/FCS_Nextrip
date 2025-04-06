import sqlite3

# Redefine data after kernel reset
activity_names = ["Culture", "Nightlife", "Beach", "Adventure"]

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
		"Culture": ["Kunstmuseum", "Basel Minster"],
		"Nightlife": ["Bar Rouge", "Atlantis Club"],
		"Adventure": ["Rhine River Cruise", "Basel Zoo"]
	},
	"Geneva": {
		"Culture": ["Jet d'Eau", "Palais des Nations"],
		"Nightlife": ["Rue de l'École-de-Médecine Bars", "Java Club"],
		"Adventure": ["Lake Geneva Boat Tour", "Mont Salève Hike"]
	},
    "Istanbul": {
        "Culture": ["Hagia Sophia", "Topkapi Palace"],
        "Nightlife": ["Taksim Square", "Kadikoy Bars"],
        "Adventure": ["Bosphorus Cruise", "Princes' Islands Tour"]
    },
    "Moscow": {
        "Culture": ["Red Square", "The Kremlin"],
        "Nightlife": ["Arbat Street", "Bolotnaya Naberezhnaya"],
        "Adventure": ["Gorky Park Activities"]
    },
    "London": {
        "Culture": ["British Museum", "Tower of London"],
        "Nightlife": ["Soho", "Camden Town"],
        "Adventure": ["Thames River Kayaking"]
    },
    "Saint Petersburg": {
        "Culture": ["Hermitage Museum", "Peter and Paul Fortress"],
        "Nightlife": ["Nevsky Prospect", "Rubinstein Street"],
        "Adventure": ["Icebreaker Cruise on Neva River"]
    },
    "Berlin": {
        "Culture": ["Brandenburg Gate", "Museum Island"],
        "Nightlife": ["Berghain", "Kreuzberg Bars"],
        "Adventure": ["Spree River Boat Tour"]
    },
    "Madrid": {
        "Culture": ["Prado Museum", "Royal Palace of Madrid"],
        "Nightlife": ["Gran Via", "Chueca District"],
        "Adventure": ["Retiro Park Rowing"]
    },
    "Rome": {
        "Culture": ["Colosseum", "Vatican Museums"],
        "Nightlife": ["Trastevere", "Campo de' Fiori"],
        "Adventure": ["Gianicolo Hill Walk"]
    },
    "Kyiv": {
        "Culture": ["Saint Sophia's Cathedral", "Kyiv Pechersk Lavra"],
        "Nightlife": ["Arena City", "Podil District"],
        "Adventure": ["Dnipro River Cruise"]
    },
    "Bucharest": {
        "Culture": ["Palace of the Parliament", "Romanian Athenaeum"],
        "Nightlife": ["Old Town Lipscani", "Control Club"],
        "Adventure": ["Herăstrău Park Boating"]
    },
    "Paris": {
        "Culture": ["Louvre Museum", "Notre-Dame Cathedral"],
        "Nightlife": ["Moulin Rouge", "Le Marais"],
        "Adventure": ["Seine River Cruise", "Montmartre Walk"]
    },
    "Belgrade": {
        "Culture": ["Belgrade Fortress", "Nikola Tesla Museum"],
        "Nightlife": ["Skadarlija", "Floating River Clubs"],
        "Adventure": ["Ada Ciganlija Lake Activities"]
    },
    "Hamburg": {
        "Culture": ["Miniatur Wunderland", "Elbphilharmonie"],
        "Nightlife": ["Reeperbahn", "Sternschanze"],
        "Adventure": ["Harbor Boat Tour"]
    },
    "Warsaw": {
        "Culture": ["Royal Castle", "POLIN Museum"],
        "Nightlife": ["Pawilony", "Nowy Świat Street"],
        "Adventure": ["Vistula River Beach"]
    },
    "Budapest": {
        "Culture": ["Buda Castle", "Hungarian Parliament"],
        "Nightlife": ["Ruin Bars in District VII", "Gozsdu Courtyard"],
        "Adventure": ["Thermal Baths", "Danube River Cruise"]
    },
    "Vienna": {
        "Culture": ["Schönbrunn Palace", "Belvedere Museum"],
        "Nightlife": ["Bermuda Triangle", "Gürtel Nightlife Mile"],
        "Adventure": ["Danube Island Activities"]
    },
    "Munich": {
        "Culture": ["Nymphenburg Palace", "Deutsches Museum"],
        "Nightlife": ["Schwabing", "Glockenbachviertel"],
        "Adventure": ["English Garden Surfing"]
    },
    "Milan": {
        "Culture": ["Duomo di Milano", "Sforza Castle"],
        "Nightlife": ["Navigli District", "Brera District"],
        "Adventure": ["Parco Sempione Walks"]
    },
    "Prague": {
        "Culture": ["Prague Castle", "Charles Bridge"],
        "Nightlife": ["Wenceslas Square", "Zizkov District"],
        "Adventure": ["Vltava River Cruise"]
    },
    "Sofia": {
        "Culture": ["Alexander Nevsky Cathedral", "National Palace of Culture"],
        "Nightlife": ["Vitosha Boulevard", "Studentski Grad"],
        "Adventure": ["Vitosha Mountain Hiking"]
    },
    "Amsterdam": {
        "Culture": ["Rijksmuseum", "Van Gogh Museum"],
        "Nightlife": ["Leidseplein", "Red Light District"],
        "Adventure": ["Canal Kayaking"]
    },
    "Stuttgart": {
        "Culture": ["Mercedes-Benz Museum", "Staatsgalerie Stuttgart"],
        "Nightlife": ["Theodor-Heuss-Straße", "Hans-im-Glück-Viertel"],
        "Adventure": ["Killesberg Park Climbing Tower"]
    },
    "Stockholm": {
        "Culture": ["Vasa Museum", "Gamla Stan"],
        "Nightlife": ["Södermalm", "Stureplan"],
        "Adventure": ["Archipelago Kayaking"]
    },
    "Lisbon": {
        "Culture": ["Belém Tower", "Jerónimos Monastery"],
        "Nightlife": ["Bairro Alto", "Cais do Sodré"],
        "Beach": ["Carcavelos Beach", "Costa da Caparica"],
        "Adventure": ["Tram 28 Ride"]
    },
    "Oslo": {
        "Culture": ["Viking Ship Museum", "Oslo Opera House"],
        "Nightlife": ["Grünerløkka", "Aker Brygge"],
        "Adventure": ["Oslofjord Sailing"]
    },
    "Athens": {
        "Culture": ["Acropolis", "National Archaeological Museum"],
        "Nightlife": ["Psiri", "Gazi District"],
        "Beach": ["Vouliagmeni Beach", "Alimos Beach"],
        "Adventure": ["Mount Lycabettus Hike"]
    },
    "Copenhagen": {
        "Culture": ["Tivoli Gardens", "The Little Mermaid"],
        "Nightlife": ["Nyhavn", "Meatpacking District"],
        "Adventure": ["Cycling Tours"]
    },
    "Zürich": {
        "Culture": ["Kunsthaus", "Swiss National Museum"],
        "Nightlife": ["Plaza", "Kanzlei Club"],
        "Adventure": ["Swimming in Lake Zurich", "Hike to Uetliberg"]
    },
    "Antwerp": {
        "Culture": ["Cathedral of Our Lady", "MAS Museum"],
        "Nightlife": ["Het Zuid", "Eilandje"],
        "Adventure": ["Scheldt River Cruise"]
    },
    "Kraków": {
        "Culture": ["Wawel Castle", "Main Market Square"],
        "Nightlife": ["Kazimierz District", "Old Town Bars"],
        "Adventure": ["Vistula River Walks"]
    },
    "Minsk": {
        "Culture": ["National Opera and Ballet Theatre", "Victory Square"],
        "Nightlife": ["Zybitskaya Street", "Nemiga Clubs"],
        "Adventure": ["Gorky Park Activities"]
    },
    "Tallinn": {
        "Culture": ["Toompea Castle", "Alexander Nevsky Cathedral"],
        "Nightlife": ["Old Town Pubs", "Telliskivi Creative City"],
        "Adventure": ["Seaside Promenade Walks"]
    },
    "Helsinki": {
        "Culture": ["Helsinki Cathedral", "Ateneum Art Museum"],
        "Nightlife": ["Kallio District", "Punavuori Bars"],
        "Adventure": ["Suomenlinna Island", "Baltic Sea Ferries"]
    },
    "Chisinau": {
        "Culture": ["Stefan Cel Mare Park", "National Museum of History"],
        "Nightlife": ["Z Lounge", "Eli-Pili"],
        "Adventure": ["Valea Morilor Lake Walk"]
    },
    "Belfast": {
        "Culture": ["Titanic Belfast", "Ulster Museum"],
        "Nightlife": ["Cathedral Quarter", "Laverys Bar"],
        "Adventure": ["Cave Hill Hike"]
    },
    "Vilnius": {
        "Culture": ["Gediminas Tower", "Vilnius Old Town"],
        "Nightlife": ["Užupis Bars", "Vilniaus Street"],
        "Adventure": ["Hot Air Balloon Ride"]
    },
    "Riga": {
        "Culture": ["House of the Blackheads", "Riga Cathedral"],
        "Nightlife": ["Old Town Bars", "Miera Iela District"],
        "Adventure": ["Daugava River Cruise"]
    },
    "Zagreb": {
        "Culture": ["Museum of Broken Relationships", "St. Mark's Church"],
        "Nightlife": ["Tkalciceva Street", "Medika Club"],
        "Adventure": ["Medvednica Mountain Hiking"]
    },
    "Sarajevo": {
        "Culture": ["Baščaršija", "Latin Bridge"],
        "Nightlife": ["Ferhadija Street Bars", "Sloga Club"],
        "Adventure": ["Cable Car to Trebević"]
    },
    "Skopje": {
        "Culture": ["Old Bazaar", "Skopje Fortress"],
        "Nightlife": ["Debar Maalo", "Bohemian Street"],
        "Adventure": ["Vodno Mountain Hike"]
    },
    "Tbilisi": {
        "Culture": ["Narikala Fortress", "Holy Trinity Cathedral"],
        "Nightlife": ["Fabrika", "Rustaveli Avenue Bars"],
        "Adventure": ["Sulfur Baths", "Mtatsminda Park"]
    },
    "Baku": {
        "Culture": ["Maiden Tower", "Heydar Aliyev Center"],
        "Nightlife": ["Nizami Street", "Port Baku Clubs"],
        "Adventure": ["Caspian Sea Boulevard Walks"],
        "Beach": ["Shikhov Beach", "Bilgah Beach"]
    },
    "Dublin": {
        "Culture": ["Trinity College & Book of Kells", "Dublin Castle"],
        "Nightlife": ["Temple Bar", "Camden Street"],
        "Adventure": ["Phoenix Park Cycling"]
    },
    "Bristol": {
        "Culture": ["SS Great Britain", "Bristol Museum"],
        "Nightlife": ["Stokes Croft", "Harbourside Bars"],
        "Adventure": ["Clifton Suspension Bridge Walk"]
    },
    "Cardiff": {
        "Culture": ["Cardiff Castle", "National Museum Cardiff"],
        "Nightlife": ["Mill Lane", "Womanby Street"],
        "Adventure": ["Cardiff Bay Kayaking"]
    },
    "Manchester": {
        "Culture": ["Manchester Art Gallery", "Science and Industry Museum"],
        "Nightlife": ["Northern Quarter", "Deansgate Locks"],
        "Adventure": ["Canal Walks", "Heaton Park Boating"]
    },
    "Leeds": {
        "Culture": ["Royal Armouries Museum", "Kirkstall Abbey"],
        "Nightlife": ["Call Lane", "Greek Street"],
        "Adventure": ["Roundhay Park Activities"]
    },
    "Liverpool": {
        "Culture": ["The Beatles Story", "Liverpool Cathedral"],
        "Nightlife": ["Mathew Street", "Concert Square"],
        "Adventure": ["Mersey Ferry Ride"]
    },
    "Newcastle upon Tyne": {
        "Culture": ["BALTIC Centre", "St. Nicholas' Cathedral"],
        "Nightlife": ["Bigg Market", "The Ouseburn"],
        "Adventure": ["Tyne Bridge Walk"]
    },
    "Sheffield": {
        "Culture": ["Millennium Gallery", "Kelham Island Museum"],
        "Nightlife": ["Division Street", "Ecclesall Road"],
        "Adventure": ["Peak District Excursions"]
    },
    "Nottingham": {
        "Culture": ["Nottingham Castle", "Galleries of Justice Museum"],
        "Nightlife": ["Hockley", "Lace Market"],
        "Adventure": ["Sherwood Forest Trips"]
    },
    "Leicester": {
        "Culture": ["King Richard III Visitor Centre", "New Walk Museum"],
        "Nightlife": ["Granby Street", "Highcross Area"],
        "Adventure": ["Bradgate Park Hike"]
    },
    "Bradford": {
        "Culture": ["National Science and Media Museum", "Cartwright Hall"],
        "Nightlife": ["Sunbridge Wells", "North Parade Bars"]
    },
    "Coventry": {
        "Culture": ["Coventry Cathedral", "Transport Museum"],
        "Nightlife": ["FarGo Village", "City Centre Pubs"]
    },
    "Birmingham": {
        "Culture": ["Birmingham Museum & Art Gallery", "Library of Birmingham"],
        "Nightlife": ["Broad Street", "Digbeth"],
        "Adventure": ["Canal Network Tours"]
    },
    "Glasgow": {
        "Culture": ["Kelvingrove Art Gallery", "Glasgow Cathedral"],
        "Nightlife": ["Sauchiehall Street", "Ashton Lane"],
        "Adventure": ["Glasgow Green Walks"]
    },
    "Edinburgh": {
        "Culture": ["Edinburgh Castle", "National Museum of Scotland"],
        "Nightlife": ["Grassmarket", "Cowgate"],
        "Adventure": ["Arthur's Seat Hike"]
    },
    "Ljubljana": {
        "Culture": ["Ljubljana Castle", "National Gallery"],
        "Nightlife": ["Metelkova", "Ljubljanica Riverside Bars"],
        "Adventure": ["Tivoli Park Cycling"]
    },
    "Tirana": {
        "Culture": ["Et'hem Bey Mosque", "Bunk'Art Museum"],
        "Nightlife": ["Blloku District", "Sky Club"],
        "Adventure": ["Dajti Mountain Cable Car"]
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
