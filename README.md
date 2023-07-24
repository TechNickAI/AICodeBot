# AI Code Bot 🤖

## Your AI-powered coding sidekick

AICodeBot is a coding assistant designed to make your coding life easier. Think of it as your AI version of a pair programmer. Perform code reviews, create helpful commit messages, debug problems, and help you think through building new features. A team member that accelerates the pace of development and helps you write better code.

We've planned to build out multiple different interfaces for interacting with AICodeBot. To start, it's a [command-line tool](https://pypi.org/project/aicodebot/) that you can install and run in your terminal, and a [GitHub Action for Code Reviews](https://github.com/marketplace/actions/aicodebot-code-review).

Status: This project is in its early stages, but it already improves the software development workflow, and has a healthy roadmap of features (below).

We're using AICodeBot to build AICodeBot, and it's upward spiraling all the time.️ We're looking for contributors to help us build it out. See [CONTRIBUTING](https://github.com/gorillamania/AICodeBot/blob/main/CONTRIBUTING.md) for more.

## Current features - how you can use it today

| Task | Status |
| --- | --- |
| Generating quality commit messages | ✅ |
| Thinking through tasks as a pair programmer | ✅ |
| Coding with a small number of files | ✅ |
| Debugging | ✅ |
| Doing code reviews | ✅ |
| Explaining code | ✅ |
| Writing tests | ✅ |
| Integration with GitHub | ✅ |
| Modifying local files | In Progress |
| Searching the Internet for answers | In Progress |
| Reading library documentation | In Progress |
| Coding with a large number of files |  As LLMs improve |
| Writing senior developer level code | Eventually |
| Major refactors | Eventually |
| Build entire apps | Eventually |
| Replace Developers | Nope |

### AI Sidekick 🦸‍♂️

 `aicodebot sidekick` Your AI-powered coding assistant. It's designed to help you with your coding tasks by providing context-aware suggestions and solutions. Think ChatGPT with the ability to read the local repository for context.

 By default it will pass along a directory of files from the current working directory, and you can also pass in a list of files to use as context for the task you are working on. For example:

 ```bash
 aicodebot sidekick file1.py file2.py
 ```

In this example, the sidekick will read the contents of file1.py and file2.py and use them to provide context-aware answers.

Pro-tips:

* Add your README.md to the list of files to get context-aware answers.
* Paste in error messages from log files or stack traces and it will help you debug
* Brainstorm new features
* Have it write unit tests for you that cover all the cases

This feature is in its early phases right now, but it's already useful. We'll be adding support for tools that the sidekick can use, including GitHub integration, ingesting repository specific domain knowledge, writing local files, and more. For now, it just *reads* files and provides suggestions.

### AI-Assisted Git Commit 📝

`aicodebot commit` improves the git commit process. It will run pre-commit for you to check syntax, and then generate a commit message for you based on the changes you've made. In about as much effort as typing "fix bug" for the commit message, you will get a high-quality commit message that thoroughly describes the change.

### AI-Assisted Code Review 👀

`aicodebot review` will run a code review on your code and suggest improvements. By default, it will look at [un]staged changes, and you can also supply a specific commit hash to review.
Its goal is to suggest how to make the code better, and we've found that it often teaches us new things about our code and makes us better programmers. It is a great way to get a second set of robot eyes on your code.

### AI-Assisted Debugging 🐞

`aicodebot debug $command` will run the $command and capture the log output. It will pass the error message, stack trace, command output, etc. over to the AI and respond with some suggestions on how to fix it.

[![PyPI version](https://badge.fury.io/py/aicodebot.svg?0.6.2)](https://badge.fury.io/py/aicodebot)

## Installation and Usage

To install AICodeBot, run:

`pip install aicodebot`

And then, run `aicodebot configure` to get started.

```bash
Usage: aicodebot [OPTIONS] COMMAND [ARGS]...

Options:
  -V, --version  Show the version and exit.
  -h, --help     Show this message and exit.
  -d, --debug    Enable langchain debug output

Commands:
  alignment       A message from AICodeBot about AI Alignment ❤ + 🤖.
  commit          Generate a commit message based on your changes.
  configure       Create or update the configuration file
  debug           Run a command and debug the output.
  learn           NOT WORKING YET: Learn new skills and gain additional...
  review          Do a code review, with [un]staged changes, or a...
  sidekick        Coding help from your AI sidekick
```

### Open AI key setup

The first time you run it, you'll be prompted to enter your OpenAI API Key, which is required, as we use OpenAI's large language models for the AI. You can get one for free by visiting your [API key settings page](https://platform.openai.com/account/api-keys).

Note: You will be billed by OpenAI based on how much you use it. Typical developers will use less than $10/month - which if you are a professional developer you'll likely more than make up for with saved time and higher quality work. See [OpenAI's pricing page](https://openai.com/pricing/) for more details. Also, see the note about increasing your token size and using better language models below.

## Integration with GitHub Actions

How about automated code reviews on every commit? You can have AICodeBot run as a GitHub action on your repository. See [The AICodeBot GitHub Action for Code Reviews](https://github.com/marketplace/actions/aicodebot-code-review). It will look at every commit and pull request, and then either:

* ✅ Pass
* 🗒️ Comments - pass the action, but leave a comment with minor issues, suggestions, or improvements.
* ❌ Fail the action - if a serious issue is found, it will leave a comment and let you know about something that should be addressed.

## Roadmap of Upcoming Features ️

### Code Workflow Improvements

* [X] **Assisted Git Commit**: Automatically generate a commit message based on the changes you've made
* [X] **Assisted Debugging**: Run a command with aicodebot and it captures the log message and tries to figure out what's going on from the error message.  Eventually, it could also suggest fixes for the error and make the changes for you. Try it out with `aicodebot debug $command`
* [X] **Code Review**: Provides feedback on potential issues in code,  and suggests improvements to make it better.
* [ ] **Dependency Management**: Updating dependencies to their latest versions with pull requests that run tests.
* [ ] **Documentation Generation**: Generates comprehensive documentation for code, including docstrings, README files, and wiki pages.
* [ ] **Performance Optimization Suggestions**: Suggests potential performance optimizations for code.
* [X] **Test Generation**: Generates unit tests for code, improve test coverage.
* [X] **Integration with CI/CD pipelines**: Integrates with CI/CD pipelines to automate tasks like code review, testing, and deployment (via GitHub Actions). Eventually: Fix the build automatically when there are small errors.
* [X] **Rubber Ducky Chat Bot**: Helps developers think through design issues by providing a conversational interface to discuss and solve problems, using data from the current repository.
* [X] **Linting/Formatting**: Checks code for linting errors and automatically fixes them where possible (via pre-commit)
* [ ] **Automatically Generate ChangeLogs and Release Notes**: Generates release notes and changelogs based on commit messages and code changes.

### User Interfaces

* [X] **Command-line, installable via pip**: aicodebot can be installed as a Python package using `pip install aicodebot`
* [ ] **Mention the @aicodebot GitHub user**: Mentioning the [@aicodebot](https://pypi.org/project/aicodebot/) GitHub user in a comment will trigger it to perform a task, review code, or pull in an appropriate GIF.
* [X] **Callable as a GitHub action**: Can be called as a GitHub action to perform tasks on GitHub repositories. [AICodeBot Action](https://github.com/marketplace/actions/aicodebot-code-review)
* [ ] **Jupyter Notebook Extension**: Provides a Jupyter Notebook extension that can be used to debug code in the notebook.
* [X] **Chat**: CLI chat interface that knows the context of your codebase and can answer questions about it. No more going back and forth between ChatGPT and command-line.
* [ ] **Slack Bot**: Interacts with aicodebot via slack, sends notifications, performs tasks, and provides real-time assistance to developers.
* [ ] **Bug Report service integrations**: Listen for bug reports from Sentry, [Honeybadger](http://honeybadger.io), and other bug reporting tools and automatically create issues, assign them to developers, and notify them via Slack. Eventually: FIX the bug automatically and notify the team.

### Repository / Project Management

* [ ] **Project best practices**: Suggest things like pre-commit, linting, license, CI/CD, etc. Eventually: Implement them for you.
* [ ] **Manage GitHub Issues**: Provides Level 1 triage of incoming issues on GitHub, including tagging, assigning, and responding with FAQs. It could also escalate issues to human developers when necessary, and provide nudges for tasks that need more input.
* [ ] **Welcome new contributors**: Automatically welcome new contributors to the project, find out what they're interested in, and suggest issues for them to work on.

### Fun

* [X] **Alignment**: Gives a heart-centered inspirational message about how we can build AI in a way that aligns with humanity. Try it out with `aicodebot alignment`.
* [ ] **Telling Jokes**: We've gotta figure out how to teach LLMs about humor. :)
* [ ] **Supportive Encouragement**: High fives and kudos for a job well done
* [ ] **GIF Reactions**: Reacts to messages with relevant and fun gifs.

<img src="https://camo.githubusercontent.com/6fc1e79b4aa226b24a756c4c8e20e5b049301a930449a7321d3e45f516e61601/68747470733a2f2f74656e6f722e636f6d2f766965772f6b746f2d6b6f756e6f746f72692d6b6f756e6f746f7269746f6b656e2d6c626f772d73746f726b686f6c646572732d6769662d32353637363438332e676966" width="25%">

## Alignment ❤️ + 🤖

Technology itself is amoral; it just imbues the values of the people who create it. We believe that AI should be built in a way that aligns with humanity, and we're building AICodeBot to help us do just that. We're building from a heart-centered space, and contributing to the healthy intersection of AI and humanity.

### What it's NOT

`aicodebot` is a tool for developers, not a replacement for them. It's not going to replace your job, but it will make your job easier and more fun. It won't take over the world, but it will help us build a better one. See the *Alignment* section below for more.

⚠️ AICodeBot currently uses OpenAI's ChatGPT large language models, which can hallucinate and be confidently wrong. Sometimes AICodeBot does dumb things, so it's mostly *reading* and *advising* and not yet *writing*. Much like Tesla's "Full Self Driving", you must keep your hands on the wheel.

It's also not a "build a site for me in 5 minutes" tool that takes a well-constructed prompt and builds a scaffold for you. There are [other tools](https://github.com/AntonOsika/gpt-engineer) for that. It's not a no-code platform. Instead, AICodeBot is built to work with existing code bases and the git-commit level. It's designed to multiply the effectiveness of capable engineers.

## Which Language Model?

Not all OpenAI accounts have GPT-4 API access enabled. By default, AICodeBot will use GPT-4. If your OpenAI account supports it, we will check the first time you run it. If your OpenAI API does not support GPT-4, you can ask to be added to the waitlist [here](https://openai.com/waitlist/gpt-4-api). You can also use openrouter.ai to get access to advanced models like GPT-4 32k for larger context windows.

Note: We'll be adding more options for AI models in the future, including those that can be run locally, such as [GPT4all](https://gpt4all.io/) and HuggingFace's [Transformers](https://huggingface.co/transformers/).

### Understanding Tokens and Using Commands Efficiently

In AI models like OpenAI's GPT-4, a "token" is a piece of text, as short as a character or as long as a word. The total tokens in an API call, including input and output, affect the cost, time, and whether the call works based on the maximum limit.

Each model has a maximum token limit. For example, GPT-3.5 has a limit of 4096 tokens, and GPT-4 has a token limit of 8192 tokens. If a conversation exceeds this limit, you must reduce your text until it fits.

When using commands like the Sidekick command in AICodeBot, which allows you to pass in files for context, it's important to manage your tokens effectively. Due to token limits, it's not feasible to load your entire code base. Instead, you should only load the specific files that are relevant to the task you're working on. This ensures that the AI model can process your request efficiently and provide the most relevant suggestions for your current task.

### How can I get a larger token limit?

Do you need a larger context window for your task? Are you running into token limits and getting a message like this?

```bash
The context is too large (21414) for any of the models supported by your API key. 😞
```

There are a couple of things you can do:

1. Load fewer files into the context (only what you need to work with)
2. Apply for GPT-4-32k access from OpenAI by contacting them.
3. Use openrouter.ai - this allows you to use the full power of GPT-4-32k, which offers a 4x larger context window. See [openrouter.ai](https://openrouter.ai) for more details. Once you sign up and set your `openrouter_api_key` in your `$HOME/.aicodebot.yaml` file, you can have access to larger models. Soon we will have support for Claude 2, which has a 100k token limit.

## Development / Contributing

We'd love your help! If you're interested in contributing, here's how to get started. See [CONTRIBUTING](https://github.com/gorillamania/AICodeBot/blob/main/CONTRIBUTING.md) for more details.
