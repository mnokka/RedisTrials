curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "bib": "101",
    "first_name": "Matti",
    "last_name": "Meikäläinen",
    "gender": "male",
    "country": "Finland",
    "category": "men30"
  }' \
  http://localhost:5000/competitor

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "bib": "102",
    "first_name": "Mikko",
    "last_name": "Virtanen",
    "gender": "male",
    "country": "Finland",
    "category": "men30"
  }' \
  http://localhost:5000/competitor

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "bib": "103",
    "first_name": "Jari",
    "last_name": "Korhonen",
    "gender": "male",
    "country": "Finland",
    "category": "men30"
  }' \
  http://localhost:5000/competitor

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "bib": "104",
    "first_name": "Pekka",
    "last_name": "Lahtinen",
    "gender": "male",
    "country": "Finland",
    "category": "men30"
  }' \
  http://localhost:5000/competitor

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "bib": "105",
    "first_name": "Antti",
    "last_name": "Nieminen",
    "gender": "male",
    "country": "Finland",
    "category": "men30"
  }' \
  http://localhost:5000/competitor




curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "bib": "201",
    "first_name": "Ellen",
    "last_name": "Ripley",
    "gender": "female",
    "country": "USA",
    "category": "women40"
  }' \
  http://localhost:5000/competitor

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "bib": "202",
    "first_name": "Sarah",
    "last_name": "Connor",
    "gender": "female",
    "country": "USA",
    "category": "women40"
  }' \
  http://localhost:5000/competitor

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "bib": "203",
    "first_name": "Leia",
    "last_name": "Organa",
    "gender": "female",
    "country": "USA",
    "category": "women40"
  }' \
  http://localhost:5000/competitor

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "bib": "204",
    "first_name": "Hermione",
    "last_name": "Granger",
    "gender": "female",
    "country": "UK",
    "category": "women40"
  }' \
  http://localhost:5000/competitor

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "bib": "205",
    "first_name": "Katniss",
    "last_name": "Everdeen",
    "gender": "female",
    "country": "USA",
    "category": "women40"
  }' \
  http://localhost:5000/competitor



curl -X POST http://localhost:5000/settimes \
  -H "Content-Type: application/json" \
  -d '{
    "bib": 101,
    "settimes": {
      "start": "08:00:00:000",
      "split1": "08:30:00:000",
      "split2": "09:00:00:000",
      "finish": "09:30:00:000"
    }
  }'

curl -X POST http://localhost:5000/settimes \
  -H "Content-Type: application/json" \
  -d '{
    "bib": 102,
    "settimes": {
      "start": "08:05:00:000",
      "split1": "08:35:00:000",
      "split2": "09:05:00:000",
      "finish": "09:35:00:000"
    }
  }'

curl -X POST http://localhost:5000/settimes \
  -H "Content-Type: application/json" \
  -d '{
    "bib": 103,
    "settimes": {
      "start": "08:10:00:000",
      "split1": "08:40:00:000",
      "split2": "09:10:00:000",
      "finish": "09:40:00:000"
    }
  }'

curl -X POST http://localhost:5000/settimes \
  -H "Content-Type: application/json" \
  -d '{
    "bib": 104,
    "settimes": {
      "start": "08:15:00:000",
      "split1": "08:45:00:000",
      "split2": "09:15:00:000",
      "finish": "09:45:00:000"
    }
  }'

curl -X POST http://localhost:5000/settimes \
  -H "Content-Type: application/json" \
  -d '{
    "bib": 105,
    "settimes": {
      "start": "08:20:00:000",
      "split1": "08:50:00:000",
      "split2": "09:15:00:000",
      "finish": "09:30:00:000"
    }
  }'




curl -X POST http://localhost:5000/settimes \
  -H "Content-Type: application/json" \
  -d '{
    "bib": 201,
    "settimes": {
      "start": "08:00:00:000",
      "split1": "08:35:00:000",
      "split2": "09:00:00:000",
      "finish": "09:30:00:000"
    }
  }'

curl -X POST http://localhost:5000/settimes \
  -H "Content-Type: application/json" \
  -d '{
    "bib": 202,
    "settimes": {
      "start": "08:00:00:000",
      "split1": "08:35:59:000",
      "split2": "09:05:00:000",
      "finish": "09:32:00:000"
    }
  }'

curl -X POST http://localhost:5000/settimes \
  -H "Content-Type: application/json" \
  -d '{
    "bib": 203,
    "settimes": {
      "start": "08:00:00:000",
      "split1": "08:40:00:000",
      "split2": "09:10:00:000",
      "finish": "09:32:59:100"
    }
  }'

curl -X POST http://localhost:5000/settimes \
  -H "Content-Type: application/json" \
  -d '{
    "bib": 204,
    "settimes": {
      "start": "08:00:00:000",
      "split1": "08:45:00:000",
      "split2": "09:15:00:000",
      "finish": "09:33:00:000"
    }
  }'

curl -X POST http://localhost:5000/settimes \
  -H "Content-Type: application/json" \
  -d '{
    "bib": 205,
    "settimes": {
      "start": "08:00:00:000",
      "split1": "08:50:00:000",
      "split2": "09:15:00:000",
      "finish": "09:30:00:000"
    }
  }'
