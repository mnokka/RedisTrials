
# Redis DB in a docker. Flask server implements race timing services

Flask server implements basic commands to keep record of timing services:

1) Create competitor (including BIB)
2) Add and change timing points (start, split points, finish time)
3) Get Bib timings points
3) Get Bib competitor info

Redis memory based DB is configured to be backup every 20s (if changes)
to docker volume 

(volumes: - /home/mika/REDIS_DATA:/data)

## Race data definitions

*db.json*

Defines all race timing points. Example:

{
    "allowed_checkpoints": ["start", "split1", "split2", "finish"]
}

*competitor.json*

Defines competitor data . Example:

{  
  "competitor_info": {
    "allowed_keys": ["bib", "first_name", "last_name", "gender", "country", "category"],
    "allowed_genders": ["male", "female", "na"],
    "allowed_categories": [
      "men20", "men30", "men40", "men50+",
      "women20", "women30", "women40", "women50+"
    ]
  }
}

## BIB number used to link competitor data to competitor timings:

Example, get BIB 123 info:

*curl -X GET http://localhost:5000/getcompetitor/123*

{
  "bib": "123",
  "first_name": "Ellen",
  "last_name": "Ripley",
  "gender": "female",
  "country": "USA",
  "category": "women40"
}

Example, get BIB 123 timing data:

*curl -X GET http://localhost:5000/gettimes/123*

{"finish":"13:00:00:000","split1":"00:00:00:000","split2":"00:00:00:000","start":"12:15:00:000"}


### Testing

Robot frame work test implementation started. See *.robot files for test

Manual sanity tests (via curl): [ManualTestsInfo.txt](./ManualTestsInfo.txt)




# Setup
1) Start docker: *docker-compose up*

2) Start Flask (Rest API server): *python3 rest_flask_config.py*

Running in *http://localhost:5000*

Both are logging, Flask extensively related server operations.


# REST API

[REST_API_DOC.txt](./REST_API_DOC.txt)


# Ranking the competitors

As Redis does not offfer SQL type operations. Small demo script was written to create race data
(competitors and results)

When Redis and Flask are running, create a race: 
*python3 test_scripts/create_race.py* 

*python3 test_scripts/men30_results.py*

Results:

All competitor BIB numbers:['103', '104', '201', '203', '105', '202', '102', '205', '204', '101']


All men30 competitors:[{'bib': '103', 'first_name': 'Jari', 'last_name': 'Korhonen', 'gender': 'male', 'country': 'Finland', 'category': 'men30'}, {'bib': '104', 'first_name': 'Pekka', 'last_name': 'Lahtinen', 'gender': 'male', 'country': 'Finland', 'category': 'men30'}, {'bib': '105', 'first_name': 'Antti', 'last_name': 'Nieminen', 'gender': 'male', 'country': 'Finland', 'category': 'men30'}, {'bib': '102', 'first_name': 'Mikko', 'last_name': 'Virtanen', 'gender': 'male', 'country': 'Finland', 'category': 'men30'}, {'bib': '101', 'first_name': 'Matti', 'last_name': 'Meikäläinen', 'gender': 'male', 'country': 'Finland', 'category': 'men30'}]


men30 bib_numbers:['103', '104', '105', '102', '101']


--------- Sorted m30 result, best first -------------

Bib: 105, Name: Antti Nieminen, Finish Time: 09:30:00:000

Bib: 101, Name: Matti Meikäläinen, Finish Time: 09:30:00:000

Bib: 102, Name: Mikko Virtanen, Finish Time: 09:35:00:000

Bib: 103, Name: Jari Korhonen, Finish Time: 09:40:00:000

Bib: 104, Name: Pekka Lahtinen, Finish Time: 09:45:00:000


In reality one should create commandline tools to fetch result list in categoryX,
all competitors in country X , sorted by categoriess and results etc etc




## Access redis cli
docker exec -it my_redis redis-cli

OR

redis-cli -h <hostname> -p <port>
redis-cli -h localhost -p 6379

Now Redis  command line usage can be done

NOTE: Via cli one can delete and alter key data so that REST API can get confused
and raports data error

### Redis is-it-alive test 

docker exec -it my_redis redis-cli ping
--> PONG









