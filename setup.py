from setuptools import setup, find_packages

setup(
    name="personal-portfolio-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "mangum",
        "sqlalchemy",
        "python-dotenv",
        "pydantic",
        "click",
    ],
    entry_points={
        'console_scripts': [
            'portfolio-cli=src.cli:cli',
        ],
    },
) 