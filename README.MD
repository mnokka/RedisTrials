
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









