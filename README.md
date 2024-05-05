![PyPI - Python Version](https://img.shields.io/pypi/pyversions/secured)
![PyPI - Downloads](https://img.shields.io/pypi/dm/secured)
![PyPI](https://img.shields.io/pypi/v/secured)
[![codecov](https://codecov.io/gh/Joaopeuko/secured/graph/badge.svg?token=W5MF118U50)](https://codecov.io/gh/Joaopeuko/secured)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/secured)
![PyPI - License](https://img.shields.io/pypi/l/secured)

# Secured

- [Secured](#secured)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Example 1: Basic Usage](#example-1-basic-usage)
    - [Example 2: Custom Usage](#example-2-custom-usage)
    - [Example 3: Config Usage](#example-3-config-usage)
  - [Features](#features)

Secure your Python data structures and secrets with Secured. This package provides a straightforward solution for obscuring sensitive data in applications. It's specifically designed for developers who need to protect API keys, database credentials, and other critical configuration details from accidental exposure. Featuring customizable security measures, our tool allows you to control how sensitive information is represented and managed securely. It's ideal for projects that demand high data confidentiality and integrity. Please note that this provides a thin layer of protection.

## Installation

To install Secured, run the following command:

```python
pip install secured
```

## Usage

Below are some examples on how to use Secured to protect your sensitive data:

### Example 1: Basic Usage

```python
from secured import Secure

# Protect a sensitive string
DATABASE_URL = "mysql://user:password@localhost/dbname"
secure_database_url = Secure(DATABASE_URL, "<Data Hidden>")

# Usage in code
print(secure_database_url)  # Output: <Data Hidden>
```

### Example 2: Custom Usage

```python
from secured import Secure

# Protect an API key with a custom message
API_KEY = "12345-abcdef-67890-ghijk"
secure_api_key = Secure(API_KEY, "API Key Protected")

# Usage in code
print(secure_api_key)  # Output: API Key Protected
```

### Example 3: Config Usage

The `Secured` class allows you to securely read configuration files containing sensitive data. Here's how you can use it:

```python
from secured.secured import Secured

# Create a Secured object to read a YAML configuration file
secured = Secured('config.yaml', secure=True)

# Access configuration attributes securely
print(secured.config.name)  # Using dot notation
print(secured.config["name"])  # Using dictionary-like notation
```

## Features

- **Data Protection**: Helps prevent the accidental logging or display of sensitive information.
- **Customizable Representations**: Set how your data is displayed when being secured.
- **Ease of Use**: Integrate seamlessly into existing Python applications.
