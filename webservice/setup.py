from distutils.core import setup

setup(
    name='scanui',
    version='0.0.1',
    author='Ronald Bister',
    author_email='mini.pelle@gmail.com',
    packages=['scanui', 'scanui.test'],
    url='http://pypi.python.org/pypi/scanui/',
    license='LICENSE.txt',
    description='A small web interface for scan to enable you to run scans, parse and compare the results in your browser or via a Restful API',
    long_description=open('README.md').read(),
)
