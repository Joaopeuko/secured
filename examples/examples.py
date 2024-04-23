from secured.attribute import AttrDict
from secured.secured import Secured

secured = Secured('examples/config-secrets.yaml', secure=True, message="<Custom Secured>")

print(secured.config_secrets.name)
print(secured.config_secrets["name"])

ad = AttrDict(secure=True, message="<Custom Secured>")
ad['password'] = 'my_secret'
print((ad.password))
print((ad['password']))
