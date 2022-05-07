#! /bin/bash

curl -X PUT "localhost:9200/general-payment" -u 'elastic:payments' -H 'Content-Type: application/json' -d'
{
  "settings": {},
  "mappings": {
    "properties": {
      "Record_ID": { "type": "keyword" },
      "all": { "type": "search_as_you_type" }
    }
  }
}
'

