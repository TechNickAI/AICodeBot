from aicodebot.output import OurMarkdown


def test_pull_code_blocks():
    markdown = OurMarkdown("```python\nprint('Hello, world!')\n```")
    code_blocks = markdown.pull_code_blocks()
    assert code_blocks == ["print('Hello, world!')\n"]


def test_pull_diff_blocks():
    markdown = OurMarkdown("```diff\n- print('Hello, world!')\n+ print('Hello, universe!')\n```")
    diff_blocks = markdown.pull_diff_blocks()
    assert diff_blocks == ["- print('Hello, world!')\n+ print('Hello, universe!')\n"]
