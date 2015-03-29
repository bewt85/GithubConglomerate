import unittest

from mock import patch
from StringIO import StringIO

from github_conglomerate.Config import ConfigParser

class TestConfig(unittest.TestCase):

  def environment_get_mock(self, fake_env):
    def get(key):
      return fake_env.get(key)
    return get

  @patch('github_conglomerate.Config.os.environ')
  @patch('github_conglomerate.Config.open', create=True)
  def test_from_file(self, open_mock, environ_mock):
    parser = ConfigParser()

    fake_config = """\
---
  github_token: secret_github_token
  github_organisations:
    - sanger-pathogens
    - wtsi-hgi
  aws_token: secret_aws_token
"""
    fake_config_file = StringIO(fake_config)
    open_mock.return_value.__enter__.return_value = fake_config_file

    environ_mock.get.side_effect = self.environment_get_mock({})

    parser.add_from_file('/home/file.yaml')

    self.assertEqual(parser.github_token, 'secret_github_token')
    self.assertEqual(parser.aws_token, 'secret_aws_token')
    self.assertItemsEqual(
      parser.organisations,
      ['sanger-pathogens', 'wtsi-hgi']
    )

  @patch('github_conglomerate.Config.os.environ')
  @patch('github_conglomerate.Config.open', create=True)
  def test_from_file_add_data(self, open_mock, environ_mock):
    parser = ConfigParser()

    parser.github_token = 'secret_github_token'

    fake_config = """\
---
  github_organisations:
    - sanger-pathogens
"""
    fake_config_file = StringIO(fake_config)
    open_mock.return_value.__enter__.return_value = fake_config_file

    environ_mock.get.side_effect = self.environment_get_mock({})

    parser.add_from_file('/home/file.yaml')

    self.assertEqual(parser.github_token, 'secret_github_token')
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

    self.assertEqual(parser.github_token, 'secret_github_token')
    self.assertItemsEqual(
      parser.organisations,
      ['sanger-pathogens', 'wtsi-hgi']
    )

  @patch('github_conglomerate.Config.os.environ')
  @patch('github_conglomerate.Config.open', create=True)
  def test_from_file_update_data(self, open_mock, environ_mock):
    parser = ConfigParser()

    parser.github_token = 'secret_github_token'

    fake_config = """\
---
    github_token: another_github_token
"""
    fake_config_file = StringIO(fake_config)
    open_mock.return_value.__enter__.return_value = fake_config_file

    environ_mock.get.side_effect = self.environment_get_mock({})

    parser.add_from_file('/home/file.yaml')

    self.assertEqual(parser.github_token, 'another_github_token')

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

    environ_mock.get.side_effect = self.environment_get_mock({})

    parser.add_from_file('/home/file.yaml')

    self.assertItemsEqual(
      parser.organisations,
      ['sanger-pathogens']
    )

  @patch('github_conglomerate.Config.os.environ')
  def test_from_enviornment(self, environ_mock):
    parser = ConfigParser()

    environ_mock.get.side_effect = self.environment_get_mock({
      'aws_token': 'secret_aws_token',
      'github_token': 'secret_github_token',
      'github_organisations': 'sanger-pathogens'
    })

    parser.add_from_environment()

    self.assertEqual(parser.aws_token, 'secret_aws_token')
    self.assertEqual(parser.github_token, 'secret_github_token')
    self.assertItemsEqual(
      parser.organisations,
      ['sanger-pathogens']
    )

  @patch('github_conglomerate.Config.os.environ')
  def test_from_enviornment_multi_org(self, environ_mock):
    parser = ConfigParser()

    environ_mock.get.side_effect = self.environment_get_mock({
      'github_organisations': 'sanger-pathogens:wtsi-hgi'
    })

    parser.add_from_environment()

    self.assertItemsEqual(
      parser.organisations,
      ['sanger-pathogens', 'wtsi-hgi']
    )

  @patch('github_conglomerate.Config.os.environ')
  def test_from_enviornment_multi_org_bad_prefix(self, environ_mock):
    parser = ConfigParser()

    environ_mock.get.side_effect = self.environment_get_mock({
      'github_organisations': ':sanger-pathogens:wtsi-hgi'
    })

    parser.add_from_environment()

    self.assertEqual(
      parser.organisations,
      ['sanger-pathogens', 'wtsi-hgi']
    )

  @patch('github_conglomerate.Config.os.environ')
  def test_from_enviornment_add_data(self, environ_mock):
    parser = ConfigParser()

    parser.organisations = ['wtsi-hgi']

    environ_mock.get.side_effect = self.environment_get_mock({
      'github_token': 'secret_github_token',
      'github_organisations': 'sanger-pathogens'
    })

    parser.add_from_environment()

    self.assertEqual(parser.github_token, 'secret_github_token')
    self.assertItemsEqual(
      parser.organisations,
      ['sanger-pathogens', 'wtsi-hgi']
    )

  @patch('github_conglomerate.Config.os.environ')
  def test_from_enviornment_update_data(self, environ_mock):
    parser = ConfigParser()

    parser.github_token = 'secret_github_token'

    environ_mock.get.side_effect = self.environment_get_mock({
      'github_token': 'another_github_token',
    })

    parser.add_from_environment()

    self.assertEqual(parser.github_token, 'another_github_token')

  @patch('github_conglomerate.Config.os.environ')
  def test_from_enviornment_duplicate(self, environ_mock):
    parser = ConfigParser()

    parser.organisations = ['sanger-pathogens']

    environ_mock.get.side_effect = self.environment_get_mock({
      'github_token': 'secret_github_token',
      'github_organisations': 'sanger-pathogens'
    })

    parser.add_from_environment()

    self.assertEqual(parser.github_token, 'secret_github_token')
    self.assertItemsEqual(
      parser.organisations,
      ['sanger-pathogens']
    )
