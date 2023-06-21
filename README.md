# AI Code Bot 🤖

## Your AI-powered coding companion

AICodeBot is a coding assistant designed to make your coding life easier. With capabilities to perform code reviews, manage dependencies, and even suggest improvements, think of it as your AI version of a pair programmer.

## MVP

For the initial release, you can get a Fun Fact related to AI and Programming.

`python cli.py funfact`

>>🤖 The first chess program written in Fortran for the IBM 704 computer in 1960 was beaten by a human in just four moves. The program relied heavily on brute force calculation, and had not yet developed sophisticated artificial intelligence algorithms.

Behind the scenes, this is talking to the Open AI API and getting a response via Langchain.

## Features

Once we've set up the bot to be able to use Large Language Models as a decision making engine at the center of Github and Python APIs, we can start to build out the following features:

### Code Improvements

- [ ] **Code Review**: Provides feedback on potential issues in code, such as style violations, potential bugs, and performance issues. It could also suggest best practices for code improvement.
- [ ] **Dependency Management**: Updating dependencies to their latest versions with pull requests that run tests.
- [ ] **Documentation Generation**: Generates comprehensive documentation for code, including docstrings, README files, and wiki pages.
- [ ] **Performance Optimization Suggestions**: Suggests potential performance optimizations for code.
- [ ] **Code Formatting**: Automatically formats code according to a specified style guide.
- [ ] **Error Detection**: Detects errors in code and suggests potential fixes.
- [ ] **Test Generation**: Generates unit tests for code.
- [ ] **Code Generation**: Generates boilerplate code for common tasks.
- [ ] **Integration with CI/CD pipelines**: Integrates with CI/CD pipelines to automate tasks like code review, testing, and deployment (via Github Actions)
- [ ] **Rubber Ducky Chat Bot**: Helps developers think through design issues by providing a conversational interface to discuss and solve problems.
- [ ] **Linting**: Checks code for linting errors and automatically fixes them where possible.
- [ ] **Handle Github Issues**: Handles issues that you assign to @aicodebot. It could also suggest labels for new issues based on their content.

### User Interfaces

- [ ] **Command line installable via pip**: autocode can be installed as a Python package using pip.
- [ ] **Callable as a Github action**: Can be called as a GitHub action to perform tasks on GitHub repositories.
- [ ] **Slack Bot**: Interacts with aicodebot via slack, sends notifications, performs tasks, and provides real-time assistance to developers.

### Repository Management

- [ ] **Handle Stale Issues**: Automatically detects and handles stale issues on GitHub by nudging the responsible parties.
- [ ] **Triage Incoming Issues**: Provides Level 1 triage of incoming issues on GitHub, including tagging, assigning, and responding with FAQs. It could also escalate issues to human developers when necessary.

### Fun

<img src="https://tenor.com/view/kto-kounotori-kounotoritoken-lbow-storkholders-gif-25676483.gif" style="width:25%; float: right">

- [X] **Fun Facts**: Provides fun facts about programming or AI. It could also share interesting news or articles related to AI and programming.
- [ ] **Telling Jokes**: Tells programming jokes. :smiley:
- [ ] **Gif Reaction**: Reacts to messages with relevant and fun gifs. It could also react to specific events in the repository, like the merging of a pull request or the closing of an issue.

- [ ] **Supportive Encouragement**: High fives and kudos for a job well done

<br clear="all">

## Setup

Follow the steps below to set up AICodeBot on your machine:

1. Clone the repository

```bash
git clone git@github.com:novara-ai/aicodebot.git
```

2. Set up a virtual environment (I recommend using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/))

```bash
mkvirtualenv --python=`which python3` aicodebot
```

3. Install the dependencies:

```bash
pip install -r requirements/requirements.txt
# Use requirements-dev.txt if you want to contribute to the project
```

## Usage

Run the following command. The first time you do, you'll be prompted to enter your OpenAI API key, which is required. You can get one for free on your [API key settings](https://platform.openai.com/account/api-keys").

```bash
python3 cli.py
```
