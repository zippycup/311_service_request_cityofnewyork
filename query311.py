#!/bin/python

import datetime as dt
import os
import pandas as pd
from config import *

def main():

    tp = pd.read_csv(csv_url, iterator=True, chunksize=1000)
    df = pd.concat(tp, ignore_index=True)

    df_populate_by_zipcode = pd.read_csv(census_population_by_zipcode)

    df_unique_zipcode = df['Incident Zip'].unique()

    df_top_zipcode = (df_populate_by_zipcode[df_populate_by_zipcode['Zip Code ZCTA']
                     .isin(df_unique_zipcode)]
                     .sort_values(census_population_column,ascending=False)
                     .head(top_zipcode))

    df_complaint = (df.groupby(['Complaint Type'])
                   .size()
                   .sort_values(ascending=False)
                   .head(top_complaints))

    df['Created Date'] = pd.to_datetime(df['Created Date'])
    df_yearly = df[df['Created Date'].dt.year == year ]

    df_yearly_with_top_complaints_borough = (df_yearly[df_yearly['Complaint Type']
                                             .isin(df_complaint.index)]
                                             .groupby(['Borough', 'Complaint Type'])
                                             .size())

    print("\nConsider only the %s most common overall complaint types. "
           "For each borough, how many of each of those %s types were there in %s?"
           % (top_complaints, top_complaints, year))

    print(df_yearly_with_top_complaints_borough)

    df_yearly_with_top_complaints_zipcode = (df_yearly[df_yearly['Complaint Type'].isin(df_complaint.index)
                                             & df_yearly['Incident Zip']
                                               .isin(df_top_zipcode['Zip Code ZCTA'])]
                                               .groupby(['Incident Zip', 'Complaint Type'])
                                               .size())

    print("\nConsider only the %s most common overall complaint types. "
          "For the %s most populous zip codes, how many of each of those %s types were there in %s?"
          % (top_complaints, top_complaints, top_complaints, year))

    print(df_yearly_with_top_complaints_zipcode)

    s_yearly_complaints_by_borough = (df_yearly[df_yearly['Borough'] != 'Unspecified']
                                     .groupby(['Borough'])
                                     .size())

    df_yearly_complaints_by_borough = pd.DataFrame({'Borough':s_yearly_complaints_by_borough.index, 
                                                    'Complaints':s_yearly_complaints_by_borough.values})

    df_merged = pd.merge(df_yearly, df_populate_by_zipcode, left_on='Incident Zip', right_on='Zip Code ZCTA')

    df_sorted = (df_merged[df_merged['Borough'] != 'Unspecified']
                 .sort_values(['Borough',
                               'Incident Zip',
                               census_population_column],
                               ascending=False))

    first = df_sorted.groupby('Incident Zip').first().reset_index()

    df_population_by_borough = (first[['Borough', census_population_column]]
                                .groupby(['Borough'], as_index=False).sum())

    df_complaint_index = (pd.merge(df_yearly_complaints_by_borough,
                                   df_population_by_borough,
                                   on = 'Borough'))

    df_complaint_index['Complaint_index'] = (df_complaint_index['Complaints']
                                             .div(df_complaint_index[census_population_column].values))

    print("\nConsidering all complaint types. "
          "Which boroughs are the biggest 'complainers' "
          "relative to the size of the population in %s?"
          % (year))

    print(df_complaint_index[['Borough', 'Complaint_index']]
         .sort_values('Complaint_index',ascending=False))


if __name__ == "__main__":

  main()
