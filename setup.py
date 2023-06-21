from pathlib import Path
from setuptools import setup

__version__ = "0.1.0"

# Get requirements from requirements.txt
with Path.open("requirements/requirements.txt") as f:
    requirements = f.read().splitlines()

# Only run setup if this is the main file (allows this file to be imported for __version__)
if __name__ == "__main__":
    setup(
        name="aicodebot",
        version="0.1.0",
        url="https://github.com/novara_ai/aicodebot",
        author="Nick Sullivan",
        description="Your AI-powered coding companion",
        install_requires=requirements,
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
