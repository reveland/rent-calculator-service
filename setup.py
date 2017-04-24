try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Rent Calculator Service',
    'author': 'Peter Reveland',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'reveland92@gmail.com',
    'version': '1',
    'install_requires': ['nose'],
    'packages': ['rent_calculator_service'],
    'scripts': [],
    'name': 'RentCalculatorService'
}

setup(**config)
