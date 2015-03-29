from setuptools import setup
import multiprocessing

setup(name='github_conglomerate',
      version='0.0.0',
      scripts=['scripts/get-repo-data'],
      test_suite='nose.collector',
      tests_require=[
        'nose',
        'mock'
      ]
)
