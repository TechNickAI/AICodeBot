from aicodebot.helpers import logger
from pathlib import Path
from types import SimpleNamespace
import re, subprocess


class Patch:
    """Handle patches in unified diff format for making changes to the local file system."""

    # Compile the regular expression used in parse_line method
    CHUNK_HEADER_REGEX = re.compile(r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@")

    @staticmethod
    def apply_patch(patch_string, is_rebuilt=False):
        """Applies a patch to the local file system using git apply."""
        try:
            result = subprocess.run(
                [
                    "git",
                    "apply",
                    "--verbose",
                    "--recount",
                ],
                input=patch_string.encode("utf-8"),
                check=True,
                capture_output=True,
            )
            logger.debug(f"git apply output {result.stdout}")
        except subprocess.CalledProcessError as e:
            logger.error("Failed to apply patch:")
            print(patch_string)  # noqa: T201
            logger.error(e.stderr)

            # Rebuild it and try again
            if not is_rebuilt:
                rebuilt_patch = Patch.rebuild_patch(patch_string)
                if patch_string != rebuilt_patch:
                    return Patch.apply_patch(rebuilt_patch, is_rebuilt=True)

            return False
        else:
            return True

    @staticmethod
    def parse_line(line):  # noqa: PLR0911
        """Parse a line of the patch and return a SimpleNamespace with the line, type, and parsed line."""
        if line.startswith(("diff --git", "index")):
            return SimpleNamespace(line=line, type="header", parsed=line)
        elif line.startswith("---"):
            return SimpleNamespace(line=line, type="source_file", parsed=line[6:])
        elif line.startswith("+++"):
            return SimpleNamespace(line=line, type="destination_file", parsed=line[6:])
        elif line.startswith("@@"):
            chunk_header_match = Patch.CHUNK_HEADER_REGEX.match(line)
            if not chunk_header_match:
                raise ValueError(f"Invalid chunk header: {line}")

            chunk_header = SimpleNamespace(
                start1=int(chunk_header_match.group(1)),
                count1=int(chunk_header_match.group(2)),
                start2=int(chunk_header_match.group(3)),
                count2=int(chunk_header_match.group(4)),
            )

            return SimpleNamespace(line=line, type="chunk_header", parsed=chunk_header)
        elif line.startswith("+"):
            return SimpleNamespace(line=line, type="addition", parsed=line[1:])
        elif line.startswith("-"):
            return SimpleNamespace(line=line, type="subtraction", parsed=line[1:])
        elif line.startswith(" "):
            return SimpleNamespace(line=line, type="context", parsed=line[1:])
        else:
            raise ValueError(f"Invalid line: '{line}'")

    @staticmethod
    def rebuild_patch(patch_string):  # noqa: PLR0915
        """We ask the LM to respond with unified patch format. It often gets it wrong, especially the chunk headers.
        This function looks at the intent of the patch and rebuilds it in a [hopefully] correct format."""

        # ------------------------- Parse the incoming patch ------------------------- #
        parsed_lines = []
        chunk_header = None
        for line in patch_string.splitlines():
            if chunk_header and not line.startswith(("+", "-", " ")):
                # Sometimes the LM will add a context line without a space
                # If we see that, we'll assume it's a context line
                line = " " + line  # noqa: PLW2901

            parsed_line = Patch.parse_line(line)
            if parsed_line.type == "chunk_header":
                chunk_header = parsed_line.parsed
            parsed_lines.append(parsed_line)

        # Check for critical fields
        source_file_line = next(line for line in parsed_lines if line.type == "source_file")
        if not source_file_line:
            raise ValueError("No source file found in patch")

        first_context_line = next(line for line in parsed_lines if line.type == "context")
        if not first_context_line:
            raise ValueError("No context line found in patch")

        if not chunk_header:
            # Chunk header missing. This shouldn't happen, but we should be able to recover
            chunk_header = SimpleNamespace(start1=0, count1=0, start2=0, count2=0)

        start1 = chunk_header.start1
        first_change_line = next(line for line in parsed_lines if line.type in ("addition", "subtraction"))
        lines_of_context = 1

        # ------------------------- Rebuild the context lines ------------------------ #
        # Get the correct start line from the first context line, by looking at the source file
        source_file = source_file_line.parsed
        source_file_contents = []
        if source_file != "/dev/null" and Path(source_file).exists():
            source_file_contents = Path(source_file).read_text().splitlines()

            # Determine the correct line of the first change
            # We will start looking at start1 - 1, and walk until we find it
            for i in range(start1 - 1, len(source_file_contents)):
                if source_file_contents[i] == first_change_line.parsed:
                    first_change_line_number = i + 1
                    start1 = first_change_line_number - lines_of_context
                    break
            else:
                raise ValueError(f"Could not find first change line in source file: {first_change_line.parsed}")

            # Disregard the existing context lines from the parsed lines
            parsed_lines = [line for line in parsed_lines if line.type != "context"]

            # Add x lines of context before the first change
            for i in range(first_change_line_number - lines_of_context, first_change_line_number):
                # Get the index number of the first changed line in parsed_lines
                first_change_line_index = next(
                    i for i, line in enumerate(parsed_lines) if line.type in ("addition", "subtraction")
                )
                parsed_lines.insert(first_change_line_index, Patch.parse_line(f" {source_file_contents[i - 1]}"))

            # Add x lines of context after the last change
            number_of_subtractions = len([line for line in parsed_lines if line.type == "subtraction"])
            start_trailing_context = first_change_line_number + number_of_subtractions
            for i in range(start_trailing_context, start_trailing_context + lines_of_context):
                parsed_lines.append(Patch.parse_line(f" {source_file_contents[i - 1]}"))

        # ------------------------- Rebuild the chunk header ------------------------- #

        # Add up the number of context lines, additions, and subtractions
        # This will be the new count1 and count2
        start2 = start1
        count1 = count2 = 0
        for line in parsed_lines:
            if line.type in ("context", "subtraction"):
                count1 += 1
            if line.type in ("context", "addition"):
                count2 += 1

        new_chunk_header = f"@@ -{start1},{count1} +{start2},{count2} @@"

        # ----------------------------- Rebuild the patch ---------------------------- #

        new_patch = []
        for line in parsed_lines:
            if line.type == "chunk_header":
                new_patch.append(new_chunk_header)
            elif line.type == "source_file":
                new_patch.append(f"--- a/{line.parsed}")
            elif line.type == "destination_file":
                new_patch.append(f"+++ b/{line.parsed}")
            else:
                new_patch.append(f"{line.line}")

        return "\n".join(new_patch) + "\n"
