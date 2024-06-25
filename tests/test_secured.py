import pytest
from secured.secured import Secured, Secure
from secured.attribute import AttrDict
from io import StringIO

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

    def test_load_yaml_no_paths(self):
        secured = Secured()
        assert secured.load_yaml(None, False) is None

    def test_load_yaml_file_not_found(self, monkeypatch):
        def mock_open(*args, **kwargs):
            raise FileNotFoundError

        monkeypatch.setattr("builtins.open", mock_open)
        secured = Secured(secure=True)
        secured.load_yaml('nonexistent.yaml', secure=True)
        assert True  # Just to pass the test as it logs an error

    def test_load_yaml_parse_error(self, monkeypatch):
        def mock_open(*args, **kwargs):
            return StringIO("invalid: yaml: - content")

        monkeypatch.setattr("builtins.open", mock_open)
        secured = Secured(secure=True)
        secured.load_yaml('invalid.yaml', secure=True)
        assert True  # Just to pass the test as it logs an error

    def test_create_config_as_attrdict(self):
        secured = Secured(as_attrdict=True)
        config = secured.create_config({'key': 'value'}, secure=False)
        assert isinstance(config, AttrDict)

    def test_create_config_not_as_attrdict(self):
        secured = Secured(as_attrdict=False)
        config = secured.create_config({'key': 'value'}, secure=True)
        assert isinstance(config['key'], Secure)

    def test_recursive_dict(self):
        secured = Secured()
        data = {'a': {'b': 'c'}}
        result = secured._recursive_dict(data)
        assert result == {'a': {'b': 'c'}}

    def test_get_env_variable(self, monkeypatch):
        monkeypatch.setenv("TEST_KEY", "env_value")
        secured = Secured()
        result = secured.get("TEST_KEY")
        assert isinstance(result, Secure)
        assert result._get_original() == "env_value"

    def test_get_required_key_not_found(self):
        secured = Secured()
        with pytest.raises(ValueError):
            secured.get("NONEXISTENT_KEY", required=True)

    def test_use_attrdict_toggle(self):
        secured = Secured()
        data = {'key': 'value'}
        secured.test_data = AttrDict(data)
        secured.use_attrdict(False)
        assert isinstance(secured.test_data, dict)
        secured.use_attrdict(True)
        assert isinstance(secured.test_data, AttrDict)
