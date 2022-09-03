from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    lic = f.read()

setup(
    name='aruodas-bot',
    version='0.1.0',
    packages=['aruodas_package'],
    install_requires=['pandas', 'bs4', 'beautifulsoup4', 'sqlalchemy', 'selenium', 'psycopg2'],
    url='https://github.com/laujak/aruodas-bot',
    license=lic,
    author='Laurynas',
    author_email='laurynas.jakstas@gmail.com',
    description='Lithuanian flat sale page web crawler.',
    long_description=readme
)
