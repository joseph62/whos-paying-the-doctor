# System Notes
A sketch of what might be needed to meet the needs outlined in the problem statement. This includes components, questions, and potential technology list.

## Problem Statement
Any time a doctor accepts things like lunches, gifts, etc. that cost greater than $10 dollars this has to be reported. Below is the site that contains all the data. There is an API or you can download the data. Either method to get the data is fine:

https://openpaymentsdata.cms.gov/about/api
https://www.cms.gov/OpenPayments/Data/Dataset-Downloads

Use this data to create a small site that imports the data. Make sure this script can run over and over again to get the most recent updates. Build a search tool with a typeahead that returns all relevant data. When search results are returned, build an export to Excel feature. Make sure that this outputs to an XLS file.

## High Level Components
### Data Source
- Open Payments API
    - How many years of data should be considered?
### Database
- Stores data from source
- Tracks metadata regarding import process (last run time, )
### Search
- Indexed data from source/database
### Backend
- Import 
    - Should run on a schedule
        - How frequently should the data be updated?
            - Less frequently if the operation requires a full data pull
            - Delta import process could be more real time like every hour
        - Does the import process also need to be manually started?
    - Should handle record updates and deletes as well as newly created records (updating backing database and search services)
    - Should only pull updated data since the previous run if possible
- Export
    - Generate XLS file format
    - Large search result behavior
        - Truncate to some arbitrary size?
- Search 
    - Indexing records in a sensible way
        - Things like descriptions and names should be configured to get partial matches
        - Monetary or other Number types able to be filtered by value comparison
    - Pagination
        - Page
        - Page Size
### Frontend
- Search Bar
    - Sends requests as the user types
- Paging
    - Search results appear in pages
    - UI components to go first, previous, next, last
- Export Excel file
    - Begins download of XLS file

## Technologies
### Database
A SQL/NOSQL database technology - PostgreSQL
### Search
A service that provides search functionality - Elasticsearch
### Backend
Something comfortable with excellent library support - Python / FastAPI 
### Frontend
Something I have used at least a little bit - React
### Glue
There are 4 distinct components of this system so there needs to be some way to glue them all together and ease the task of managing it all - Containers and Docker Compose

## Technologies at the end
I found that Elasticsearch was able to easily house the full data for excel export as well as provide search results so I removed any sql database usage. 
### Search & Database
Elasticsearch
### Backend
Python / FastAPI
### Frontend
React / MaterialUI
### Glue
Docker / Docker Compose