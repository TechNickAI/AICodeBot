# AICodeBot Sidekick

⚠️ WARNING: The 'sidekick' feature is currently experimental and, frankly, it sucks right now.
Due to the token limitations with large language models, the amount of context
that can be sent back and forth is limited, and slow. This means that sidekick will struggle with
complex tasks and will take longer than a human for simpler tasks.

Play with it, but don't expect too much. Do you feel like [contributing](../CONTRIBUTING.md)? 😃

We'll document it here anyway, so you can see where we're going with it, ala
[README driven development](https://tom.preston-werner.com/2010/08/23/readme-driven-development.html)

The `sidekick` command for AICodeBot is designed to automate coding
tasks based on instructions from you. This feature aims to boost developer
productivity by handling various aspects of the coding process, but keeping you
in charge of the process and committing the code.

It's not intended to build entire applications, but instead improve existing
code bases one git commit at a time.

## Feature Overview

`aicodebot sidekick` works as an agent with several steps:

1. **Task Understanding**: AICodeBot interprets the coding task by prompting you
   for requirements.

2. **Planning**: AICodeBot devises a plan of action for the task, identifying
   the necessary steps and potential challenges, and determining where it needs
   clarification on the requirements.

3. **Clarification**: If any aspect of the task is unclear, AICodeBot asks
   clarifying questions to ensure a comprehensive understanding of the task.
   Great engineers know how to talk to the customer to see what they want.

4. **Code Generation**: AICodeBot generates code that aligns with the style of
   the existing codebase, following conventions and best practices.

5. **Self-Review**: AICodeBot reviews and improves the generated code,
   identifying potential issues or areas for enhancement. Note: This practice
   of self-reflection has been shown to boost the effectiveness of AI systems.

6. **Code Modification**: AICodeBot modifies the local code with the new
   changes, making them available for review with a diff.

7. **Unit Testing**: AICodeBot writes and runs unit tests for the new code,
   debugging and modifying the code as necessary until all tests pass.

8. **Code Review**: AICodeBot submits the code for review, and marks the task
   as complete and ready for you to commit.

**Future** - Reinforcement Learning and Active Learning

AICodeBot is designed to learn from each interaction, improving its performance
over time based on feedback like code acceptance, compilation success, and passing
test results.

[![](https://mermaid.ink/img/pako:eNp1lMFuozAQhl9l5JVyaq97yGFXDWSjSEnLhkSrVenBxUNi1djUNq1Q1XffMZg0rZYLgpnf38z8Nn5jpRHI5uxoeXMqNMBhd1-wgxZonedawJ67J9jhcyst1qi9K9gDXF__gIR0OeITJIpbWcmSe2k0VNbUcHBoSRd4CYmhYCv0fRTWuml9wQbEheCyBMT6xoiozKhYprgGf8K-pUjPhsVrQctk1UHusXEwg-TElUJ9RBcBGwJskFsNt1iic9x21EplbN23HXGbsRdH0vIEC3QebprGGk5fM7jJ1iMwWd2HqTRa7hEScnEceDVAEotjhh7aSeepSXiV_tQHH7nDyMqD5zt8kfgKwfN1TRVfPlHz3ZdJMxNwkqtRHTdnaG5LwK0RQbgxJYkuG9wOqMzSmNQReRWMAjIDhiYi5bAnyh8raYoZ7FpN2yI97MkTF1GH_YBaatfaOOvvlivpu8hICZHiY3sEWX1YH5encaZQ3sNd6-loUKleP64PO5-aoSpk3Lmf4-K493_Pe7zsXeSi60dJTF1L_0V8a0ZuiDrfKaQTD5VUav7t-3KxSH99JJKJeDYR30xxVhOJfLLydiJBhv8_kU7Fp5pdfoqzK1Yj_QtS0F3wFlQFo1-tpjMzp1eBFW8VmVnod5Ly1pu80yWbe9viFWsbQUc9lZxukZrNK67cOboU0ht7DmL_uR0unf7uef8H0zJtIQ?type=png)](https://mermaid.live/edit#pako:eNp1lMFuozAQhl9l5JVyaq97yGFXDWSjSEnLhkSrVenBxUNi1djUNq1Q1XffMZg0rZYLgpnf38z8Nn5jpRHI5uxoeXMqNMBhd1-wgxZonedawJ67J9jhcyst1qi9K9gDXF__gIR0OeITJIpbWcmSe2k0VNbUcHBoSRd4CYmhYCv0fRTWuml9wQbEheCyBMT6xoiozKhYprgGf8K-pUjPhsVrQctk1UHusXEwg-TElUJ9RBcBGwJskFsNt1iic9x21EplbN23HXGbsRdH0vIEC3QebprGGk5fM7jJ1iMwWd2HqTRa7hEScnEceDVAEotjhh7aSeepSXiV_tQHH7nDyMqD5zt8kfgKwfN1TRVfPlHz3ZdJMxNwkqtRHTdnaG5LwK0RQbgxJYkuG9wOqMzSmNQReRWMAjIDhiYi5bAnyh8raYoZ7FpN2yI97MkTF1GH_YBaatfaOOvvlivpu8hICZHiY3sEWX1YH5encaZQ3sNd6-loUKleP64PO5-aoSpk3Lmf4-K493_Pe7zsXeSi60dJTF1L_0V8a0ZuiDrfKaQTD5VUav7t-3KxSH99JJKJeDYR30xxVhOJfLLydiJBhv8_kU7Fp5pdfoqzK1Yj_QtS0F3wFlQFo1-tpjMzp1eBFW8VmVnod5Ly1pu80yWbe9viFWsbQUc9lZxukZrNK67cOboU0ht7DmL_uR0unf7uef8H0zJtIQ)

## Sample task prompts

These are example prompts that you can use to guide AICodeBot in performing various coding tasks, ranging from practical code improvements to fun and whimsical modifications.

1. "Add thorough and helpful logging"
1. "Find places that make API calls and add a link to the documentation for the API endpoint."
1. "Find all instances of the word 'bug' in the comments and replace them with 'feature'."
1. "Update the README.md file to include a link to the project's documentation."
1. "Replace the non descript variable names with more descriptive names and make sure the tests pass when you are done"
1. "Identify potential performance improvements in the code."
1. "Scan the code for potential security vulnerabilities."
1. "Find sections of code that lack comments and add appropriate, helpful comments."
1. "Find complex sections of code and suggest ways to simplify them."
1. "Check codecov.io for code coverage and suggest areas where additional tests could be added."
1. "Review the project's documentation and tell me what's undocumented."
1. "Look at Honeybadger.io for error reports and fix bugs that you can, suggest pointers for the ones that you can't"
1. "Identify areas where the use of a library or framework could simplify the code."
1. "Review the codebase and suggest improvements based on best practices for the latest version of Python, Javascript, etc. Update the code to use the latest best practices."
1. "Identify areas where error handling could be improved."
1. "Find areas where the code could be made more robust against failure."
1. "Find and remove any dead or unused code."
1. "Emojis. Emojis everywhere."
