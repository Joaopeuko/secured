import tomlkit # type: ignore
from setuptools import setup, find_packages # type: ignore

# Read and parse the pyproject.toml file
with open("pyproject.toml", "r") as toml_file:
    pyproject = tomlkit.parse(toml_file.read())

def convert_version(poetry_version): # type: ignore
    """ Convert Poetry version specifier to setuptools specifier. """
    if poetry_version.startswith('^'):
        version = poetry_version[1:]
        major_version = version.split('.')[0]
        next_major_version = str(int(major_version) + 1)
        return f">={version},<{next_major_version}.0.0"
    return poetry_version

# Extract dependencies and convert versions
dependencies = [
    f"{pkg}{convert_version(ver)}" for pkg, ver in pyproject['tool']['poetry']['dependencies'].items() # type: ignore
    if pkg != "python"
]

# Read README.md for the long description
with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="secured",
    version=pyproject['tool']['poetry']['version'],
    author="Joao Paulo Euko",
    description="Secure your Python data with Secured. This tool protects sensitive information like API keys and database credentials, offering customizable settings for high confidentiality and integrity. Note: Provides a thin layer of protection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=dependencies
)
