from setuptools import setup, find_packages

setup(
    name='eppoPynder',
    version='1.0.0',
    description='A Wrapper for EPPO Codes',
    long_description='The eppoPynder package provides a wrapper around the European and Mediterranean Plant Protection Organization (EPPO) database public APIs. It enables users to retrieve EPPO-related data through searches across the entire EPPO database or by utilizing specific services, including categorization, taxonomy, and more. The package also includes a data wrangling function to integrate taxonomy and rank information, and a function that returns the list of member countries for each Regional Plant Protection Organization acronym which is used in the EPPO database.',
    long_description_content_type='text/markdown',
    author='Luca Belmonte, Dayana Stephanie Buzle, Rafael Vieira, Agata Kaczmarek',
    author_email='luca.belmonte@efsa.europa.eu',
    maintainer='Luca Belmonte',
    maintainer_email='luca.belmonte@efsa.europa.eu',
    url='https://github.com/openefsa/eppoPynder',
    project_urls={
        'Luca Belmonte ORCID': 'https://orcid.org/0000-0002-7977-9170',
        'Dayana Stephanie Buzle ORCID': 'https://orcid.org/0009-0003-2990-7431',
        'Rafael Vieira ORCID': 'https://orcid.org/0009-0009-0289-5438',
        'Agata Kaczmarek ORCID': 'https://orcid.org/0000-0002-7463-5821',
    },
    license='GPL-3.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy>=2.1.3',
        'pandas>=2.2.3',
        'python-dateutil>=2.9.0.post0',
        'requests>=2.32.3',
        'certifi>=2024.8.30',
        'charset-normalizer>=3.4.0',
        'idna>=3.10',
        'urllib3>=2.2.3',
        'pytz>=2024.2',
        'tzdata>=2024.2',
        'python-dotenv>=1.0.0'
    ],
    extras_require={
        'dev': [
            'setuptools>=75.3.0',
            'coverage>=7.6.4',
            'colorama>=0.4.6',
            'pytest>=8.3.3',
            'iniconfig>=2.0.0',
            'pluggy>=1.5.0',
            'packaging>=24.1',
            'six>=1.16.0'
        ],
    },
    python_requires='>=3.11'
    )
