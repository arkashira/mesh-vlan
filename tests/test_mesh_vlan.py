import json
from unittest.mock import patch
from mesh_vlan import MeshVLANConfig, MeshVLANWebUI, run_server

def test_load_config():
    config_data = '{"test_key": "test_value"}'
    config = MeshVLANConfig()
    config.load_config(config_data)
    assert config.config == {"test_key": "test_value"}

def test_save_config():
    config = MeshVLANConfig()
    config.config = {"test_key": "test_value"}
    saved_config = config.save_config()
    assert json.loads(saved_config) == {"test_key": "test_value"}

def test_update_config():
    config = MeshVLANConfig()
    config.update_config("new_key", "new_value")
    assert config.config["new_key"] == "new_value"

@patch('mesh_vlan.HTTPServer')
def test_run_server(mock_httpserver):
    mock_server_instance = mock_httpserver.return_value
    run_server(8000)
    mock_httpserver.assert_called_once_with(('', 8000), MeshVLANWebUI)
    mock_server_instance.serve_forever.assert_called_once()
