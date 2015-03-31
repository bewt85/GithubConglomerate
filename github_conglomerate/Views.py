import dateutil.parser
import json

class Repos(object):

  def __init__(self):
    self.created_at = None
    self.data = []

  def fix_datetimes(self, repo):
    datetime_attributes = [
      'created_at',
      'last_released',
      'updated_at'
    ]
    for attribute in datetime_attributes:
      try:
        repo[attribute] = dateutil.parser.parse(repo[attribute])
      except:
        pass

  def load_json(self, json_data):
    data = json.loads(json_data)
    self.created_at = dateutil.parser.parse(data['created_at'])
    for repo in data['repos']:
      self.fix_datetimes(repo)
    self.data = data['repos']
