# from distutils.core import  setup
from setuptools import setup, find_packages
setup(name='mytools',
	version='0.4.0',
	author='Non-Existent987',
	packages=find_packages(),
	install_requires = [ "geopandas",'geographiclib','kml2geojson','pyshp','python-docx'] )