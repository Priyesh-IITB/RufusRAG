from setuptools import setup, find_packages

setup(
    name="rufus",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "aiohttp",
        "beautifulsoup4",
        "pyyaml",
        "google-generativeai",
        "googlesearch-python",
        "numpy",
    ],
    entry_points={
        "console_scripts": [],
    }
)
