# AI Code Bot 🤖

## Your AI-powered coding sidekick

AICodeBot is a coding assistant designed to make your coding life easier. With capabilities to perform code reviews, manage dependencies, and even suggest improvements, think of it as your AI version of a pair programmer - a team member that accelerates the pace of development and helps you write better code.

We've planned to build out multiple different interfaces for interacting with AICodeBot. To start, it's a [command-line tool](https://pypi.org/project/aicodebot/) that you can use to generate commit messages, debug code, and review code. In the future, we plan to integrate it with GitHub Actions, Slack, and other tools to make it even more useful.

⚠️ Status: This project is in its infancy with very limited features, but it already improves the software development workflow, and has a healthy Roadmap of features.

⚠️ AICodeBot currently uses OpenAI's ChatGPT large language models, which can hallucinate and be confidently wrong. Sometimes it does dumb things, which is why we have you confirm before it does anything permanent. Much like Tesla's Full Self Driving, you have to keep your hands on the wheel.

We're using AICodeBot to build AICodeBot, and it's getting better all the time.️ We're looking for contributors to help us build it out. See [CONTRIBUTING](https://github.com/gorillamania/AICodeBot/blob/main/CONTRIBUTING.md) for more.

### What it's not

`aicodebot` is a tool for developers, not a replacement for them. It's not going to replace your job, but it will make your job easier and more fun. It's not going to take over the world, but it will help us build a better one. See the *Alignment* section below for more.

It's also not a "build a site for me in 5 minutes" tool that takes a well constructed prompt and builds a scaffold for you. There are [other tools](https://github.com/AntonOsika/gpt-engineer) for that, Instead, AICodeBot is built to work with existing code bases and help you improve them at the git-commit level. It's designed to multiply the effectiveness of capable engineers.

## Current features - how you can use it today

### AI Sidekick

 `aicodebot sidekick` Your AI-powered coding assistant. It's designed to help you with your coding tasks by providing context-aware suggestions and solutions. Think ChatGPT with the ability to read local files for context.

 ```bash
 aicodebot sidekick file1.py file2.py
 ```

In this example, the sidekick will read in the contents of file1.py and file2.py and use them to provide context-aware answers. For example:

* How can I make this code better?
* Tell me how to add a new feature to this code.
* Fix an issue that I'm having when... (describe the issue)
* Write unit tests for the xyz function.

Please note that this feature is still in its experimental stage. While it can already provide valuable assistance, it's not perfect and we're continuously working on improving it.

### AI-Assisted Git Commit

`aicodebot commit` will run pre-commit for you to check syntax, and then generate a commit message for you based on the changes you've made. In about as much effort as typing "fix bug" for the commit message, you will get a high quality commit message that thoroughly describes the change.

### AI-Assisted Code Review

`aicodebot review` will run a code review on your code and suggest improvements. By default it will look at [un]staged changes, and you can also supply a specific commit hash to review. It's goal is to suggest how to make the code better, and we've found that it often teaches us new things about our code and makes us better programmers. It's not perfect, but it's a great way to get a second set of robot eyes on your code.

### AI-Assisted Debugging

`aicodebot debug $command` will run the command and capture the log message. It will pass the error message, stack trace, command output, etc. to the AI and respond with some suggestions on how to fix it. It saves a trip to stackoverflow in a separate window, allowing you to stay in terminal with all the context.

[![PyPI version](https://badge.fury.io/py/aicodebot.svg?0.6.2)](https://badge.fury.io/py/aicodebot)

## Installation and Usage

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

#### Which Language Model? GPT-3.5 vs GPT-4

When using AICodeBot, you have the option to use either GPT-3.5 or GPT-4. While GPT-4 can often provide more accurate and detailed responses, GPT-3.5 is faster and might be sufficient for simpler tasks. We highly recommend GPT-4.

Not all OpenAI accounts have GPT-4 API access enabled. By default, AICodeBot will use GPT-4 if your OpenAI account supports it, we will check the first time you run it. Tip: If your OpenAI API does not support GPT-4, you can ask to be added to the waitlist [here](https://openai.com/waitlist/gpt-4-api)

Note: We'll be adding more options for AI models in the future, including those that can be run locally, such as [GPT4all](https://gpt4all.io/) and HuggingFace's [Transformers](https://huggingface.co/transformers/).

## Roadmap of Upcoming Features

### Code Workflow Improvements

* [X] **Assisted Git Commit**: Automatically generate a commit message based on the changes you've made
* [X] **Assisted Debugging**: Run a command with aicodebot and it captures the log message and tries to figure out what's going on from the error message.  Eventually, it could also suggest fixes for the error and make the changes for you. Try it out with `aicodebot debug $command`
* [X] **Code Review**: Provides feedback on potential issues in code,  and suggests improvements to make it better.
* [ ] **Dependency Management**: Updating dependencies to their latest versions with pull requests that run tests.
* [ ] **Documentation Generation**: Generates comprehensive documentation for code, including docstrings, README files, and wiki pages.
* [ ] **Performance Optimization Suggestions**: Suggests potential performance optimizations for code.
* [ ] **Test Generation**: Generates unit tests for code, improve test coverage.
* [ ] **Integration with CI/CD pipelines**: Integrates with CI/CD pipelines to automate tasks like code review, testing, and deployment (via GitHub Actions). Eventually: Fix the build automatically when there are small errors.
* [ ] **Rubber Ducky Chat Bot**: Helps developers think through design issues by providing a conversational interface to discuss and solve problems, using data from the current repository.
* [X] **Linting/Formatting**: Checks code for linting errors and automatically fixes them where possible (via pre-commit)
* [ ] **Handle GitHub Issues**: Handles basic tasks that you assign to [@aicodebot](https://pypi.org/project/aicodebot/)
* [ ] **Automatically Generate ChangeLogs and Release Notes**: Generates release notes and changelogs based on commit messages and code changes.

### User Interfaces

* [X] **Command-line, installable via pip**: aicodebot can be installed as a Python package using `pip install aicodebot`
* [ ] **Mention the @aicodebot GitHub user**: Mentioning the [@aicodebot](https://pypi.org/project/aicodebot/) GitHub user in a comment will trigger it to perform a task, review code, or pull in an appropriate GIF.
* [ ] **Callable as a GitHub action**: Can be called as a GitHub action to perform tasks on GitHub repositories.
* [ ] **Jupyter Notebook Extension**: Provides a Jupyter Notebook extension that can be used to debug code in the notebook.
* [ ] **Chat**: CLI chat interface that knows the context of your codebase and can answer questions about it. No more going back and forth between ChatGPT and command-line.
* [ ] **Slack Bot**: Interacts with aicodebot via slack, sends notifications, performs tasks, and provides real-time assistance to developers.
* [ ] **Bug Report service integrations**: Listen for bug reports from Sentry, Honeybadger, and other bug reporting tools and automatically create issues, assign them to developers, and notify them via Slack. Eventually: FIX the bug automatically and notify the team.

### Repository / Project Management

* [ ] **Project best practices**: Suggest things like pre-commit, linting, license, CI/CD, etc. Eventually: Implement them for you.
* [ ] **Manage Github Issues**: Provides Level 1 triage of incoming issues on GitHub, including tagging, assigning, and responding with FAQs. It could also escalate issues to human developers when necessary, and provide nudges for tasks that need more input.
* [ ] **Welcome new contributors**: Automatically welcome new contributors to the project, find out what they're interested in, and suggest issues for them to work on.

### Fun

* [X] **Fun Facts**: Provides fun facts about programming or AI. It could also share interesting news or articles related to AI and programming. Try it out with `aicodebot fun-fact`.
* [X] **Alignment**: Gives a heart-centered inspirational message about how we can build AI in a way that aligns with humanity. Try it out with `aicodebot alignment`.
* [ ] **Telling Jokes**: We've gotta figure out how to teach LLMs about humor. :)
* [ ] **Supportive Encouragement**: High fives and kudos for a job well done
* [ ] **GIF Reactions**: Reacts to messages with relevant and fun gifs.

<img src="https://camo.githubusercontent.com/6fc1e79b4aa226b24a756c4c8e20e5b049301a930449a7321d3e45f516e61601/68747470733a2f2f74656e6f722e636f6d2f766965772f6b746f2d6b6f756e6f746f72692d6b6f756e6f746f7269746f6b656e2d6c626f772d73746f726b686f6c646572732d6769662d32353637363438332e676966" width="25%">

## Alignment ❤️ + 🤖

Technology itself is amoral, it just imbues the values of the people who create it. We believe that AI should be built-in a way that aligns with humanity, and we're building AICodeBot to help us do just that. We're building from a heart-centered space, and contributing to the healthy intersection of AI and humanity.

## Development / Contributing

We'd love your help! If you're interested in contributing, here's how to get started. See [CONTRIBUTING](https://github.com/gorillamania/AICodeBot/blob/main/CONTRIBUTING.md) for more details.
