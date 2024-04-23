from secured.attribute import AttrDict
from secured.secured import Secured

secured = Secured('examples/config-secrets.yaml', secure=True)

print(secured.config_secrets.name)
print(secured.config_secrets["name"])

ad = AttrDict(secure=True)
ad['password'] = 'my_secret'
print((ad.password))
print((ad['password']))
