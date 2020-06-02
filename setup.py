import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jdcv19",
    version="0.0.1",
    author="Jen Dobson",
    author_email="jendobson@gmail.com",
    description="Visualization Tools for San Diego Covid-19 Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_namespace_packages(where="src"),
    include_package_data=True,
    package_data = {
        '': ['*.shp','*.shx','*.dbf','*.SHX','*.shp'],
    },
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)