import os
import yaml

class ConfigParser(object):
  def __init__(self):
    self.api_token = None
    self.organisations = []

  def add_from_file(self, path):
    with open(path, 'r') as config_file:
      new_config = yaml.load(config_file)
    new_api_token = new_config.get('github_api_token')
    new_organisations = new_config.get('github_organisations')
    if new_api_token:
      self.api_token = new_api_token
    if new_organisations:
      both_org_sets = set(self.organisations).union(new_organisations)
      self.organisations = list(both_org_sets)
