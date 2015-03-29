import os
import yaml

class ConfigParser(object):
  def __init__(self):
    self.github_token = None
    self.organisations = []

  def add_from_file(self, path):
    with open(path, 'r') as config_file:
      new_config = yaml.load(config_file)

    new_github_token = new_config.get('github_token')
    self.add_github_token(new_github_token)

    new_organisations = new_config.get('github_organisations')
    self.add_organisations(new_organisations)

  def add_from_environment(self):
    new_github_token = os.environ.get('github_token')
    self.add_github_token(new_github_token)

    new_organisations = os.environ.get('github_organisations')
    def split_and_filter(org_string):
      if org_string == None:
        return []
      organisations = org_string.split(':')
      return [org.strip() for org in organisations if org]
    self.add_organisations(split_and_filter(new_organisations))

  def add_github_token(self, github_token):
    if github_token:
      self.github_token = github_token

  def add_organisations(self, organisations):
    if organisations:
      both_org_sets = set(self.organisations).union(organisations)
      self.organisations = list(both_org_sets)
