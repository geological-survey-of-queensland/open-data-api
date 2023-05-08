#!/usr/bin/env python
# coding: utf-8
import requests
import json
from tqdm import tqdm

import pandas as pd
import os

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

#https://geoscience.data.qld.gov.au/api/action/package_search?q=geochem&rows=1000&start=0
#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# set the API endpoint
api = 'https://geoscience.data.qld.gov.au/api/action/'
# construct our query
query = api + 'package_search?q=reports&rows=1000'
# make the get request and store it in the response object
response = requests.get(query, headers=headers)
# view the payload as JSON

if 1 == 1:
    #json_response = response.json()
    json_response = json.loads(response.text)

    #and get a count of results we can retrieve
    total_results = json_response['result']['count']
    print(total_results)
    
    #print(json_response['result']['results'][0])

    #hack without understanding/researching the api too much
    getloop = int(total_results/1000) + 1

    if getloop > 1:
        results_list = []
        for i in range(getloop):
            loopq = query + "&start=" + str(i*1000)
            print(loopq)
            response = requests.get(loopq, headers=headers)
            #json_response = response.json()
            json_response = json.loads(response.text)

            results_list.append(json_response)


result_ids = []
for batch in tqdm(results_list, total=len(results_list) ):
    results = batch['result']['results']
    for r in results:
        rid = r['id']
        rauthor = r['author']
        rspatial = r['spatial']
        rtype = r['type']
        
        if len(r['resources']) > 0:
            part_list = []
            for part in r['resources']:
                #modify the columns here to include what you want
                df = pd.DataFrame([part])
                df['rid'] = rid
                df['rauthor'] = rauthor
                df['rspatial'] = rspatial
                df['type'] = rtype
                part_list.append(df)
                allparts = pd.concat(part_list)
                
            result_ids.append(allparts)

dfDatasets = pd.concat(result_ids)            

dfDatasets.to_csv(r'GSQ_Report_Datasets.csv', index=False)

docx = dfDatasets.loc[dfDatasets['resource:format'] == 'DOCX']
docx.shape

def save_link(book_link, book_name):
    the_book = requests.get(book_link, headers=headers, stream=True)
    with open(book_name, 'wb') as f:
      for chunk in the_book.iter_content(1024 * 1024 * 2):  # 2 MB chunks
        f.write(chunk)

qldir = r'qld'
for index, row in tqdm(docx.iterrows(), total=docx.shape[0]):
    url = row['url']
    #print(url)
    urlist = url.split('/')
    name = urlist[-1]
    save_link(url, os.path.join(qldir,name))
    #break

