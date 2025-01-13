# eppoPynder

## Overview

Welcome to the *eppoPynder* package! This package is a wrapper around the public APIs of the European and Mediterranean Plant Protection Organization (EPPO) database. It provides a straightforward way to access a wide range of pest-specific information that has been produced or collected by EPPO.

*eppoPynder* is designed for use by researchers and practitioners working in plant protection who need easy access to the EPPO database using Python.

## Prerequisites

To use the *eppoPynder* package, you need a stable internet connection, as it interacts with the EPPO database online services to fetch and manipulate data. A reliable internet connection is essential for the functionality of the package.

## Installation

You can install the *eppoPynder* package from PyPi using the following command:

```         
pip install eppoPynder
```

Alternatively, if you want to install the package from GitHub (for the latest development version), use:

```         
pip install git+https://github.com/openefsa/eppoPynder.git
```

## Working with API Tokens

The *eppoPynder* package requires your unique token to be included in each API request for proper functionality. There are three ways to provide this token:

1.  **Using the `.env` file**
2.  **Manually adding it to each API request**

### 1. Setting Environment Variables via `.env`

The `.env` file is used to specify environment variables that Python loads at the start of every session. It is particularly useful for setting variables, such as API keys, that can be accessed by Python scripts and functions.

After installing the *eppoPynder* package, you should create a `.env` file in your project's root directory (i.e., the same directory as `setup.py`). This is important because the `python-dotenv` package expects the `.env` file to be in this location by default.

#### Example Project Structure:

```         
/eppoPynder
    ├── .env # Place your .env file here
    ├── setup.py
    ├── src/
    │   └── eppoPynder/
    │       └── __init__.py
    │       └── module.py
    └── README.md
```

You can create or modify the `.env` file manually using any text editor. In the `.env` file, you set environment variables in the following format:

`EPPO_token=your-eppo-token`

After adding your EPPO token to the `.env` file, save and close the file. Python will automatically read the token when it starts up, and you can access it in any Python session using `os.getenv('EPPO_token')`.

### 2. Manually adding your token to each API request

For functions that require an API token, you can manually specify the token in the `token` argument of the function. This method is useful if you want to use different tokens for different function calls or if you don't want to store the token globally. For example:

`query_the_eppo_for_service(queried_eppocode = "BEMITA", service = "general", token = "your-eppo-token")`

#### Explanation:

`query_the_eppo_for_service(queried_eppocode = "BEMITA", service = "general", token = "your-eppo-token")`: This calls the function with the necessary parameters:

-   `queried_eppocode = "BEMITA"`: The EPPO code for which you want to query a service.
-   `service = "general"`: Specifies the service you want to query (you can replace this with any valid service type).
-   `token = "your-eppo-token"`: Passes the token for authentication. Replace "your-eppo-token" with your actual EPPO token enclosed in quotes.

## Basic Usage

The primary functionality of *eppoPynder* is to query the EPPO database for specific EPPO codes and retrieve data across various services. Users can either choose to: 1) query a single service for a given EPPO code or 2) query all available services in the database for more comprehensive information.

For plant and pest species, the basic available information includes scientific names, synonyms, common names in different languages, and taxonomic position. For each pest of regulatory interest, more detailed information can also be retrieved regarding its host plants and categorization (quarantine status).

The examples below will guide you on how to use the functions in this package to access these data, but to begin, we need to load the *eppoPynder* package with this command:

```         
import eppoPynder
```

If you want to learn more about the arguments and usage of a particular function, you can use Python's built-in `help()` function. Simply run:

```         
help(function_name)
```

This will display the detailed documentation for the function, including its arguments, return values, and examples.

For example, if you're working with a function called `query_the_eppo_for_service()`, you would use:

```         
help(query_the_eppo_for_service)
```

## Querying a Specific Service

To query a specific service (e.g., categorization) for an EPPO code (e.g., "BEMITA"), you can use the `query_the_eppo_for_service()` function as follows:

```         
categorization_BEMITA = query_the_eppo_for_service("BEMITA", service = "categorization")
```

### Expected Output:

```         
>>> categorization_BEMITA
   nomcontinent isocode  ...  queried_on                                        queried_url
0       America      CL  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
1          Asia      BH  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
2          Asia      KZ  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
3        Europe      AZ  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
4        Europe      BY  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
5        Europe      GE  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
6        Europe      MD  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
7        Europe      NO  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
8        Europe      RU  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
9        Europe      RS  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
10       Europe      CH  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
11       Europe      TR  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
12       Europe      UA  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
13       Europe      GB  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
14      Oceania      NZ  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
15      RPPO/EU      9M  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
16      RPPO/EU      9A  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
17      RPPO/EU      9L  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
18      RPPO/EU      9L  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
19      RPPO/EU      9H  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...

[20 rows x 11 columns]
```

`categorization_BEMITA` is a dataframe containing information about the categorization of the EPPO code "BEMITA", and includes the following columns:

-   **nomcontinent**: The continent where the country is located.
-   **isocode**: The ISO country code.
-   **country**: The name of the country or region.
-   **qlist**: A code representing the pest status or classification.
-   **qlistlabel**: A label explaining the pest classification (e.g., "A1 list" or "Quarantine pest").
-   **yr_add**: The year the country was added to the list.
-   **yr_del**: The year the country was removed (if applicable).
-   **yr_trans**: The year the country transitioned (if applicable).
-   **queried_eppocode**: The input EPPO code.
-   **queried_on**: The date when the query was performed.
-   **queried_url**: The queried URL.

