"""
This python script provides an example of how bulk reports and datasets can be downloaded directly
from GSQ's Open Data Portal using API calls.
You will need to have prepared a csv file containing the PID of the Reports you want 
to download, here called 'Datasets.csv' (change the variable in the script to suit your CSV file)

Author: Eric McCowan
November 2020
"""

import csv
import os
import requests
from urllib import parse
import json
from pathlib import Path

CSV_FILE = 'Datasets.csv'
CKAN_URL = 'https://geoscience.data.qld.gov.au/api/action/'
DATA_DIR = 'downloads'
ID_FIELD = 'PID'

if __name__ == '__main__':

    if not os.path.exists(DATA_DIR):
        Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

    # Open CSV file for reading
    with open(CSV_FILE) as csvfile:
        reader = csv.DictReader(csvfile)

        # Iterate through rows
        for row in reader:

            # Get the dataset PID
            dataset = row[ID_FIELD]
            print('Starting report {}'.format(dataset))

            # Make an API call to the Data Portal for the dataset details
            response = requests.get(CKAN_URL + 'package_show', dict(id=dataset))
            # print(response.text)

            if response.ok:

                # Transform the response so it contains the details we need
                content = response.json().get('result', {})

                if content.get('num_resources', 0) == 0:
                    print('There are no resources available to download.')
                    continue

                # Make a folder with the name of the dataset for our downloads
                if not os.path.exists(os.path.join(DATA_DIR, dataset)):
                    os.mkdir(os.path.join(DATA_DIR, dataset))

                # This variable will help store names of downloads
                download_metadata = list()

                # Iterate through each resource available
                for resource in content.get('resources', []):
                    # print(resource)
                    # Determine the filename to use for the download
                    filename = ''
                    if resource.get('url'):
                        filename = resource['url']
                        while '%2' in filename:
                            filename = parse.unquote_plus(filename)
                        filename = os.path.basename(filename)

                    else:
                        filename = resource['name']
                        extension = resource['format'].lower()

                        if not filename.lower().endswith(extension):
                            filename = filename + '.' + extension

                    # Determine the download link
                    download_link = ''
                    if resource.get('download_url'):
                        download_link = resource['download_url']
                    elif resource.get('url'):
                        download_link = resource['url']
                    else:
                        print('No available download link.')
                        continue

                    # Download the resource using the new filename to the data directory
                    download_response = requests.get(download_link)

                    if download_response.ok:
                        print('Downloading {} ({}) to {}'.format(
                            resource['name'], download_link, os.path.join(DATA_DIR, dataset, filename)))

                        with open(os.path.join(DATA_DIR, dataset, filename), 'wb') as w:
                            w.write(download_response.content)

                        download_metadata.append(
                            {
                                filename: {
                                    'name': resource['name'],
                                    'description': resource.get('resource:description', resource.get('description', '')),
                                    'download_link': download_link
                                }
                            }
                        )

                    else:
                        print('There was an issue with the download.')

                if download_metadata:
                    with open(os.path.join(DATA_DIR, dataset, 'metadata.json'), 'w') as w:
                        w.write(json.dumps(download_metadata, indent=4))

            else:
                print('There was an issue retrieving the dataset.')
