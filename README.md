# GSQ Open Data Portal API Guide

## Bulk Download of New Release Reports, March 2021
With the Queensland Government's recent changes to the way confidentiality applies to reports, the Geological Survey of Queensland now has the opportunity to release a range of reports which were previously embargoed to the public. For those who want to access and download all 20000+ reports in one go, we offer a customised python script and the required accompanying CSV file. These two files are available on this page, in the files listed above. You will need both to download the reports in bulk. Instructions are included within the python script, and more information on using our Open Data Portal API is available below. 

## API User Guide
The open data portal provides an API for developers who want to write code that interacts with the open data portal.

CKAN’s Action API is an RPC-style API that exposes all of CKAN’s core features to API clients. All of a CKAN website’s core functionality (everything you can do with the web interface and more) can be used by external code that calls the CKAN API. See the user guide at: <https://docs.ckan.org/en/2.9/api/> for an overview and <https://docs.ckan.org/en/2.9/api/#api-guide> for more specific instructions.

## Datasets vs Resources

Data is published in units called a dataset - a parcel of data. For example, it could be a seismic survey dataset or a geochemical dataset for a Block.

When users search for data, the search results they see will be individual datasets.

A dataset contains two things:

* **Information** or **metadata** about the data. For example, the title, description, date, etc.
* **Resources** which hold the data itself. A resource can be CSV or Excel, XML, PDF, image file, linked data in RDF format, etc. A dataset can contain any number of resources.

> **Note:** On early CKAN versions, datasets were called “packages” and this name has stuck in some places, specially internally and on API calls. Package has exactly the same meaning as "dataset".

## Making an API request

An API call has three parts; the API address, the action requested and any filters on the data to be returned.

The address for the GSQ's Open Data Portal API is <https://geoscience.data.qld.gov.au/api/3/action/> 

The action requested can be one of several types, usually 'package_search' or 'package_show', see <https://docs.ckan.org/en/tracking-fixes/api.html> for more options.

The filters possible are many and varied, and are described below in the 'data elements' section. Multiple filters can be used in conjunction to really narrow down on your search results. Filters often start with 'q?=' or 'fq?=' and multiple filters can be joined using the '+' symbol in your query.

The API call can be typed directly into your browser or used in a script. 
If using in your browser, add a JSON Extension to your browser to make the returned data easier to read.

From a script, to call the CKAN API, post a JSON dictionary in an HTTP GET or POST request to the CKAN API URL  
<https://geoscience.data.qld.gov.au/api/3/action/>

The parameters for the API function should be given in the JSON dictionary. 
An example using python code: 

    response = requests.get('https://geoscience.data.qld.gov.au/api/3/action/' + 'package_search',
                   params={
                       'ext_bbox':[148.7, -26.6, 148.9, -26.5],
                       'fq':[
                           'type:report',
                           'earth_science_data_category:geochemistry'
                       ]
                   })
                   
CKAN will also return its response in a JSON dictionary. CKAN always tries to respond with a 200 status code, so in case of failure the 'success' flag in the response should be checked. 

## Example queries

Search for a list of contents
<https://geoscience.data.qld.gov.au/api/3/action/package_list>

Search for a specific seismic survey
<https://geoscience.data.qld.gov.au/api/3/action/package_show?id=ss095544>

Search for new datasets and changes to existing data
<https://geoscience.data.qld.gov.au/api/3/action/recently_changed_packages_activity_list>

Search for all Petroleum Well Completion reports
<https://geoscience.data.qld.gov.au/api/3/action/package_search?fq=+type:report%20+vocab_commodity:*petroleum%20+georesource_report_type:*well-completion-report>

Search for all datasets about boreholes
<https://geoscience.data.qld.gov.au/api/3/action/package_search?q=type:borehole> 

Show a specific report
<https://geoscience.data.qld.gov.au/api/3/action/package_show?q=type:report&id=cr072299>

Search for all mineral permit final reports that became open file since beginning of November 2021
<https://geoscience.data.qld.gov.au/api/3/action/package_search?fq=+georesource_report_type:*permit-report-final+open_file_date:[2021-11-01T00:00:00Z%20TO%20NOW]>



## Using Python

HTTP API requests can be made using Python’s standard `urllib` module and the `requests` library. Note that there is a hard limit of 1000 results returned, so an iterator is needed to fetch more results than that.

