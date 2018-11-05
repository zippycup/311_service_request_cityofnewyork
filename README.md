# 311_service_request_cityofnewyork

## Description
Demonstrate the use of NYC OpenData: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9. 
We use python Panda library to make queries from a online csv provided at https://data.cityofnewyork.us/api/views/erm2-nwe9/rows.csv
Data from https://blog.splitwise.com/2013/09/18/the-2010-us-census-population-by-zip-code-totally-free/ to obtain population data to further parse data by zipcode.

## Requirements
- python 2.7 minimum
- python library panda. I recommend install Anaconda which already has panda installed in the default environment. https://conda.io/docs/user-guide/install/index.html

## Run Demo
- git clone or download this repo
- cd [working_directory]
- python query311.py
