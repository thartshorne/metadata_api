# Fragile Families Metadata API Repository

[![Build Status](https://travis-ci.org/fragilefamilieschallenge/metadata_api.svg?branch=master)](https://travis-ci.org/fragilefamilieschallenge/metadata_api)

This is a Python Flask app that provides access to the Fragile Families Metadata through HTTP endpoints that return JSON results. The web endpoints allow web users to query, select and filter the metadata variables in several ways.

Access to the 'raw' metadata CSV file is also provided. The latest CSV files are available in the 'data' folder of the ffmeta package.

## We provide three API endpoints:

### Filter
This endpoint is to be used to search variable names based on a search criteria.

#### Return a list of variables where fieldName matches (fully or partially) the provided value.
General Format: `/filter?<fieldName>=<value>`

`/filter?name=f1b6a`
```
{
    "matches": [
        "f1b6a"
    ]
}
```

`/filter?name=f1b6`
```
{
    "matches": [
        "f1b6a",
        "f1b6b",
        "f1b6c",
        "f1b6d",
        "f1b6e",
        "f1b6f"
    ]
}
```

`/filter?topic=education` 
```
{
  "matches": [
    "cf1edu", 
    "f1i1", 
    "f1i2", 
    "f1i2a1", 
    "f1i2a2", 
    "f1i3", 
    "f1i3a1", 
    "f1i3a2", 
    "cm1edu", 
    "m1i1", 
    "m1i3", 
    "m1i6", 
    "f2k1a", 
    "f2k2", 
    "f2k3a", 
    ...
    ...
    ...
```

### Search
This endpoint can also be used to search variable names based on a search criteria.

#### Return a list of variables where \<value\> is found in \<fieldName\>.
General Format: `/search?fieldName=<fieldName>&query=<value>`

`/search?fieldName=label&query=CPS`
```
{
  "matches": [
    "p4j2", 
    "p4j3_mo", 
    "p4j3_yr", 
    "p4j6", 
    "p4j7_1", 
    "p4j7_2", 
    "p4j7_3", 
    "p4j8", 
    "p5q10_1", 
    "p5q10_2", 
    "p5q10_3", 
    "p5q11", 
    "p5q5", 
    "p5q7", 
    "p5q8_1", 
    "p5q8_101", 
    "p5q8_2", 
    "p5q8_3", 
    "p5q8_4", 
    "p6j59", 
    "p6j60a", 
    "p6j60b", 
    "p6j61", 
    "p6j62_1", 
    "p6j62_101", 
    "p6j62_102", 
    "p6j62_2", 
    "p6j62_3", 
    "p6j62_4", 
    "p6j63", 
    "p6j64_1", 
    "p6j64_2", 
    "p6j64_3", 
    "p6j64_4"
  ]
}
```

### Select
Once you know the name of the variable you're interested in, this endpoint is to be used to retrieve metadata for a variable, given its name.

#### Returns metadata for variable with name \<varName\>.
General Format: `/select?varName=<varName>`

`/select?varName=m1a3`
```
{
    "data_source": "questionnaire",
    "data_type": "bin",
    "group_id": "221",
    "group_subid": null,
    "id": 449,
    "label": "Have you picked up a (name/names) for the (baby/babies) yet?",
    "leaf": "3",
    "name": "m1a3",
    "old_name": "m1a3",
    "respondent": "m",
    "responses": {
        "1": "Yes",
        "2": "No",
        "-9": "Not in wave",
        "-8": "Out of range",
        "-7": "N/A",
        "-6": "Skip",
        "-5": "Not asked",
        "-4": "Multiple ans",
        "-3": "Missing",
        "-2": "Don't know",
        "-1": "Refuse"
    },
    "scope": "20",
    "section": "a",
    "topics": [
        {
            "topic": "parenting abilities",
            "umbrella": "Parenting"
        }
    ],
    "warning": 0,
    "wave": "1"
}
```

#### Optionally, if you also know the name of the field you're interested in, it can return only the field specified by \<fieldName\>.
General Format: `/select?varName=<varName>&fieldName=<fieldName>`

`/select?varName=m1a3&fieldName=label`
```
{
  "label": "Have you picked up a (name/names) for the (baby/babies) yet?"
}
```

## Errors

### Getting the metadata for a variable name that doesn't exist:

`/select?varName=m1a2` (no variable by name `m1a2` exists)

returns an HTTP 400 (Bad Request) Response with the message body:
```
{
    "message": "Invalid variable name."
}
```
### Searching in a field that doesn't exist

`/search?fieldName=toppic&query=car` (note that `toppic` is misspelled to illustrate the point)

returns an HTTP 400 (Bad Request) Response with the message body:
```
{
    "message": "Invalid field name."
}
```

