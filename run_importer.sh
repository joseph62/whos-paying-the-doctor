#! /bin/bash
docker run -it -e IMPORT_TYPE=full -e IMPORT_LIMIT=100000 --network payments payments-importer