from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-rasterimport',
	version=version,
	description="Allows importing raster data into ckan through a wcst service",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Alex Dumitru',
	author_email='dumitru@rasdaman.com',
	url='http://rasdaman.com',
	license='MIT',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.rasterimport'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		"python-magic",
        "GDAL"
	],
	entry_points=\
	"""
        [ckan.plugins]
	# Add plugins here, eg
		rasterimport=ckanext.rasterimport.plugin:RasterImportPlugin
	""",
)
