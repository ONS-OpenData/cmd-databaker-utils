from distutils.core import setup
setup(
  name = 'databakerUtils',
  packages = ['databakerUtils'],
  version = '0.1',
  description = 'Some additional utilities for using databaker with ONS digital publishing',
  author = 'Michael Adams',
  author_email = 'michael.adams@ons.gov.uk',
  url = 'https://github.com/ONS-OpenData/databakerUtils',
  download_url = 'https://github.com/ONS-OpenData/databakerUtils/archive/0.1.tar.gz',
  keywords = ['databaker', 'addon', 'utility'],
  classifiers = [],
  include structures/*.py
)
