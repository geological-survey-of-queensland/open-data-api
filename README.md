# GSQ Open Data Portal API Guide

The open data portal provides an API for developers who want to write code that interacts with the open data portal.

CKAN’s Action API is an RPC-style API that exposes all of CKAN’s core features to API clients. All of a CKAN website’s core functionality (everything you can do with the web interface and more) can be used by external code that calls the CKAN API. See the user guide at: https://docs.ckan.org/en/2.8/api/

## Making an API request
To call the CKAN API, post a JSON dictionary in an HTTP POST request to the CKAN API URL https://geoscience.data.qld.gov.au/api/3/action/

The parameters for the API function should be given in the JSON dictionary. CKAN will also return its response in a JSON dictionary.

## Example queries
https://geoscience.data.qld.gov.au/api/3/action/package_list

https://geoscience.data.qld.gov.au/api/3/action/recently_changed_packages_activity_list

# Using Python 

HTTP API requests can be made using Python’s standard urllib2 module.

````
#!/usr/bin/env python
import requests
import json
import urllib

# Make the HTTP request
ckan = 'https://geoscience.data.qld.gov.au/api/action/'
uri = ckan + 'package_search?q=geochemistry'
response = requests.request("POST", uri)
response.json()
````

# Data elements

All datasets in the Open Data Portal are defined by structured metadata. Use these elements for more precise queries.

|Element|Description|Vocabulary|
|---|---|---|
|	dataset_type|The top-level dataset category|electrical, electromagnetic, gravity, gravity-gradiometry, magnetic, magnetotelluric, radiometric, seismic, spectral, report, geochemistry, borehole, map collection|
|	extra:theme|Broad dataset thematic description|[GSQ Dataset themes](https://vocabs.gsq.digital/vocabulary/gsq-dataset-theme)|
|	title|Title of the dataset||
|	name|URL of the dataset persistent identifier|[Read here](https://github.com/geological-survey-of-queensland/persistent-identifiers)|
|	extra:identifier|Dataset persistent identifier|[Read here](https://github.com/geological-survey-of-queensland/persistent-identifiers)|
|	alias|Borehole alias (Borehole dataset only)||
|	notes|Description or abstract of the dataset||
|	georesource_report_type|Georesource report type (Reports only)|[Georesource report](http://vocabs.gsq.digital/vocabulary/georesource-report)|
|	resource_authority_permit|Resource authority identifier (not used in Geochemistry or Map Collection)||
|	owner|Report owner (Report dataset only)|[GSQ Agent Roles](http://vocabs.gsq.digital/vocabulary/gsq-roles)|
|	was_generated_by|The survey that yielded the data (Report datasets only)||
|	earth_science_data_category|Reports and map collections only)|[Earth Science Data Category](http://vocabs.gsq.digital/vocabulary/earth-science-data-category)|
|	commodity|Report dataset only|[Geoscience commodities](http://vocabs.gsq.digital/vocabulary/geo-commodities)|
|	geologic_feature|Geological feature of interest (Report dataset and Dataset only)|[Geologic Feature Types](https://vocabs.gsq.digital/vocabulary/geofeatures)|
|	geoadmin_feature|Feature of interest (Geochemistry dataset - Block name)|[GeoAdmin Feature](https://vocabs.gsq.digital/vocabulary/geoadminfeatures)|
|	borehole_purpose|Borehole datasets only|[Borehole purpose](http://vocabs.gsq.digital/vocabulary/borehole-purpose)
|	borehole_sub_purpose|Borehole datasets only|[Borehole sub-purpose](http://vocabs.gsq.digital/vocabulary/borehole-sub-purpose)|
|	borehole_class|Borehole datasets only|[Borehole class](http://linked.data.gov.au/def/resource-project-lifecycle/borehole-class)|
|	rig_release_date|Borehole datasets only||
|	operator|Borehole and Survey datasets||
|	contractor|Survey datasets||
|	job_number|Survey datasets||
|	survey_method|Survey datasets|[Sampling method](https://vocabs.gsq.digital/vocabulary/sampling-method)|
|	observation_method||[Observation method](https://vocabs.gsq.digital/vocabulary/geological-observation-method)|
|	observation_instrument|Used in all Survey datasets||
|	survey_resolution|Survey interval	in metres (not used in Seismic surveys)||
|	survey_lines|Electrical, magnetic and seismic surveys||
|	status|Satus (Surveys and Borehole dataset only)|[Borehole status](http://linked.data.gov.au/def/site-status/borehole-status)|
|	dataset_start_date|Temporal start date||
|	dataset_completion_date|Temporal end date||
|	GeoJSONextent	|Detailed spatial extents of the dataset in GeoJSON||
|	spatial	|Bounding box in GeoJSON||
|	extra:access_rights	|Data access rights|[Data access rights](http://vocabs.gsq.digital/vocabulary/data-access-rights)|
|	open_file_date|Date dataset became open data||
|	resource_fields.url|Resource URL||
|	resource_fields.name|Resource name||
|	resource_fields.resource:description|Resource description||
|	resource_fields.resource:format|File format||
|	resource_fields.resource:size|Byte size||


> **Note:** On early CKAN versions, datasets were called “packages” and this name has stuck in some places, specially internally and on API calls. Package has exactly the same meaning as "dataset".

## License

This code repository's content are licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/), the deed of which is stored in this repository here: [LICENSE](LICENSE).

## Contacts

*System owner*:  
**Geological Survey of Quensland**  
Department of Natural Resources, Mines and Energy  
Queensland, Australia  
<GSQOpenData@dnrme.qld.gov.au>  

*Author*:  
**David Crosswell**  
Enterprise Architect  
Cross-Lateral  
<https://crosslateral.com.au>
