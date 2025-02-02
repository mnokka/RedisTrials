import redis
import requests



r = redis.Redis(host='localhost', port=6379, db=0)

cursor = 0
competitor_bibs = []

# Use SCAN to get EVERY competitor bib numbers
while True:
    cursor, keys = r.scan(cursor=cursor, match='competitor:*', count=100)
    for key in keys:
        # Poista 'competitor:'-etuliite ja lisää bib-numero listalle
        bib_number = key.decode('utf-8').split(':')[1]
        competitor_bibs.append(bib_number)
    if cursor == 0:
        break

print(f"All competitor BIB numbers:{competitor_bibs}")
print("-------------------------------------------------")

# toinen tapa hakea kaikki bib numerot
# for key in r.scan_iter('competitor:*'):
#    print(key)

# Get all m30 category participants
m30_competitors = []
for bib in competitor_bibs:
    response = requests.get(f'http://localhost:5000/getcompetitor/{bib}')
    if response.status_code == 200:
        competitor_data = response.json()
        if competitor_data.get('category') == 'men30':
            m30_competitors.append(competitor_data)
    else:
        print(f"Virhe haettaessa bib-numeron {bib} tietoja: {response.status_code}")

print(f"All men30 competitors:{m30_competitors}")
print("---------------------------------------------------------------")

bib_numbers = [competitor['bib'] for competitor in m30_competitors]
print(f"men30 bib_numbers:{bib_numbers}")

#Create men30 datastructure (bib,first_name,last_name,finish_time)
competitor_times = []
for bib in bib_numbers:
    timing_response = requests.get(f'http://localhost:5000/gettimes/{bib}')
    if timing_response.status_code == 200:
        timing_data = timing_response.json()
        finish_time = timing_data.get('finish')
        if finish_time:
            # Find the competitor's data
            competitor = next((comp for comp in m30_competitors if comp['bib'] == bib), None)
            if competitor:
                competitor_times.append({
                    'bib': bib,
                    'first_name': competitor['first_name'],
                    'last_name': competitor['last_name'],
                    'finish_time': finish_time
                })
    else:
        print(f"Error fetching timing data for bib {bib}: {timing_response.status_code}")

# Sort competitors men30 datastructure by finish time
sorted_competitors = sorted(competitor_times, key=lambda x: x['finish_time'])

# Display sorted competitors
print(f"--------- Sorted m30 result, best first -------------")
for competitor in sorted_competitors:
    print(f"Bib: {competitor['bib']}, Name: {competitor['first_name']} {competitor['last_name']}, Finish Time: {competitor['finish_time']}")