**[Requests](https://requests.readthedocs.io/en/master/)** allows you to send HTTP requests easily. There’s no need to manually add query strings to your URLs, or to form-encode your POST data. Keep-alive and HTTP connection pooling are 100% automatic, thanks to [urllib3](https://urllib3.readthedocs.io/en/latest/).

### Dataset search query

````python
import requests
import json

# set the API endpoint
api = 'https://geoscience.data.qld.gov.au/api/action/'
# construct our query
query = api + 'package_search?q=quamby'
# make the get request and store it in the response object
response = requests.get(query)
# view the payload as JSON
json_response = response.json()
print(json_response)

# print the GeoJSON for the results
for dataset in json_response['result']['results']:
    print(dataset.get('GeoJSONextent'))
# {"type":"Polygon","coordinates":[[[140.217847053169,-20.0651426032713],[140.217846866281,-20.0818094534046],[140.217846679393,-20.098476305538],[140.217846494505,-20.1151431576712],[140.217846308617,-20.1318100088045],[140.20117986795,-20.1318102200127],[140.201179682062,-20.1484770721459],[140.184513241396,-20.1484772833552],[140.18451305651,-20.1651441374885],[140.184512871624,-20.1818109906216],[140.184512686738,-20.1984778437548],[140.184512502851,-20.2151446978879],[140.184512318964,-20.2318115510211],[140.201178757624,-20.2318113368118],[140.201178572735,-20.2484781899449],[140.201178390847,-20.265145043078],[140.201178208958,-20.2818118962111],[140.201178028069,-20.2984787493441],[140.184511590415,-20.2984789665533],[140.184511408527,-20.3151458196863],[140.184511227638,-20.3318126738193],[140.18451104575,-20.3484795289523],[140.184510864861,-20.3651463820852],[140.184510683973,-20.3818132362181],[140.184510502084,-20.398480089351],[140.184510219194,-20.4151469904839],[140.184509936305,-20.4318138906168],[140.201176401949,-20.4318136554078],[140.217842867592,-20.4318134202],[140.234509334236,-20.4318131849934],[140.25117579888,-20.4318129497879],[140.267842265524,-20.4318127145836],[140.284508731169,-20.4318124793805],[140.301175196813,-20.4318122431786],[140.317841659457,-20.4318120809779],[140.317841839357,-20.4151452358448],[140.317842020257,-20.3984783917118],[140.317842205157,-20.3818115465788],[140.317842390056,-20.3651447014456],[140.317842576955,-20.3484778563125],[140.317842761854,-20.3318110101794],[140.317842946753,-20.3151441640463],[140.317843132652,-20.2984773189131],[140.31784331755,-20.2818104737799],[140.317843502448,-20.2651436286467],[140.30117702579,-20.2651437498476],[140.284510586133,-20.2651439660497],[140.284510403237,-20.2818108161829],[140.284510219342,-20.2984776663161],[140.284510036446,-20.3151445164492],[140.28450985255,-20.3318113665823],[140.267843414897,-20.3318115837855],[140.267843232003,-20.3484784349186],[140.251176794352,-20.348478653123],[140.251176612458,-20.365145505256],[140.251176429564,-20.381812356389],[140.234509992916,-20.3818125765945],[140.234509810023,-20.3984794277275],[140.217843374376,-20.3984796479342],[140.217843556268,-20.3818127958012],[140.21784373916,-20.3651459436682],[140.217843920051,-20.3484790915352],[140.217844101942,-20.3318122384023],[140.217844284833,-20.3151453852692],[140.234510722486,-20.3151451680625],[140.234510904378,-20.2984783169294],[140.234511087269,-20.2818114637963],[140.234511270161,-20.2651446126632],[140.234511451052,-20.24847776053],[140.234511637943,-20.2318109083969],[140.234511822834,-20.2151440572637],[140.234512008724,-20.1984772051305],[140.234512194615,-20.1818103539973],[140.234512379505,-20.1651435028641],[140.25117882117,-20.1651432906583],[140.251179007062,-20.148476440525],[140.251179192953,-20.1318095883917],[140.251179378844,-20.1151427382584],[140.251179564734,-20.098475887125],[140.251179752625,-20.0818090379917],[140.251179940515,-20.0651421878583],[140.234513496842,-20.0651423950642],[140.217847053169,-20.0651426032713]]]}
# {"type":"Polygon","coordinates":[[[140.217847053169,-20.0651426032713],[140.217846866281,-20.0818094534046],[140.217846679393,-20.098476305538],[140.217846494505,-20.1151431576712],[140.217846308617,-20.1318100088045],[140.20117986795,-20.1318102200127],[140.201179682062,-20.1484770721459],[140.184513241396,-20.1484772833552],[140.18451305651,-20.1651441374885],[140.184512871624,-20.1818109906216],[140.184512686738,-20.1984778437548],[140.184512502851,-20.2151446978879],[140.184512318964,-20.2318115510211],[140.201178757624,-20.2318113368118],[140.201178572735,-20.2484781899449],[140.201178390847,-20.265145043078],[140.201178208958,-20.2818118962111],[140.201178028069,-20.2984787493441],[140.184511590415,-20.2984789665533],[140.184511408527,-20.3151458196863],[140.184511227638,-20.3318126738193],[140.18451104575,-20.3484795289523],[140.184510864861,-20.3651463820852],[140.184510683973,-20.3818132362181],[140.184510502084,-20.398480089351],[140.184510219194,-20.4151469904839],[140.184509936305,-20.4318138906168],[140.201176401949,-20.4318136554078],[140.217842867592,-20.4318134202],[140.234509334236,-20.4318131849934],[140.25117579888,-20.4318129497879],[140.267842265524,-20.4318127145836],[140.284508731169,-20.4318124793805],[140.301175196813,-20.4318122431786],[140.317841659457,-20.4318120809779],[140.317841839357,-20.4151452358448],[140.317842020257,-20.3984783917118],[140.317842205157,-20.3818115465788],[140.317842390056,-20.3651447014456],[140.317842576955,-20.3484778563125],[140.317842761854,-20.3318110101794],[140.317842946753,-20.3151441640463],[140.317843132652,-20.2984773189131],[140.31784331755,-20.2818104737799],[140.317843502448,-20.2651436286467],[140.30117702579,-20.2651437498476],[140.284510586133,-20.2651439660497],[140.284510403237,-20.2818108161829],[140.284510219342,-20.2984776663161],[140.284510036446,-20.3151445164492],[140.28450985255,-20.3318113665823],[140.267843414897,-20.3318115837855],[140.267843232003,-20.3484784349186],[140.251176794352,-20.348478653123],[140.251176612458,-20.365145505256],[140.251176429564,-20.381812356389],[140.234509992916,-20.3818125765945],[140.234509810023,-20.3984794277275],[140.217843374376,-20.3984796479342],[140.217843556268,-20.3818127958012],[140.21784373916,-20.3651459436682],[140.217843920051,-20.3484790915352],[140.217844101942,-20.3318122384023],[140.217844284833,-20.3151453852692],[140.234510722486,-20.3151451680625],[140.234510904378,-20.2984783169294],[140.234511087269,-20.2818114637963],[140.234511270161,-20.2651446126632],[140.234511451052,-20.24847776053],[140.234511637943,-20.2318109083969],[140.234511822834,-20.2151440572637],[140.234512008724,-20.1984772051305],[140.234512194615,-20.1818103539973],[140.234512379505,-20.1651435028641],[140.25117882117,-20.1651432906583],[140.251179007062,-20.148476440525],[140.251179192953,-20.1318095883917],[140.251179378844,-20.1151427382584],[140.251179564734,-20.098475887125],[140.251179752625,-20.0818090379917],[140.251179940515,-20.0651421878583],[140.234513496842,-20.0651423950642],[140.217847053169,-20.0651426032713]]]}
# {"type":"MultiPolygon","coordinates":[[[[140.217843556268,-20.3818127958012],[140.217843374376,-20.3984796479342],[140.217843121485,-20.4151465340671],[140.217842867592,-20.4318134202],[140.2178426147,-20.4484803053329],[140.217842360807,-20.4651471914658],[140.234508857449,-20.4651469422591],[140.25117535209,-20.4651466920538],[140.251175128195,-20.4818135621867],[140.251174905299,-20.4984804333195],[140.251174681403,-20.5151473044523],[140.251174457507,-20.5318141755852],[140.267841013143,-20.531813896381],[140.28450756878,-20.531813616178],[140.301174122416,-20.5318133379762],[140.301174301316,-20.5151464888433],[140.301174480216,-20.4984796397105],[140.301174660115,-20.4818127905775],[140.301174839015,-20.4651459414446],[140.301175017914,-20.4484790923116],[140.301175196813,-20.4318122431786],[140.301175376712,-20.4151453950456],[140.30117555561,-20.3984785459126],[140.301175738508,-20.3818116967796],[140.28450930186,-20.3818119169815],[140.267842865212,-20.3818121361847],[140.251176429564,-20.381812356389],[140.234509992916,-20.3818125765945],[140.217843556268,-20.3818127958012]]],[[[139.784513520744,-20.2984850839258],[139.784513374888,-20.3151519680583],[139.784513230032,-20.3318188521908],[139.801179882681,-20.3318185629535],[139.81784653633,-20.3318182737173],[139.834513189979,-20.3318179844823],[139.834513036119,-20.3484848766148],[139.834512882258,-20.3651517687473],[139.834512818902,-20.3720484118022],[139.834512728397,-20.3818186618799],[139.834512575536,-20.3984855530123],[139.834512487674,-20.4151524341448],[139.834512400813,-20.4318193132773],[139.834512313951,-20.4484861934097],[139.834512227089,-20.465153073542],[139.851178857727,-20.4651527963084],[139.867845489366,-20.4651525480759],[139.884512121005,-20.4651522998446],[139.901178751644,-20.4651520526145],[139.901178868512,-20.448485167482],[139.901178984379,-20.4318182833495],[139.901179100246,-20.415151398217],[139.901179217113,-20.3984845150844],[139.901179352979,-20.3818176269519],[139.901179489846,-20.3651507398193],[139.901179625712,-20.3484838516867],[139.901179762577,-20.3318169645541],[139.901179898443,-20.3151500774214],[139.901180035309,-20.2984831892887],[139.884513408656,-20.2984834275191],[139.867846784004,-20.2984836667506],[139.851180157352,-20.2984839049832],[139.8345134987,-20.2984841992171],[139.817846838048,-20.2984844944521],[139.801180179396,-20.2984847886884],[139.784513520744,-20.2984850839258]]]]}
# ...
````

### Dataset details and resources with [package_show](https://docs.ckan.org/en/2.9/api/#ckan.logic.action.get.package_show)

````python
# Tip: The dataset ID can be found by searching or accessed in the URI
# Example dataset URI https://geoscience.data.qld.gov.au/report/cr119416
response = requests.get(api + 'package_show', 
                             params=dict(
                                 id='cr119416'
                             ))
for resource in response.json()['result']['resources']:
    print(resource['resource:format'], resource['name'], resource['url'], sep=', ')
# PDF, BODY OF REPORT, https://gsq-prod-ckan-horizon-public.s3-ap-southeast-2.amazonaws.com/Report/119416/Document/1254522/cr_119416_1.pdf
# PDF, APPENDIX 1 - NWQ PROTEROZOIC TIME-SPACE CHART 2018, https://gsq-prod-ckan-horizon-public.s3-ap-southeast-2.amazonaws.com/Report/119416/Document/1254523/cr_119416_2.pdf
# CSV, APPENDIX 2 - 2020_02_28 DEPTH TO BASEMENT DATABASE, https://gsq-prod-ckan-horizon-public.s3-ap-southeast-2.amazonaws.com/Report/119416/Document/1254524/cr_119416_3.csv
# CSV, APPENDIX 3 - GLOSSARY OF DESCRIPTORS, https://gsq-prod-ckan-horizon-public.s3-ap-southeast-2.amazonaws.com/Report/119416/Document/1254525/cr_119416_4.csv
# ZIP, APPENDIX 4 - DOMAIN MAP GIS PACKAGE, https://geoscience.data.qld.gov.au/dataset/a25f3b2a-1e1d-4ff1-b8e5-9af811df51e8/resource/854b0405-5830-48bc-bc62-4a9e09f66618/download/domain-map-of-northwest-queensland.zip
````

### Search reports by geospatial bounding box

Note: To search by complex geometry, please use [GeoResGlobe](https://georesglobe.information.qld.gov.au/) or parse the GeoJSONextent attribute of downloaded responses.

````python
# Note: the dataset search page has an interactive map tool that can generate coordinates
bbox = [148.7, -26.6, 148.9, -26.5]

# Search using bounding box provided, and filter the query (fq) to reports only
response = requests.get(api + 'package_search',
                   params={
                       'ext_bbox': bbox,
                       'fq':[
                           'type:report'
                       ]
                   })
# Show dataset count
print(response.json()['result']['count'])
# 2016

# To check the first result is a report
response.json()['result']['results'][0]['type'] == 'report'
# True
````

## Data elements

All datasets in the Open Data Portal are defined by structured metadata. Use these elements for more precise queries.

|Element|Description|Vocabulary|
|---|---|---|
|type|The top-level dataset category|electrical, electromagnetic, gravity, gravity-gradiometry, magnetic, magnetotelluric, radiometric, seismic, spectral, report, geochemistry, borehole, map collection|
|extra:theme|Broad dataset thematic description|See [GSQ Dataset themes](https://vocabs.gsq.digital/vocabulary/gsq-dataset-theme)|
|title|Title of the dataset||
|name|URL of the dataset persistent identifier|[Read here](https://github.com/geological-survey-of-queensland/persistent-identifiers)|
|extra:identifier|Dataset persistent identifier e.g. CR00123|[Read here](https://github.com/geological-survey-of-queensland/persistent-identifiers)|
|alias|Borehole alias|
|notes|Description or abstract of the dataset||
|georesource_report_type|Georesource report type|See [Georesource report](http://vocabs.gsq.digital/vocabulary/georesource-report)|
|resource_authority_permit|Resource authority identifier||
|owner|Report owner|[GSQ Agent Roles](http://vocabs.gsq.digital/vocabulary/gsq-roles)|
|was_generated_by|The survey that yielded the data||
|earth_science_data_category|The field of research for the data|[Earth Science Data Category](http://vocabs.gsq.digital/vocabulary/earth-science-data-category)|
|vocab_commodity|Commodities mentioned in the dataset|[Geoscience commodities](http://vocabs.gsq.digital/vocabulary/geo-commodities)|
|geologic_feature|Geological feature of interest (Report dataset and Dataset only)|[Geologic Feature Types](https://vocabs.gsq.digital/vocabulary/geofeatures)|
|geoadmin_feature|Administrative feature of interest|[GeoAdmin Feature](https://vocabs.gsq.digital/vocabulary/geoadminfeatures)|
|borehole_purpose|Borehole datasets only|[Borehole purpose](http://vocabs.gsq.digital/vocabulary/borehole-purpose)
|borehole_sub_purpose|Borehole datasets only|[Borehole sub-purpose](http://vocabs.gsq.digital/vocabulary/borehole-sub-purpose)|
|borehole_class|Borehole datasets only|[Borehole class](http://linked.data.gov.au/def/resource-project-lifecycle/borehole-class)|
|rig_release_date|Borehole datasets only||
|operator|Borehole and Survey datasets||
|contractor|Survey datasets||
|job_number|Survey datasets||
|survey_method|Survey datasets|[Survey method](https://vocabs.gsq.digital/vocabulary/survey-method)|
|observation_method|Survey observation method|[Observation method](https://vocabs.gsq.digital/vocabulary/geological-observation-method)|
|observation_instrument|Used in all Survey datasets||
|survey_resolution|Survey interval in metres||
|survey_lines|For electrical, magnetic and seismic surveys||
|status|Satus of the survey or borehole|[Borehole status](http://linked.data.gov.au/def/site-status/borehole-status)|
|dataset_start_date|Temporal start date||
|dataset_completion_date|Temporal end date||
|GeoJSONextent|Detailed spatial extents of the dataset in GeoJSON|See [GeoJSON](https://github.com/geological-survey-of-queensland/spatial-coordinate-handling/blob/master/geosjon.md)|
|spatial|Bounding box in GeoJSON|See [GeoJSON](https://github.com/geological-survey-of-queensland/spatial-coordinate-handling/blob/master/geosjon.md)|
|extra:access_rights|Data access rights|See [Data access rights](http://vocabs.gsq.digital/vocabulary/data-access-rights)|
|open_file_date|Date dataset became open data||
|resources.package_id|The id of the dataset that the resource belongs to||
|resources.url|Resource URL||
|resources.name|Resource name||
|resources.resource:description|Resource description||
|resources.resource:format|Resoure file format||
|resources.resource:size|Resource byte size||

## Data elements by dataset type

### report

GeoJSONextent, vocab_commodity, dataset_completion_date, dataset_start_date, earth_science_data_category, extra:access_rights, extra:identifier, georesource_report_type, license_id, name, notes, open_file_date, owner, owner_org, private, resource_authority_permit, spatial, title, type, was_generated_by

### borehole

GeoJSONextent, alias, borehole_class, borehole_purpose, borehole_sub_purpose, dataset_start_date, extra:access_rights, extra:identifier, license_id, name, notes, open_file_date, operator, owner_org, private, resource_authority_permit, rig_release_date, spatial, status, title,type

### seismic

GeoJSONextent, contractor, dataset_completion_date, dataset_start_date, extra:access_rights, extra:identifier, license_id, name, notes, observation_instrument, observation_method, open_file_date, operator, owner_org, private, resource_authority_permit, spatial, status, survey_method, title, type

### magnetic

GeoJSONextent, contractor, dataset_completion_date, extra:access_rights, extra:identifier, license_id, name, notes,observation_instrument,observation_method,open_file_date,operator,owner_org,private,resource_authority_permit,spatial,status,survey_method,title,type

### radiometric

GeoJSONextent, contractor, dataset_completion_date, extra:access_rights, extra:identifier, license_id, name, notes, observation_instrument, observation_method, open_file_date, operator, owner_org, private, spatial, status, survey_method, title, type

### electromagnetic

GeoJSONextent, contractor, dataset_completion_date, extra:access_rights, extra:identifier, license_id, name, notes, observation_instrument, observation_method, open_file_date, operator, owner_org, private, resource_authority_permit, spatial, status, survey_method, title, type

### gravity

GeoJSONextent, contractor, dataset_start_date, extra:access_rights, extra:identifier, license_id, name, notes, observation_instrument, observation_method, open_file_date, operator, owner_org, private, resource_authority_permit, spatial, status, survey_method, title, type

### spectral

GeoJSONextent, contractor, extra:access_rights, extra:identifier, license_id, name, notes, observation_instrument, observation_method, open_file_date, operator, owner_org, private, spatial, status, survey_method, title, type

### dataset

GeoJSONextent, dataset_start_date, dataset_end_date, earth_science_data_category, extra:identifier, extra:theme, license_id, name, notes, owner_org, private, spatial, title, type

### gravity-gradiometry

GeoJSONextent, contractor, dataset_completion_date, extra:access_rights, extra:identifier, license_id, name, notes, observation_instrument, observation_method, open_file_date, operator, owner_org, private, resource_authority_permit, spatial, status, survey_method, title, type

### map-collection

GeoJSONextent, dataset_start_date, earth_science_data_category, extra:access_rights, extra:identifier, extra:theme, license_id, map_series, name, notes, open_file_date, owner_org, private, spatial, title, type

### magnetotelluric

GeoJSONextent, contractor, dataset_completion_date, dataset_start_date, extra:identifier, job_number, license_id, name, notes, observation_instrument, observation_method, operator, owner_org, private, spatial, status, survey_method, survey_resolution, title, type

## Leveraging the SOLR search engine

Our CKAN instance uses the SOLR search engine - built on Apache Lucence. You can use the SOLR queries in your API calls.

### Field search

You can search any field by typing the field name followed by a colon ":" and then the term you are looking for. As an example, if you want to search the title and the description field, you can enter:

    title:Cloncurry AND text:"radiometric survey"

or

    title:"Super Isa Basin" AND "well completion report"

Note: Since text is the default field, the field indicator is not required.

### Wildcard Searches

To perform a single character wildcard search use the "?" symbol.

To perform a multiple character wildcard search use the "*" symbol.

The single character wildcard search looks for terms that match that with the single character replaced. For example, to search for "text" or "test" you can use the search: te?t

Multiple character wildcard searches looks for 0 or more characters. For example, to search for test, tests or tester, you can use the search:

    test*

You can also use the wildcard searches in the middle of a term.

    te*t

Note: You cannot use a * or ? symbol as the first character of a search.

### Fuzzy Searches

To do a fuzzy search use the tilde, "~", symbol at the end of a Single word Term. For example to search for a term similar in spelling to "roam" use the fuzzy search:

    roam~

This search will find terms like foam and roams.

### Proximity Searches

Lucene supports finding words are a within a specific distance away. To do a proximity search use the tilde, "~", symbol at the end of a Phrase. For example to search for a "apache" and "jakarta" within 10 words of each other in a document use the search:

    "jakarta apache"~10

### Range Searches

Range Queries allow one to match documents whose field(s) values are between the lower and upper bound specified by the Range Query. Range Queries can be inclusive or exclusive of the upper and lower bounds. Sorting is done lexicographically.

    metadata_modified:[2020-11-01T00:00:00Z TO 2021-11-30T00:00:00Z]

This will find documents whose metadata_modified fields have values between 2020-11-01 and 2020-11-30, inclusive. Note that the time component 'T00:00:00Z' should be included with the date.

Range Queries are not reserved for date fields. You could also use range queries with non-date fields:

    title:{Adavale TO Camooweal}

This will find all documents whose titles are between Aida and Carmen, but not including Aida and Carmen.

Inclusive range queries are denoted by square brackets. Exclusive range queries are denoted by curly brackets.

### Boosting a Term

Lucene provides the relevance level of matching documents based on the terms found. To boost a term use the caret, "^", symbol with a boost factor (a number) at the end of the term you are searching. The higher the boost factor, the more relevant the term will be.

Boosting allows you to control the relevance of a document by boosting its term. For example, if you are searching for

    jakarta apache

and you want the term "jakarta" to be more relevant boost it using the ^ symbol along with the boost factor next to the term. You would type:

    jakarta^4 apache

This will make documents with the term jakarta appear more relevant. You can also boost Phrase Terms as in the example:

    "jakarta apache"^4 "Apache Lucene"

By default, the boost factor is 1. Although the boost factor must be positive, it can be less than 1 (e.g. 0.2)

### Boolean Operators
Boolean operators allow terms to be combined through logic operators. Lucene supports AND, "+", OR, NOT and "-" as Boolean operators(Note: Boolean operators must be ALL CAPS).

The OR operator is the default conjunction operator. This means that if there is no Boolean operator between two terms, the OR operator is used. The OR operator links two terms and finds a matching document if either of the terms exist in a document. This is equivalent to a union using sets. The symbol || can be used in place of the word OR.

To search for documents that contain either "jakarta apache" or just "jakarta" use the query:

    "jakarta apache" jakarta

or

    "jakarta apache" OR jakarta

**AND**

The AND operator matches documents where both terms exist anywhere in the text of a single document. This is equivalent to an intersection using sets. The symbol && can be used in place of the word AND.

To search for documents that contain "jakarta apache" and "Apache Lucene" use the query:

    "jakarta apache" AND "Apache Lucene"

**+**

The "+" or required operator requires that the term after the "+" symbol exist somewhere in a the field of a single document.

To search for documents that must contain "jakarta" and may contain "lucene" use the query:

    +jakarta lucene

**NOT**

The NOT operator excludes documents that contain the term after NOT. This is equivalent to a difference using sets. The symbol ! can be used in place of the word NOT.

To search for documents that contain "jakarta apache" but not "Apache Lucene" use the query:

    "jakarta apache" NOT "Apache Lucene"

Note: The NOT operator cannot be used with just one term. For example, the following search will return no results:

    NOT "jakarta apache"

**-**
The "-" or prohibit operator excludes documents that contain the term after the "-" symbol.

To search for documents that contain "jakarta apache" but not "Apache Lucene" use the query:

    "jakarta apache" -"Apache Lucene"

**Grouping**

Lucene supports using parentheses to group clauses to form sub queries. This can be very useful if you want to control the boolean logic for a query.

To search for either "jakarta" or "apache" and "website" use the query:

    (jakarta OR apache) AND website

This eliminates any confusion and makes sure you that website must exist and either term jakarta or apache may exist.

**Field Grouping**

Lucene supports using parentheses to group multiple clauses to a single field.

To search for a title that contains both the word "geologist" and the phrase "love rocks" use the query:

    title:(+geologist +"love rocks")

**Escaping Special Characters**

Lucene supports escaping special characters that are part of the query syntax. The current list special characters are

    + - && || ! ( ) { } [ ] ^ " ~ * ? : \

To escape these character use the \ before the character. For example to search for (1+1):2 use the query:

    \(1\+1\)\:2

## License

This code repository's content are licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/), the deed of which is stored in this repository here: [LICENSE](LICENSE).

## Contacts

*System owner*:  
**Mark Gordon**,
Geological Survey of Queensland,
Department of Resources,
Brisbane, QLD, Australia,
<mark.gordon@resources.qld.gov.au>  

*Contributors*:  
**Vance Kelly**,
Principal Data Manager,
Geological Survey of Queensland,
Department of Resources,
Brisbane, QLD, Australia,  
<vance.kelly@resources.qld.gov.au>

**Luke Hauck**,
Geoscientist,
Geological Survey of Queensland,
Department of Resources,
Brisbane, QLD, Australia,
<luke.hauck@resources.qld.gov.au>
