from secured.secured import Secured

# Define the custom secure message
MESSAGE = "🔒 <Data Secured> 🔒"
CONFIG_PATH = "examples/config.yaml"

# Protect a sensitive string
DATABASE_URL = "mysql://{user}:{password}@localhost/dbname"
secure = Secured(CONFIG_PATH, secure=True, message=MESSAGE)

# Usage in code
secure_database_url  = secure.compose(DATABASE_URL, user="guest", password="guest_password")
print(secure_database_url)  # Output: 🔒 <Data Secured> 🔒
print(secure_database_url._get_original()) # Careful! This will print the original data, do not use it.
print(secure_database_url == "mysql://guest:guest_password@localhost/dbname")

# Example secured object
secured = Secured('examples/config.yaml', secure=True, message=MESSAGE)

# Composing the auth header
print("Original data:", secured.config.databases['db3']['connection']['host']._get_original())
auth_header = secured.compose("Bearer {host}", host=secured.config.databases['db3']['connection']['host'])
print(auth_header)  # Output: 🔒 <Data Secured> 🔒
print(auth_header == "Bearer db-server.local")  # Output: True

# Formatting the Secure object
formatted_key = secured.compose("{host}{port}", host=secured.config.databases['db3']['connection']['host'], port=secured.config.databases['db3']['connection']['port'])
print(formatted_key)  # Output: 🔒 <Data Secured> 🔒
print(formatted_key == "db-server.local5432")  # Output: True
