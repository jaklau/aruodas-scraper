from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    lic = f.read()

setup(
    name='aruodas-bot',
    version='0.1.0',
    packages=['aruodas_package'],
    install_requires=['pandas', 'beautifulsoup4'],
    url='',
    license=lic,
    author='Laurynas',
    author_email='laurynas.jakstas@gmail.com',
    description='Lithuanian flat sale page web crawler.',
    long_description=readme
)
