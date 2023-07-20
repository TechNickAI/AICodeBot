from aicodebot import version
from pathlib import Path
from setuptools import setup

# Pull in the long description from the README
long_description = Path("README.md").read_text(encoding="utf-8")

# Get requirements from requirements.in
requirements = Path("requirements/requirements.in").read_text(encoding="utf-8").splitlines()
# Remove lines that are empty or start with # (comments)
requirements = [line for line in requirements if line and not line.startswith("#")]

setup(
    name="aicodebot",
    python_requires=">=3.9",
    version=version,
    url="https://github.com/gorillamania/AICodeBot",
    author="Nick Sullivan",
    description="AI-powered tool for developers, simplifying coding tasks and improving workflow efficiency.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="AI, coding, assistant, pair-programming, automation, productivity, workflow, artificial intelligence",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "aicodebot = aicodebot.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
