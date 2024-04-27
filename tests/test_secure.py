from secured.secure import Secure

def test_secure_initialization():
    """Test the initialization and representation of Secure objects."""
    secure = Secure("sensitive_data", "<Data Hidden>")
    assert str(secure) == "<Data Hidden>"
    assert repr(secure) == "<Data Hidden>"

def test_secure_default_message():
    """Test the default message used when no custom message is provided."""
    secure = Secure("sensitive_data")
    assert str(secure) == "<Sensitive data secured>"

def test_to_int_success():
    """Test converting secured data to an integer successfully."""
    secure = Secure("123")
    assert secure.to_int() == 123

def test_to_int_failure():
    """Test failing to convert secured data to an integer."""
    secure = Secure("sensitive_data")
    assert secure.to_int() == "<Sensitive data secured>"

def test_to_float_success():
    """Test converting secured data to a float successfully."""
    secure = Secure("123.45")
    assert secure.to_float() == 123.45

def test_to_float_failure():
    """Test failing to convert secured data to a float."""
    secure = Secure("sensitive_data")
    assert secure.to_float() == "<Sensitive data secured>"


def test_key_success():
    """Test failing to convert secured data to a float."""
    secure = Secure("sensitive_data")
    assert secure == "sensitive_data"
    secure = Secure("12345")
    assert secure == "12345"
    assert secure._original == "12345"
