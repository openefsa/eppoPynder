# Introduction to eppoPynder

## Overview

**eppoPynder** provides a Python interface to the public APIs of the **European
and Mediterranean Plant Protection Organization (EPPO)** database.
The package facilitates access to a wide range of pest-related information
collected and maintained by EPPO, allowing users to query, retrieve, and
process this data directly from Python.

The package is intended for researchers, analysts, and practitioners in plant
protection who require convenient programmatic access to EPPO data.

## Installation

### From PyPi

```bash
$ pip install eppoPynder
```

### Development version

To install the latest development version:

```bash
$ pip install git+https://github.com/openefsa/eppoPynder.git
```

## Requirements

An active internet connection is required, as the package communicates with
EPPO's online services to fetch and process data.

## Working with API keys

The *eppoPynder* package requires your unique API token to function properly.
You can provide this token in one of two ways:

1.  By setting it in a `.env` file.
2.  By including it manually during the client initialization.

### Setting the API key via `.env`

A `.env` file is used to define environment variables that Python can load at
runtime. This approach is particularly convenient for sensitive information
like API keys, as it allows you to use them in any Python script or function
without hardcoding them.

Place the `.env` file in the root directory of you project (for example,
`C:/Users/username/Documents/myProject/.env` on Windows or
`~/Documents/myProject/.env` on Unix-like systems). You can create or edit this
file with any plain text editor.

Add your EPPO API key in the following format:

`EPPO_API_KEY=<your_eppo_api_key>`

Once the file is saved, the variable will be correctly set for the library to
use during execution.

### Setting the API key manually during client initialization

Alternatively, you can provide the API key directly in the `api_key` argument
of client instantiation. This is useful if you prefer not to store the token
globally. For example:

```python
from eppopynder import Client

client = Client(api_key="<your_eppo_api_key>")
```

Note that if an API key is explicitly provided, the API key set through the
`.env` file will be ignored, if any.

## Basic usage

The main purpose of *eppoPynder* is to query the EPPO database for specific
EPPO codes and retrieve relevant information across various endpoints. For each
endpoint, you can either:

1.  Query all available services to obtain more comprehensive data.
2.  Query one or more services to obtain specific data.

For plant and pest species, the basic information returned includes scientific
names, synonyms, common names in different languages, and taxonomic
classification. For pests of regulatory interest, you can also retrieve more
detailed information, such as host plants and quarantine categorization.

Below are examples demonstrating how to use the functions in this package.
First, load the *eppoPynder* package:

```python
from eppopynder import *
```

Then, initialize the client by specifying the API key you want to use:

```python
client = Client() # Use the API key defined in .env file.
client = Client(api_key="<your_eppo_api_key>") # Manually define the API key.
```

To explore the arguments and usage of a specific function, you can run:

```python
help(function_name)
```

This will show the full documentation for the function, including its
arguments, return values, and usage examples.

For example, if you are working with the `uniform_taxonoy()` function,
you can check its documentation with:

```python
help(uniform_taxonomy)
```

Again, if you want to check the documentation of a function that represents a
category, you can run:

```python
help(Client.taxon)
```

Note that the functions representing the categories are all defined inside the
`Client` class.

## Querying a specific category

The *eppoPynder* package allows you to query all categories available in
version 2.0 of the EPPO APIs: General, Taxons, Taxon, Country, Tools, Reporting
Services, and References.

Each category has a corresponding function in the package with the same name
in *snake_case* format: general(), taxons(), taxon(), country(), tools(),
reporting_service(), and reportings(). By default, these functions return all
data available under the selected category, but you can customize the query by
specifying the desired services.

For example, to query all services of the Taxon category for the EPPO code
"BEMITA", you can use the following code:

```python
data = client.taxon(eppo_codes=["BEMITA"])
```

Some services require certain mandatory parameters, which must be provided when
making the request. For example:

```python
data = client.tools(
    services=[ToolsService.NAME2CODES],
    params={
        ToolsService.NAME2CODES: {
            "name": "Bemisia tabaci"
        }
    }
)
```

Each category comes with a set of service names that can be queried. These are
stored in an enumeration whose name follows the convention Category +
"Service". For example, for the Taxon category, the collection of queryable
services is named `TaxonService`, and its values are `OVERVIEW`, `INFOS`,
`NAMES` and so on,  exactly matching the names of the available services.
Keep in mind that services can be provided to the corresponding functions only
through their dedicated enum.

