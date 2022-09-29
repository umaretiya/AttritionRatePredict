import setuptools

with open('README.md','r',encoding="utf-8") as f:
    long_description = f.read()
    
__version__ = "0.0.1"

REPO_NAME = "AttritionRatePredict"
AUTHOR_USER_NAME = "umaretiya"
PROJECT_REPO = "attritionRate"
AUTHOR_EMAIL = 'umaretiya@gmail.com'

setuptools.setup(
    name=PROJECT_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small Machine Learning Project with Scikit-Learn",
    long_description=long_description,
    long_description_content = "text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"":"project"},
    packages=setuptools.find_packages(where="project"),
)