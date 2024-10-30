# setup.py
from setuptools import setup, find_packages

setup(
    name="pyboot",
    version="0.1.0",
    packages=find_packages(include=['backend', 'backend.*']),
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "flask-cors",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-flask",
            "pytest-cov",
        ]
    }
)