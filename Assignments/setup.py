from setuptools import setup, find_packages

setup(
    name="techshop",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'pyodbc',
    ],
    python_requires='>=3.8',
) 