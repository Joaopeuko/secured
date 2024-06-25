import pytest
from secured.attribute import AttrDict
from secured.secure import Secure

def test_attribute_access():
    """Test attribute-style access to dictionary keys."""
    ad = AttrDict({'key1': 'value1', 'key2': 'value2'})
    assert ad.key1 == 'value1'
    assert ad.key2 == 'value2'

def test_secure_value_access():
    """Test that values are secured correctly when the secure flag is True."""
    ad = AttrDict({'password': 'my_secret'}, secure=True, message="<Custom Secured>")
    assert isinstance(ad.password, Secure)
    assert str(ad.password) == "<Custom Secured>"

def test_nested_dict_conversion():
    """Test that nested dictionaries are converted into AttrDict instances."""
    ad = AttrDict({'nested': {'key': 'value'}}, secure=False)
    assert isinstance(ad.nested, AttrDict)
    assert ad.nested.key == 'value'

def test_setattr_behavior():
    """Test setting attributes using dot notation."""
    ad = AttrDict(secure=False)
    ad.new_key = 'new_value'
    assert 'new_key' in ad
    assert ad['new_key'] == 'new_value'

def test_secure_flag_inheritance():
    """Test that the secure flag is inherited by nested AttrDict instances."""
    ad = AttrDict({'nested': {'key': 'value'}}, secure=True, message="<Custom Secured>")
    assert isinstance(ad.nested.key, Secure)
    assert str(ad.nested.key) == "<Custom Secured>"

def test_exception_for_nonexistent_attribute():
    """Test that accessing a nonexistent attribute raises an AttributeError."""
    ad = AttrDict(secure=False)
    with pytest.raises(AttributeError):
        _ = ad.nonexistent

def test_initialization_with_args_kwargs():
    """Test initialization with various arguments and keyword arguments."""
    ad = AttrDict({'key1': 'value1'}, key2='value2')
    assert ad.key1 == 'value1'
    assert ad.key2 == 'value2'

def test_convert_dicts_method():
    """Test that _convert_dicts method correctly converts nested dictionaries."""
    ad = AttrDict({'nested': {'key': 'value'}})
    ad._convert_dicts()
    assert isinstance(ad.nested, AttrDict)
    assert ad.nested.key == 'value'

def test_convert_value_method():
    """Test that _convert_value method correctly secures values based on the secure flag."""
    ad = AttrDict(secure=True, message="<Custom Secured>")
    secured_value = ad._convert_value('my_secret')
    assert isinstance(secured_value, Secure)
    assert str(secured_value) == "<Custom Secured>"

def test_get_original_method():
    """Test that _get_original method correctly retrieves the original value."""
    ad = AttrDict({'password': 'my_secret'}, secure=True, message="<Custom Secured>")
    original_value = ad._get_original('password')
    assert original_value == 'my_secret'

def test_get_original_attrdict_with_secure():
    """Test that _get_original method returns the original value for a nested AttrDict with Secure instances."""
    ad = AttrDict({'nested': {'password': 'my_secret'}}, secure=True, message="<Custom Secured>")
    original_value = ad._get_original('nested')
    assert original_value == {'password': 'my_secret'}

def test_get_original_regular_value():
    """Test that _get_original method returns the original value for a regular value."""
    ad = AttrDict({'key': 'value'}, secure=False)
    original_value = ad._get_original('key')
    assert original_value == 'value'

def test_get_original_nonexistent_attribute():
    """Test that _get_original method raises an AttributeError for a nonexistent attribute."""
    ad = AttrDict(secure=False)
    with pytest.raises(AttributeError):
        ad._get_original('nonexistent')

def test_setitem_behavior():
    """Test that __setitem__ secures values when being set through item assignment."""
    ad = AttrDict(secure=True, message="<Custom Secured>")
    ad['password'] = 'my_secret'
    assert isinstance(ad.password, Secure)
    assert str(ad.password) == "<Custom Secured>"