You can import the enumeration associated with a specific category as shown
below:

```python
from eppopynder import TaxonService, ToolsService # And so on...
```

Alternatively, you can import all of them at once by importing everything from
the library:

```python
from eppopynder import *
```

## Querying a specific service

To query a specific service within an endpoint, *eppoPynder* allows you to
specify it directly in the function call. For example, to access only the
`/taxons/taxon/categorization` service for the EPPO code "BEMITA", you can use
the `Client.taxon()` function as follows:

```python
data = client.taxon(
    eppo_codes=["BEMITA"],
    services=[TaxonService.CATEGORIZATION]
)
```

### Expected output

```python
print(data)
```
```python
{<TaxonService.CATEGORIZATION: 'categorization'>:    queried_eppo_code  continent_id continent_name country_iso              country_name  ... year_add year_delete  year_transient                                        queried_url                 queried_on
0             BEMITA             4        America          CL                     Chile  ...     2019        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
1             BEMITA             2           Asia          BH                   Bahrain  ...     2003        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
2             BEMITA             2           Asia          KZ                Kazakhstan  ...     2017        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
3             BEMITA             1         Europe          AZ                Azerbaijan  ...     2024        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
4             BEMITA             1         Europe          BY                   Belarus  ...     1994        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
5             BEMITA             1         Europe          GE                   Georgia  ...     2018        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
6             BEMITA             1         Europe          MD      Moldova, Republic of  ...     2017        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
7             BEMITA             1         Europe          NO                    Norway  ...     2012        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
8             BEMITA             1         Europe          RU  Russian Federation (the)  ...     2014        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
9             BEMITA             1         Europe          RS                    Serbia  ...     2015        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
10            BEMITA             1         Europe          CH               Switzerland  ...     2019        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
11            BEMITA             1         Europe          TR                   Türkiye  ...     2016        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
12            BEMITA             1         Europe          UA                   Ukraine  ...     2019        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
13            BEMITA             1         Europe          GB            United Kingdom  ...     2020        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
14            BEMITA             5        Oceania          NZ               New Zealand  ...     2000        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
15            BEMITA             6        RPPO/EU          9M                      EAEU  ...     2016        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
16            BEMITA             6        RPPO/EU          9A                      EPPO  ...     1989        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
17            BEMITA             6        RPPO/EU          9L                        EU  ...     2019        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
18            BEMITA             6        RPPO/EU          9L                        EU  ...     2019        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414
19            BEMITA             6        RPPO/EU          9H                     OIRSA  ...     1992        None            None  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 14:58:20.605414

[20 rows x 12 columns]}
```

All function calls return a dictionary of data frames, each containing the
information from the requested services.

## Querying all available services

To fetch data from all available services within a specific endpoint, simply
use the corresponding function without modifying the `services` parameter. Each
function will return a dictionary of data frames, with each data frame
containing information from one service.

```python
data = client.taxon(eppo_codes=["BEMITA"])
```

### Expected output

```python
# Print the names of the services in the result.
print(data.keys())
```
```python
dict_keys([<TaxonService.OVERVIEW: 'overview'>, <TaxonService.INFOS: 'infos'>, <TaxonService.NAMES: 'names'>, <TaxonService.TAXONOMY: 'taxonomy'>, <TaxonService.CATEGORIZATION: 'categorization'>, <TaxonService.KINGDOM: 'kingdom'>, <TaxonService.HOSTS: 'hosts'>, <TaxonService.PESTS: 'pests'>, <TaxonService.VECTORS: 'vectors'>, <TaxonService.VECTOR_OF: 'vectorof'>, <TaxonService.BCA: 'bca'>, <TaxonService.BCA_OF: 'bcaof'>, <TaxonService.PHOTOS: 'photos'>, <TaxonService.REPORTING_ARTICLES: 'reporting_articles'>, <TaxonService.DOCUMENTS: 'documents'>, <TaxonService.STANDARDS: 'standards'>, <TaxonService.DISTRIBUTION: 'distribution'>])
```

```python
# Print the data from a specific service.
print(data[TaxonService.OVERVIEW])
```
```python
  queried_eppo_code eppocode           datecreate           lastupdate infos replacedby        prefname  is_active datatype                                        queried_url                 queried_on
0            BEMITA   BEMITA  2002-10-28 00:00:00  2002-10-28 00:00:00  None       None  Bemisia tabaci       True      GAI  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 15:08:26.388685
```

