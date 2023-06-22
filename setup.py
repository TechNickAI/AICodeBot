from aicodebot import version
from pathlib import Path
from setuptools import find_packages, setup

# Pull in the long description from the README
with Path("README.md").open("r", encoding="utf-8") as f:
    long_description = f.read()

# Get requirements from requirements.txt
with Path.open("requirements/requirements.txt") as f:
    requirements = f.read().splitlines()

if __name__ == "__main__":  # Only run setup if this is the main file (allows this file to be imported for __version__)
    setup(
        python_requires=">=3.9",
        name="aicodebot",
        version=version,
        url="https://github.com/novara_ai/aicodebot",
        author="Nick Sullivan",
        description="Your AI-powered coding companion: AI Code Bot 🤖",
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires=requirements,
        entry_points={
            "console_scripts": [
                "aicodebot = aicodebot.cli:cli",
            ],
        },
        packages=find_packages(exclude=["tests", "tests.*"]),
        package_data={
            "aicodebot": ["prompts/*.yaml"],
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
