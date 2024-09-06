from setuptools import setup, find_packages

setup(
    name="config_handler",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "PyYAML",
        "configparser"
    ],
    entry_points={
        "console_scripts": [
            "config-handler=config_handler.config_reader:main"
        ]
    },
    description="A module to read configurations from various formats and export or set in OS environment",
)
