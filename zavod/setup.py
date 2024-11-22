from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()


setup(
    name="zavod",
    version="0.8.0",
    description="Data factory for followthemoney data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="data mapping identity followthemoney etl parsing",
    author="OpenSanctions",
    author_email="friedrich@opensanctions.org",
    url="https://github.com/opensanctions/opensanctions",
    license="MIT",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    namespace_packages=[],
    include_package_data=True,
    package_data={"": ["zavod/data/*", "zavod/py.typed"]},
    zip_safe=False,
    install_requires=[
        "followthemoney == 3.7.*",
        "nomenklatura[leveldb,tantivy,duckdb] @ git+https://github.com/opensanctions/nomenklatura.git@duckdb-2",
        "plyvel == 1.5.1",
        "rigour == 0.7.0",
        "datapatch >= 1.1,< 1.3",
        "fingerprints == 1.2.*",
        "certifi",
        "colorama",
        "google-cloud-storage",
        "jinja2",
        "types-jinja2",
        "lxml == 5.3.0",
        "openpyxl == 3.1.5",
        "orjson == 3.10.11",
        "ijson > 3.2, < 4.0",
        "pantomime == 0.6.1",
        "pdfplumber == 0.11.4",
        "prefixdate",
        "psycopg2-binary",
        "pyicu == 2.14",
        "pywikibot==9.5.0",
        "openai >= 1.33.0, < 2.0.0",
        "requests[security]",
        "requests_oauthlib",
        "sqlalchemy[mypy]",
        "structlog",
        "xlrd == 2.0.1",
        "cryptography",
        "duckdb < 2.0.0",
    ],
    tests_require=[],
    entry_points={
        "console_scripts": [
            "zavod = zavod.cli:cli",
        ],
    },
    extras_require={
        "dev": [
            "black==24.10.0",
            "wheel>=0.29.0",
            "twine",
            "mypy",
            "flake8>=2.6.0",
            "pytest",
            "ruff>=0.4.0,<1.0.0",
            "pytest-cov",
            "lxml-stubs == 0.5.1",
            "coverage>=4.1",
            "requests-mock",
            "types-setuptools",
            "types-requests",
            "types-openpyxl",
            "types-google-cloud-ndb",
            "types-redis",
        ],
        "docs": [
            "pillow",
            "cairosvg",
            "mkdocs",
            "mkdocstrings[python]",
            "mkdocs-material",
        ],
    },
)
