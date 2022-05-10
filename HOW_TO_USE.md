# How to Use

## Prerequisites
Docker and Docker Compose plugin: https://docs.docker.com/get-docker/

## Setup Instructions
1) Open a terminal and navigate to the project root directory
2) Execute `docker compose up -d` -- This will build and bring up the search service, backend, and frontend containers
3) Execute `build_importer.sh` -- This will create the image for the data ingest logic
4) Execute `run_importer.sh` -- This will start importing data into the search service, If a ConnectionError is thrown you may need to wait ten seconds and run the script again
5) Open a browser and navigate to the search page at http://localhost:3000
6) When you are down navigate back to the project root and execute `docker compose down` to shutdown all containers

## Notes
The importer script is set to ingest a small subset of the data for a quick out of the box experience. Adjusting the value of `IMPORT_LIMIT` in the `run_importer.sh` script will change how many records are imported from the source data.