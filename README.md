# AI Code Bot 🤖

## Your AI-powered coding companion

AICodeBot is a coding assistant designed to make your coding life easier. With capabilities to perform code reviews, manage dependencies, and even suggest improvements, think of it as your AI version of a pair programmer.

⚠️ Status: This project is in its infancy with very limited features. Right now it only tells you fun facts, but you can look at the Features list below to get an idea of where it is going. Give the project a star and follow along while we build out more of the foundation.

## MVP

For the initial release, you can get a Fun Fact related to AI and Programming.

`aicodebot fun-fact`

>>🤖 The first chess program written in Fortran for the IBM 704 computer in 1960 was beaten by a human in just four moves. The program relied heavily on brute force calculation, and had not yet developed sophisticated artificial intelligence algorithms.

Behind the scenes, this is talking to the Open AI API and getting a response via Langchain.

#### Commit Message

Automate your commits by having aicodebot generate a commit message for you.

## Features

Once we've set up the bot to be able to use Large Language Models as a decision making engine at the center of Github and Python APIs, we can start to build out the following features:

### Code Workflow Improvements

- [X] **Assisted Git Commit**: Automatically generate a commit message.
- [ ] **Code Review**: Provides feedback on potential issues in code, such as style violations, potential bugs, and performance issues. It could also suggest best practices for code improvement. Eventually: FIX the code automatically and notify the team.
- [ ] **Dependency Management**: Updating dependencies to their latest versions with pull requests that run tests.
- [ ] **Assisted Debugging**: Run a command with aicodebot and it captures the log message and tries to figure out what's going on from the error message.  Eventually, it could also suggest fixes for the error and make the changes for you.
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

- [ ] **Command line installable via pip**: aicodebot can be installed as a Python package using pip
- [ ] **Chat**: CLI chat interface that knows the context of your code base and can answer questions about it. No more going back and forth between ChatGPT and command line.
- [ ] **Callable as a Github action**: Can be called as a GitHub action to perform tasks on GitHub repositories.
- [ ] **Slack Bot**: Interacts with aicodebot via slack, sends notifications, performs tasks, and provides real-time assistance to developers.
- [ ] **Bug Report service integrations**: Listen for bug reports from Sentry, Honeybadger, and other bug reporting tools and automatically create issues, assign them to developers, and notify them via Slack. Eventually: FIX the bug automatically and notify the team.

### Repository Management

- [ ] **Project best practices**: Suggest things like pre-commit, linting, license, CI/CD, etc. Eventually: Implement them for you.
- [ ] **Handle Stale Issues**: Automatically detects and handles stale issues on GitHub by nudging the responsible parties.
- [ ] **Triage Incoming Issues**: Provides Level 1 triage of incoming issues on GitHub, including tagging, assigning, and responding with FAQs. It could also escalate issues to human developers when necessary.
- [ ] **Rate the complexity of PRs**: Rates the complexity of pull requests and assigns them to developers based on their skill level and context

### Fun

- [X] **Fun Facts**: Provides fun facts about programming or AI. It could also share interesting news or articles related to AI and programming.
- [ ] **Telling Jokes**: Tells programming jokes. :smiley:
- [ ] **Supportive Encouragement**: High fives and kudos for a job well done
- [ ] **Gif Reactions**: Reacts to messages with relevant and fun gifs. It could also react to specific events in the repository, like the merging of a pull request or the closing of an issue.

<img src="https://camo.githubusercontent.com/6fc1e79b4aa226b24a756c4c8e20e5b049301a930449a7321d3e45f516e61601/68747470733a2f2f74656e6f722e636f6d2f766965772f6b746f2d6b6f756e6f746f72692d6b6f756e6f746f7269746f6b656e2d6c626f772d73746f726b686f6c646572732d6769662d32353637363438332e676966" style="width:25%">

## Setup and Usage

Follow the steps below to set up AICodeBot on your machine:

`pip install aicodebot`

The first time you run it, you'll be prompted to enter your OpenAI API key, which is required. You can get one for free on your [API key settings](https://platform.openai.com/account/api-keys").

```bash
> aicodebot --help
Usage: aicodebot [OPTIONS] COMMAND [ARGS]...

Options:
  -V, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  commit    Generate a git commit message based on the diff, and then...
  fun-fact  Tell me something interesting about programming or AI.
  version   Print the version number.
```

## Development

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
pip install -r requirements/requirements-dev.txt
# Use requirements-dev.txt if you want to contribute to the project
```
