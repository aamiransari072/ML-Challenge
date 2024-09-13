import setuptools
from setuptools import find_packages

with open("README.md", "r", encoding = 'utf-8') as f:
    long_description = f.read()

__version__ = '0.0.0'

REPO_NAME = 'ML-Challenge'
AUTHOR_USER_NAME = 'aamiransri072'
SRC_REPO = 'featureExtractor'
AUTHOR_EMAIL = 'amirbxr2003@gmail.com'

setuptools.setup(
    name = SRC_REPO,
    version=__version__,
    author = AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description='ML Challenge',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content = "text/markdown",
    url = f'https://github/com/{AUTHOR_USER_NAME}/{REPO_NAME}',
    project_url = {
        f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues"
    },


)

