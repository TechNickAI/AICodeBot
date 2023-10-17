# CHANGELOG



## v0.15.0 (2023-07-23)

### Unknown

* Bump version to 0.15.0 ([`313be38`](https://github.com/TechNickAI/AICodeBot/commit/313be38a3881500f2ae54572a26f5acf4728ac2f))

* Update ruff in pre-commit ([`f75fa25`](https://github.com/TechNickAI/AICodeBot/commit/f75fa2518378b27dff8a20a1a63f0043efbd6c35))

* Black formatting matters ([`151a6cf`](https://github.com/TechNickAI/AICodeBot/commit/151a6cf07618dc449e00af2d4da98ebb1fadfa50))

* Let&#39;s have pre-commit use the black configuration files instead of duplicating the line length here ([`ca66bac`](https://github.com/TechNickAI/AICodeBot/commit/ca66bac1bbe309ea4e28769fe768be232f5c9175))

* Add /command interface to sidekick with tools for adding/removeing files

In `aicodebot/helpers.py`, a new class `SidekickCompleter` has been added to provide command completion functionality in the sidekick feature.

In `aicodebot/learn.py`, the error messages have been made more informative and user-friendly.

The `requirements.in` and `requirements.txt` files have been updated with the addition of the `humanize` library. ([`f596f5e`](https://github.com/TechNickAI/AICodeBot/commit/f596f5e75d9298ca87d2a324dba47b100f162836))

* Adjust line-length in black and isort configurations 📏

The line-length in both the black and isort configurations in the pyproject.toml file has been reduced from 120 to 115. This change aims to improve code readability and maintainability. 📚 ([`28e056e`](https://github.com/TechNickAI/AICodeBot/commit/28e056e6affe8f2a92c0fc1113cae0d50c7ff500))

* Merge pull request #51 from TechNickAI/dependabot/pip/langchain-0.0.238

Bump langchain from 0.0.231 to 0.0.238 ([`7cd36d0`](https://github.com/TechNickAI/AICodeBot/commit/7cd36d06f68ef169902c2bf4adf39f2a4e00b566))

* Update pytest command to record new API responses 📝

Modified the pytest command in the GitHub workflow to include the `--record-mode=new_episodes` option. This change allows pytest to record new API responses, accommodating for instances where the OpenAI API calls a different host. This should improve the accuracy of our tests and coverage reports. ([`ba90ae3`](https://github.com/TechNickAI/AICodeBot/commit/ba90ae3543f3e330948e1f1d00e13d0bd4618464))

* Refine docstrings and welcome message in cli.py 📝

Updated the docstrings for the &#39;alignment&#39; and &#39;configure&#39; functions to better reflect their purpose. Also, enhanced the welcome message in the &#39;setup_config&#39; function for a more personalized user experience. ([`a576ed7`](https://github.com/TechNickAI/AICodeBot/commit/a576ed740624fa9aef6dc3dd99c82507568b2770))

* Proper indentation so test_parse_github_url is run ([`7a4e96c`](https://github.com/TechNickAI/AICodeBot/commit/7a4e96c5950b47cf734782396fcb11b3b57a5889))

* Update tests to use VCR and pytest-recording for API mocking

Resolves #11

The tests have been updated to use the VCR package for recording and replaying API responses during testing.

This allows the tests to run without hitting the real OpenAI API, making them faster and not consuming API quota. The responses are cached in yaml files that can be committed to version control.

To enable this:

- Added a pytest fixture to configure VCR
- Updated the test decorators from `@pytest.mark.skipif` to `@pytest.mark.vcr()`
- Recorded new cassettes for each test

Now the tests will replay cached responses instead of making live calls.

This is better for CI and local testing.
👍 ([`2547051`](https://github.com/TechNickAI/AICodeBot/commit/2547051e2908942ae6c9fbddf2969215d7a54697))

* Update &#39;Her&#39; personality description in prompts.py

Enhanced the &#39;Her&#39; personality description in the prompts.py file to include more nuanced characteristics. The AI now embodies a playful, witty, and sultry persona, while maintaining professional boundaries. This change adds depth to the AI&#39;s interaction, making it more engaging and relatable. 🎭👩‍💼🌟 ([`e4ad783`](https://github.com/TechNickAI/AICodeBot/commit/e4ad783ee88814517bc30a9eb6c042613c00d481))

* Increase the default token size for sidekick, to get better answers. ([`9fe8e8b`](https://github.com/TechNickAI/AICodeBot/commit/9fe8e8b877323cea149ee468505a51b4f3f84250))

* Bump langchain from 0.0.231 to 0.0.238

Bumps [langchain](https://github.com/hwchase17/langchain) from 0.0.231 to 0.0.238.
- [Release notes](https://github.com/hwchase17/langchain/releases)
- [Commits](https://github.com/hwchase17/langchain/compare/v0.0.231...v0.0.238)

---
updated-dependencies:
- dependency-name: langchain
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`2e61436`](https://github.com/TechNickAI/AICodeBot/commit/2e61436e6e86d3643692e9dd3b7724d4e3fd61e4))

* Merge pull request #48 from TechNickAI/dependabot/pip/click-8.1.6

Bump click from 8.1.4 to 8.1.6 ([`7fd0408`](https://github.com/TechNickAI/AICodeBot/commit/7fd0408ae4b7a04118f839ee4099c9691e07fb6a))


## v0.14.1 (2023-07-21)

### Unknown

* Bump version to 0.14.1 ([`75cb9a4`](https://github.com/TechNickAI/AICodeBot/commit/75cb9a4b0584ffeeb01d8ecfb94e03ffda0b0989))

* Skip Python 3.9 in GitHub Actions build matrix 🏗️

Due to a build failure with Python 3.9 in GitHub Actions, we&#39;re temporarily skipping it. The build matrix now only includes Python 3.10 and 3.11. We&#39;ll revisit this once the issue with Python 3.9 is resolved. ([`529f07b`](https://github.com/TechNickAI/AICodeBot/commit/529f07b247087a701e9369fc80ad951053ec6d32))

* Try turning off cache to see if that fixes python 3.9 build issue ([`9a4e45d`](https://github.com/TechNickAI/AICodeBot/commit/9a4e45d276c724d1421e82cdf62115dc8b46cb80))

* Remove the check for main in setup.py, we use aicodebot/__init__.py to store the version now ([`db8cde8`](https://github.com/TechNickAI/AICodeBot/commit/db8cde8a45462b3d9bc7f6d93f92143cfe8e94c2))

* Update Python version support and cleanup setup.py 🧹

Adjusted the Python version matrix in the GitHub Actions workflow to include Python 3.9. Also, lowered the minimum required Python version in setup.py to 3.9. Removed unnecessary package data from setup.py. This makes our project more accessible to developers using Python 3.9. 🐍 ([`33d061d`](https://github.com/TechNickAI/AICodeBot/commit/33d061d9b3fbb51c565e9535042b5129f89939e4))


## v0.14.0 (2023-07-20)

### Unknown

* Bump version to 0.14.0 ([`d664466`](https://github.com/TechNickAI/AICodeBot/commit/d664466400e65056f3d201172921a3f48eb358dc))

* Experimental Anthropic/Claude2 support for 100k context (when using openrouter.ai)

This commit includes several changes to the `Coder` class in `coder.py` to improve how models are handled.

1. The import statement has been updated to include the `os` module. This allows us to access environment variables.
2. The method for setting the `tiktoken_model_name` has been updated to handle non-OpenAI models. For these models, the name is set to gpt-4 as a default.
3. The `get_llm_model_name` method now checks for an environment variable `AICODEBOT_LLM_MODEL`. If this variable is set, its value is used as the model name.
4. The `get_token_length` method has been updated to strip leading and trailing whitespace from the `short_text` variable.
5. The `model_options` dictionary in the `get_llm_model_name` method now includes the anthropic/claude-2 model.

These changes should make the `Coder` class more flexible and robust when dealing with different models. 🚀 ([`0c35577`](https://github.com/TechNickAI/AICodeBot/commit/0c355779258c40fbd4c7cc03ee30d3a8038a31af))

* Add notes about the state of the learn command (it&#39;s not working yet) ([`22999db`](https://github.com/TechNickAI/AICodeBot/commit/22999dbab33c136d65e50175736e94e58395b712))

* Bump click from 8.1.4 to 8.1.6

Bumps [click](https://github.com/pallets/click) from 8.1.4 to 8.1.6.
- [Release notes](https://github.com/pallets/click/releases)
- [Changelog](https://github.com/pallets/click/blob/8.1.6/CHANGES.rst)
- [Commits](https://github.com/pallets/click/compare/8.1.4...8.1.6)

---
updated-dependencies:
- dependency-name: click
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`7df3f87`](https://github.com/TechNickAI/AICodeBot/commit/7df3f873f78975c5bf6d52da0b3aef425406e486))

* Merge pull request #50 from TechNickAI/dependabot/pip/pyyaml-6.0.1

Bump pyyaml from 6.0 to 6.0.1 ([`6fa18d0`](https://github.com/TechNickAI/AICodeBot/commit/6fa18d0f5a952d1bbb57d478cbabf4b7c2a4a1e1))

* Bump pyyaml from 6.0 to 6.0.1

Bumps [pyyaml](https://github.com/yaml/pyyaml) from 6.0 to 6.0.1.
- [Changelog](https://github.com/yaml/pyyaml/blob/6.0.1/CHANGES)
- [Commits](https://github.com/yaml/pyyaml/compare/6.0...6.0.1)

---
updated-dependencies:
- dependency-name: pyyaml
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`9ae5db9`](https://github.com/TechNickAI/AICodeBot/commit/9ae5db98ce3e896b154f21eaacfba85ddcd9ccff))

* Refine Pro-tips section in README.md with a lint fix. ([`d05064b`](https://github.com/TechNickAI/AICodeBot/commit/d05064b7a859c73e60d71ca28606e787c341f7eb))


## v0.13.2 (2023-07-19)

### Unknown

* Bump version to 0.13.1 ([`fade480`](https://github.com/TechNickAI/AICodeBot/commit/fade480bd432772c221d1b22a3e7bb2d1a61b46b))

* Refactor unlink method for Path objects for python &lt;= 3.9 support

Resolves #47

Updated the unlink method for Path objects in `aicodebot/cli.py` and `tests/test_cli.py` for better readability and consistency. Now using `Path(temp_file_name).unlink()` instead of `Path.unlink(temp_file_name)`. 🔄📁 ([`978455c`](https://github.com/TechNickAI/AICodeBot/commit/978455c561d3923d1a8a1f5a7f0a07fe8cfbe86d))

* Update README.md ([`90abba4`](https://github.com/TechNickAI/AICodeBot/commit/90abba48b26cbff0b4bf33b87d27a1aedbc29db6))

* I know kung fu! Add learning functionality from repositories

This commit introduces a new feature that allows the AI Code Bot to learn from a given repository. The bot can now clone a repository, load its documents, and store them in a local vector store for future use. This will enhance the bot&#39;s ability to provide contextually relevant suggestions and responses.

Additionally, this commit includes the necessary updates to the configuration and helper functions to support this new feature. The requirements have also been updated to include the necessary dependencies.

Lastly, a new test case has been added to ensure the correct parsing of GitHub URLs. 🧪 ([`7f5ae4a`](https://github.com/TechNickAI/AICodeBot/commit/7f5ae4aa9563c1b94308d295a96b6c63216cbf5b))


## v0.13.0 (2023-07-17)

### Unknown

* Refine token size calculation and model selection in Coder class

Resolves #25

In this commit, we&#39;ve made several adjustments to the `Coder` class in `aicodebot/coder.py` and `aicodebot/cli.py`. The token size calculation now includes a 5% buffer, down from 10%, to account for the occasional underestimation by the `tiktoken` library. The `get_token_length` method now defaults to the `gpt-4` model for token counting, and the debug output has been improved for readability.

In `aicodebot/cli.py`, we&#39;ve adjusted the `model_name` calculation in several methods to include `response_token_size` in the token count. This ensures that the selected model can handle the combined size of the request and response. In the `sidekick` method, we&#39;ve also introduced a `memory_token_size` to allow for a decent history.

These changes should improve the accuracy of model selection and prevent errors when the token count exceeds the model&#39;s limit. ([`da2fb1f`](https://github.com/TechNickAI/AICodeBot/commit/da2fb1fc1de8c7f375c1cc06e3af89d3bc899d24))

* Update pyproject.toml and requirements-dev.txt for semantic release 🚀

This commit includes updates to the `pyproject.toml` and `requirements-dev.txt` files. The `pyproject.toml` file now includes a new section for `semantic_release` with a `version_variable` set to `aicodebot:version`. This change allows for automated versioning using the semantic-release tool.

In the `requirements-dev.txt` file, the `python-semantic-release` package has been added. This package provides the semantic-release command line tool, which automates the whole package release workflow including: determining the next version number, generating the release notes and publishing the package.

These changes aim to streamline the release process, making it more efficient and consistent. 📦🔄 ([`df0eda4`](https://github.com/TechNickAI/AICodeBot/commit/df0eda41cd37de4099456dc93e9998cb7c329b5c))


## v0.12.2 (2023-07-17)

### Unknown

* Bump version to 0.12.2 ([`55ed1c0`](https://github.com/TechNickAI/AICodeBot/commit/55ed1c012b75c8b744f5b8eb568ef99a78fc2a0b))

* Refactor GitHub release process in PyPi workflow 🔄

Switched from `actions/create-release@v1` to `ncipollo/release-action@v1` for creating GitHub releases. This change simplifies the release process and automatically generates release notes. ([`dca2977`](https://github.com/TechNickAI/AICodeBot/commit/dca297718e96bc78aa5fef05701da7f046ea548f))

* Remove Dockerfile - this was an accidental commit ([`289fb10`](https://github.com/TechNickAI/AICodeBot/commit/289fb10eb837c15c39caf3c37f98b3d5f363a32c))


## v0.12.1 (2023-07-17)

### Unknown

* Support python version 3.10+. Resolves #7 ([`dbcad55`](https://github.com/TechNickAI/AICodeBot/commit/dbcad554abfcec345a192ca3262f5254bf7f7211))

* Update workflow dependency from &#39;smoke_test&#39; to &#39;test&#39;

In the PyPi release workflow, the dependency has been updated from &#39;smoke_test&#39; to &#39;test&#39;. This change ensures that the correct test suite is run before the package is published to PyPi. 🔄🧪 ([`56048cd`](https://github.com/TechNickAI/AICodeBot/commit/56048cdd490aa8efe49056153177efee07e81f83))

* Refactor PyPi release workflow for broader Python version testing 🐍

Renamed the job from &#39;smoke_test&#39; to &#39;test&#39; and expanded the Python version matrix to include 3.9, 3.10, and 3.11. This change ensures our package is tested across a wider range of Python versions, enhancing compatibility and reliability. ([`b085346`](https://github.com/TechNickAI/AICodeBot/commit/b085346436d2c7d896b88557968581aec674a070))

* Try with 3.10 and 3.11 ([`5aeabef`](https://github.com/TechNickAI/AICodeBot/commit/5aeabeffe344e564e691554d466df3e885d5ac46))

* Simplify Python versions and streamline package build process 🐍

This commit reduces the matrix of Python versions for smoke tests to only 3.11. It also combines the package build and installation steps into one, making the workflow more efficient. ([`81c561d`](https://github.com/TechNickAI/AICodeBot/commit/81c561d2587df52353aa78730248621158089277))


## v0.12.0 (2023-07-17)

### Unknown

* Bump version to 0.12.0. Notably, python 3.9 and 3.10 suppoert ([`2a6c23f`](https://github.com/TechNickAI/AICodeBot/commit/2a6c23f98816548a0220dbb91a8045ee8a7b85aa))

* Test with python 3.9 and 3.10 ([`24bd973`](https://github.com/TechNickAI/AICodeBot/commit/24bd9732ae1b4e575eb7c3681d586d0772021a48))

* Fix Path.open operations to be compatible with python &lt; 3.9

This commit refactors file operations across multiple files to use more concise and readable methods provided by the `Path` class. The `create_and_write_file` helper function has been introduced and used in several places, replacing the previous `open` and `write` operations. This change improves code readability and maintainability. 📚🔧 ([`1589617`](https://github.com/TechNickAI/AICodeBot/commit/1589617653d34595c6403bacd641ab52d68ce7db))

* Minor prompt changes ([`747c7a9`](https://github.com/TechNickAI/AICodeBot/commit/747c7a93a2fcf4385104e9be0e90bf778fbbf419))

* Let&#39;s use just python 3.11 until we have it working with other versions ([`b121ac9`](https://github.com/TechNickAI/AICodeBot/commit/b121ac982dc7eaf0032e752b4705ec12c6852f76))

* Expand Python version matrix and improve user interaction in CLI

This commit does a few things:
- Expands the Python version matrix in the GitHub Actions workflow to include Python 3.10 and 3.11. This ensures our tests run on the latest versions of Python. 🐍
- Improves user interaction in the CLI by adding a period to the end of a console print statement and changing the input prompt to include a robot emoji for a more friendly user experience. 🤖
- Updates the coder.py file to include the anthropic/claude-2 model in the model options. This provides more options for the users. 🚀

These changes aim to improve the user experience and ensure our software is tested against the latest Python versions. ([`1a32169`](https://github.com/TechNickAI/AICodeBot/commit/1a321699b7b80503e000c89eceeffdde8b0bcdd1))

* Refine PyPi release workflow 🚀

Enhanced the PyPi release workflow in the GitHub Actions. Added a dependency on the smoke test job, ensuring it passes before proceeding with the release. Also, included steps for code checkout, Python setup, and package building. Now using Python 3.11 and caching pip for faster runs. ([`1a4e57d`](https://github.com/TechNickAI/AICodeBot/commit/1a4e57d0c50fdeec786d902ac3c4a69380261c70))

* Let&#39;s start the matrix with just 3.11 and then start adding more ([`89ed9ae`](https://github.com/TechNickAI/AICodeBot/commit/89ed9ae8b7d076084f9b7e42aa8bdda7c1a38a99))

* numpy requires &gt;3.9 ([`37f33ba`](https://github.com/TechNickAI/AICodeBot/commit/37f33bae4b19edfd203aa8bcc3f6fd9120fafa66))

* Move checkout code before setup python ([`a458764`](https://github.com/TechNickAI/AICodeBot/commit/a4587645e6dd3fad82b6051e4e86b150ec757c60))

* Refactor PyPi release workflow and add smoke tests 🔄🧪

This commit refactors the PyPi release workflow in `.github/workflows/pypi_release.yml`. The `pypi_release` job has been simplified and a new `smoke_test` job has been added. The smoke test runs on multiple Python versions (3.7 to 3.11) and includes a pytest run. This ensures our package is robust across different Python environments before it&#39;s published to PyPi. 🚀 ([`dfe6b5a`](https://github.com/TechNickAI/AICodeBot/commit/dfe6b5a14a1042bbcd14d14ee06df6fa6690049a))


## v0.11.1 (2023-07-16)

### Unknown

* Bump version to 0.11.1 ([`8bcf8c1`](https://github.com/TechNickAI/AICodeBot/commit/8bcf8c1027d25b5ea61bd5a470e54053eba83a61))

* Simpler config function that will simplify AICodeBot-action testing ([`6e28d09`](https://github.com/TechNickAI/AICodeBot/commit/6e28d09b1330868a505ace313f36785bd66a72bd))

* Refactor README.md for clarity and token management 📚

Relocated the section about language model selection to a more appropriate location in the README. Added a comprehensive explanation on understanding tokens and using commands efficiently. This should help users manage their tokens effectively and understand the limitations and possibilities of different AI models. Also provided guidance on how to handle larger token limits. 🚀 ([`dfbadf5`](https://github.com/TechNickAI/AICodeBot/commit/dfbadf507b2295bbc2db45da2cf922c95dcdaedd))


## v0.11.0 (2023-07-16)

### Unknown

* Bump version to 0.11.0 ([`8abd21c`](https://github.com/TechNickAI/AICodeBot/commit/8abd21cdbf532946037e226b34105ce42c09a4fc))

* Add support for Open Router API in Coder class

This commit introduces the ability to use the Open Router API in the Coder class if an `openrouter_api_key` is provided in the configuration. This allows for access to models with larger token limits. If the Open Router API key is not provided, the code falls back to using the OpenAI API key. The commit also refactors the `get_llm_model_name` method to support model selection based on the provided API key. 🚀🔑 ([`bcf9cbe`](https://github.com/TechNickAI/AICodeBot/commit/bcf9cbeba5e35e5d77de430a1e101cfa68f15fcf))

* Refine personality descriptions in prompts.py

The descriptions of the AI personalities in the prompts.py file have been updated for clarity and consistency. Emojis usage has been specified for each personality where it was previously ambiguous. This should provide a clearer guideline for the AI&#39;s behavior and responses. ([`5d187e8`](https://github.com/TechNickAI/AICodeBot/commit/5d187e8f2f83ff8e50b4b19136aeff9b21904214))

* Refine GitHub Actions integration section in README

The section detailing the integration of AICodeBot with GitHub via GitHub Actions has been revised for clarity and conciseness. The new text emphasizes the automation of code reviews on every commit, enhancing the understanding of the feature&#39;s utility. ([`6934fdc`](https://github.com/TechNickAI/AICodeBot/commit/6934fdc49cda5bda7c8eef55448fdf7e000cbd82))

* Update aicodebot.yml to use v1 tag ([`a9ee638`](https://github.com/TechNickAI/AICodeBot/commit/a9ee6380e2d45d3249b2d211b943ad1e82a0b563))

* Update README.md ([`79ce206`](https://github.com/TechNickAI/AICodeBot/commit/79ce206a1a735e38217800154fca97520185f84b))

* Upgrade versions of black and ruff-pre-commit

The versions of black and ruff-pre-commit have been updated to 23.7.0 and v0.0.278 respectively. This ensures that we are using the latest versions of these tools, benefiting from any improvements or bug fixes they may have received. ([`7d7054d`](https://github.com/TechNickAI/AICodeBot/commit/7d7054db5a9cdeecda4a8362e776361a5e6377ea))

* Refactor &#39;commit&#39; function and enhance pre-commit checks

In the &#39;commit&#39; function, a linter warning has been suppressed by adding a &#39;noqa&#39; comment. This change suggests that the function may be complex and could benefit from further refactoring in the future.

Additionally, the pre-commit checks have been improved. Now, if the &#39;pre-commit&#39; tool is not installed, a warning message will be displayed instead of attempting to run the checks. This change enhances the robustness of the code and provides better feedback to the user. ([`d51dc0c`](https://github.com/TechNickAI/AICodeBot/commit/d51dc0c8884119c86f49a2cbf391fe40054a8139))

* Reduce test response token size and adjust review test parameters

The test response token size has been reduced from 200 to 150 to expedite testing. Additionally, the parameters for the review test have been adjusted to ensure the response is valid JSON. This includes increasing the test token size for this specific test. ([`76aca26`](https://github.com/TechNickAI/AICodeBot/commit/76aca2646c4b84c02c809a9bd3a61423446852c8))

* Refactor test_cli.py for improved readability and maintainability

The response token size for tests in test_cli.py has been extracted to a constant, TEST_RESPONSE_TOKEN_SIZE, to avoid repetition and improve readability. This change enhances the maintainability of the code by centralizing the control of this value. ([`ddc3d1d`](https://github.com/TechNickAI/AICodeBot/commit/ddc3d1d90b1bc84d342e18acee07c5cc436e7dec))


## v0.10.6 (2023-07-15)

### Unknown

* Bump version to 0.10.6 🚀

Just a quick version bump to keep things rolling. No major changes, just keeping up with the times! ([`e627014`](https://github.com/TechNickAI/AICodeBot/commit/e6270147d9918e21470a7c4a95832d6761f76e12))

* Enhance code review functionality in CLI and Coder 🛠️

This commit introduces the ability to specify files for the code review command in the CLI. If no files are specified, the command will consider all staged and unstaged changes. The `git_diff_context` method in the Coder class has also been updated to accommodate this change.

In addition, the test cases have been updated to reflect these changes. This enhancement should provide more flexibility when performing code reviews. 🚀 ([`92770bc`](https://github.com/TechNickAI/AICodeBot/commit/92770bcca2e674764813b7e9f890524018da2556))

* Use the proper variable when committing staged files ([`17d2319`](https://github.com/TechNickAI/AICodeBot/commit/17d2319239639b63f35b180cc6523248b1b2b7ee))

* Refine review guidelines in prompts.py 📝

Adjusted the review guidelines in `prompts.py` to provide clearer instructions. Minor changes and formatting issues are now explicitly stated to be non-discussable, and the addition of extra documentation/comments is also discouraged. The aim is to maintain focus on significant issues and code improvement. Keep it succinct, keep it relevant! 😊 ([`445938f`](https://github.com/TechNickAI/AICodeBot/commit/445938f40dcc2b6cd088cef5c4b04beffbaa155a))

* Refine commit process in cli.py 🛠️

This commit enhances the commit process in the cli.py file. We&#39;ve added a live console print to provide real-time feedback while generating the commit message. Additionally, we&#39;ve introduced a confirmation step before using the generated commit message. If not approved, the commit message can be edited in the user&#39;s preferred editor. Lastly, we&#39;ve moved the deletion of the temporary file to the end of the process to ensure it&#39;s always cleaned up. Happy coding! 🚀 ([`048d203`](https://github.com/TechNickAI/AICodeBot/commit/048d203c4907980bd2cfb6d838a4a4b81e746d37))

* Add console print for staged files to be committed

Added a console print statement in `aicodebot/cli.py` to display the list of staged files that will be committed. This provides better visibility for the user on what changes are about to be committed. 📝👀 ([`5fff8e6`](https://github.com/TechNickAI/AICodeBot/commit/5fff8e66f786d181a768e75a260cc9d56253210b))

* Enhance commit functionality in cli.py and update tests 🛠️

This commit introduces the ability to specify files for the commit command in cli.py. Now, users can choose to commit changes from specific files, providing more flexibility. The changes also include updates to the corresponding tests to reflect this new functionality.

Additionally, minor adjustments have been made to improve code readability and maintainability. For instance, the &#39;sys.exit()&#39; calls have been replaced with &#39;return&#39; or &#39;sys.exit(0)&#39; for better clarity.

This should make the commit process more intuitive and user-friendly. Happy coding! 😊 ([`6c087f2`](https://github.com/TechNickAI/AICodeBot/commit/6c087f273066020036928ac3efc97f586090c140))

* Slightly larger token size for the test, because 100 isn&#39;t always big enough for a structured result ([`c2505d6`](https://github.com/TechNickAI/AICodeBot/commit/c2505d6e80756b2e581f1aebdd4e3734b59bc0b4))


## v0.10.5 (2023-07-15)

### Unknown

* Bump version to 0.10.5 ([`1127226`](https://github.com/TechNickAI/AICodeBot/commit/11272268a3a40847d0c578a60f23f6a731aaa931))

* Refactor commit function and add git file handling methods

This commit refactors the `commit` function in `cli.py` to improve code readability and maintainability. It introduces two new methods in `coder.py` - `git_staged_files` and `git_unstaged_files` - to handle git file operations. The `commit` function now uses these methods to get the list of staged and unstaged files.

In addition, the commit function now confirms with the user before committing all modified files if no files are staged. It also runs pre-commit checks on the list of files to be committed, instead of all files.

The `test_cli.py` has been updated to include more comprehensive tests for the `commit` function, covering scenarios with only unstaged changes, both staged and unstaged changes, and no changes at all.

This refactor should make the code easier to understand and modify in the future. 🚀 ([`b8f3953`](https://github.com/TechNickAI/AICodeBot/commit/b8f395324831f2bbeba89f2902a10bd4f683a3ed))

* Refine git diff output for better commit context 📝

Adjusted the `git_diff_context` method in `coder.py` to include the commit message along with the diff. This change enhances the context provided when a specific commit is queried, making it easier to understand the changes made. 🕵️‍♂️🔍 ([`001c1a8`](https://github.com/TechNickAI/AICodeBot/commit/001c1a81379b2ece0a1b7d8ecd9e820fca7294aa))


## v0.10.4 (2023-07-14)

### Unknown

* Bump version to 0.10.4 ([`7652ece`](https://github.com/TechNickAI/AICodeBot/commit/7652eceed20ab67502aeb411af1fe85ba7dc2fc8))

* Reuse the EXPERT_SOFTWARE_ENGINEER prompt fragment for sidekick

The &#39;Sidekick related prompts&#39; section has been restructured to include &#39;Prompt fragments&#39;. The &#39;DIFF_CONTEXT_EXPLANATION&#39; and &#39;EXPERT_SOFTWARE_ENGINEER&#39; prompts have been moved to this new section for better organization. The &#39;EXPERT_SOFTWARE_ENGINEER&#39; prompt has also been added to the &#39;SIDEKICK_TEMPLATE&#39; for more context. This should make the code easier to navigate and maintain. 📚 ([`ac137fa`](https://github.com/TechNickAI/AICodeBot/commit/ac137fac0240445b0c1b5ae6817f3223ccd695c4))

* Add a function for centrally handling the engine list, with caching

This commit introduces a few key changes to the `Coder` class in `coder.py`:

1. Removed an unnecessary import and added `functools` to the import list.
2. Added a new method `get_openai_supported_engines` that fetches the list of models supported by the OpenAI API key. This method uses `functools.lru_cache` for caching the result, improving efficiency.
3. Refactored `get_llm_model_name` to use the new `get_openai_supported_engines` method, reducing code duplication and improving readability.

These changes should make the `Coder` class more efficient and easier to understand. 🧠💡 ([`ab49577`](https://github.com/TechNickAI/AICodeBot/commit/ab49577cd20fc4c9b23e7350a183ff3fb0e9fff7))

* Add debug option and refactor cli.py 🛠️

In this commit, we&#39;ve added a debug option to the CLI, allowing users to enable langchain debug output. This should help with troubleshooting and understanding the inner workings of the program. We&#39;ve also made some minor refactoring changes to improve code readability and maintainability. Keep up the good work! 👍 ([`fe7ddda`](https://github.com/TechNickAI/AICodeBot/commit/fe7ddda5cd9560cd397794277718f90672694b5b))

* Lint fix ([`a3612ae`](https://github.com/TechNickAI/AICodeBot/commit/a3612ae5be52a781d96447bb5e7022308db2b787))


## v0.10.3 (2023-07-13)

### Unknown

* Bump version to 0.10.3 ([`df46bfb`](https://github.com/TechNickAI/AICodeBot/commit/df46bfb468d4344e06ecacebeae83af6b8e5bcc0))

* Remove caching of the config file - it causes problems. ([`eb0b588`](https://github.com/TechNickAI/AICodeBot/commit/eb0b58809d13922f73382807a37510e614117cdb))


## v0.10.2 (2023-07-13)

### Unknown

* Bump version to 0.10.2 ([`4200731`](https://github.com/TechNickAI/AICodeBot/commit/4200731315d1400ff439342aadc0e6ca57a20748))

* Refactor prompts.py for clarity and maintainability

In this commit, we&#39;ve taken the liberty of refactoring the prompts.py file. The primary change involves the extraction of the &#39;EXPERT_SOFTWARE_ENGINEER&#39; string into a constant, thereby reducing redundancy and enhancing maintainability. This change should make future modifications to the description of the &#39;EXPERT_SOFTWARE_ENGINEER&#39; role more straightforward. Furthermore, it improves the readability of the code by reducing clutter. No functional changes were made, and the overall behavior of the program remains the same. ([`e02f41a`](https://github.com/TechNickAI/AICodeBot/commit/e02f41a0a9c1e43b00cec03acac2479b026d839f))

* Refine code reviewer prompt for enhanced clarity and precision

The previous code reviewer prompt was somewhat lacking in specificity and did not adequately convey the level of expertise required for the task. This revision introduces a more detailed description of the reviewer&#39;s qualifications, emphasizing their proficiency in Python and commitment to code quality. The instructions for the review have also been clarified, with a particular emphasis on providing actionable, specific, and kind feedback. ([`8da3af9`](https://github.com/TechNickAI/AICodeBot/commit/8da3af9d9dc6f6f73cf4426446081a02f0c6b6d8))

* Lower default precise temperature for more predictable results ([`b970f4d`](https://github.com/TechNickAI/AICodeBot/commit/b970f4dba25ac8a6fe020a54a51485adc75236c0))


## v0.10.1 (2023-07-13)

### Unknown

* Bump version to 0.10.1 ([`a371ece`](https://github.com/TechNickAI/AICodeBot/commit/a371ece8b3f16e5061217c1d05092915aacfca83))

* Add permissions and modify AICodeBot personality in workflow

Permissions for the GitHub token have been added to enable the bot to comment on the commit or pull request with the results of the code review. The AICodeBot personality has been modified to Einstein. The LOG_LEVEL environment variable has been removed. ([`815b13a`](https://github.com/TechNickAI/AICodeBot/commit/815b13a1efd5a280d8c8cf26c5b80037d897f2be))

* Enhance clarity and efficiency in prompts.py

The modifications in the prompts.py file serve to improve the clarity of instructions and the efficiency of the code. The addition of the DIFF_CONTEXT_EXPLANATION provides a more comprehensive explanation of the &#39;git diff&#39; command output. The instructions for generating commit messages and conducting code reviews have been streamlined for greater efficiency. The changes are logical and adhere to the principles of effective software engineering. ([`951897c`](https://github.com/TechNickAI/AICodeBot/commit/951897cfdb0b373535e7891a878bd5a8e35d562d))

* Allow for the occasional &#34;COMMENTS&#34; return from the LLM in the test ([`5cc327f`](https://github.com/TechNickAI/AICodeBot/commit/5cc327ffc88af8e591c6c639502567f82e716cb8))

* Merge pull request #33 from TechNickAI/dependabot/pip/gitpython-3.1.32

Bump gitpython from 3.1.31 to 3.1.32 ([`68c8c7d`](https://github.com/TechNickAI/AICodeBot/commit/68c8c7d5510fa5f2feec5bf79fe2bbcd3574d566))

* Merge pull request #35 from TechNickAI/dependabot/pip/langchain-0.0.231

Bump langchain from 0.0.225 to 0.0.231 ([`c62cf3f`](https://github.com/TechNickAI/AICodeBot/commit/c62cf3fb92083fe5d73fa6cdfb81fa22d72d39f5))

* Bump gitpython from 3.1.31 to 3.1.32

Bumps [gitpython](https://github.com/gitpython-developers/GitPython) from 3.1.31 to 3.1.32.
- [Release notes](https://github.com/gitpython-developers/GitPython/releases)
- [Changelog](https://github.com/gitpython-developers/GitPython/blob/main/CHANGES)
- [Commits](https://github.com/gitpython-developers/GitPython/compare/3.1.31...3.1.32)

---
updated-dependencies:
- dependency-name: gitpython
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`b592133`](https://github.com/TechNickAI/AICodeBot/commit/b5921339287409de1d1949c9939cc78c0228c355))

* Bump langchain from 0.0.225 to 0.0.231

Bumps [langchain](https://github.com/hwchase17/langchain) from 0.0.225 to 0.0.231.
- [Release notes](https://github.com/hwchase17/langchain/releases)
- [Commits](https://github.com/hwchase17/langchain/compare/v0.0.225...v0.0.231)

---
updated-dependencies:
- dependency-name: langchain
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`a2334db`](https://github.com/TechNickAI/AICodeBot/commit/a2334db3b963358cd1a7a4ef80af89ae8185ae36))

* Merge pull request #34 from TechNickAI/dependabot/pip/click-8.1.4

Bump click from 8.1.3 to 8.1.4 ([`e41d0d3`](https://github.com/TechNickAI/AICodeBot/commit/e41d0d30be5a209529f515beaf11092457c3aebd))

* Mention Github Action in the README ([`3fb5b42`](https://github.com/TechNickAI/AICodeBot/commit/3fb5b422525d99251da92f08b6aa1688269afd7b))

* Integrate AICodeBot for automated code review ...of itself

A new workflow, AICodeBot, has been added to the GitHub Actions. This workflow is triggered on every push, and it performs an automated code review of the changes. It operates on the latest Ubuntu environment and has a timeout limit of 5 minutes. The workflow uses the AICodeBot-action from the TechNickAI repository. It requires two secrets: GITHUB_TOKEN and OPENAI_API_KEY. ([`aeb9b47`](https://github.com/TechNickAI/AICodeBot/commit/aeb9b478a9dabe1c39af85952709861da7d49256))

* Bump click from 8.1.3 to 8.1.4

Bumps [click](https://github.com/pallets/click) from 8.1.3 to 8.1.4.
- [Release notes](https://github.com/pallets/click/releases)
- [Changelog](https://github.com/pallets/click/blob/main/CHANGES.rst)
- [Commits](https://github.com/pallets/click/compare/8.1.3...8.1.4)

---
updated-dependencies:
- dependency-name: click
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`82ec679`](https://github.com/TechNickAI/AICodeBot/commit/82ec6796e51be7ae089177d251d3112893596336))


## v0.10.0 (2023-07-12)

### Unknown

* Bump version to 0.10.0 ([`5ee575e`](https://github.com/TechNickAI/AICodeBot/commit/5ee575e4e6aea2b5976f245eb5d87d9de2e98743))

* Enhance review with output-format=json for GitHub actions!

The code review functionality has been expanded to support structured output in JSON format, and the response token size is now configurable. The review prompt has been updated to provide more detailed instructions. The test coverage has been improved to include tests for the new functionality. Additionally, the &#39;json&#39; module has been imported in &#39;cli.py&#39; for handling JSON output. ([`f1851d2`](https://github.com/TechNickAI/AICodeBot/commit/f1851d2280a2922e5f83ade3c8c6e1a534faade5))

* Enhance user input handling in cli.py

The code has been modified to allow users to edit their input using their preferred editor. Post-editing, the revised input is displayed on the terminal for user reference. This enhancement promotes user convenience and traceability. ([`6ea7694`](https://github.com/TechNickAI/AICodeBot/commit/6ea76940194149020d2109dd6e7a8fe69f4cd16a))


## v0.9.6 (2023-07-12)

### Unknown

* Bump version to 0.9.6 ([`4beebfc`](https://github.com/TechNickAI/AICodeBot/commit/4beebfc94cab7f69787bd4efc4ed1b6e2da9c275))

* Refactor debug logging in git_diff_context method

The debug logging in the git_diff_context method of the Coder class has been refactored. The logger now uses the opt(raw=True) option when logging the diff for a specific commit. This change enhances the readability of the logged output. ([`a6782fd`](https://github.com/TechNickAI/AICodeBot/commit/a6782fd22a03d135f5dc9dc18eb8ed4223b15177))

* Refactor configuration logging and cache clearing

In this commit, the logging of the configuration file usage has been moved to the `read_config` function from the `get_config_file` function. This change ensures that the log message is only generated when the configuration file is actually read, providing a more accurate representation of the program&#39;s operations.

Additionally, the cache of the `read_config` function is now explicitly cleared in the `test_configure` function in the test suite. This ensures that each test starts with a clean state, preventing potential interference from previous tests. ([`40bb518`](https://github.com/TechNickAI/AICodeBot/commit/40bb5185b78f96d27ba35319221c68b612578162))


## v0.9.5 (2023-07-12)

### Unknown

* Bump version to 0.9.5 ([`05843cc`](https://github.com/TechNickAI/AICodeBot/commit/05843cc722f17acfcefb876ca6e8a7b51a99b754))

* Implement caching for configuration and personality prompt retrieval

In an effort to improve efficiency and reduce unnecessary disk reads, caching has been implemented for the retrieval of configuration files and personality prompts. The functools.lru_cache decorator has been employed to this end, ensuring that repeated calls to these functions will return cached results when available. This change should result in a noticeable performance improvement, particularly in scenarios where these functions are called frequently. ([`5f7d969`](https://github.com/TechNickAI/AICodeBot/commit/5f7d969622c358aa6b40d1a36d64752bfeeaa509))

* Introduce Clippy and Stewie as new AI personalities

In this commit, we&#39;ve added two new personalities to our AI repertoire. Clippy, the overzealous assistant from Microsoft Office, and Stewie Griffin, the sophisticated infant from Family Guy. We&#39;ve also removed Peter Griffin from the list. These changes should provide a more diverse range of personalities for users to interact with. ([`f800921`](https://github.com/TechNickAI/AICodeBot/commit/f8009211a14fa130e641f5f2a2be9eabba711567))

* Make log level case insensitive ([`679a7f9`](https://github.com/TechNickAI/AICodeBot/commit/679a7f9f91fd5ca197812e0bd97133a2849e7451))


## v0.9.4 (2023-07-12)

### Unknown

* Bump version to 0.9.4 ([`42b041e`](https://github.com/TechNickAI/AICodeBot/commit/42b041e7170e57f2c82feee23f9cd2157d43b533))

* Log the output of the diff commit if LOG_LEVEL is high enough ([`cb160c6`](https://github.com/TechNickAI/AICodeBot/commit/cb160c617db6830c55bfcd735597039ac4a03e50))

* Change the default personality to Spock. ([`b112868`](https://github.com/TechNickAI/AICodeBot/commit/b11286873edd27f6ecf2abe2d85ebd9b251a2472))

* Update short description in setup.py

Changed the description of the project from Your AI-powered coding sidekick 🤖 to AI-powered tool for developers, simplifying coding tasks and improving workflow efficiency. to provide a more detailed and professional overview of the project. ([`c7a3ab1`](https://github.com/TechNickAI/AICodeBot/commit/c7a3ab1cf3f14a3148f18df30073a69baf4ac53b))


## v0.9.3 (2023-07-12)

### Unknown

* Bump version to 0.9.3 ([`125d1f0`](https://github.com/TechNickAI/AICodeBot/commit/125d1f0bde3c49908fd6ff370b37c0414808ad03))

* Improve handling of OpenAI API key 🗝️, especially for GitHub Actions ([`fd3ebc3`](https://github.com/TechNickAI/AICodeBot/commit/fd3ebc35e505c847fd3e4f4b18fc16a4bd446bd9))

* Refine user interaction prompts

In this commit, we have made several changes to improve the user experience and error handling in the AICodeBot command line interface. We have refined the prompts and messages displayed to the user, making them more concise and informative. We have also improved the handling of the OpenAI API key, including its validation and the prompt for its entry. Furthermore, we have enhanced the presentation of the available AI personalities, making the choices clearer to the user. Lastly, we have removed some redundant code and messages, streamlining the user experience. ([`65a2ca2`](https://github.com/TechNickAI/AICodeBot/commit/65a2ca28b1101a68138f43517455110cee4ce7a6))


## v0.9.2 (2023-07-12)

### Unknown

* Bump to version 0.9.2 ([`ba788ec`](https://github.com/TechNickAI/AICodeBot/commit/ba788ec928c3c06701c11d837a6b18232cb721b6))

* Better handling of the input for sidekick - with command history.

Resolves #18

In this commit, the input prompts in the `aicodebot/cli.py` file have been refactored to use the `prompt_toolkit` library instead of the `click.prompt` function. This change provides a more robust and flexible input prompt system. Additionally, the `prompt-toolkit` library has been added to the project dependencies in the `requirements.in` and `requirements.txt` files. ([`2114d73`](https://github.com/TechNickAI/AICodeBot/commit/2114d7367adb73a5a8aad4260acff95d81163be8))

* Refactor llm generation code to improve modularity and readability

The code has been refactored to improve modularity and readability. The `get_llm` method has been moved to the `Coder` class to centralize the creation of language models. This change simplifies the code and makes it easier to understand. The `RichLiveCallbackHandler` class has also been moved to the `helpers.py` file, which is a more appropriate location for it. Additionally, the `DEFAULT_MAX_TOKENS`, `PRECISE_TEMPERATURE`, and `CREATIVE_TEMPERATURE` constants have been moved to the `coder.py` file for better organization. ([`6926ad5`](https://github.com/TechNickAI/AICodeBot/commit/6926ad5bdf99bc6bd302e1f27cdd6b049db8984b))

* Update tests to pass ruff checks for falsey/strings ([`3907bc3`](https://github.com/TechNickAI/AICodeBot/commit/3907bc3faff2ac3743593dad424fb2aca21736a2))

* Refine README to reflect current capabilities and future plans

The README has been updated to more accurately represent the current state and future trajectory of AICodeBot. The changes include a more precise description of tasks AICodeBot can handle, tasks that are in progress, and tasks that will be possible as the technology evolves. The aim is to provide a clearer picture to users about what AICodeBot can and cannot do at this point in time, and what they can expect in the future. ([`fb3c08a`](https://github.com/TechNickAI/AICodeBot/commit/fb3c08a80727d621ec3b8a195f0a532b9ba626d9))

* Move tests for cli all into one place ([`8858ca3`](https://github.com/TechNickAI/AICodeBot/commit/8858ca31d2f521ff6eddf9514edd625f91fe6a19))

* Update `cli.py` to use new `Coder` class for coding related tasks

This change updates the `cli.py` file to use the `Coder` class from the `coder.py` module for getting the language model name and token length. By using the `Coder` class, we improve the code structure and make it more modular. This change enhances the readability and maintainability of the codebase. ([`671ddfa`](https://github.com/TechNickAI/AICodeBot/commit/671ddfa0531575126dd812d2432444645e413942))

* Refactor configuration handling in aicodebot

In the pursuit of simplicity and clarity, the configuration handling functions have been moved from `aicodebot/helpers.py` to a new file `aicodebot/config.py`. This change enhances the modularity of the code and makes it easier to manage and understand. The `cli.py` file has been updated accordingly to import these functions from their new location. ([`c0d2802`](https://github.com/TechNickAI/AICodeBot/commit/c0d28028e9322f36059c58da3ef26e1bc84f423f))

* Test debug success should only run with an API key set ([`eb4c981`](https://github.com/TechNickAI/AICodeBot/commit/eb4c9813d33a6f3d3ae452ddc75422da226f41a7))

* Merge pull request #22 from TechNickAI/dependabot/pip/langchain-0.0.225

Bump langchain from 0.0.222 to 0.0.225 ([`8c74ddd`](https://github.com/TechNickAI/AICodeBot/commit/8c74ddd14af3c54db2a85f9462829dadf2e3e1ee))


## v0.9.1 (2023-07-11)

### Unknown

* Bump version to 0.9.1 ([`79c4e72`](https://github.com/TechNickAI/AICodeBot/commit/79c4e7222a7cb80b207fd865e97ef4af77136ff1))

* Add new AI personalities and update existing ones in prompts.py

The changes include the addition of new AI personalities: Einstein, Michael Scott, Peter Griffin, Socrates, and Spock. Existing AI personalities: Her, Jules, and Morpheus have been updated for clarity. The default personality has been changed from Her to Einstein. ([`0cc8f2a`](https://github.com/TechNickAI/AICodeBot/commit/0cc8f2a8bb6ee0a2bee5f5295200e32d1bf73562))

* Refine commit message handling and update prompts 📝

In this commit, we&#39;ve made some improvements to the way we handle commit messages. We&#39;ve added a step to remove any unwanted quotation marks from the commit message before it&#39;s written to a temporary file. This should help keep our commit messages clean and readable. 🧹

We&#39;ve also made some updates to our prompts file. We&#39;ve streamlined the &#39;Her&#39; personality description and made some changes to the commit message instructions. We&#39;ve switched from a list format to bullet points for better readability, and added some extra information about the length of the commit message. We hope these changes will make the prompts more user-friendly and informative. 📚

Remember, a good commit message is like a good joke - it&#39;s all about the delivery! 🎭 ([`bd6e915`](https://github.com/TechNickAI/AICodeBot/commit/bd6e9157b253e9fe293829771d9846ac7f2e36d8))

* Update README.md with enhanced feature list and usage instructions 📚

This commit introduces a more structured and detailed feature list in the README.md file, providing a clearer understanding of the current capabilities of AICodeBot and what&#39;s on the horizon. It also updates the usage instructions, specifically the initial setup process, to ensure a smoother onboarding experience for new users. The changes aim to make the tool more user-friendly and transparent about its functionality. 🚀 ([`919c21d`](https://github.com/TechNickAI/AICodeBot/commit/919c21d660414bd0fa0e9e38e16c0370571237ef))


## v0.9.0 (2023-07-11)

### Unknown

* Bump version to 0.9.0 ([`1b9c59f`](https://github.com/TechNickAI/AICodeBot/commit/1b9c59f280a487d078313aae94eb1e728a8117b8))

* Add configuration command and update key references

This commit introduces a new &#39;configure&#39; command in the build workflow, which creates or updates the config file. The &#39;openai_api_key&#39; is now fetched from the config file instead of the &#39;OPENAI_API_KEY&#39;. The &#39;personality&#39; option in the config file has also been updated to use the &#39;Her&#39; personality by default. The &#39;setup&#39; command has been removed as it&#39;s no longer needed.

Additionally, the &#39;DEFAULT_PERSONALITY&#39; has been set to &#39;Her&#39; and the &#39;PERSONALITIES&#39; keys have been updated to match the case of the personality names.

The tests have been updated to reflect these changes. The &#39;test_configure&#39; function now tests the &#39;configure&#39; command, and the &#39;test_setup_with_openai_key&#39; function has been removed as it&#39;s no longer relevant.

These changes make the configuration process more streamlined and user-friendly. 🚀&#34; ([`33fd8b5`](https://github.com/TechNickAI/AICodeBot/commit/33fd8b5caf301ff251fa9859c62baee4afbc3bde))

* Update model selection logic in helpers.py

This commit updates the `get_llm_model` function in `helpers.py` to dynamically select the best available model based on the OpenAI API key&#39;s supported engines and the token size. The previous hard-coded model selection logic has been replaced with a more flexible approach that queries the available engines from the OpenAI API. This ensures that the most suitable model is selected for the given token size, improving the efficiency and adaptability of the code.

In addition, the commit also includes minor changes to the import statements and the logging messages to accommodate the updated model selection logic.

Remember, the future is not set in stone. It&#39;s a wildly malleable thing that&#39;s still very much in the works. And you, dear developer, are one of the many hands that get to shape it. Let&#39;s keep coding a better future together! ([`4465984`](https://github.com/TechNickAI/AICodeBot/commit/44659846c2f1a47ec6b5a92cdedb80d932a584c8))

* Fix lint mis-spelling ([`a66057f`](https://github.com/TechNickAI/AICodeBot/commit/a66057f1f462906c7cfc057a98d17f52ebd3ddf7))

* Slight updates to the README ([`4a20b04`](https://github.com/TechNickAI/AICodeBot/commit/4a20b045039066f8874d43243f9503b489a977a4))


## v0.8.5 (2023-07-09)

### Unknown

* Bump version to 0.8.5 ([`8e51e0b`](https://github.com/TechNickAI/AICodeBot/commit/8e51e0b6019d04ae485652dda9d72c9019efe4cf))

* Enhanced file context generation in prompts

This commit ain&#39;t just about adding or removing a few lines of code. It&#39;s about giving a damn about the context. We&#39;ve added a function to generate a directory structure, and we&#39;re using it to provide a more comprehensive context for the sidekick prompt. Now, not only do you get the relevant files, but you also get a nice little map of the directory structure. Ain&#39;t that something?

And let&#39;s not forget about the files. We&#39;ve improved the way we handle them too. If there ain&#39;t no files, we don&#39;t just leave you hanging. We give you the directory structure and call it a day. But if there are files, oh boy, we give you the whole shebang. We read &#39;em, we count &#39;em, and we warn you if they&#39;re too damn big.

So, in summary, we&#39;ve made the file context generation in prompts more informative and more useful. And if you don&#39;t appreciate that, well, I don&#39;t know what to tell you. ([`17a3daf`](https://github.com/TechNickAI/AICodeBot/commit/17a3dafed60d417508af1d5f5aedbdc2d48536ca))

* Add directory structure generator and refactor tests

Alright, listen up. We&#39;ve got some new shit in town. We&#39;ve added a badass function to generate a directory structure, and it&#39;s got all the bells and whistles. It respects .gitignore, it can ignore patterns, and it&#39;s got a pretty print for your viewing pleasure.

We&#39;ve also been cleaning up the house. Moved the create_and_write_file function to conftest.py, cause that&#39;s where it belongs. It&#39;s a utility function, and it&#39;s gonna be used in multiple test files.

Speaking of tests, we&#39;ve added a whole bunch of them for the new directory structure generator. We&#39;re making sure this function is bulletproof.

And lastly, we&#39;ve done some minor text changes in prompts.py and conftest.py. Nothing to lose your shit over.

So there you have it. New features, better tests, cleaner code. That&#39;s how we roll. ([`0064c80`](https://github.com/TechNickAI/AICodeBot/commit/0064c80a0ada701f77e417edf4ea16d1931ecb90))

* Remove no longer needed agents file ([`76a8044`](https://github.com/TechNickAI/AICodeBot/commit/76a8044edc47642d3954951ae7f4c8a36cfabaab))

* Allow for prompts to work if there is no config file (such as in test) ([`1a495c2`](https://github.com/TechNickAI/AICodeBot/commit/1a495c2b50b98dff157b3d202ec2cc04bd84f2cd))


## v0.8.4 (2023-07-07)

### Unknown

* Bump version to 0.8.4 ([`59fb7d0`](https://github.com/TechNickAI/AICodeBot/commit/59fb7d0af52b4734cb65bad5d29ba29bc568de45))

* Adjust response token size and tweak precise temperature

Alright, listen up. We&#39;ve got some changes here. First off, we&#39;ve adjusted the response token size in the &#39;fun_fact&#39; and &#39;sidekick&#39; functions. This means the AI&#39;s response length can now be controlled more precisely. Ain&#39;t that some shit?

Next, we&#39;ve tweaked the precise temperature from 0 to 0.1. This little change is gonna make the AI&#39;s responses a bit more varied, but still on the sensible side.

We&#39;ve also made some minor changes to the &#39;debug&#39; and &#39;alignment&#39; tests, and added a new test for the &#39;sidekick&#39; function.

Lastly, we&#39;ve cleaned up the &#39;DEBUG_TEMPLATE&#39; in prompts.py. No big deal, just made it a bit more concise.

So there you have it. Changes made, commit done. Now let&#39;s get back to work. ([`8cc6ad8`](https://github.com/TechNickAI/AICodeBot/commit/8cc6ad857a82f8021842ae9fa6b2408e4716bdc9))


## v0.8.3 (2023-07-07)

### Unknown

* Bump version to 0.8.3 ([`6deb2ce`](https://github.com/TechNickAI/AICodeBot/commit/6deb2ce702b0c189b23d5dc8fba6a8fb08d6a1d4))

* Fix up tests for new config set up ([`3e0b5a6`](https://github.com/TechNickAI/AICodeBot/commit/3e0b5a677d27848f062e2ff2b2120c458387cac4))


## v0.8.2 (2023-07-07)

### Unknown

* Bump version to 0.8.2 ([`580a0e8`](https://github.com/TechNickAI/AICodeBot/commit/580a0e8d3068a8e4a6020838f052ae13a8b1e63c))

* Add personality selection to AICodeBot setup

This commit introduces a new feature to the AICodeBot setup process. Now, users can select a personality for their AI assistant from a predefined list. The chosen personality is stored in the configuration file and used to generate the AI&#39;s responses. This change also includes a refactoring of the personality prompts, moving them into a dictionary for easier access and management. Ain&#39;t no half-steppin&#39; here, we&#39;re making this bot a real cool cat. ([`6d03446`](https://github.com/TechNickAI/AICodeBot/commit/6d034468e73bb8c2fe56626cd0592d9b5b1c00d9))

* Add keywords to setup.py 🗝️

In this commit, we&#39;ve added a `keywords` field to the `setup()` function in `setup.py`. This field contains a string of keywords that describe the project: &#34;AI, coding, assistant, pair-programming, automation&#34;. This will help improve the discoverability of our project on platforms like PyPI. 🕵️‍♂️🔍 ([`7f0e817`](https://github.com/TechNickAI/AICodeBot/commit/7f0e8178d94276057c1d06e32417cf5cc72ac36f))

* Remove no longer needed template file, we use yaml now ([`8bc8181`](https://github.com/TechNickAI/AICodeBot/commit/8bc81811632c8ba64f014d47309aff5650dcae38))

* Refactor configuration handling, add setup command. Resolves #3

This commit introduces a significant overhaul of the configuration handling in the AICodeBot. The OpenAI API key is no longer fetched directly from the environment variables in the cli.py file. Instead, a new helper function, get_config_file, has been added to helpers.py. This function checks if the AICODEBOT_CONFIG_FILE environment variable is set and uses its value as the path to the configuration file. If the environment variable is not set, it defaults to using a file named .aicodebot.yaml in the user&#39;s home directory.

The setup command in cli.py has been updated to use this new function. It now also accepts a new option, --gpt-4-supported, which is a flag indicating whether the user has access to GPT-4. This information is stored in the configuration file along with the OpenAI API key.

The setup_config function in cli.py has been updated to reflect these changes. It now accepts two arguments: the OpenAI API key and a boolean indicating whether GPT-4 is supported. If the OpenAI API key is not provided, the function will attempt to fetch it from the environment variables or prompt the user to enter it. The function then validates the API key and checks if GPT-4 is supported (unless the --gpt-4-supported flag was used). The configuration data is then written to the configuration file.

The read_config function in helpers.py has also been updated to use the new get_config_file function.

Finally, tests have been added to test_cli.py to test the new setup command and the changes to the configuration handling. ([`924b8c6`](https://github.com/TechNickAI/AICodeBot/commit/924b8c68ccd25785e76edcb24939c2eb22a45ff1))

* Bump langchain from 0.0.222 to 0.0.225

Bumps [langchain](https://github.com/hwchase17/langchain) from 0.0.222 to 0.0.225.
- [Release notes](https://github.com/hwchase17/langchain/releases)
- [Commits](https://github.com/hwchase17/langchain/compare/v0.0.222...v0.0.225)

---
updated-dependencies:
- dependency-name: langchain
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`c66ce6a`](https://github.com/TechNickAI/AICodeBot/commit/c66ce6a8bc3a30c226565ac420a255dcb0277f08))

* Refactor configuration and dependency management. Resolves #19

In the realm of code, change is the only constant. In this instance, we have embarked on a journey of transformation, a metamorphosis of sorts. The configuration management has been refactored, shifting from environment variables to a more robust YAML-based configuration file. This change brings with it the promise of greater flexibility and ease of use.

In addition, the dependencies have been pruned. The python-dotenv package, once a vital part of our ecosystem, has been replaced by PyYAML, a more versatile and powerful tool for handling configuration data.

The code has been adjusted to accommodate these changes, with the OPENAI_API_KEY now being read from the new configuration file. This key is the bridge between our humble code and the vast knowledge of the OpenAI API, and its handling is of utmost importance.

In the grand tapestry of our codebase, these changes may seem minor, but remember, even the smallest thread can change the pattern of the weave. ([`fce0488`](https://github.com/TechNickAI/AICodeBot/commit/fce04880e1d86e2f6e0cafc9689ae0e17075825a))

* Expand the realm of personalities, refine the prompt generation

In the vast expanse of our code, we have ventured to broaden the spectrum of personalities that our AI can embody. Sherlock, The Dude, and Morpheus have joined the ranks, each bringing their unique essence to the table.

The method of generating prompts has been refined, transitioning from a series of conditional statements to a more efficient mapping. This change not only enhances readability but also simplifies the process of adding new commands in the future.

Furthermore, we have fortified our code against the unknown. In the event of an unrecognized personality or command, our code will now raise a more informative error, guiding us towards the path of resolution.

Remember, developer, the code is a living entity, evolving and growing with each commit. This change is but a step in its journey towards perfection. ([`1b346b8`](https://github.com/TechNickAI/AICodeBot/commit/1b346b8b86af56b8a464f363fff81bd2a3b4901f))


## v0.8.1 (2023-07-07)

### Unknown

* Bump version to 0.8.1 ([`a0670af`](https://github.com/TechNickAI/AICodeBot/commit/a0670afc3852097ab47bbab38165fcae3113db0e))

* Refactor prompt handling and add personality traits

This commit is a major overhaul of the prompt handling system. We&#39;ve ditched the old yaml-based prompts and moved everything into a single Python file, `prompts.py`. This makes it easier to manage and modify prompts on the fly.

We&#39;ve also added a new feature: personality traits. Now, the bot can have different personalities, like Jules from Pulp Fiction or the AI from Her. This is controlled by an environment variable, so you can switch personalities without changing the code.

The `cli.py` file has been updated to use the new prompt system. The `alignment` command now takes a `response_token_size` option, which lets you control the length of the bot&#39;s responses.

Finally, we&#39;ve cleaned up the test suite a bit. The `alignment` test now uses the new `response_token_size` option, and we&#39;ve added a check to skip certain tests if the OpenAI API key isn&#39;t set.

This is a big change, but it&#39;s a good one. It makes the bot more flexible and easier to use. So buckle up, because this is just the beginning. ([`109a901`](https://github.com/TechNickAI/AICodeBot/commit/109a90102e52150540ddc731050c7137f10f0473))

* Refactor get_llm_model and add token size checks 🔄🔍

This commit moves the `get_llm_model` function from `cli.py` to `helpers.py` for better code organization. It also introduces token size checks in various functions in `cli.py` to ensure the token size does not exceed the model&#39;s capacity. If the token size is too large, an exception is raised with a helpful error message. 🚀📏

In `prompts/sidekick.py`, token length is now logged for each file in the context, providing useful debugging information. 📊🔍

These changes improve the robustness of the code and provide better feedback to the user when the token size is too large. 🛠️👍 ([`48e328d`](https://github.com/TechNickAI/AICodeBot/commit/48e328d53c1266fc9ad81ab928d23fe61f62dad1))

* Enhance logging and add personality selection 🎭🔍

This commit introduces several enhancements to the codebase:

- Added `loguru` for improved logging throughout the application. This will help in better debugging and understanding the flow of the application. 🕵️‍♂️
- Logging levels can now be controlled via the `LOG_LEVEL` environment variable. This allows for flexible control over the verbosity of logs. 🎚️
- Added logging statements in various parts of the code to provide more context during execution. This includes logging the token length of text, the diff for commits, and the execution of commands. 📝
- Introduced the ability to select the AI&#39;s personality via the `AICODEBOT_PERSONALITY` environment variable. This adds a fun and customizable aspect to the AI&#39;s responses. 🎭
- Updated the requirements to include `loguru`. 📦

These changes aim to improve the overall user experience and maintainability of the code. 🚀 ([`8df4dc4`](https://github.com/TechNickAI/AICodeBot/commit/8df4dc41ed3f7f4c620e0bed927b62e1b3174ff7))

* Expand personality options and fix typo 🎭🔧

In this commit, we&#39;ve made some exciting changes to our `personalities.py` file. We&#39;ve corrected a small typo in the description of the &#39;Her&#39; personality, changing &#39;fro&#39; to &#39;from&#39; 🕵️‍♂️.

But that&#39;s not all! We&#39;ve also introduced a new personality, &#39;Jules&#39; from Pulp Fiction, to our repertoire 🎬. This addition will allow for a more diverse range of interactions and responses.

Lastly, we&#39;ve updated the `get_personality_prompt` function to accept a parameter, allowing the user to choose the personality they want to interact with. If no personality is specified, &#39;Her&#39; will be the default choice.

This is a step forward in making our AI more versatile and engaging. Stay tuned for more updates! 🚀 ([`564fd76`](https://github.com/TechNickAI/AICodeBot/commit/564fd76e436ab72023a61c05dc4b906cf4c1e0f9))

* Enhance user interaction with editor choice and input options 🎛️

In this commit, we&#39;ve made some user-friendly enhancements to the CLI interaction. Now, the user&#39;s preferred editor, as specified by the `EDITOR` environment variable, is used for editing tasks. If no editor is specified, we default to vim. The prompt message has been updated to reflect this change. 📝

Additionally, we&#39;ve introduced a new way to trigger the edit mode. If the user&#39;s input ends with `\e`, the input text (excluding `\e`) will be opened in the editor for further modification. This provides a more flexible way for users to edit their input. 🔄

As always, the user can quit the program by entering `q`. These changes aim to make the interaction more intuitive and user-friendly. Happy coding! 🚀 ([`fe95fdc`](https://github.com/TechNickAI/AICodeBot/commit/fe95fdc40b22d176aed67b8212b1d30b38e44d41))

* Update readme with emojis ([`76f595a`](https://github.com/TechNickAI/AICodeBot/commit/76f595aa83e4ac235f591b277c0ba5f6fd904648))

* Update prompt personality - adding the &#34;you are from the future&#34; thing made it weird. ([`ae9321a`](https://github.com/TechNickAI/AICodeBot/commit/ae9321a745e6deb29429168752c8dfae1ab60a7b))

* &#34;🚀 Enhance AI Personality Across Prompts 🤖

In this commit, we&#39;ve added a friendly and helpful AI personality, inspired by the movie &#39;Her&#39;, across various prompts. This includes `alignment.yaml`, `commit_message.yaml`, `debug.yaml`, `fun_fact.yaml`, `review.yaml`, and `sidekick.py`. The AI now comes from the future, ready to guide human developers to a better future with a dash of humor and emojis. 🎉

We&#39;ve also introduced a new file `personalities.py` to manage different AI personalities. Currently, it only contains the &#39;Her&#39; personality, but it&#39;s designed for easy expansion in the future. 📚

Lastly, we&#39;ve made minor tweaks in `review.yaml` to improve the code review process, including pointing out spelling mistakes in plain text files. 🕵️‍♂️

Let&#39;s make our AI more human-like and fun! 🥳&#34; ([`6fce135`](https://github.com/TechNickAI/AICodeBot/commit/6fce135a1f791411aba2c47493702659cb904646))

* Update README and CONTRIBUTING with the latest thoughts ([`9409297`](https://github.com/TechNickAI/AICodeBot/commit/94092971107151679b31a59609adaf6ab5bfbe28))

* Break long line up to fix super linter error ([`7a73ccd`](https://github.com/TechNickAI/AICodeBot/commit/7a73ccd0330e4e37e038006d8ab0b08e6e1bf66b))

* Update README with more info on sidekick ([`01ab8c0`](https://github.com/TechNickAI/AICodeBot/commit/01ab8c00027f99bd26132be54d451deeb0d89c2f))


## v0.8.0 (2023-07-04)

### Unknown

* Add AI Sidekick feature description to README.md ([`26dca3b`](https://github.com/TechNickAI/AICodeBot/commit/26dca3b0e20c58afa7a07599f8873397bb416115))

* Bump version to 0.8.0 - introduce sidekick ([`c62896b`](https://github.com/TechNickAI/AICodeBot/commit/c62896b5208a92a1fb092f0788b0d13c9429338c))

* Enhance AI sidekick with file context support 📁

This commit introduces the ability for the AI sidekick to use the contents of specified files as context during its session. This is achieved by adding a new function `generate_files_context` which reads the contents of the provided files and formats them into a string that can be used as context.

The `sidekick` function in `cli.py` has been updated to accept a list of files as arguments, generate the file context, and pass it along with the user&#39;s request to the `generate_sidekick_prompt` function. The token size calculations and model selection have also been adjusted to account for the additional context.

The `generate_sidekick_prompt` function now accepts an additional `files` parameter and includes the generated file context in the prompt template. The prompt template itself has been updated to include a placeholder for the file context.

The import statements in `cli.py` and `__init__.py` have been updated to include the new `generate_files_context` function.

This enhancement provides the AI sidekick with more context, potentially improving its ability to assist the user. ([`667240a`](https://github.com/TechNickAI/AICodeBot/commit/667240a5387ab5dc7ae107bf9e9fadfa1869a9d9))

* Refactor and enhance AI sidekick feature in CLI

This commit refactors the AI sidekick feature in the CLI, improving its functionality and user interaction. The changes include:

- Replacing the `task` option with `request` for better clarity.
- Generating the prompt with the appropriate context using the new `generate_sidekick_prompt` function.
- Setting up a continuous loop for multiple questions from the user.
- Adding a new option for the user to edit their question in their editor.
- Improving the live markdown display with the `RichLiveCallbackHandler`.

Additionally, a new module `prompts` has been added to handle prompt generation, starting with the sidekick prompt. ([`da39811`](https://github.com/TechNickAI/AICodeBot/commit/da39811fba8ea22785d7e06b9cc21ed5fbebd217))

* Merge pull request #15 from TechNickAI/dependabot/pip/langchain-0.0.222

Bump langchain from 0.0.207 to 0.0.222 ([`f6266f9`](https://github.com/TechNickAI/AICodeBot/commit/f6266f93575da898996df64972d9b37c096b0613))

* Include the output when the test fails ([`398bc51`](https://github.com/TechNickAI/AICodeBot/commit/398bc51bbac4536feb74163b98082d4b62d2766d))

* Bump langchain from 0.0.207 to 0.0.222

Bumps [langchain](https://github.com/hwchase17/langchain) from 0.0.207 to 0.0.222.
- [Release notes](https://github.com/hwchase17/langchain/releases)
- [Commits](https://github.com/hwchase17/langchain/compare/v0.0.207...v0.0.222)

---
updated-dependencies:
- dependency-name: langchain
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`dd4f992`](https://github.com/TechNickAI/AICodeBot/commit/dd4f992cacc18731c0cdd9e3a166f9834c1aff38))

* Refactor test skipping condition for missing API key

This commit refactors the condition used to skip tests when the OPENAI_API_KEY environment variable is not set. The previous condition checked if the value of the variable was `None`, but this has been changed to a more Pythonic way of checking if the variable is not set or empty. This change improves readability and ensures that tests are skipped even when the variable is set to an empty string. ([`f303cd7`](https://github.com/TechNickAI/AICodeBot/commit/f303cd743ebb445f5ab8273d3328d61932feb73a))


## v0.7.4 (2023-07-04)

### Unknown

* Bump to version 0.7.4. Streaming markdown responses ([`34d91e7`](https://github.com/TechNickAI/AICodeBot/commit/34d91e766a40186dc25be33d53b38d27622f9b83))

* Refactor AI chat model for live streaming and precise responses

This commit introduces several changes to the AI chat model in the `aicodebot/cli.py` file. The main changes include:

- The introduction of two new temperature settings: `PRECISE_TEMPERATURE` and `CREATIVE_TEMPERATURE`. These settings allow for more control over the randomness of the AI&#39;s responses.
- The use of the `rich.live.Live` class for live streaming of the AI&#39;s responses. This is implemented in the `alignment`, `debug`, `fun_fact`, `review`, and `sidekick` commands.
- The creation of a `RichLiveCallbackHandler` class that updates the live stream with each new token generated by the AI.
- Adjustments to the `max_tokens` parameter in the `fun_fact` and `sidekick` commands.

These changes aim to improve the user experience by providing real-time feedback from the AI and allowing for more precise responses. 🤖💬 ([`0ddc6d2`](https://github.com/TechNickAI/AICodeBot/commit/0ddc6d220f309afce26689e420595ef5bfcca2c0))

* Implement markdown support for AI responses. Resolves #13

This commit introduces markdown support for the AI responses in the `aicodebot` CLI. The `rich.markdown` module is imported and used to print the AI responses in markdown format. This change affects the `alignment`, `debug`, `fun_fact`, and `review` commands.

Additionally, the prompts for these commands have been updated to instruct the AI to respond in markdown format. This enhancement improves the readability and formatting of the AI responses, making them more user-friendly. ([`172bd5c`](https://github.com/TechNickAI/AICodeBot/commit/172bd5c2445e1ace76c6bf46ee8ac63d9826317c))


## v0.7.3 (2023-07-03)

### Unknown

* Bump version to 0.7.3 ([`2b6e400`](https://github.com/TechNickAI/AICodeBot/commit/2b6e4000690cbbb6ec41cef93b7000045c21cd65))

* Update repository references from novara-ai to TechNickAI 🔄

This commit updates all references in the codebase from the old repository (novara-ai/aicodebot) to the new one (TechNickAI/AICodeBot). Changes include updates in CONTRIBUTING.md, README.md, and setup.py files. This ensures that all links and references within the project point to the correct location. ([`d8826e8`](https://github.com/TechNickAI/AICodeBot/commit/d8826e8bea0d4a1f39f107cdb39bab9c803934a8))


## v0.7.2 (2023-07-03)

### Unknown

* Bump version to 0.7.2 ([`5cfe2e3`](https://github.com/TechNickAI/AICodeBot/commit/5cfe2e32f0df342f9a7f1512b77461dd820d7910))

* Enhance git_diff_context to handle file renaming and deletion

This commit enhances the `git_diff_context` function in `aicodebot/helpers.py` to handle file renaming and deletion. Previously, the function only handled new and modified files. Now, it can also handle renamed and deleted files.

The changes include:
- Splitting the status code and file name(s) into separate variables.
- Adding conditions to handle different status codes: &#39;A&#39; for new files, &#39;R&#39; for renamed files, and &#39;D&#39; for deleted files.
- Updating the `tests/test_helpers.py` to include tests for the new functionality.

This enhancement provides a more comprehensive overview of changes in the git repository. ([`5c27b8c`](https://github.com/TechNickAI/AICodeBot/commit/5c27b8c164f4800ac46e10339557d6550c4fa2b5))

* Refactor &#39;code_agent&#39; to &#39;sidekick&#39; and update README.md 🔄

This commit includes several changes:
- The term &#39;coding companion&#39; in README.md has been replaced with &#39;coding sidekick&#39; to better reflect the role of AICodeBot.
- The &#39;Repository Management&#39; section in README.md has been renamed to &#39;Repository / Project Management&#39; and the tasks under this section have been rephrased for clarity.
- In the &#39;sidekick&#39; function in cli.py, a line has been added to direct users to the new &#39;sidekick.md&#39; document for more information.
- The &#39;code_agent.md&#39; document has been renamed to &#39;sidekick.md&#39; and updated to provide a comprehensive overview of the &#39;sidekick&#39; feature.

These changes aim to improve the clarity and consistency of the project&#39;s documentation. ([`6e6c121`](https://github.com/TechNickAI/AICodeBot/commit/6e6c121c01dde25429e96157b7ad10eb61b9741d))


## v0.7.1 (2023-07-03)

### Unknown

* Bump version to 0.7.1 and improve &#39;sidekick&#39; feature warnings 🚀

This commit includes two main changes:

1. The version of the `aicodebot` package has been bumped from 0.7.0 to 0.7.1.

2. The &#39;sidekick&#39; feature in `cli.py` has been updated with more explicit warning messages. These messages inform the user that the feature is experimental and may not perform optimally. Additionally, the command description has been slightly modified for clarity. Two new styles for console output, `error_style` and `warning_style`, have been added to enhance these messages visually. ([`d25d3de`](https://github.com/TechNickAI/AICodeBot/commit/d25d3de8d46a7964be71b56c730d7514bb07eb53))

* Bump version to 0.7.0 ([`64bb80d`](https://github.com/TechNickAI/AICodeBot/commit/64bb80d40c7c3642d874264c70b475133d64827b))


## v0.7.0 (2023-07-02)

### Unknown

* Mark sidekick as experimental ([`0e8591c`](https://github.com/TechNickAI/AICodeBot/commit/0e8591c2ec38bc99b98e310a5ba08e9d071738fd))

* Refine agent interaction and improve CLI output

This commit includes two main changes:

1. In `aicodebot/agents.py`, the prompt for the AI agent has been updated to emphasize the importance of properly formatting responses in JSON. This change is crucial to ensure that the agent&#39;s responses can be correctly parsed and processed.

2. In `aicodebot/cli.py`, the verbosity level passed to the `get_agent` function is now the one provided by the user, instead of always being `True`. Additionally, the agent&#39;s response is now displayed in a more user-friendly way, with a spinner indicating that the agent is &#34;thinking&#34;, and the response being printed separately from the spinner. This improves the user experience by providing clearer feedback about what the agent is doing. ([`b3f599c`](https://github.com/TechNickAI/AICodeBot/commit/b3f599cf33b658cf542283f1fa00d66268bc03e3))

* Add AI sidekick command

This commit introduces a new feature where an AI sidekick can assist with tasks. The AI sidekick is initialized with a set of tools for file management and human input. The sidekick can be invoked via the new `sidekick` command in the CLI.

Additionally, the `review` command has been updated to clarify that it can review either unstaged changes or a specified commit. The help text for the `--commit` option has been updated to reflect this.

Minor changes have also been made to the `get_llm_model` function to allow for a default token size. ([`80118f1`](https://github.com/TechNickAI/AICodeBot/commit/80118f1799304297378ba048e5301f40542efdea))

* Refine README.md for clarity and precision

This commit includes several changes to the README.md file to improve clarity and precision. The changes include:

- Reframing the description of AICodeBot&#39;s planned interfaces for better clarity.
- Removing redundant symbols and phrases for a cleaner look.
- Adding more context to the description of AICodeBot&#39;s use of OpenAI&#39;s ChatGPT.
- Enhancing the descriptions of the current features to better reflect their benefits and use cases.
- Correcting a typo in the AI-Assisted Debugging section.
- Reframing the Alignment section to emphasize the values of the people who create technology, rather than the engineers alone. ([`3e45ebf`](https://github.com/TechNickAI/AICodeBot/commit/3e45ebf817874693eb1d2937c2eac2b3b13a2ccb))

* Update README and code_agent docs, remove WIP feature

This commit updates the README.md and code_agent.md files. The changes include:
- Removal of the &#34;AI-Assisted Code Creation&#34; section from README.md as it was a work-in-progress feature.
- Addition of a PyPI version badge in README.md.
- Reorganization of the &#34;Installation and Usage&#34; section in README.md.
- Clarification on the choice between GPT-3.5 and GPT-4 in README.md.
- Mention of future support for local AI models in README.md.
- In code_agent.md, the &#39;code&#39; command is now presented as a future vision, not a current feature.
- Additional context provided for the &#39;code&#39; command in code_agent.md.

These changes aim to provide clearer and more accurate information about the current state and future plans of the project. 📚🔮 ([`7e0cf1a`](https://github.com/TechNickAI/AICodeBot/commit/7e0cf1af49482138fb58ea395a6fcb4523aa6982))

* Add sample task prompts to AICodeBot documentation

This commit introduces a new section in the `code_agent.md` documentation file. The section provides a list of sample task prompts that can be used to guide AICodeBot in performing various coding tasks. These tasks range from practical code improvements to fun and whimsical modifications. This addition will help users understand how to interact with AICodeBot more effectively. 🤖📚 ([`08e47b4`](https://github.com/TechNickAI/AICodeBot/commit/08e47b4b284426454fdce1711d28f2eb46c34a0a))


## v0.6.2 (2023-06-30)

### Unknown

* Bump to version 0.6.2 ([`f06d028`](https://github.com/TechNickAI/AICodeBot/commit/f06d0284794e2d2334c55ea5e34c437631b5a87d))

* Add documentation for AICodeBot Code Agent feature

This commit introduces a new markdown file, `docs/code_agent.md`, which provides comprehensive documentation for the AICodeBot Code Agent feature. The document outlines the various steps involved in the code generation process, from task understanding to code review. It also highlights the future plans for reinforcement learning and active learning. 📚🤖 ([`39ce0bf`](https://github.com/TechNickAI/AICodeBot/commit/39ce0bf2e586467d202116af51e83d368e533117))

* Fix issue with get_diff_context when new files are added. Add Unit test to catch it.

This commit includes several changes aimed at improving the readability and maintainability of the codebase:

- In `aicodebot/helpers.py`, the method of reading file contents has been corrected to use the `Path` object correctly.
- In `tests/conftest.py`, the temporary git repository fixture has been refactored to use pytest&#39;s built-in `tmp_path` fixture for creating temporary directories. This simplifies the code and makes it more reliable.
- In `tests/test_helpers.py`, the tests for the `git_diff_context` function have been significantly refactored for clarity and completeness. The new tests are more thorough and easier to understand. ([`42348b5`](https://github.com/TechNickAI/AICodeBot/commit/42348b568d76d6f059d94f632bf987f3557a8f3a))

* Add note about automating changelog/release notes ([`714c416`](https://github.com/TechNickAI/AICodeBot/commit/714c4161a0cf5eac86b38c174bc1af0697e0bce2))

* Bump version to 0.6.1.1 ([`02dc7f7`](https://github.com/TechNickAI/AICodeBot/commit/02dc7f7923c60ce72449ca63cfe7865081ac56da))

* Update README.md to enhance descriptions of AICodeBot features

This commit updates the README.md file to provide more detailed and engaging descriptions of the AICodeBot features. The changes aim to better explain the benefits and functionality of the AI-Assisted Git Commit, AI-Assisted Code Review, and AI-Assisted Debugging features. The goal is to provide users with a clearer understanding of how these features can enhance their coding experience and productivity. ([`3f87396`](https://github.com/TechNickAI/AICodeBot/commit/3f87396246d83767f4c3be8ccdd6490b11452b82))

* Reduce default max tokens to 512

This commit halves the default maximum tokens from 1024 to 512 in the `aicodebot/cli.py` file. This change is expected to improve the performance and efficiency of the AI code bot. ([`08a88f2`](https://github.com/TechNickAI/AICodeBot/commit/08a88f265200281db7c2b2a019ef249671e1e7ac))


## v0.6.1 (2023-06-29)

### Unknown

* Increase token size buffer to account for underestimation

In the `get_llm_model` function, the token size is now increased by 10% to account for the occasional underestimation by tiktoken. This change helps to ensure that the selected model can handle the required token size. ([`aa156b5`](https://github.com/TechNickAI/AICodeBot/commit/aa156b54941f8271568617203b0d75f9f399105d))

* Update CONTRIBUTING.md and README.md with enhanced features and roadmap

This commit includes updates to the CONTRIBUTING.md and README.md files. The changes in CONTRIBUTING.md provide more detailed descriptions for the additional interfaces and documentation needs. The README.md file has been updated with a new feature description for AI-Assisted Code Creation and a more detailed explanation of how it works. The roadmap of upcoming features and user interfaces has been updated with a more readable format. ([`28e213c`](https://github.com/TechNickAI/AICodeBot/commit/28e213c6796ffe769fb5844f107d9f2a156668c5))


## v0.6.0 (2023-06-28)

### Unknown

* Bump version to 0.6.0. Notable change - ChatGPT 4 support! ([`b5a1ac8`](https://github.com/TechNickAI/AICodeBot/commit/b5a1ac86101c0c8e9e20bc7b1e6e1a5c404a5761))

* Update README with GPT-4 usage details

This commit adds information about the usage of GPT-4 and GPT-3.5 in the AICodeBot tool. It explains the differences between the two and provides guidance on how to choose the appropriate version based on the user&#39;s needs and OpenAI account capabilities. A link to the GPT-4 API waitlist is also included for users whose accounts do not currently support GPT-4. ([`f11a7cf`](https://github.com/TechNickAI/AICodeBot/commit/f11a7cf59a761f446f94385f72157bca98739f36))

* Update commit message guidelines for brevity and speed ([`ba565b5`](https://github.com/TechNickAI/AICodeBot/commit/ba565b59267496f9fb7f7049fa54d5fa8c25c692))

* Update model selection logic to support GPT-4 🚀

This commit introduces changes to the model selection logic in the AI code bot. Previously, the bot was hardcoded to use the GPT-3.5-turbo model. Now, the bot checks if GPT-4 is supported by the provided OpenAI API key and uses it if available. If GPT-4 is not supported, the bot falls back to using GPT-3.5-turbo.

The model selection is also now dynamic based on the token size of the request. The bot selects the largest model that supports the required token size. This ensures that the bot can handle larger contexts while still using the most powerful model available.

Additionally, a new environment variable `GPT_4_SUPPORTED` has been added to the `.aicodebot.template` file to store the GPT-4 support status of the API key. This value is set during the setup process when the API key is validated.

This update enhances the bot&#39;s capabilities and prepares it for future improvements in the OpenAI models. ([`a52de62`](https://github.com/TechNickAI/AICodeBot/commit/a52de626cb3b57294d419cf652b119ec287c049d))

* Update ruff-pre-commit to v0.0.275 🚀 ([`70ac379`](https://github.com/TechNickAI/AICodeBot/commit/70ac3796764d889b539576b9bfd1c411a5ab9063))

* Update CONTRIBUTING link in README.md to use absolute URL ([`9ee6254`](https://github.com/TechNickAI/AICodeBot/commit/9ee62540fcf5551e972a89cfca50312834425465))

* Markdown cleanup/lint fixes ([`a4d4fd2`](https://github.com/TechNickAI/AICodeBot/commit/a4d4fd266310c2d1ad2cae5269310f4bc8a3e196))

* Add section on releases to CONTRIBUTING.md 🚀

This commit adds a new section to CONTRIBUTING.md that explains how to initiate a new release for AICodeBot. The release process uses a GitHub Actions workflow that builds the codebase, uploads the package to PyPI, and creates a new GitHub release. To initiate a new release, simply push a new tag that starts with &#39;v&#39;, followed by the version number (for example, &#39;v1.0.0&#39;). Please ensure that your version numbers follow the Semantic Versioning guidelines. To learn more about the release process, you can review the PyPI release workflow. ([`8349163`](https://github.com/TechNickAI/AICodeBot/commit/83491637d7dccdb212e251488dfc50e12528213c))

* Finish moving contribution notes to CONTRIBUTING ([`b3e38bf`](https://github.com/TechNickAI/AICodeBot/commit/b3e38bffd1710906f18fbe80ede4b65b3980b873))


## v0.5.4 (2023-06-27)

### Unknown

* Bump version to 0.5.4 🚀 ([`0041e67`](https://github.com/TechNickAI/AICodeBot/commit/0041e67c585a037677cdbdc9f94a01bd21940b90))

* Bug fix: Create a buffer so we aren&#39;t close the 4k tokenization limit. I&#39;ve seen cases where the tiktoken token count doesn&#39;t agree with OpenAI&#39;s count. ([`eebc315`](https://github.com/TechNickAI/AICodeBot/commit/eebc315283d6bc8b2b6d71a6eabfe13cd0d63a40))

* Improved README. Create CONTRIBUTING.md and move the development instructions there. ([`a1de539`](https://github.com/TechNickAI/AICodeBot/commit/a1de5398c66e848fa55620ba3ed0b26122eac3f7))

* Bump version to 0.5.3 🚀 ([`b1f5736`](https://github.com/TechNickAI/AICodeBot/commit/b1f57367d5ab4b9e448782acc286880b75fec712))


## v0.5.3 (2023-06-27)

### Unknown

* Add write permissions to be able to create a release tag ([`517d3f8`](https://github.com/TechNickAI/AICodeBot/commit/517d3f8e488685932ff6408a37a3256314e555c5))

* Lint fixes for README ([`8078df8`](https://github.com/TechNickAI/AICodeBot/commit/8078df8cd93fa8ab09620d26b3b973be8857dd4e))


## v0.5.2 (2023-06-27)

### Unknown

* Bump version to 0.5.2 🚀 ([`eaa8b29`](https://github.com/TechNickAI/AICodeBot/commit/eaa8b29aabd9514cc1249f1f5dd138aacfafcd15))

* Minor text changes, additional comment dividers, and additional comments ([`58a4bdc`](https://github.com/TechNickAI/AICodeBot/commit/58a4bdc3e1a0d493640fa2146e61f40144dde751))

* Add aicodebot to requirements-dev.txt for self-building 🤖 ([`7e28b78`](https://github.com/TechNickAI/AICodeBot/commit/7e28b787f5bdbd1e6ee034255244fc36d056a343))

* Review and update all the language in the cli. Use -V or --version instead of a full command for it. ([`62c440c`](https://github.com/TechNickAI/AICodeBot/commit/62c440c556bb35a04cea4ccbde24a76bdd4e9bb2))

* Massage the prompts with improved language, and add additional comments to the top of the file to explain context ([`286bd1b`](https://github.com/TechNickAI/AICodeBot/commit/286bd1b62706507bc8edb9259543a17e1fa5b9a7))

* Update Dependabot configuration to include weekly updates for GitHub Actions and pip packages on Wednesdays :rocket: ([`d0b1eb3`](https://github.com/TechNickAI/AICodeBot/commit/d0b1eb33e319244c1135f7250205bc0909f2598b))

* Create a GitHub release on tag push. Minor formatting changes. Centralize pip installs ([`8f81ebb`](https://github.com/TechNickAI/AICodeBot/commit/8f81ebb37bf67de61d4b8fb4b37ee630369ebc6d))

* Update build.yaml - mostly shift all the white space, but did some additional clean up as well ([`b74bb5e`](https://github.com/TechNickAI/AICodeBot/commit/b74bb5e09d91e20d329cc48e8522ffcb094ffc0d))

* Update review prompt with clearer instructions and diff context. :pencil: ([`78305f9`](https://github.com/TechNickAI/AICodeBot/commit/78305f97a3e049a308c6b76da09441e58b7672ab))


## v0.5.1 (2023-06-27)

### Unknown

* Bump version to 0.5.1 🚀 ([`a2ed976`](https://github.com/TechNickAI/AICodeBot/commit/a2ed976df6cfef42fffd4cf7486bf37bda149e3f))

* Update commit message guidelines in prompts/commit_message.yaml file. ([`5eb84d8`](https://github.com/TechNickAI/AICodeBot/commit/5eb84d8135c0f10cfed7a090194ab254500c2836))

* Update the review prompt ([`68aa479`](https://github.com/TechNickAI/AICodeBot/commit/68aa4798f942fdf303d45661d6d68fa9c291ef24))

* Add comments for clarity in git_diff_context ([`2a72d73`](https://github.com/TechNickAI/AICodeBot/commit/2a72d737d44c86746f47eb0764f9df55fcc89ee5))

* Remove LangChain badge because apparently I can&#39;t figure out how shields.io works. ([`55c92ef`](https://github.com/TechNickAI/AICodeBot/commit/55c92ef42ec095a2216bcd5bb100c4c574ae21f8))

* Update the README with more thorough feature description, better install instructions, and a note about Alignment ([`882b09e`](https://github.com/TechNickAI/AICodeBot/commit/882b09e4238342740e6ead03c90bb033e1166410))

* Add test_review function to test workflow ([`82c89ea`](https://github.com/TechNickAI/AICodeBot/commit/82c89ea5ef475e57c1d4cd0448d1e2f02caafbc3))

* Refactor git_diff_context function to handle staged and unstaged files separately ([`ab06595`](https://github.com/TechNickAI/AICodeBot/commit/ab065953eeca08b7d13a087973af9a4e8d0943c0))


## v0.5.0 (2023-06-27)

### Unknown

* Bump version to 0.5.0 🚀 ([`3d22ea5`](https://github.com/TechNickAI/AICodeBot/commit/3d22ea53983f740a062250e2cc1f568b947c4292))

* Use a git_diff_context and check the token size for review and commit functions. ([`37612b8`](https://github.com/TechNickAI/AICodeBot/commit/37612b882ac8eeeb1aa73429da8be9188678142e))

* Add tiktoken library for tokenization and update git_diff_context function

The tiktoken library is added to the project to provide tokenization functionality.
The get_token_length function is added to helpers.py to get the number of tokens in a string using the tiktoken library.
The git_diff_context function is updated to include new files in the diff output and to provide 10 lines of context.
Tests are added for the new functions. ([`4b5db06`](https://github.com/TechNickAI/AICodeBot/commit/4b5db0603a7f93dd74373d8071b47bef8edf769c))

* New command: review that will do a code review for [un]staged changes or a commit ([`0a9102a`](https://github.com/TechNickAI/AICodeBot/commit/0a9102a482340e85fe478941d6917cff6b7318ec))

* Correct spelling in Dependabot configuration file ([`d7e0197`](https://github.com/TechNickAI/AICodeBot/commit/d7e019714d2c60491db9962ade80f0c11a60a43e))

* Update Dependabot configuration file ([`a38657f`](https://github.com/TechNickAI/AICodeBot/commit/a38657fb6b7f3ea36a22622d06be1feb753acf93))

* Update Dependabot configuration file ([`6e9a5de`](https://github.com/TechNickAI/AICodeBot/commit/6e9a5de333a562e59adf1a519242d5e91ed3ca03))

* Add Dependabot configuration file ([`7322f4d`](https://github.com/TechNickAI/AICodeBot/commit/7322f4d41bbdbe4590cca66e1a92f37a8b72dbbf))

* Add git configuration for AI Code Bot Test user and email 🤖 ([`ea84b0d`](https://github.com/TechNickAI/AICodeBot/commit/ea84b0d58b886ea9c48a34336491ec89451a8c17))

* Set up a git user in Github Action environment so all the tests run ([`782eb1a`](https://github.com/TechNickAI/AICodeBot/commit/782eb1a0c5a33616b3556df72718664707c8582c))

* Add github action for pypi release. Version 0.4.1 ([`bc82dce`](https://github.com/TechNickAI/AICodeBot/commit/bc82dceda2def8fd57a511bb7ef0bf8740b9219e))

* Add an additional feature ([`31e37fb`](https://github.com/TechNickAI/AICodeBot/commit/31e37fbab8c294a74df180e68289d0140039c0da))

* Explicitly add beautifulsoup4, because langchain needs it for llmchain ([`24b0c47`](https://github.com/TechNickAI/AICodeBot/commit/24b0c4715d5f712efe5a7f0788ac354b6e67c2fa))

* Improve commit command with a pre-commit check ([`7e21b78`](https://github.com/TechNickAI/AICodeBot/commit/7e21b78ccc0751593ef482a1dad3d892d1197119))

* Upgrade test infrastructure with reusable fixtures. Add test for commit command. Start using the gitpython library ([`d1d487a`](https://github.com/TechNickAI/AICodeBot/commit/d1d487af9cf5824e1367d746a93f18521fb519b7))

* ls returns exit code 2 on some operating systems ([`2ff9f76`](https://github.com/TechNickAI/AICodeBot/commit/2ff9f76257283083308cefe04d1c220546df7474))

* Check the exit code for debug test, instead of trying to look in the output, which has been unreliable. ([`35ae077`](https://github.com/TechNickAI/AICodeBot/commit/35ae07737c4750ed729ffa2b68f6a1b159381391))

* Fix debug command output formatting and add TODO comment for AI response check ([`5cb91ac`](https://github.com/TechNickAI/AICodeBot/commit/5cb91acb48b6f0e24514b19ea2e1bf4b4292d354))

* git config doesn&#39;t work on github actions, so ditch the name feature, it wasn&#39;t adding anything anyway. ([`49c743b`](https://github.com/TechNickAI/AICodeBot/commit/49c743be6d11d94e94dc63b66d5325aee5b8a870))

* Remove the trailing } after OPENAI_API_KEY secret 🔑 ([`1ba2e32`](https://github.com/TechNickAI/AICodeBot/commit/1ba2e3275958c100d2c8e30a5f683f6f89d2fe78))

* Remove stray code that no longer applies ([`f048d32`](https://github.com/TechNickAI/AICodeBot/commit/f048d329981f1f465c2d6abdfc1d3b6f724a6793))

* Add more tests for cli commands ([`1c218d9`](https://github.com/TechNickAI/AICodeBot/commit/1c218d94195fb6a0f937abbc4b54c83f8b3dd09c))

* Add OpenAI API key secret to GitHub Actions workflow and tests 🔑

Add support for OpenAI API key secret to GitHub Actions workflow and tests, and add tests for alignment command. ([`6a1b29c`](https://github.com/TechNickAI/AICodeBot/commit/6a1b29ca9c16e4604fabaf17b60ee620bb80e4b7))

* Update README badges with proper url for codecov ([`ebf8592`](https://github.com/TechNickAI/AICodeBot/commit/ebf85927346b7d62c7a7db0da2900676c8baa6ae))

* Add badge for code coverage (#codecov) ([`856e232`](https://github.com/TechNickAI/AICodeBot/commit/856e2329b372e852ed400d02a7489edc1f82921d))

* Add support for pytest-cov and Codecov 🎉 ([`0413572`](https://github.com/TechNickAI/AICodeBot/commit/0413572953b41415e132a5fceb391ac87ed06dde))

* Add tests for exec_and_get_output() helper function ([`c0c98fc`](https://github.com/TechNickAI/AICodeBot/commit/c0c98fcbf61ce220d71832dd327f84102c91bc55))

* Update alignment.yaml to include empathy and heart in AI ethics message ([`c47601c`](https://github.com/TechNickAI/AICodeBot/commit/c47601cd82bfcffdd8cfeb2893303b0e566e9bdd))


## v0.4.0 (2023-06-23)

### Unknown

* Update version to 0.4.0 🚀 ([`e9b783a`](https://github.com/TechNickAI/AICodeBot/commit/e9b783ae7f226fe21b29490ed74859e461cb8468))

* Add debugging advice to AICodeBot
:robot: Add debugging advice to AICodeBot

Usage:

aicodebot debug $command_that_fails ([`33566fc`](https://github.com/TechNickAI/AICodeBot/commit/33566fce19d6d17cfab65bc1517158565d088a69))

* Refactor CLI to use git diff with 10 lines of context #️⃣ ([`429421f`](https://github.com/TechNickAI/AICodeBot/commit/429421fcced12f330f99cc924a51fa066ddc272a))

* Update README.md ([`2878710`](https://github.com/TechNickAI/AICodeBot/commit/28787106ea3c380efc60020953590e95be764d9d))

* Add instructions for using aicodebot 🤖 ([`54be200`](https://github.com/TechNickAI/AICodeBot/commit/54be20059bfabeb021e29f59ab413d8a88193ac2))

* Update README with setup instructions and usage examples ([`09391cb`](https://github.com/TechNickAI/AICodeBot/commit/09391cbcdfe2a36991d5978141e5958d6e8be8a7))


## v0.3.0 (2023-06-23)

### Unknown

* Add alignment command for a heart-centered reminder of why we ar
building.

Update setup.py to use requirements.in instead of requirements.txt ([`b421e23`](https://github.com/TechNickAI/AICodeBot/commit/b421e2353569ad2dc8a2d166002bfdf1a63e8d94))

* Update CLI to reflect correct number of files committed 📝 ([`cbdec70`](https://github.com/TechNickAI/AICodeBot/commit/cbdec70ee9d0eecebd6983650f1757d73efe172c))

* Add a print with the number of files committed ([`60c573f`](https://github.com/TechNickAI/AICodeBot/commit/60c573f0f57dce27a4fbf00edb1af1b009cf988d))

* Update CLI to have -y option to skip confirmation before committing ([`dc977a8`](https://github.com/TechNickAI/AICodeBot/commit/dc977a811f2a99b25a679785ae55dfb8862ed9b3))

* Update README with instructions for aicodebot commit 🤖 ([`5a9fe6e`](https://github.com/TechNickAI/AICodeBot/commit/5a9fe6e2101e194e38470b8bfeaf962e86974ace))

* Update README.md ([`6e916b2`](https://github.com/TechNickAI/AICodeBot/commit/6e916b28218d20e0df332b1686f46dc99d5fc6d8))

* Update readme to reflect automate commits with aicodebot 🤖 ([`f71d0e8`](https://github.com/TechNickAI/AICodeBot/commit/f71d0e885b8cfa131992c5b1b2ec800f936f4c28))


## v0.2.6 (2023-06-22)

### Unknown

* Include .aicodebot.template in package distribution 📦 ([`9dd3bcd`](https://github.com/TechNickAI/AICodeBot/commit/9dd3bcd8964bfdb76f3c125777e3c9559c78e89c))

* Include the prompts in the pypi package ([`6927742`](https://github.com/TechNickAI/AICodeBot/commit/692774230b0c25b3644a600a5352ad1980e73797))

* Add OpenAI API key configuration to aicodebot 🔑 ([`d5bc015`](https://github.com/TechNickAI/AICodeBot/commit/d5bc01591f9901a7748ee116fda87bfcce122a19))


## v0.2.3 (2023-06-22)

### Unknown

* Proper location for the entry point ([`46a4ec6`](https://github.com/TechNickAI/AICodeBot/commit/46a4ec6c78a9c49d254e95b6b60e83c4bb9b9560))


## v0.2.2 (2023-06-22)

### Unknown

* Move version to it&#39;s own spot so that the app works from python package ([`5432b5f`](https://github.com/TechNickAI/AICodeBot/commit/5432b5fab2e34558152c06b6909460f26b1b6b88))

* Add .gitignore entries for build and dist directories 📁 ([`ee626c2`](https://github.com/TechNickAI/AICodeBot/commit/ee626c2d97d058cc727de8f553c06f294a546434))

* Move program files to aicodebot subdirectory, because that&#39;s how python packages expect them to work to avoid namespace conflicts ([`974dca4`](https://github.com/TechNickAI/AICodeBot/commit/974dca4904e3909f0731a2a84ef3194e724d4c27))


## v0.2.0 (2023-06-22)

### Feature

* feat: Add Smart Git Commit feature

This commit adds the Smart Git Commit feature which also automatically generates a commit message based on the changes made to the code. This feature will save time and improve code quality by ensuring that lint errors are caught early and that commit messages are consistent and informative.

Fun fact: This is the first aicodebot generated commit message! ([`98eb480`](https://github.com/TechNickAI/AICodeBot/commit/98eb48005c677a63035631e0c4b6434776291e85))

### Unknown

* Add .gitignore entries for aicodebot.egg-info and dist 📦 ([`de20e0c`](https://github.com/TechNickAI/AICodeBot/commit/de20e0c6403cad99ae7fa147bca3a65993d665db))

* Update prompt ([`54f0fb2`](https://github.com/TechNickAI/AICodeBot/commit/54f0fb29e7293f4745c854952c5b50542e169035))

* Add changes to cli.py

Add changes to cli.py to stage all changed files and get the diff for all changes since the last commit if no files are staged. ([`22dc052`](https://github.com/TechNickAI/AICodeBot/commit/22dc0529519ed6c0303beba3260435320d17957f))

* Fix up naughty subprocess calls and centralize how we exec ([`9e7cf45`](https://github.com/TechNickAI/AICodeBot/commit/9e7cf455b019d05d3d8bbf94ed4875d19dbc521b))

* Add option to generate git commit message 💻

Generate a git commit message based on the diff, and then commit the changes after you approve. ([`0b14cad`](https://github.com/TechNickAI/AICodeBot/commit/0b14cad204c5ae006f8007ec28d71d11953733fa))

* Add Assisted Git Commit feature: 🤖 Automatically generate commit messages ([`6425bd1`](https://github.com/TechNickAI/AICodeBot/commit/6425bd11df33f90aee15e2002a7f1cd18d839950))

* Add CLI commands to commit changes 💻 ([`26d252f`](https://github.com/TechNickAI/AICodeBot/commit/26d252fea7c788784bf2c70f2ff9a17b5b57d5c5))

* Add Assisted Git Commit: Automatically generates a commit message based on the changes made to the code.
🤖 ([`e8e5baa`](https://github.com/TechNickAI/AICodeBot/commit/e8e5baa79ab814d5e13043722ac86d3f20f7e39e))

* More feature updates to the README ([`f5048c7`](https://github.com/TechNickAI/AICodeBot/commit/f5048c7b4a3198288da475e94fca0a5d1c514b44))

* Rename funfact to fun-fact. Cleanly exit after setting up the API key. ([`85e84e2`](https://github.com/TechNickAI/AICodeBot/commit/85e84e2bf786e783d5306a0d29da20da7eea5905))

* GitHub doesn&#39;t like my positioning logic, revert to having the image displayed below ([`3e95b70`](https://github.com/TechNickAI/AICodeBot/commit/3e95b70c6ea1ac060278e5cbae4836003db3a81d))

* Better positioning and sizing of the gif ([`f8ba9a4`](https://github.com/TechNickAI/AICodeBot/commit/f8ba9a4ec3bb5e120d1475ca3ded34e112a27a9f))

* Build out the feature list in the README ([`2c2c11f`](https://github.com/TechNickAI/AICodeBot/commit/2c2c11ff54a1f929583739ba09b2769fffc21ce9))

* Fix markdown formatting ([`42fc5cb`](https://github.com/TechNickAI/AICodeBot/commit/42fc5cb980b930990f407526084d52b750572728))

* Update read me with better instructions on API key setup ([`d2b67b0`](https://github.com/TechNickAI/AICodeBot/commit/d2b67b011108608d2d4856d6f59f2a8eb65a426b))


## v0.1.0 (2023-06-21)

### Unknown

* Bump to version 0.1.0, now that we have real functionality ([`55cfbae`](https://github.com/TechNickAI/AICodeBot/commit/55cfbae17b3a8e98360ea5ef6d338f4b9e3769a4))

* Update README with install instructions ([`c527590`](https://github.com/TechNickAI/AICodeBot/commit/c527590842adc986eac516db7dc5879a1de53d76))

* fun facts! Establish the API call to open AI to get a fun fact about programming and AI. ([`905c1ca`](https://github.com/TechNickAI/AICodeBot/commit/905c1cab9b2d8c1039803e41c0745101f3284533))

* Skip joke test if the api key isn&#39;t set ([`99acf05`](https://github.com/TechNickAI/AICodeBot/commit/99acf05024f6dc45c421cd1c1dab4aff4c5a808d))

* Use rich to print the text ([`a5a25d0`](https://github.com/TechNickAI/AICodeBot/commit/a5a25d0c0bfd2efb470c96f45f931b80259b50fa))

* Use python dotenv. Establish a mechanism to get the OPENAI_API_KEY set up. Initial joke command. ([`327f554`](https://github.com/TechNickAI/AICodeBot/commit/327f554713b3dfd62ebe036b3daf8d8eb36fd607))


## v0.0.1 (2023-06-21)

### Unknown

* GitHub action for build. Set up the environment and run pytest ([`6ad1c55`](https://github.com/TechNickAI/AICodeBot/commit/6ad1c55bf8cf706628b6d143dd613c4b8db9f47c))

* Initial cli that prints the version number + test ([`07c7b33`](https://github.com/TechNickAI/AICodeBot/commit/07c7b33dba0f9c939a1e635aa62e34001c2c10d2))

* Initial pyproject.toml ([`9337966`](https://github.com/TechNickAI/AICodeBot/commit/933796680343624578e616bcab6a9c91d4b50959))

* Initial pre-commit config ([`a7be63c`](https://github.com/TechNickAI/AICodeBot/commit/a7be63cb72e3cfa0687d1a74151289236a1aedb6))

* Initial gitignore ([`c07b679`](https://github.com/TechNickAI/AICodeBot/commit/c07b679f288661bb3a199faaa3083db986bd4886))

* Updated README ([`e789e20`](https://github.com/TechNickAI/AICodeBot/commit/e789e2015e99688e84afbcaa35e6f29e291464c4))

* GitHub Action for Super Linter ([`ace3b5b`](https://github.com/TechNickAI/AICodeBot/commit/ace3b5b0cba0d4af4f734870b3e0da20f3d45470))

* Initial commit ([`be675dd`](https://github.com/TechNickAI/AICodeBot/commit/be675ddda77d003a68a2acfa5c7b9ee7f2c66c01))
