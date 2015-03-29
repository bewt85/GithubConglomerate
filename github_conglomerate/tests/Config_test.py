import unittest

from mock import patch
from StringIO import StringIO

from github_conglomerate.Config import ConfigParser

class TestConfig(unittest.TestCase):

  @patch('github_conglomerate.Config.os.environ')
  @patch('github_conglomerate.Config.open', create=True)
  def test_from_file(self, open_mock, environ_mock):
    parser = ConfigParser()

    fake_config = """\
---
  github_api_token: secret_token
  github_organisations:
    - sanger-pathogens
    - wtsi-hgi
"""
    fake_config_file = StringIO(fake_config)
    open_mock.return_value.__enter__.return_value = fake_config_file

    environ_mock = {}

    parser.add_from_file('/home/file.yaml')

    self.assertEqual(parser.api_token, 'secret_token')
    self.assertItemsEqual(
      parser.organisations,
      ['sanger-pathogens', 'wtsi-hgi']
    )

  @patch('github_conglomerate.Config.os.environ')
  @patch('github_conglomerate.Config.open', create=True)
  def test_from_file_add_data(self, open_mock, environ_mock):
    parser = ConfigParser()

    parser.api_token = 'secret_token'

    fake_config = """\
---
  github_organisations:
    - sanger-pathogens
"""
    fake_config_file = StringIO(fake_config)
    open_mock.return_value.__enter__.return_value = fake_config_file

    environ_mock = {}

    parser.add_from_file('/home/file.yaml')

    self.assertEqual(parser.api_token, 'secret_token')
    self.assertItemsEqual(
      parser.organisations,
      ['sanger-pathogens']
    )

    fake_config = """\
---
  github_organisations:
    - wtsi-hgi
"""
    fake_config_file = StringIO(fake_config)
    open_mock.return_value.__enter__.return_value = fake_config_file

    parser.add_from_file('/home/file.yaml')

    self.assertEqual(parser.api_token, 'secret_token')
    self.assertItemsEqual(
      parser.organisations,
      ['sanger-pathogens', 'wtsi-hgi']
    )

  @patch('github_conglomerate.Config.os.environ')
  @patch('github_conglomerate.Config.open', create=True)
  def test_from_file_update_data(self, open_mock, environ_mock):
    parser = ConfigParser()

    parser.api_token = 'secret_token'

    fake_config = """\
---
    github_api_token: another_token
"""
    fake_config_file = StringIO(fake_config)
    open_mock.return_value.__enter__.return_value = fake_config_file

    environ_mock = {}

    parser.add_from_file('/home/file.yaml')

    self.assertEqual(parser.api_token, 'another_token')

  @patch('github_conglomerate.Config.os.environ')
  @patch('github_conglomerate.Config.open', create=True)
  def test_from_file_duplicate(self, open_mock, environ_mock):
    parser = ConfigParser()

    parser.organisations = ['sanger-pathogens']

    fake_config = """\
---
  github_organisations:
    - sanger-pathogens
"""
    fake_config_file = StringIO(fake_config)
    open_mock.return_value.__enter__.return_value = fake_config_file

    environ_mock = {}

    parser.add_from_file('/home/file.yaml')

    self.assertItemsEqual(
      parser.organisations,
      ['sanger-pathogens']
    )
