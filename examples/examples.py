from secured.attribute import AttrDict
from secured.secured import Secured
message = "🔒 <Data Secured> 🔒"
secured = Secured('examples/config-secrets.yaml', secure=True, message=message)

print(secured.config_secrets.name)
print(secured.config_secrets["name"])

ad = AttrDict(secure=True, message=message)
ad['password'] = 'my_secret'
print((ad.password))
print((ad['password']))
