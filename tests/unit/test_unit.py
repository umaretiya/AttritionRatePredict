from urllib import response
import pytest
from attritionRate.utils import read_yaml
from pathlib import Path
from box import ConfigBox
from ensure.main import EnsureError

yaml_files = [
    "tests/data/empty.yaml",
    "tests/data/demo.yaml",
]

def test_read_yaml_empty():
    with pytest.raises(ValueError):
        read_yaml(Path(yaml_files[0]))
        
def test_read_yaml_return_type():
    respons = read_yaml(Path(yaml_files[-1]))
    assert isinstance(respons, ConfigBox)
    
@pytest.mark.parametrize("path_to_yaml",yaml_files)
def test_read_yaml_bad_type(path_to_yaml):
    with pytest.raises(EnsureError):
        read_yaml(path_to_yaml)

class Pytest_Unit:
    yaml_files = [
        "tests/data/empty.yaml",
        "tests/data/demo.yaml",
    ]
    def test_read_yaml_empty(self):
        with pytest.raises(ValueError):
            read_yaml(Path(self.yaml_files[0]))
            
    def test_read_yaml_return_type(self):
        respons = read_yaml(Path(self.yaml_files[-1]))
        assert isinstance(respons, ConfigBox)
        
    @pytest.mark.parametrize("path_to_yaml",yaml_files)
    def test_read_yaml_bad_type(path_to_yaml):
        with pytest.raises(EnsureError):
            read_yaml(path_to_yaml)