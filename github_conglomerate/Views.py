import dateutil.parser
import json

from datetime import datetime, timedelta
from math import log, sqrt

class Repos(object):

  def __init__(self, json_data='{}'):
    self.now = datetime.now()
    self.created_at = None
    self.load_json(json_data)
    for repo in self.data:
      self.fix_datetimes(repo)
      self.score_repo(repo)
    self.data = self.sorted_by(self.data, 'score')

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

  def score_repo(self, repo):
    score = 0
    score += 1 if repo['description'] else 0
    score += self.get_count_points(repo['forks_count'])
    score += self.get_date_points(repo['last_released'])
    score += self.get_count_points(repo['release_count'])
    score += self.get_count_points(repo['stargazers_count'])
    score += self.get_date_points(repo['updated_at'])
    repo['score'] = score

  def get_date_points(self, when):
    if not isinstance(when, datetime):
      return 0
    elif when > self.now:
      # Suspicious but we'll give you the benefit of the doubt
      return 5.0
    else:
      age_delta = abs(self.now - when)
      # abs: if the repo is somehow in the future, reflect it into the past across now
      age_hours = age_delta.days * 24 + age_delta.seconds / 3600
      age_hours += 4 # aiming for stability in the face of very recent times
      return max(0, 5 - sqrt(age_hours) * 2 / 46.5 )
      # 5        : max score
      # 2 / 46.5 : scale to lose 2 points at 90 days old

  def get_count_points(self, count):
    return int(log(abs(count)+1)*2.1668*100 + 0.5)/100.0
    # abs(count) + 1 : now we can work on any int
    # 2.1668         : factor to match previous step algorithm at 100 => 10.0
    # then round to 2dp

  def sorted_by(self, repos, *args):
    repos = repos[:]
    if args == []:
      args = ['score']
    for attribute in args[-1::-1]:
      def cmp_function(repoA, repoB):
        valueA = repoA.get(attribute)
        valueB = repoB.get(attribute)
        if valueB == None:
          return -1
        elif valueA == None:
          return 1
        elif isinstance(valueA, str):
          return cmp(valueA, valueB)
        else:
          return -cmp(valueA, valueB)
      repos = sorted(repos, cmp=cmp_function)
    return repos

  def filter_contains(self, repos, **kwargs):
    repos = repos[:]
    for attribute, value in kwargs.items():
      def filter_function(repo):
        return value.lower() in repo.get(attribute, '').lower()
      repos = filter(filter_function, repos)
    return repos

  def join(self, repos, other_repos):
    repos = [tuple(repo.items()) for repo in repos[:]]
    other_repos = [tuple(repo.items()) for repo in other_repos[:]]
    joint_repos = list(set(repos + other_repos))
    return [{k: v for k,v in repo} for repo in joint_repos]
