from setuptools import find_packages, setup
from Catow.version import get_version

CLASSIFIERS = """
Development Status :: 3 - Alpha
License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)
Operating System :: OS Independent
Framework :: FastAPI
Programming Language :: Python :: 3.8
Programming Language :: Python :: Implementation :: PyPy
""".strip().splitlines()

def get_long_description():
      with open('README.md','r') as file:
            return file.read()


def get_requirements():
      with open('requirements.txt','r') as file:
            return file.readlines()


setup(name='camunda-topic-watcher',
      version=get_version(),
      classifiers=CLASSIFIERS,
      description='Camunda Topic Watcher triggering a HTTP endpoint when finding a process instance at a defined topic.',
      author='Markus Stahl',
      packages=find_packages(),
      install_requires=[
            get_requirements()
      ],
      long_description=get_long_description(),
      long_description_content_type='text/markdown',
      url='https://github.com/Noordsestern/catow',
      zip_safe=False)
