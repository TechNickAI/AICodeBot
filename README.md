# AI Code Bot 🤖

## Your AI-powered coding companion

AICodeBot is a coding assistant designed to make your coding life easier. With capabilities to perform code reviews, manage dependencies, and even suggest improvements, think of it as your AI version of a pair programmer - a team member that accelerates the pace of development and helps you write better code.

There are lot of ways to use AICodeBot that we have planned. To start, it's a [command-line tool](https://pypi.org/project/aicodebot/) that you can use to generate commit messages, debug code, and review code. In the future, we plan to integrate it with GitHub Actions, Slack, and other tools to make it even more useful.

⚠️ Status: This project is in its infancy with very limited features, but it already improves the software development workflow, and has a healthy Roadmap of features. ⬇

⚠️ It uses OpenAI's ChatGPT large language models, which can hallucinate and be confidently wrong. Sometimes it does dumb things, which is why we have you confirm before it does anything permanent.

We're using AICodeBot to build AICodeBot, and it's getting better all the time.️ We're looking for contributors to help us build it out. See [CONTRIBUTING](CONTRIBUTING.md) for more.

### What it's not

`aicodebot` is a tool for developers, not a replacement for them. It's not going to replace your job, but it will make your job easier and more fun. It's not going to take over the world, but it will help us build a better one. See the *Alignment* section below for more.

It's also not a "build a website for me in 5 minutes" tool that takes a well constructed prompt and builds a scaffold for you. There are [other tools](https://github.com/AntonOsika/gpt-engineer) for that, Instead, AICodeBot is built to work with existing code bases and help you improve them at the git-commit level. It's designed to multiply the effectiveness of capable engineers.

## Current features - how you can use it

### AI-Assisted Git Commit

`aicodebot commit` will run pre-commit for you to check syntax, and then generate a commit message for you based on the changes you've made. It will also commit the changes for you once everything checks out.

### AI-Assisted Debugging

`aicodebot debug $command` will run the command and capture the log message. It will then try to figure out what's going on from the error message and suggest a fix.

### AI-Assisted Code Review

`aicodebot review` will run a code review on your code and suggest improvements. By default it will look at [un]staged changes, and you can also supply a specific commit hash to review. It also suggests best practices for code improvement.

## Getting Started

