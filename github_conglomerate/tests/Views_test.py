import unittest

from datetime import datetime

from github_conglomerate.Views import Repos

class TestRepos(unittest.TestCase):

  def uninitialised_repos(self):
    return Repos.__new__(Repos)

  def test_load_json(self):

    json_data = """\
{
  "created_at": "2015-03-30T23:26:03",
  "repos": [
    {
      "created_at": "2014-04-30T09:44:21",
      "description": "de novo virus assembler of Illumina paired reads",
      "forks_count": 1,
      "html_url": "https://github.com/sanger-pathogens/iva",
      "last_released": "2015-03-27T11:36:49",
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
      "last_released": "2015-03-28T16:58:12",
      "latest_release": "release/0.0.6",
      "name": "json2email",
      "organisation": "sanger-pathogens",
      "release_count": 2,
      "stargazers_count": 1,
      "updated_at": "2015-03-28T16:58:12"
    }
  ]
}"""

    repos = self.uninitialised_repos()
    repos.load_json(json_data)

    self.assertEqual(repos.created_at, datetime(2015, 3, 30, 23, 26, 3))

    expected_data = [
      {
        "created_at": datetime(2014, 4, 30, 9, 44, 21),
        "description": "de novo virus assembler of Illumina paired reads",
        "forks_count": 1,
        "html_url": "https://github.com/sanger-pathogens/iva",
        "last_released": datetime(2015, 3, 27, 11, 36, 49),
        "latest_release": "v0.11.5",
        "name": "iva",
        "organisation": "sanger-pathogens",
        "release_count": 19,
        "stargazers_count": 2,
        "updated_at": datetime(2015, 3, 27, 11, 36, 49)
      },
      {
        "created_at": datetime(2015, 3, 25, 11, 16, 25),
        "description": "Takes a jinja2 template and some json and sends an email",
        "forks_count": 1,
        "html_url": "https://github.com/sanger-pathogens/json2email",
        "last_released": datetime(2015, 3, 28, 16, 58, 12),
        "latest_release": "release/0.0.6",
        "name": "json2email",
        "organisation": "sanger-pathogens",
        "release_count": 2,
        "stargazers_count": 1,
        "updated_at": datetime(2015, 3, 28, 16, 58, 12)
      }
    ]

    self.assertEqual(repos.data, expected_data)

  def test_sorted_by(self):
    repos = self.uninitialised_repos()
    data = [
      {
        'foo': 'foo',
        'score': 1
      },
      {
        'foo': 'bar',
        'score': 1
      },
      {
        'foo': 'baz',
        'score': 2
      },
      { 'another': 'thing' }
    ]

    expected = [
      {
        'foo': 'baz',
        'score': 2
      },
      {
        'foo': 'foo',
        'score': 1
      },
      {
        'foo': 'bar',
        'score': 1
      },
      { 'another': 'thing' }
    ]

    self.assertEqual(data[0]['foo'], 'foo', "Original data unaffected")
    self.assertEqual(repos.sorted_by(data, 'score'), expected)

    expected = [
      {
        'foo': 'baz',
        'score': 2
      },
      {
        'foo': 'bar',
        'score': 1
      },
      {
        'foo': 'foo',
        'score': 1
      },
      { 'another': 'thing' }
    ]

    self.assertEqual(repos.sorted_by(data, 'score', 'foo'), expected)

  def test_filter_contains(self):
    repos = self.uninitialised_repos()
    data = [
      {
        'foo': 'foo',
        'score': 1
      },
      {
        'foo': 'bar',
        'score': 1
      },
      {
        'foo': 'baz',
        'another': 'BAZ',
        'score': 2
      },
      { 'another': 'baz' }
    ]

    expected = [
      {
        'foo': 'bar',
        'score': 1
      },
      {
        'foo': 'baz',
        'another': 'BAZ',
        'score': 2
      }
    ]

    self.assertEqual(data[0]['foo'], 'foo', "Original data unaffected")
    self.assertEqual(repos.filter_contains(data, foo='a'), expected)

    expected = [
      {
        'foo': 'baz',
        'another': 'BAZ',
        'score': 2
      }
    ]

    self.assertEqual(
      repos.filter_contains(data, foo='a', another='A'),
      expected
    )

  def test_join(self):
    repos = self.uninitialised_repos()

    data = [
      {
        'foo': 'foo',
        'score': 1
      },
      {
        'foo': 'bar',
        'score': 1
      }
    ]

    other_data = [
      {
        'foo': 'bar',
        'score': 1
      },
      {
        'foo': 'baz',
        'score': 2
      },
      { 'another': 'thing' }
    ]

    expected = [
      {
        'foo': 'foo',
        'score': 1
      },
      {
        'foo': 'bar',
        'score': 1
      },
      {
        'foo': 'baz',
        'score': 2
      },
      { 'another': 'thing' }
    ]

    self.assertItemsEqual(repos.join(data, other_data), expected)
