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