[![PyPI version](https://badge.fury.io/py/aicodebot.svg)](https://badge.fury.io/py/aicodebot)

To install AICodeBot, run:

`pip install aicodebot`

And then run `aicodebot --help` to get started.

```bash
Usage: aicodebot [OPTIONS] COMMAND [ARGS]...

Options:
  -V, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  alignment  Get a message about Heart-Centered AI Alignment ❤ + 🤖.
  commit     Generate a commit message based on your changes.
  debug      Run a command and debug the output.
  fun-fact   Get a fun fact about programming and artificial intelligence.
  review     Do a code review, with [un]staged changes, or a specified...
  ```

### Open AI key setup

The first time you run it, you'll be prompted to enter your OpenAI API Key, which is required, as we use OpenAI's large language models for the AI. You can get one for free by visiting your [API key settings page](https://platform.openai.com/account/api-keys").

Pro tip: You can also set the `OPENAI_API_KEY` environment variable to your API key, and it will use that instead of prompting you.

## Roadmap of Upcoming Features

### Code Workflow Improvements

- [X] **Assisted Git Commit**: Automatically generate a commit message based on the changes you've made
- [X] **Assisted Debugging**: Run a command with aicodebot and it captures the log message and tries to figure out what's going on from the error message.  Eventually, it could also suggest fixes for the error and make the changes for you. Try it out with `aicodebot debug $command`
- [X] **Code Review**: Provides feedback on potential issues in code,  and suggests improvements to make it better.
- [ ] **Dependency Management**: Updating dependencies to their latest versions with pull requests that run tests.
- [ ] **Documentation Generation**: Generates comprehensive documentation for code, including docstrings, README files, and wiki pages.
- [ ] **Performance Optimization Suggestions**: Suggests potential performance optimizations for code.
- [ ] **Test Generation**: Generates unit tests for code, improve test coverage.
- [ ] **Integration with CI/CD pipelines**: Integrates with CI/CD pipelines to automate tasks like code review, testing, and deployment (via GitHub Actions). Eventually: Fix the build automatically when there are small errors.
- [ ] **Rubber Ducky Chat Bot**: Helps developers think through design issues by providing a conversational interface to discuss and solve problems, using data from the current repo.
- [X] **Linting/Formatting**: Checks code for linting errors and automatically fixes them where possible (via pre-commit)
- [ ] **Handle GitHub Issues**: Handles basic tasks that you assign to [@aicodebot](https://pypi.org/project/aicodebot/)

### User Interfaces

- [X] **Command-line, installable via pip**: aicodebot can be installed as a Python package using `pip install aicodebot`
- [ ] **Mention the @aicodebot GitHub user**: Mentioning the [@aicodebot](https://pypi.org/project/aicodebot/) GitHub user in a comment will trigger it to perform a task, review code, or pull in an appropriate gif.
- [ ] **Callable as a GitHub action**: Can be called as a GitHub action to perform tasks on GitHub repositories.
- [ ] **Chat**: CLI chat interface that knows the context of your codebase and can answer questions about it. No more going back and forth between ChatGPT and command-line.
- [ ] **Slack Bot**: Interacts with aicodebot via slack, sends notifications, performs tasks, and provides real-time assistance to developers.
- [ ] **Bug Report service integrations**: Listen for bug reports from Sentry, Honeybadger, and other bug reporting tools and automatically create issues, assign them to developers, and notify them via Slack. Eventually: FIX the bug automatically and notify the team.

### Repository Management

- [ ] **Project best practices**: Suggest things like pre-commit, linting, license, CI/CD, etc. Eventually: Implement them for you.
- [ ] **Handle Stale Issues**: Automatically detects and handles stale issues on GitHub by nudging the responsible parties.
- [ ] **Triage Incoming Issues**: Provides Level 1 triage of incoming issues on GitHub, including tagging, assigning, and responding with FAQs. It could also escalate issues to human developers when necessary.
- [ ] **Rate the complexity of PRs**: Rates the complexity of pull requests and assigns them to developers based on their skill level and context

### Fun

- [X] **Fun Facts**: Provides fun facts about programming or AI. It could also share interesting news or articles related to AI and programming. Try it out with `aicodebot fun-fact`.
- [X] **Alignment**: Gives a heart-centered inspirational message about how we can build AI in a way that aligns with humanity. Try it out with `aicodebot alignment`.
- [ ] **Telling Jokes**: We've gotta figure out how to teach LLMs about humor. :)
- [ ] **Supportive Encouragement**: High fives and kudos for a job well done
- [ ] **GIF Reactions**: Reacts to messages with relevant and fun gifs.

<img src="https://camo.githubusercontent.com/6fc1e79b4aa226b24a756c4c8e20e5b049301a930449a7321d3e45f516e61601/68747470733a2f2f74656e6f722e636f6d2f766965772f6b746f2d6b6f756e6f746f72692d6b6f756e6f746f7269746f6b656e2d6c626f772d73746f726b686f6c646572732d6769662d32353637363438332e676966" width="25%">

## Development / Contributing

### The Stack

#### Test and Build

[![GitHub Build](https://github.com/novara-ai/aicodebot/actions/workflows/build.yml/badge.svg)](https://github.com/novara-ai/aicodebot/actions?query=build)
[![CodeCov](https://codecov.io/gh/novara-ai/aicodebot/branch/main/graph/badge.svg)](https://codecov.io/gh/novara-ai/aicodebot)
[![Pytest](https://img.shields.io/badge/%F0%9F%A7%AA-Pytest-blue)](https://docs.pytest.org/en/stable/contents.html)

#### Code Quality

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Super Linter](https://github.com/novara-ai/aicodebot/actions/workflows/linter.yml/badge.svg)](https://github.com/novara-ai/aicodebot/actions/workflows/linter.yml)

#### Infrastructure

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Open AI](https://img.shields.io/badge/OpenAI-412991.svg?logo=OpenAI&logoColor=white)](https://openai.com)

## Alignment ❤️ + 🤖

Technology itself is amoral, it just imbues the values of the engineers who create it. We believe that AI should be built in a way that aligns with humanity, and we're building aicodebot to help us do just that. We're building from a heart-centered space, and contributing to the healthy intersection of AI and humanity.

## Contributing

We'd love your help! If you're interested in contributing, here's how to get started. See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.
