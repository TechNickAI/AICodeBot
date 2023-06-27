# Contributions Welcome

We need your help to make AICodeBot better.

We welcome contributions of all kinds, including code, documentation, bug reports, feature requests, and more. We use [GitHub issues](https://github.com/novara-ai/AICodeBot/issues) to track all of these.

In particular, we need help with:

* Improving the intelligence of the responses from the language model
  * Better [prompts](prompts)
  * Explore different language models
  * Self verifying/validating responses. Reflection.
* Building additional commands in the [CLI](aicodebot/cli.py)
  * `aicodebot code` - translate natural language to local changes in code
  * `aicodebot learn` - Read the local codebase or online documentation and use that to improve the quality of the answers.
* Adding additional interfaces
  * GitHub Action
  * The @aicodebot mention
* Documentation. We don't even have a docs folder yet. Setting up an automated process for this.
* YouTube walk-throughs of using AICodeBot

## Code Contributions

We use the normal fork/pull request workflow. If you're not familiar with this, check out [this guide](https://docs.github.com/en/get-started/quickstart/contributing-to-projects)

## Local Development Environment

1. Clone the repository

```bash
git clone git@github.com:novara-ai/aicodebot.git
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

4. **Use aicodebot to build aicodebot** 😎 Doing so can be a little tricky, when you are developing from the local repo you can run `python -m aicodebot.cli $command` to run/test your changes. This will use the local version of aicodebot instead of the version installed via pip

```
python -m aicodebot.cli --help
```

Pro-tips:

* You can use the -v flag for all commands to get more verbose output, including information about what prompts are being sent to the language model.
* Have aicodebot review your changes before you commit, with `python -m aicodebot.cli review`

### Code quality

We're obsessive about automated tooling, as you can imagine. 😎

We use pre-commit to run a bunch of checks on the code before it gets committed. After you've installed the dev requirements file with `pip install -r requirements/requirements-dev.txt`, you can run  `pre-commit install` to install the git hook. This will run the checks on every commit. If you want to run the checks manually, you can run `pre-commit run --all-files`. If you want to skip the checks, you can run `git commit --no-verify`, but it's also as part of the [GitHub Actions build workflow](.github/workflows/build.yml), so you'll get caught there.

We use [Ruff](https://github.com/astral-sh/ruff) as our main linter. Ruff runs all the other underlying favorite tools like pylint and flake8 with a centralized config. We [black](https://black.readthedocs.io/en/stable/) for formatting, and isort for imports. See [pyproject.toml](pyproject.toml) for the config.

Highly recommend you set up your editor to run all of these on each file save, it saves a lot of time.

### Testing

Install the test dependencies with
`pip install -r requirements/requirements-test.txt` - this is what is used in the [Github Actions workflow](https://github.com/novara-ai/AICodeBot/actions), you can look at the [build workflow](.github/workflows/build.yml) to see how to run the tests.

We use `pytest` for testing. It will skip some tests if OPENAI_API_KEY is not set, so to test everything, run pytest with your OPENAI_API_KEY set.

```bash
OPENAI_API_KEY=your_key pytest
```

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
