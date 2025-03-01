from setuptools import setup, find_packages

setup(
    name="rpa_automation",
    version="1.0.0",
    packages=find_packages(),
)

# to install the package, run the following command in the terminal:
# pip install -e .
# This will install the package in editable mode, so you can make changes to the code and test them without reinstalling the package.

# To uninstall the package, run the following command:
# pip uninstall rpa_automation
# This will uninstall the package from your environment.

# To run the bot, you can use the following command:
# python -m rpa_automation
# This will execute the main function in the rpa_automation package.

# To run the tests, you can use the following command:
# pytest
# This will run all the tests in the tests folder.

# To run the tests with coverage, you can use the following command:
# pytest --cov=rpa_automation
# This will run all the tests in the tests folder and show the coverage report.

# To generate the coverage report in HTML format, you can use the following command:
# pytest --cov=rpa_automation --cov-report html
# This will generate an HTML report in the htmlcov folder.

# To run the linter, you can use the following command:
# flake8
# This will check the code for linting errors.

# To run the formatter, you can use the following command:
# black .
# This will format the code according to the Black code style.