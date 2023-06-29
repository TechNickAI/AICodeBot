# AICodeBot Code Agent

The 'code' command is a new feature of AICodeBot designed to automate coding
tasks based on instructions from you. This feature aims to boost developer
productivity by handling various aspects of the coding process, but keeping you
in charge of the process.

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
