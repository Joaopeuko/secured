from setuptools import setup, find_packages

# Function to parse pyproject.toml file to extract dependencies
def parse_pyproject_dependencies():
    with open("pyproject.toml", "r") as f:
        content = f.read()

    # Extract dependencies from content
    dependencies_start = content.find("[tool.poetry.dependencies]")
    dependencies_end = content.find("[", dependencies_start + 1)
    dependencies_section = content[dependencies_start:dependencies_end].strip()

    dependencies = {}
    for line in dependencies_section.split("\n")[1:]:
        if line.strip() and "=" in line:
            dep, version = line.split("=")
            dependencies[dep.strip()] = version.strip().replace('"', '')

    return dependencies

# Function to parse pyproject.toml file to extract dev dependencies
def parse_pyproject_dev_dependencies():
    with open("pyproject.toml", "r") as f:
        content = f.read()

    # Extract dev dependencies from content
    dev_dependencies_start = content.find("[tool.poetry.group.dev.dependencies]")
    dev_dependencies_end = content.find("[", dev_dependencies_start + 1)
    dev_dependencies_section = content[dev_dependencies_start:dev_dependencies_end].strip()

    dev_dependencies = {}
    for line in dev_dependencies_section.split("\n")[1:]:
        if line.strip() and "=" in line:
            dep, version = line.split("=")
            dev_dependencies[dep.strip()] = version.strip().replace('"', '')

    return dev_dependencies

# Read README.md file
with open("README.md", "r") as fh:
    long_description = fh.read()

# Get dependencies from pyproject.toml
install_requires = [f"{dep}=={version}" for dep, version in parse_pyproject_dependencies().items() if dep != "python"]

# Get dev dependencies from pyproject.toml
extras_require = {
    "dev": [f"{dep}=={version}" for dep, version in parse_pyproject_dev_dependencies().items()]
}

setup(
    name="secured",
    version="0.1.0",
    author="Joao Paulo Euko",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require=extras_require,
)
