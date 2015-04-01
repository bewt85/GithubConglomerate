github_conglomerate
===================

Some organisations choose to give each team their own github organisation to simplify administration.  This is a bit of a pain when trying to find interesting software to reuse.  Github's tools to sort / compare repos are a bit limited.

This will create a little Heroku hostable web app which uses the Github API to get a list of repos for each 'Github organisation' and amalgamate them into one nice view.

The script is outlined below which collected the required data and puts it into a json formatted file.  This should then be made accessible via a URL which a simple web app will query on startup.

Things you could help with
--------------------------

- The scoring algorithm for repos is a bit arbitrary.  A second opinion on `Repos.score_repo <https://github.com/bewt85/GithubConglomerate/blob/master/github_conglomerate/Views.py>`_ would be great.
- I'm not sure I've got a very complete list of repos.  Feel free to `suggest some more <https://github.com/bewt85/GithubConglomerate/blob/master/example_config.yaml>`_ via a Pull Request.
- I'm not very good at CSS, HTML, Javascript.  Any `suggestions for improvements <https://github.com/bewt85/GithubConglomerate/blob/master/scripts/static/templates/index.html>`_ would be great or perhaps you could suggest a book to improve my skills?

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

Web App
-------

The web app is pretty simple at the moment.  You can start it using the following command and view the results at http://localhost:8080.

::

  ./scripts/web.py

Tests
-----

::

  ./run_tests.sh

or

::

  python setup.py test

TODO
----

- get Travis working
- setup a cron job to update the data (daily?)
- create some more interesting 'views' (newest, recent releases)

Licence
-------

GPL v3

Affiliation
-----------

This software is not endorsed or condoned by any of the organisations mentioned in this README or the code.  The Wellcome Trust Sanger Institute has loads of 'Github organisations' though so I thought this might be especially helpful for them :)
