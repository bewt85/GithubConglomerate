import requests
import dateutil.parser

from github import Github


class OrgParser(object):

  def get_repos(self, org_name):
    github_api = Github()
    user = github_api.get_user(org_name)
    repos = user.get_repos()
    self.repos = map(RepoParser, repos)
    self.name = org_name

  def to_dict(self):
    repos = [repo.to_dict() for repo in self.repos]
    def add_org_name(repo):
      repo['organisation'] = self.name
      return repo
    return {
      'repos': map(add_org_name, repos)
    }

class RepoParser(object):

  def __init__(self, repo):
    self.name = repo.name
    self.description = repo.description
    self.html_url = repo.html_url
    self.updated_at = repo.updated_at
    self.stargazers_count = repo.stargazers_count
    self.forks_count = repo.forks_count
    self.release_count = None
    self.last_released = None
    self.latest_release = None
    self.get_release_data(repo.url)

  def get_release_data(self, url):
    releases_url = '/'.join([url, 'releases'])
    releases_data = requests.get(requests).json()
    self.release_count = len(releases_data)
    def created_at(release):
      date_string = release['created_at']
      return dateutil.parser.parse(date_string)
    latest_release = sorted(releases_data, key=created_at)[-1]
    self.last_released = created_at(latest_release)
    self.latest_release = latest_release['tag_name']

  def to_dict(self):
    params_to_return = [
      "name",
      "description",
      "html_url",
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
