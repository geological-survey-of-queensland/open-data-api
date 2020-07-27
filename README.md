# GSQ Open Data Portal API Guide

The open data portal provides an API for developers who want to write code that interacts with the open data portal.

CKAN’s Action API is an RPC-style API that exposes all of CKAN’s core features to API clients. All of a CKAN website’s core functionality (everything you can do with the web interface and more) can be used by external code that calls the CKAN API. See the user guide at:  
<https://docs.ckan.org/en/2.8/api/>

## Datasets vs Resources

Data is published in units called a dataset - a parcel of data. For example, it could be a seismic survey dataset or a geochemical dataset for a Block.

When users search for data, the search results they see will be individual datasets.

A dataset contains two things:

* **Information** or **metadata** about the data. For example, the title, description, date, etc.
* **Resources** which hold the data itself. A resource can be CSV or Excel, XML, PDF, image file, linked data in RDF format, etc. A dataset can contain any number of resources.

> **Note:** On early CKAN versions, datasets were called “packages” and this name has stuck in some places, specially internally and on API calls. Package has exactly the same meaning as "dataset".

## Making an API request

To call the CKAN API, post a JSON dictionary in an HTTP POST request to the CKAN API URL  
<https://geoscience.data.qld.gov.au/api/3/action/>

The parameters for the API function should be given in the JSON dictionary. CKAN will also return its response in a JSON dictionary.

## Example queries

<https://geoscience.data.qld.gov.au/api/3/action/package_list>

<https://geoscience.data.qld.gov.au/api/3/action/package_show?id=95544>

<https://geoscience.data.qld.gov.au/api/3/action/recently_changed_packages_activity_list>

## Using Python

HTTP API requests can be made using Python’s standard urllib module. Note that there is a hard limit of 1000 results returned.

````python
import requests
import json
import urllib

# Make the HTTP request
ckan = 'https://geoscience.data.qld.gov.au/api/action/'
url = ckan + 'package_search?q=quamby'
response = requests.request("POST", url)
response.json()
````

## Data elements

All datasets in the Open Data Portal are defined by structured metadata. Use these elements for more precise queries.

|Element|Description|Vocabulary|
|---|---|---|
|dataset_type|The top-level dataset category|electrical, electromagnetic, gravity, gravity-gradiometry, magnetic, magnetotelluric, radiometric, seismic, spectral, report, geochemistry, borehole, map collection|
|extra:theme|Broad dataset thematic description|[GSQ Dataset themes](https://vocabs.gsq.digital/vocabulary/gsq-dataset-theme)|
|title|Title of the dataset||
|name|URL of the dataset persistent identifier|[Read here](https://github.com/geological-survey-of-queensland/persistent-identifiers)|
|extra:identifier|Dataset persistent identifier|[Read here](https://github.com/geological-survey-of-queensland/persistent-identifiers)|
|alias|Borehole alias (Borehole dataset only)||
|notes|Description or abstract of the dataset||
|georesource_report_type|Georesource report type (Reports only)|[Georesource report](http://vocabs.gsq.digital/vocabulary/georesource-report)|
|resource_authority_permit|Resource authority identifier (not used in Geochemistry or Map Collection)||
|owner|Report owner (Report dataset only)|[GSQ Agent Roles](http://vocabs.gsq.digital/vocabulary/gsq-roles)|
|was_generated_by|The survey that yielded the data (Report datasets only)||
|earth_science_data_category|Reports and map collections only)|[Earth Science Data Category](http://vocabs.gsq.digital/vocabulary/earth-science-data-category)|
|commodity|Report dataset only|[Geoscience commodities](http://vocabs.gsq.digital/vocabulary/geo-commodities)|
|geologic_feature|Geological feature of interest (Report dataset and Dataset only)|[Geologic Feature Types](https://vocabs.gsq.digital/vocabulary/geofeatures)|
|geoadmin_feature|Feature of interest (Geochemistry dataset - Block name)|[GeoAdmin Feature](https://vocabs.gsq.digital/vocabulary/geoadminfeatures)|
|borehole_purpose|Borehole datasets only|[Borehole purpose](http://vocabs.gsq.digital/vocabulary/borehole-purpose)
|borehole_sub_purpose|Borehole datasets only|[Borehole sub-purpose](http://vocabs.gsq.digital/vocabulary/borehole-sub-purpose)|
|borehole_class|Borehole datasets only|[Borehole class](http://linked.data.gov.au/def/resource-project-lifecycle/borehole-class)|
|rig_release_date|Borehole datasets only||
|operator|Borehole and Survey datasets||
|contractor|Survey datasets||
|job_number|Survey datasets||
|survey_method|Survey datasets|[Sampling method](https://vocabs.gsq.digital/vocabulary/sampling-method)|
|observation_method||[Observation method](https://vocabs.gsq.digital/vocabulary/geological-observation-method)|
|observation_instrument|Used in all Survey datasets||
|survey_resolution|Survey interval in metres (not used in Seismic surveys)||
|survey_lines|Electrical, magnetic and seismic surveys||
|status|Satus (Surveys and Borehole dataset only)|[Borehole status](http://linked.data.gov.au/def/site-status/borehole-status)|
|dataset_start_date|Temporal start date||
|dataset_completion_date|Temporal end date||
|GeoJSONextent|Detailed spatial extents of the dataset in GeoJSON||
|spatial|Bounding box in GeoJSON||
|extra:access_rights|Data access rights|[Data access rights](http://vocabs.gsq.digital/vocabulary/data-access-rights)|
|open_file_date|Date dataset became open data||
|resource_fields.url|Resource URL||
|resource_fields.name|Resource name||
|resource_fields.resource:description|Resource description||
|resource_fields.resource:format|File format||
|resource_fields.resource:size|Byte size||

## Leveraging the SOLR search engine

Our CKAN instance uses the SOLR search engine - built on Apache Lucence. You can use the SOLR queries in your API calls.

### Field search

You can search any field by typing the field name followed by a colon ":" and then the term you are looking for. As an example, if you want to search the title and the description field, you can enter:

    title:Cloncurry AND text:”radiometric survey”

or

    title:”Super Isa Basin” AND “well completion report”

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

    mod_date:[20020101 TO 20030101]

This will find documents whose mod_date fields have values between 20020101 and 20030101, inclusive. Note that Range Queries are not reserved for date fields. You could also use range queries with non-date fields:

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
**Geological Survey of Quensland**  
Department of Natural Resources, Mines and Energy  
Queensland, Australia  
<GSQOpenData@dnrme.qld.gov.au>  

*Author*:  
**David Crosswell**  
Enterprise Architect  
Cross-Lateral  
<https://crosslateral.com.au>
