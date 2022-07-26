from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in building_block_retail/__init__.py
from building_block_retail import __version__ as version

setup(
	name="building_block_retail",
	version=version,
	description="Building Block Retail",
	author="Thirvusoft",
	author_email="thivusoft@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
