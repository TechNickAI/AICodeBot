from aicodebot.patch import Patch
from pathlib import Path
from tests.conftest import in_temp_directory
import pytest, shutil, textwrap


def test_apply_patch(temp_git_repo):
    # Use in_temp_directory for the test
    with in_temp_directory(temp_git_repo.working_dir):
        add_file = Path("add_file.txt")
        assert not add_file.exists()

        # Create a file to be modified
        mod_file = Path("mod_file.txt")
        mod_file.write_text("AICodeBot is your coding sidekick.\nIt is here to make your coding life easier.\n")

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


@pytest.mark.parametrize(
    "test_name, expected_chunk_header",
    [
        ("prompts", "@@ -6,5 +6,5 @@"),
        ("coder", "@@ -5,3 +5,3 @@"),
        ("input", "@@ -2,3 +2,3 @@"),
    ],
)
def test_rebuild_patch_parameterized(tmp_path, test_name, expected_chunk_header):
    test_files_dir = Path("tests/rebuild_patch_data")
    shutil.copy(test_files_dir / f"{test_name}.py", tmp_path)
    bad_patch = Path(test_files_dir / f"{test_name}.patch").read_text()
    expected_result = Path(test_files_dir / f"{test_name}_expected.py").read_text()

    # Use in_temp_directory for the test
    with in_temp_directory(tmp_path):
        print(f"Bad patch:\n{bad_patch}")
        rebuilt_patch = Patch.rebuild_patch(bad_patch)
        print(f"Rebuilt patch:\n{rebuilt_patch}")

        assert expected_chunk_header in rebuilt_patch

        # Apply the rebuilt patch
        assert Patch.apply_patch(rebuilt_patch) is True

        patched_contents = Path(f"{test_name}.py").read_text()
        print(f"Patched contents:\n{patched_contents}")
        print(f"Expected result:\n{expected_result}")
        assert patched_contents == expected_result
