import requests
import dateutil.parser

from github import Github


class ConglomerateParser(object):

  def __init__(self, orgs, api_token=None):
    self.orgs = None
    self.api_token = api_token
    self.get_orgs(orgs, api_token)

  def get_orgs(self, orgs, api_token):
    self.orgs = [OrgParser(org, api_token) for org in orgs]

  def to_dict(self):
    def flatten_lists(lists):
      # [[1,2,3], [4,5], [6], []] => [1,2,3,4,5,6]
      return [e for l in lists for e in l]
    org_repos = [org.to_dict()['repos'] for org in self.orgs]
    return {
      'repos': flatten_lists(org_repos)
    }

class OrgParser(object):

  def __init__(self, org_name, api_token=None):
    self.name = org_name
    self.api_token = api_token
    self.repos = None
    self.get_repos(self.name, self.api_token)

  def get_repos(self, org_name, api_token):
    github_api = Github(api_token) if api_token else Github()
    user = github_api.get_user(org_name)
    repos = user.get_repos()
    self.repos = [RepoParser(repo, api_token) for repo in repos]

  def to_dict(self):
    repos = [repo.to_dict() for repo in self.repos]
    def add_org_name(repo):
      repo['organisation'] = self.name
      return repo
    return {
      'repos': map(add_org_name, repos)
    }

class RepoParser(object):

  def __init__(self, repo, api_token=None):
    self.api_token = api_token
    self.name = repo.name
    self.description = repo.description
    self.html_url = repo.html_url
    self.created_at = repo.created_at
    self.updated_at = repo.updated_at
    self.stargazers_count = repo.stargazers_count
    self.forks_count = repo.forks_count
    self.release_count = None
    self.last_released = None
    self.latest_release = None
    self.get_release_data(repo.url, api_token)

  def get_release_data(self, url, api_token):
    releases_url = '/'.join([url, 'releases'])
    if api_token:
      headers = {'Authorization': 'token %s' % api_token}
    else:
      headers = {}
    releases_data = requests.get(releases_url, headers=headers).json()
    self.release_count = len(releases_data)
    def created_at(release):
      date_string = release['created_at']
      return dateutil.parser.parse(date_string)
    if releases_data:
      latest_release = sorted(releases_data, key=created_at)[-1]
      self.last_released = created_at(latest_release)
      self.latest_release = latest_release['tag_name']
    else:
      # There haven't been any releases (yet)
      self.last_released = None
      self.latest_release = None

  def to_dict(self):
    params_to_return = [
      "name",
      "description",
      "html_url",
      "created_at",
      "updated_at",
      "stargazers_count",
      "forks_count",
      "release_count",
      "last_released",
      "latest_release"
    ]
    return {
      param: self.__getattribute__(param) for param in params_to_return
    }
