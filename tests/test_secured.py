import pytest
from secured.secured import Secured, Secure

class TestSecured:
    @pytest.fixture
    def setup_secured(self):
        message = "🔒 <Data Secured> 🔒"
        secured = Secured('examples/config.yaml', secure=True, message=message)
        secured_host = Secure('db-server.local', message)
        secured_password = Secure('password123', message)
        return secured, secured_host, secured_password

    def test_compose_single_value(self, setup_secured):
        secured, secured_host, secured_password = setup_secured
        DATABASE_URL = "mysql://{user}:{password}@localhost/dbname"
        composed_url = secured.compose(DATABASE_URL, user="guest", password="guest_password")
        assert composed_url._get_original() == "mysql://guest:guest_password@localhost/dbname"
        assert composed_url == "mysql://guest:guest_password@localhost/dbname"

    def test_compose_multiple_values(self, setup_secured):
        secured, secured_host, secured_password = setup_secured
        composed_url = secured.compose(
            "Connection to {host} with password {password}",
            host=secured_host,
            password=secured_password
        )
        assert composed_url._get_original() == "Connection to db-server.local with password password123"
        assert composed_url == "Connection to db-server.local with password password123"
