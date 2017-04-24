try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Rent Reckoner Service',
    'author': 'Peter Reveland',
    'url': '',
    'download_url': '',
    'author_email': 'reveland92@gmail.com',
    'version': '1.0',
    'install_requires': ['nose'],
    'packages': ['rent_reckoner'],
    'scripts': [],
    'name': 'rent-reckoner-service'
}

setup(**config)
