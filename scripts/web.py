#!/usr/bin/env python

import os

import flask
from flask import Flask, render_template

from github_conglomerate.Views import Repos

parent_folder = os.path.abspath(os.path.dirname(__file__))
template_folder = os.path.join(parent_folder, 'static', 'templates')
path_to_data = os.path.join(parent_folder, '..', 'all_output.json')

app = Flask(__name__, template_folder=template_folder)

@app.route('/')
def index():
  return render_template('index.html', 
                         repos=repos.sorted_by(repos.data, 'score'),
                         created_at=repos.created_at,
                         google_analytics_token=google_analytics_token)

if __name__ == '__main__':
  with open(path_to_data, 'r') as data_file:
    repos = Repos(data_file.read())

  google_analytics_token = os.environ.get("GA_TOKEN")
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
