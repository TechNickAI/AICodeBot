from aicodebot import version
from pathlib import Path
from setuptools import setup

# Pull in the long description from the README
with Path("README.md").open("r", encoding="utf-8") as f:
    long_description = f.read()

# Get requirements from requirements.in
with Path.open("requirements/requirements.in") as f:
    requirements = f.read().splitlines()

if __name__ == "__main__":  # Only run setup if this is the main file (allows this file to be imported for __version__)
    setup(
        name="aicodebot",
        python_requires=">=3.9",
        version=version,
        url="https://github.com/gorillamania/AICodeBot",
        author="Nick Sullivan",
        description="AI-powered tool for developers, simplifying coding tasks and improving workflow efficiency.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        keywords="AI, coding, assistant, pair-programming, automation",
        install_requires=requirements,
        entry_points={
            "console_scripts": [
                "aicodebot = aicodebot.cli:cli",
            ],
        },
        package_data={
            "aicodebot": ["prompts/*.yaml", ".aicodebot.template"],
        },
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU Affero General Public License v3",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ],
    )
