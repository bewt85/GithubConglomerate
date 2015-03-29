github_conglomerate
===================

Some organisations choose to give each team their own github organisation to simplify administration.  This is a bit of a pain when trying to find interesting software to reuse.  Github's tools to sort / compare repos are a bit limited.

This will create a little Heroku hostable web app which uses the Github API to get a list of repos for each 'Github organisation' and amalgamate them into one nice view.

This data can be stored locally or on Amazon S3; the latter being preferable on Heroku because they recycle containers regularly.

At the moment I've only got the bits to download the data working; I've not done any web development or AWS bits yet.

Usage
-----

::

  get-repo-data --orgs sanger-pathogens wtsi-hgi \
                --github <api-token> \
                --output example_output.json

Example output
--------------

::

  cat example_output.json | python -m json.tool

Gives:

::

  {
    "created_at": "2015-03-29T23:12:29.573859", 
    "repos": [
      {
        "created_at": "2014-04-30T09:44:21", 
        "description": "de novo virus assembler of Illumina paired reads", 
        "forks_count": 1, 
        "html_url": "https://github.com/sanger-pathogens/iva", 
        "last_released": "2015-03-27T11:36:49+00:00", 
        "latest_release": "v0.11.5", 
        "name": "iva", 
        "organisation": "sanger-pathogens", 
        "release_count": 19, 
        "stargazers_count": 2, 
        "updated_at": "2015-03-27T11:36:49"
      }, 
      {
        "created_at": "2015-03-25T11:16:25", 
        "description": "Takes a jinja2 template and some json and sends an email", 
        "forks_count": 1, 
        "html_url": "https://github.com/sanger-pathogens/json2email", 
        "last_released": "2015-03-28T16:58:12+00:00", 
        "latest_release": "release/0.0.6", 
        "name": "json2email", 
        "organisation": "sanger-pathogens", 
        "release_count": 2, 
        "stargazers_count": 1, 
        "updated_at": "2015-03-28T16:58:12"
      },
      {
        loads more
      }
    ]
  }


You can also load data from YAML config files as follows:

::

  ---
  github_token: <api_token>
  github_organisations:
  - sanger-pathogens
  - wtsi-hgi

Tests
-----

::

  ./run_tests.sh

or

::

  python setup.py test

TODO
----

- save data to S3
- load data from S3
- create a flask app
- make it bootstrap-py
- deploy to heroku
- get Travis working
- setup a cron job to update the data (daily?)
- create some more interesting 'views' (newest, recent releases)

Licence
-------

GPL v3

Affiliation
-----------

This software is not endorsed or condoned by any of the organisations mentioned in this README or the code.  The Wellcome Trust Sanger Institute has loads of 'Github organisations' though so I thought this might be especially helpful for them :)
