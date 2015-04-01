import dateutil.parser
import json

from datetime import datetime, timedelta

now = datetime.now()
this_week = now - timedelta(days=7)
this_month = now - timedelta(days=28)
three_months_ago = now - timedelta(days=90)
six_months_ago = now - timedelta(days=180)
this_year = now - timedelta(days=365)

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
    elif when < this_week:
      return 5
    elif when < this_month:
      return 4
    elif when < three_months_ago:
      return 3
    elif when < six_months_ago:
      return 2
    elif when < this_year:
      return 1
    else:
      return 0

  def get_count_points(self, count):
    if count > 100:
      # No more than 10 points
      return 10
    elif count > 50:
      # 7 to 10 points
      return 7 + 3 * (float(count) - 50) / 50
    elif count > 10:
      # 5 to 10 points
      return 5 + 2 * (float(count) - 10) / 40
    elif count > 5:
      # 3 to 5 points
      return 3 + 2 * (float(count) - 5) / 2
    elif count > 4:
      return 2.5
    elif count > 3:
      return 2
    elif count > 0:
      return 1
    else:
      return 0

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
