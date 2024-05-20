from secured.attribute import AttrDict
from secured.secured import Secured
message = "🔒 <Data Secured> 🔒"
secured = Secured('examples/config-secrets.yaml', secure=True, message=message)

print(secured.config_secrets.name) # type: ignore
print(secured.config_secrets["name"]) # type: ignore

ad = AttrDict(secure=True, message=message)
ad['password'] = 'my_secret'
print((ad.password))
print((ad['password']))
print(ad.password == "my_secret")

# Example secured object
secured = Secured('examples/config.yaml', secure=True, message=message)

# Composing the auth header
print("Original data:", secured.config.databases['db3']['connection']['host']._get_original())
auth_header = secured.compose("Bearer {host}", host=secured.config.databases['db3']['connection']['host'])
print(auth_header)  # Output: 🔒 <Data Secured> 🔒
print(auth_header == "Bearer db-server.local")  # Output: True

# Formatting the Secure object
formatted_key = secured.compose("{host}{port}", host=secured.config.databases['db3']['connection']['host'], port=secured.config.databases['db3']['connection']['port'])
print(formatted_key)  # Output: 🔒 <Data Secured> 🔒
print(formatted_key == "db-server.local5432")  # Output: True
