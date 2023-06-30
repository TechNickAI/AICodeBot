# AICodeBot Code Agent

Note: The `code` feature does not exist, yet. It is a vision for the future,
ala [README driven development](https://tom.preston-werner.com/2010/08/23/readme-driven-development.html)

The 'code' command for AICodeBot is designed to automate coding
tasks based on instructions from you. This feature aims to boost developer
productivity by handling various aspects of the coding process, but keeping you
in charge of the process and commiting the code.

It's not intended to build entire applications, but instead improve existing
code bases one git commit at a time.

## Feature Overview

`aicodebot code` has several steps:

1. **Task Understanding**: AICodeBot interprets the coding task by prompting you
   for requirements.

2. **Planning**: AICodeBot devises a plan of action for the task, identifying
   the necessary steps and potential challenges, and determining where it needs
   clarification on the requirements.

3. **Learning**: AICodeBot gathers the information required to complete the
   task. This includes researching the best approach, understanding the existing
   codebase and architecture, and learning about necessary libraries or APIs.

4. **Clarification**: If any aspect of the task is unclear, AICodeBot asks
   clarifying questions to ensure a comprehensive understanding of the task.
   Great engineers know how to talk to the customer to see what they want.

5. **Code Generation**: AICodeBot generates code that aligns with the style of
   the existing codebase, following conventions and best practices.

6. **Self-Review**: AICodeBot reviews and improves the generated code,
   identifying potential issues or areas for enhancement. Note: This practice
   of self-reflection has been shown to boost the effectiveness of AI systems.

7. **Code Modification**: AICodeBot modifies the local code with the new
   changes, making them available for review with a diff.

8. **Unit Testing**: AICodeBot writes and runs unit tests for the new code,
   debugging and modifying the code as necessary until all tests pass.

9. **Code Review**: AICodeBot submits the code for review, and marks the task
    as complete and ready for you to commit.

**Future** - Reinforcement Learning and Active Learning

AICodeBot is designed to learn from each interaction, improving its performance
over time based on feedback like code acceptance, compilation success, and passing
test results.

[![](https://mermaid.ink/img/pako:eNp1lMFuozAQhl9l5JVyaq97yGFXDWSjSEnLhkSrVenBxUNi1djUNq1Q1XffMZg0rZYLgpnf38z8Nn5jpRHI5uxoeXMqNMBhd1-wgxZonedawJ67J9jhcyst1qi9K9gDXF__gIR0OeITJIpbWcmSe2k0VNbUcHBoSRd4CYmhYCv0fRTWuml9wQbEheCyBMT6xoiozKhYprgGf8K-pUjPhsVrQctk1UHusXEwg-TElUJ9RBcBGwJskFsNt1iic9x21EplbN23HXGbsRdH0vIEC3QebprGGk5fM7jJ1iMwWd2HqTRa7hEScnEceDVAEotjhh7aSeepSXiV_tQHH7nDyMqD5zt8kfgKwfN1TRVfPlHz3ZdJMxNwkqtRHTdnaG5LwK0RQbgxJYkuG9wOqMzSmNQReRWMAjIDhiYi5bAnyh8raYoZ7FpN2yI97MkTF1GH_YBaatfaOOvvlivpu8hICZHiY3sEWX1YH5encaZQ3sNd6-loUKleP64PO5-aoSpk3Lmf4-K493_Pe7zsXeSi60dJTF1L_0V8a0ZuiDrfKaQTD5VUav7t-3KxSH99JJKJeDYR30xxVhOJfLLydiJBhv8_kU7Fp5pdfoqzK1Yj_QtS0F3wFlQFo1-tpjMzp1eBFW8VmVnod5Ly1pu80yWbe9viFWsbQUc9lZxukZrNK67cOboU0ht7DmL_uR0unf7uef8H0zJtIQ?type=png)](https://mermaid.live/edit#pako:eNp1lMFuozAQhl9l5JVyaq97yGFXDWSjSEnLhkSrVenBxUNi1djUNq1Q1XffMZg0rZYLgpnf38z8Nn5jpRHI5uxoeXMqNMBhd1-wgxZonedawJ67J9jhcyst1qi9K9gDXF__gIR0OeITJIpbWcmSe2k0VNbUcHBoSRd4CYmhYCv0fRTWuml9wQbEheCyBMT6xoiozKhYprgGf8K-pUjPhsVrQctk1UHusXEwg-TElUJ9RBcBGwJskFsNt1iic9x21EplbN23HXGbsRdH0vIEC3QebprGGk5fM7jJ1iMwWd2HqTRa7hEScnEceDVAEotjhh7aSeepSXiV_tQHH7nDyMqD5zt8kfgKwfN1TRVfPlHz3ZdJMxNwkqtRHTdnaG5LwK0RQbgxJYkuG9wOqMzSmNQReRWMAjIDhiYi5bAnyh8raYoZ7FpN2yI97MkTF1GH_YBaatfaOOvvlivpu8hICZHiY3sEWX1YH5encaZQ3sNd6-loUKleP64PO5-aoSpk3Lmf4-K493_Pe7zsXeSi60dJTF1L_0V8a0ZuiDrfKaQTD5VUav7t-3KxSH99JJKJeDYR30xxVhOJfLLydiJBhv8_kU7Fp5pdfoqzK1Yj_QtS0F3wFlQFo1-tpjMzp1eBFW8VmVnod5Ly1pu80yWbe9viFWsbQUc9lZxukZrNK67cOboU0ht7DmL_uR0unf7uef8H0zJtIQ)

## Sample task prompts

These are example prompts that you can use to guide AICodeBot in performing various coding tasks, ranging from practical code improvements to fun and whimsical modifications.

1. "Identify areas in the code where additional logging would be beneficial."
1. "Find places that make API calls and add a link to the documentation for the API."
1. "Replace all instances of the variable name 'foo' with 'bar'."
1. "Find all instances of the word 'bug' in the comments and replace them with 'feature'."
1. "Identify areas in the code where more descriptive variable names could be used."
1. "Identify potential performance improvements in the code."
1. "Scan the codebase for potential security vulnerabilities."
1. "Identify areas where comments could be added for better understanding."
1. "Find sections of code that lack comments and add appropriate comments."
1. "Identify sections of code that could be refactored for better readability or efficiency."
1. "Find complex sections of code and suggest ways to simplify them."
1. "Check codecov.io for code coverage and suggest areas where additional tests could be added."
1. "Find and remove any dead or unused code."
1. "Review the project's documentation and suggest improvements."
1. "Look at Honeybadger.io for error reports and suggest improvements."
1. "Find all the sad comments in the code and add a happy emoji next to them."
1. "Find areas in the code that could be made more efficient by using a different data structure."
1. "Identify areas where the use of a library or framework could simplify the code."
1. "Review the codebase and suggest improvements based on best practices for Python 3.11"
1. "Find instances where concurrency or parallelism could be used for efficiency."
1. "Identify areas where error handling could be improved."
1. "Find areas where the code could be made more robust against failure."