## Querying All Available Services

If you wish to query all available services for the EPPO code "BEMITA", you can use the `query_the_whole_eppo()` function. This will return a dictionary of dataframes, each corresponding to a different service.

```         
result_dict = query_the_whole_eppo("BEMITA")
```

### Expected Output:

```         
# Print the names of the services in the result

>>> result_dict.keys()
dict_keys(['general', 'names', 'taxonomy', 'categorization', 'hosts', 'pests', 'kingdom'])
``` 

`result_dict.keys()` returns the names of the services: general, names, taxonomy, categorization, hosts, pests, and kingdom.

``` 
# Print the data from a specific service, e.g., categorization

>>> result_dict["categorization"]
   nomcontinent isocode  ...  queried_on                                        queried_url
0       America      CL  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
1          Asia      BH  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
2          Asia      KZ  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
3        Europe      AZ  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
4        Europe      BY  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
5        Europe      GE  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
6        Europe      MD  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
7        Europe      NO  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
8        Europe      RU  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
9        Europe      RS  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
10       Europe      CH  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
11       Europe      TR  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
12       Europe      UA  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
13       Europe      GB  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
14      Oceania      NZ  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
15      RPPO/EU      9M  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
16      RPPO/EU      9A  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
17      RPPO/EU      9L  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
18      RPPO/EU      9L  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
19      RPPO/EU      9H  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...

[20 rows x 11 columns]
```

Accessing a specific service (e.g., `result_dict["categorization"]`) will show the data related to that particular service for the EPPO code "BEMITA".

## Wrangling Data

The *eppoPynder* package also provides a data wrangling function, `taxonomy_ranked()`, which can combine the data fetched from the "taxonomy" and "kingdom" EPPO services to create a unified, integrated dataframe.

For example, assume you have two dataframes: `taxonomy` and `kingdom`, which were obtained by querying the "taxonomy" and "kingdom" services for the EPPO code "BEMITA" using the `query_the_eppo_for_service()` function.

You can combine these two dataframes as follows:

```         
# Query the taxonomy service for the EPPO code "BEMITA"
taxonomy = query_the_eppo_for_service("BEMITA", service = "taxonomy")

# Query the kingdom service for the EPPO code "BEMITA"
kingdom = query_the_eppo_for_service("BEMITA", service = "kingdom")

# Combine taxonomy and kingdom data
wrangled_data = taxonomy_ranked(taxonomy, kingdom)
```

### Expected Output:

```         
>>> wrangled_data
      rank  codeid  ...  queried_on                                        queried_url
0  kingdom   57021  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
1     <NA>   57200  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
2     <NA>   77963  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
3     <NA>   59061  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
4     <NA>   58830  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
5     <NA>   73260  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
6     <NA>   56905  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
7     <NA>   57321  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...
8     <NA>    5935  ...  2024-12-19  https://data.eppo.int/api/rest/1.0/taxon/BEMIT...

[9 rows x 8 columns]
```

`wrangled_data` is a dataframe that combines the taxonomy and kingdom information for the EPPO code "BEMITA". This integration provides a more comprehensive view of the organism's taxonomic rank.

Specifically, the output dataframe contains the following columns:

-   **rank**: The taxonomic rank.
-   **codeid**: A unique identifier for each entry.
-   **eppocode**: The EPPO code representing the taxonomic group.
-   **prefname**: The preferred name of the taxonomic group (e.g., "Animalia", "Insecta").
-   **level**: The taxonomic level in the hierarchy (1 for the broadest category, progressing to more specific levels).
-   **queried_eppocode**: The input EPPO code.
-   **queried_on**: The date when the query was performed.
-   **queried_url**: The queried URL.

## Retrieving Countries in Regional Plant Protection Organizations

The `getting_countries()` function allows you to retrieve all the member countries of a specific Regional Plant Protection Organization (RPPO).

For example, to get the member countries of the EAEU (Eurasian Economic Union), you can use the following command:

```         
EAEU_countries = getting_countries('EAEU')
```

### Expected Output:

```         
>>> EAEU_countries
'Armenia, Belarus, Kazakhstan, Kyrgyzstan, Russia'
```

`EAEU_countries` is a string of country names that are members of the EAEU.

## Data Dump for Multiple EPPO Codes

The `data_dump()` function allows you to retrieve a comprehensive data dump for multiple EPPO codes. This function queries all available EPPO services for a list of input codes.

The following is an example of how the function can be used to query all available EPPO services for the EPPO codes "APHIPO" and "LEUCSC":

```         
data_dump_result = data_dump(["APHIPO", "LEUCSC"])
```

### Expected Output:

```   
# Print the names of the services in the result

>>> data_dump_result.keys()
dict_keys(['general', 'names', 'taxonomy', 'categorization', 'hosts', 'pests', 'kingdom'])
```  

The output is a dictionary of dataframes, each corresponding to a different service: general, names, taxonomy, categorization, hosts, pests, and kingdom.

```
# Print the data from a specific service, e.g., general

>>> data_dump_result["general"]
  pestCode  ...                                        queried_url
0   APHIPO  ...  https://data.eppo.int/api/rest/1.0/taxon/APHIP...
0   LEUCSC  ...  https://data.eppo.int/api/rest/1.0/taxon/LEUCS...

[2 rows x 20 columns]
```

Accessing a specific service (e.g., `data_dump["general"]`) will show the data related to that particular service for the EPPO codes "APHIPO" and "LEUCSC". The column `queried_eppocode` in the dataframe distinguishes which data have been retrieved for each EPPO code.