# Open Payments Data Notes

## Publication Frequency
There are two publications per year. The first or 'Initial Data Publication' happens on or by June 30 and includes records published. The second publication or 'Refresh Publication' happens _at least_ once anually usually at the beginning of the calendar year.

Program Years are available from 2013 through 2020 currently.

## Payment Types
- General Payments: Transfers of value not related to a research agreement or research protocol
- Research Payments: Transfers of value related to a research agreement or research protocol
- Physician Ownership or Investment Interest Information: Physician ownership or investment interest in a manufacturer, GPO, or with immediate family holding such interest

## Change Types
Records of all payment types include a change type to indicate the status related to previous publications

- `NEW`: submitted during the most recent window and is being published for the first time
- `ADD`: submitted prior to most recent window, but was not eligible for publication until the current window
- `CHANGED`: published previously and has been modified since last publication
- `UNCHANGED`: no change made since prior publication

A separate file includes `DELETED` and `REMOVED` records. This file includes `Record ID`, `Payment Type`, and `Program Year` of previously published records that have been deleted or removed from the system.
The initial publication of a program year will not include such a file. If no records have been removed or deleted the file will not be included.

## Physician Profile Supplement Detail
A file that contains all identifying information for physicians and physician principal investigators who were included in the data

## Data Scale
The number of records per file included in Program Year 2020 (as reference):

|File Name|Number of Rows|Number of Columns|Raw File Size|
|---------|--------------|-----------------|-------------|
|General Payments Details|5,767,202|75|3.2G|
|Research Payments Details|588,942|176|484M|
|Physician Ownership Details|3,238|29|1.5M|
|Deleted and Removed Records Details|18,394|4|666K|

## Data Definitions
The definitions of each record type can be found the appendicies of the CMS provided [pdf about Open Payments](https://www.cms.gov/OpenPayments/Downloads/OpenPaymentsDataDictionary.pdf)

Note the years 2014 and 2015 have separate appendicies as their model is slightly different

|Record Type|Appendix Letter|Page|
|-----------|---------------|----|
|General Payments Detail               |B|22|
|Research Payments Detail              |D|48|
|Physician Ownership Information Detail|F|112|
|Deleted and Removed Records           |G|118|
|Physician Profile Supplement          |H|119|

## Questions


How many Previous Program Years should be included in the dataset?

