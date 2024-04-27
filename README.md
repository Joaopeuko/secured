# Secured

- [Secured](#secured)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Example 1: Basic Usage](#example-1-basic-usage)
    - [Example 2: Custom Usage](#example-2-custom-usage)
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

## Features

- **Data Protection**: Helps prevent the accidental logging or display of sensitive information.
- **Customizable Representations**: Set how your data is displayed when being secured.
- **Ease of Use**: Integrate seamlessly into existing Python applications.