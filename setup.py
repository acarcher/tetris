try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Alexander Archer',
    'url': 'github.com/acarcher/NAME',
    'download_url': 'Where to download it.',
    'author_email': 'alex@acarcher.dev',
    'version': '0.1',
    'install_requires': ['nose2, flake8'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)
