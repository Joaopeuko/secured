from secured.secured import Secured

secured = Secured('examples/config-secrets.yaml', secure=True)

print(secured.config_secrets)