Using `data.keys()` will display the names of the queried services. You can
then access a specific service to view the data associated with it.

## Data wrangling

The *eppoPynder* package provides a convenient function, `uniform_taxonomy()`,
to create a complete and standardized taxonomy data frame. This function takes
the taxonomy data returned by the taxonomy service and ensures a uniform
structure, including all expected taxonomic ranks, even if some ranks are
missing in the original result.

For example, assume you have retrieved taxonomy data for the EPPO code "BEMITA"
using the `Client.taxon()` function:

```python
data = client.taxon(eppo_codes=["BEMITA"], services=[TaxonService.TAXONOMY])
```

You can then generate a uniform taxonomy table with all ranks using:

```python
taxonomy = uniform_taxonomy(data[TaxonService.TAXONOMY])
```

### Expected output

```python
print(taxonomy)
```
```python
         type queried_eppo_code eppocode        prefname                                        queried_url                 queried_on
0     Kingdom            BEMITA   1ANIMK        Animalia  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 15:26:07.594529
1      Phylum            BEMITA   1ARTHP      Arthropoda  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 15:26:07.594529
2   Subphylum            BEMITA   1HEXAQ        Hexapoda  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 15:26:07.594529
3       Class            BEMITA   1INSEC         Insecta  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 15:26:07.594529
4    Subclass               NaN      NaN             NaN                                                NaN                        NaT
5       Order            BEMITA   1HEMIO       Hemiptera  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 15:26:07.594529
6    Suborder            BEMITA   1STERR  Sternorrhyncha  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 15:26:07.594529
7      Family            BEMITA   1ALEYF     Aleyrodidae  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 15:26:07.594529
8   Subfamily               NaN      NaN             NaN                                                NaN                        NaT
9       Genus            BEMITA   1BEMIG         Bemisia  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 15:26:07.594529
10    Species            BEMITA   BEMITA  Bemisia tabaci  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 15:26:07.594529
```

## Data retrieval for multiple EPPO or ISO codes

The `Client.taxon()` and `Client.country()` functions allow you to retrieve
also a complete data dump for multiple EPPO or ISO codes by querying all
available EPPO services for each of them.

Here is an example showing how to use the function to fetch all available
information for the EPPO codes "BEMITA" and "GOSHI":

```python
data = client.taxon(eppo_codes=["BEMITA", "GOSHI"])
```

### Expected output

```python
# Print the names of the services in the result.
print(data.keys())
```
```python
dict_keys([<TaxonService.OVERVIEW: 'overview'>, <TaxonService.INFOS: 'infos'>, <TaxonService.NAMES: 'names'>, <TaxonService.TAXONOMY: 'taxonomy'>, <TaxonService.CATEGORIZATION: 'categorization'>, <TaxonService.KINGDOM: 'kingdom'>, <TaxonService.HOSTS: 'hosts'>, <TaxonService.PESTS: 'pests'>, <TaxonService.VECTORS: 'vectors'>, <TaxonService.VECTOR_OF: 'vectorof'>, <TaxonService.BCA: 'bca'>, <TaxonService.BCA_OF: 'bcaof'>, <TaxonService.PHOTOS: 'photos'>, <TaxonService.REPORTING_ARTICLES: 'reporting_articles'>, <TaxonService.DOCUMENTS: 'documents'>, <TaxonService.STANDARDS: 'standards'>, <TaxonService.DISTRIBUTION: 'distribution'>])
```

```python
# Print the data from a specific service.
print(data[TaxonService.OVERVIEW])
```
```python
  queried_eppo_code eppocode           datecreate           lastupdate  ... is_active datatype                                        queried_url                 queried_on
0            BEMITA   BEMITA  2002-10-28 00:00:00  2002-10-28 00:00:00  ...      True      GAI  https://api.eppo.int/gd/v2/taxons/taxon/BEMITA... 2025-12-10 15:31:54.300453
1             GOSHI    GOSHI  2004-04-21 00:00:00  2004-04-21 00:00:00  ...      True      PFL  https://api.eppo.int/gd/v2/taxons/taxon/GOSHI/... 2025-12-10 15:31:54.864112
```

Using `data.keys()` will display the names of the queried services. You can
then access a specific service to view the data associated with it.
