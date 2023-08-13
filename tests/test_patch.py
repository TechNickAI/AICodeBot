from aicodebot.helpers import create_and_write_file
from aicodebot.patch import Patch
from pathlib import Path
from tests.conftest import in_temp_directory
import textwrap


def test_apply_patch(temp_git_repo):
    # Use in_temp_directory for the test
    with in_temp_directory(temp_git_repo.working_dir):
        add_file = Path("add_file.txt")
        assert not add_file.exists()

        # Create a file to be modified
        mod_file = Path("mod_file.txt")
        mod_file.write_text("AICodeBot is your coding sidekick.\nIt is here to make your coding life easier.")

        # Create a file to be removed
        remove_file = Path("remove_file.txt")
        remove_file.write_text("Remember, AICodeBot has got your back!\n")

        # Create patch strings
        add_patch = textwrap.dedent(
            """
            --- /dev/null
            +++ b/add_file.txt
            @@ -0,0 +1,1 @@
            +AICodeBot is here to help!
            """
        ).lstrip()
        assert Patch.apply_patch(add_patch)
        assert add_file.exists()
        assert add_file.read_text() == "AICodeBot is here to help!\n"

        # Note the spacing here is critical
        mod_patch = textwrap.dedent(
            """
            --- a/mod_file.txt
            +++ b/mod_file.txt
            @@ -1,2 +1,3 @@
             AICodeBot is your coding sidekick.
             It is here to make your coding life easier.
            +It is now even better!
            """
        ).lstrip()
        assert Patch.apply_patch(mod_patch)
        assert "It is now even better!" in mod_file.read_text()

        rem_patch = textwrap.dedent(
            """
            --- a/remove_file.txt
            +++ /dev/null
            @@ -1 +0,0 @@
            -Remember, AICodeBot has got your back!
            """
        ).lstrip()
        assert Patch.apply_patch(rem_patch)
        assert not remove_file.exists()


def test_rebuild_patch(tmp_path):
    # Use in_temp_directory for the test
    with in_temp_directory(tmp_path):
        # Set up the original file
        Path(tmp_path / "aicodebot").mkdir()
        create_and_write_file(
            "aicodebot/prompts.py",
            textwrap.dedent(
                """
                from aicodebot.coder import Coder
                from aicodebot.config import read_config
                from aicodebot.helpers import logger
                from langchain import PromptTemplate
                from langchain.output_parsers import PydanticOutputParser
                from pathlib import Path
                from pydantic import BaseModel, Field
                from types import SimpleNamespace
                import arrow, functools, os, platform


                # Comment
                """
            ),
        )
        prompts_file = Path("aicodebot/prompts.py").read_text()
        assert "platform" in prompts_file

        # A few problems with this patch:
        # 1. The chunk header is wrong (wrong line in the file and wrong number of lines)
        # 2. No " " before the unchanged lines
        # 3. Duplicated added/removed lines (that should just be unchanged)
        # The original goal of the patch was to remove the "platform" import
        bad_patch = textwrap.dedent(
            """
            diff --git a/aicodebot/prompts.py b/aicodebot/prompts.py
            --- a/aicodebot/prompts.py
            +++ b/aicodebot/prompts.py
            @@ -6,7 +6,7 @@
            from langchain import PromptTemplate
            from langchain.output_parsers import PydanticOutputParser
            from pathlib import Path
            -from pydantic import BaseModel, Field
            -from types import SimpleNamespace
            -import arrow, functools, os, platform
            +from pydantic import BaseModel, Field
            +from types import SimpleNamespace
            +import arrow, functools, os

            """
        )

        print("Bad patch:\n", bad_patch)
        rebuilt_patch = Patch.rebuild_patch(bad_patch)
        print("Rebuilt patch:\n", rebuilt_patch)

        # Apply the rebuilt patch
        assert Patch.apply_patch(rebuilt_patch) is True

        assert "platform" not in Path("aicodebot/prompts.py").read_text()


def test_rebuild_patch_coder(tmp_path):
    # Use in_temp_directory for the test
    with in_temp_directory(tmp_path):
        # Set up the original file
        file = "aicodebot/coder.py"
        Path(tmp_path / "aicodebot").mkdir()
        create_and_write_file(
            file,
            textwrap.dedent(
                """
                from aicodebot.helpers import exec_and_get_output, logger
                from aicodebot.lm import token_size
                from pathlib import Path
                from pygments.lexers import ClassNotFound, get_lexer_for_mimetype, guess_lexer_for_filename
                from types import SimpleNamespace
                import fnmatch, mimetypes, re, subprocess, unidiff


                class Coder:
                """
            ).lstrip(),
        )
        assert "unidiff" in Path(file).read_text()

        # A few problems with this patch:
        # 1. The chunk header is wrong (wrong line in the file and wrong number of lines)
        # 2. No " " before the unchanged lines
        # 3. Duplicated added/removed lines (that should just be unchanged)
        # The original goal of the patch was to remove the "platform" import
        bad_patch = textwrap.dedent(
            """
            diff --git a/aicodebot/coder.py b/aicodebot/coder.py
            --- a/aicodebot/coder.py
            +++ b/aicodebot/coder.py
            @@ -3,7 +3,7 @@
             from pathlib import Path
             from pygments.lexers import ClassNotFound, get_lexer_for_mimetype, guess_lexer_for_filename
             from types import SimpleNamespace
            -import fnmatch, mimetypes, re, subprocess, unidiff
            +import fnmatch, mimetypes, re, subprocess


             class Coder
            """
        ).lstrip()

        print("Bad patch:\n", bad_patch)
        rebuilt_patch = Patch.rebuild_patch(bad_patch)
        print("Rebuilt patch:\n", rebuilt_patch)

        # Apply the rebuilt patch
        assert Patch.apply_patch(rebuilt_patch) is True

        assert "unidiff" not in Path(file).read_text()
