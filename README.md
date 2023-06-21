# AI Code Bot 🤖

## Your AI-powered coding companion

AICodeBot is a coding assistant designed to make your coding life easier. With capabilities to perform code reviews, manage dependencies, and even suggest improvements, think of it as your AI version of a pair programmer.

## MVP

For the initial release, you can get a Fun Fact related to AI and Programming.

`python cli.py funfact`

>>🤖 The first chess program written in Fortran for the IBM 704 computer in 1960 was beaten by a human in just four moves. The program relied heavily on brute force calculation, and had not yet developed sophisticated artificial intelligence algorithms.

Behind the scenes, this is talking to the Open AI API and getting a response via Langchain.

## Future Features (WIP)

- **Code Reviews**: Analyzes code for common issues or deviations from best practices.
- **Dependency Management**: Checks for outdated dependencies and suggests updates.
- **Documentation Improvement**: Analyzes README or other documentation files and suggests improvements.
- **Performance Improvements**: Analyzes code for potential performance issues and suggests optimizations.
- **Linting**: Checks code for stylistic or programming errors.

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

Run the following command. The first time you do, you'll be prompted to enter your OpenAI API key, which is required. You can get one for free on your [api key settings](https://platform.openai.com/account/api-keys").

```bash

```bash
python3 cli.py --help
```
