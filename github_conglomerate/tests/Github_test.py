import datetime
import unittest

import dateutil.parser
from mock import patch, MagicMock

from github_conglomerate.Github import RepoParser

class TestOrgParser(unittest.TestCase):
  pass

class TestRepoParser(unittest.TestCase):

  def uninitialised_repo(self):
    return RepoParser.__new__(RepoParser)

  @patch('github_conglomerate.Github.RepoParser.get_release_data')
  def test_init(self, release_mock):
    repo_mock = MagicMock()
    repo_mock.description = u'Takes a jinja2 template and some json and sends an email'
    repo_mock.forks_count = 1
    repo_mock.html_url = u'https://github.com/sanger-pathogens/json2email'
    repo_mock.name = u'json2email'
    repo_mock.stargazers_count = 1
    repo_mock.updated_at = datetime.datetime(2015, 3, 28, 16, 58, 12)
    repo_mock.url = u'https://api.github.com/repos/sanger-pathogens/json2email'

    repo = RepoParser(repo_mock)
    self.assertEqual(repo.name, u'json2email')
    self.assertEqual(
      repo.description,
      u'Takes a jinja2 template and some json and sends an email'
    )
    self.assertEqual(
      repo.html_url,
      u'https://github.com/sanger-pathogens/json2email'
    )
    self.assertEqual(
      repo.updated_at,
      datetime.datetime(2015, 3, 28, 16, 58, 12)
    )
    self.assertEqual(repo.stargazers_count, 1)
    self.assertEqual(repo.forks_count, 1)

    release_mock.assert_called_once_with(
      u'https://api.github.com/repos/sanger-pathogens/json2email'
    )

  @patch('github_conglomerate.Github.requests.get')
  def test_get_release_data(self, requests_mock):
    response_mock = MagicMock()
    response_mock.json.return_value = [
      {
        'created_at': u'2015-03-28T16:58:12Z',
        'tag_name': u'release/0.0.6'
      },
      {
        'created_at': u'2015-03-25T18:05:31Z',
        'tag_name': u'release/0.0.4'
      }
    ]

    requests_mock.return_value = response_mock

    repo = self.uninitialised_repo()
    repo.get_release_data(
      u'https://api.github.com/repos/sanger-pathogens/json2email'
    )

    self.assertEqual(repo.release_count, 2)
    self.assertEqual(
      repo.last_released,
      dateutil.parser.parse(u'2015-03-28T16:58:12Z')
    )
    self.assertEqual(repo.latest_release, u'release/0.0.6')
