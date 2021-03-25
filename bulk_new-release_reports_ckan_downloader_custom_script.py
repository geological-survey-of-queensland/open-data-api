# -*- coding: utf-8 -*-
"""
Python3 script
Created on Thu Mar 25 8:27:18 2021
Original Author: Eric McCowan (November 2020)

Modified/customised by Kate Wathen-Dunn <Kate.WathenDunn@resources.qld.gov.au>

This is a customised python ckan_downloader script created for the public
to download all the 20655 reports released as a bulk batch of open-file
reports on the 29th March 2021, via GSQ's Open Data Portal API.

GSQ has also prepared a customised CSV file containing the PID of the reports
of interest for use with this script.

You will need to have the CSV in the same directory as this python script,
and this directory is also where the reports will be downloaded to.

This script will create a new directory to hold the downloaded reports,
and will download all resources associated with the reports.

"""

import csv
import os
import requests
from urllib import parse
import json
from pathlib import Path

CSV_FILE = '2021-03-29_GSQ_bulk_report_release_contents.csv'
CKAN_URL = 'https://geoscience.data.qld.gov.au/api/action/'
DATA_DIR = 'downloaded_bulk-release_reports_2021-03-29'
ID_FIELD = 'report_pid'

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
            print('Starting report {}: {}'.format(dataset, row[ID_FIELD]))

            # Make an API call to the Data Portal for the dataset details
            response = requests.get(CKAN_URL + 'package_show', dict(id=dataset))

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

        print('\n')
        print('Download of the new release open-file reports batch from GSQ is complete')