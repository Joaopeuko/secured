from setuptools import setup, find_packages
import toml

# Load and parse the pyproject.toml file
with open("pyproject.toml", "r") as f:
    pyproject = toml.load(f)

# Extract dependencies
dependencies = pyproject['tool']['poetry']['dependencies']
dev_dependencies = pyproject['tool']['poetry']['group']['dev']['dependencies']

# Read README.md for the long description
with open("README.md", "r") as file:
    long_description = file.read()

# Convert dependencies to the required format for setuptools
install_requires = [f"{dep}{version}" for dep, version in dependencies.items() if dep != "python"]
extras_require = {
    "dev": [f"{dep}{version}" for dep, version in dev_dependencies.items()]
}

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
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require=extras_require
)
