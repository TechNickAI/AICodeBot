# Contributions Welcome

## The Stack

### Test and Build

[![GitHub Build](https://github.com/TechNickAI/AICodeBot/actions/workflows/build.yml/badge.svg)](https://github.com/TechNickAI/AICodeBot/actions?query=build)
[![CodeCov](https://codecov.io/gh/TechNickAI/AICodeBot/branch/main/graph/badge.svg)](https://codecov.io/gh/TechNickAI/AICodeBot)
[![Pytest](https://img.shields.io/badge/%F0%9F%A7%AA-Pytest-blue)](https://docs.pytest.org/en/stable/contents.html)

### Code Quality

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Super Linter](https://github.com/TechNickAI/AIcodeBot/actions/workflows/linter.yml/badge.svg)](https://github.com/TechNickAI/AIcodeBot/actions/workflows/linter.yml)

### Infrastructure

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Open AI](https://img.shields.io/badge/OpenAI-412991.svg?logo=OpenAI&logoColor=white)](https://openai.com)

## How to Contribute

We need your help to make AICodeBot better.

We welcome contributions of all kinds, including code, documentation, bug reports, feature requests, and more. We use [GitHub issues](https://github.com/TechNickAI/AICodeBot/issues) to track all of these.

In particular, we need help with:

* Improving the intelligence of the responses from the language model
  * Better [prompts](aicodebot/prompts)
  * Explore different language models
  * Self verifying/validating responses. Reflection.
* Building additional commands in the [CLI](aicodebot/cli.py)
  * `aicodebot sidekick` - translate natural language to local changes in code
  * `aicodebot setup` - walk users through first time set up. Collecting API keys, etc.
* Adding additional interfaces
  * GitHub Action to run AICodeBot on a pull request or commit
  * The @aicodebot mention to allow you to interact with AICodeBot in a GitHub issue or pull request, or assign it a task.
* Documentation. Setting up an automated process for this would be great
* YouTube walk-throughs of using AICodeBot

See the [issues](https://github.com/TechNickAI/AICodeBot/issues) for an up-to-date list of tasks that need help.

## Code Contributions

We use the normal fork/pull request workflow. If you're not familiar with this, check out [this guide](https://docs.github.com/en/get-started/quickstart/contributing-to-projects)

## Local Development Environment

1. Clone the repository

```bash
git clone git@github.com:gorillanania/AICodeBot.git
```

2. Set up a virtual environment (recommend using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/))

```bash
# We use Python 3.11
mkvirtualenv --python=`which python3` AICodeBot
```

3. Install the dependencies:
Note that [requirements.txt](requirements/requirements.txt) is for production dependencies, and [requirements-dev.txt](requirements/requirements-dev.txt) is for development dependencies.

```bash
pip install -r requirements/requirements-dev.txt
```

Note: We use [pip-tools](https://pypi.org/project/pip-tools/) to manage our the production dependencies, so if you want to add a new dependency, add it to [requirements.in](requirements/requirements.in) and then run `pip-compile requirements/requirements.in` to update [requirements.txt](requirements/requirements.txt).

4. **Use aicodebot to build aicodebot** 😎 Doing so can be a little tricky, when you are developing from the local repository you can run `python -m aicodebot.cli $command` to run/test your changes. This will use the local version of aicodebot instead of the version installed via pip

```bash
python -m aicodebot.cli --help
```

Pro-tips:

* You can use the -v flag for all commands to get more verbose output, including information about what prompts are being sent to the language model.
* Have aicodebot review your changes before you commit, with `python -m aicodebot.cli review`

### Code quality

We're obsessive about automated tooling, as you can imagine. 😎

We use pre-commit to run a bunch of checks on the code before it gets committed. After you've installed the dev requirements file with `pip install -r requirements/requirements-dev.txt`, you can run  `pre-commit install` to install the git hook. This will run the checks on every commit.

If you want to run the checks manually, you can run `pre-commit run --all-files`. If you want to skip the checks, you can run `git commit --no-verify`, but it's also as part of the [GitHub Actions build workflow](.github/workflows/build.yml), so you'll get caught there.

We use [Ruff](https://github.com/astral-sh/ruff) as our main linter. Ruff runs all the other underlying favorite tools like pylint and flake8 with a centralized config. We [black](https://black.readthedocs.io/en/stable/) for formatting, and isort for imports. See [pyproject.toml](pyproject.toml) for the config.

Highly recommend you set up your editor to run all of these on each file save, it saves a lot of time.

### Testing

Install the test dependencies with
`pip install -r requirements/requirements-test.txt` - this is what is used in the [GitHub Actions workflow](https://github.com/TechNickAI/AICodeBot/actions), you can look at the [build workflow](.github/workflows/build.yml) to see how to run the tests.

We use `pytest` for testing. It will skip some tests if OPENAI_API_KEY is not set, so to test everything, run pytest with your OPENAI_API_KEY set.

```bash
OPENAI_API_KEY=your_key pytest
```

## Releases

AICodeBot uses a GitHub Actions workflow for releases. This workflow is designed to watch for tags that start with 'v'. When such a tag is detected, the workflow triggers a series of actions:

1. Package Build: The codebase is built into a distributable format.
1. Upload to PyPI: The built package is uploaded to the Python Package Index (PyPI), making it available for others to install via pip.
1. Create a GitHub Release: A new release is created on GitHub, providing a versioned snapshot of the codebase. This release will be tagged with the triggering 'v' tag.

To initiate a new release, simply push a new tag that starts with 'v', followed by the version number (for example, 'v1.0.0'). Please ensure that your version numbers follow the [Semantic Versioning guidelines](https://semver.org/).

To learn more about the release process, you can review the [PyPI release workflow](.github/workflows/pypi_release.yml).

## Coding Principles

Borrowed from the [zen of python](http://c2.com/cgi/wiki?PythonPhilosophy), with a couple of changes.

```text
1. **Readability is the number 1 code quality metric**.
2. Beautiful is better than ugly.
3. Explicit is better than implicit.
4. Simple is better than complex.
5. Complex is better than complicated.
6. Flat is better than nested.
7. Sparse is better than dense.
8. Special cases aren't special enough to break the rules.
    * Although practicality beats purity.
9. Errors should never pass silently.
    * Unless explicitly silenced.
10. In the face of ambiguity, refuse the temptation to guess.
11. There should be one -- and preferably only one -- obvious way to do it.
12. Now is better than never.
```
