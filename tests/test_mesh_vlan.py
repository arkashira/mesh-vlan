from mesh_vlan import MeshVLAN, SSID

def test_create_ssid():
    mesh_vlan = MeshVLAN()
    ssid = mesh_vlan.create_ssid("test_ssid", "test_password")
    assert ssid.name == "test_ssid"
    assert ssid.password == "test_password"

def test_delete_ssid():
    mesh_vlan = MeshVLAN()
    mesh_vlan.create_ssid("test_ssid", "test_password")
    mesh_vlan.delete_ssid("test_ssid")
    assert len(mesh_vlan.get_ssids()) == 0

def test_update_radio_settings():
    mesh_vlan = MeshVLAN()
    mesh_vlan.update_radio_settings({"2.4GHz": False, "5GHz": True})
    assert mesh_vlan.get_radio_settings() == {"2.4GHz": False, "5GHz": True}

def test_persist_settings():
    mesh_vlan = MeshVLAN()
    mesh_vlan.update_radio_settings({"2.4GHz": False, "5GHz": True})
    persisted_settings = mesh_vlan.persist_settings()
    assert persisted_settings == {"2.4GHz": False, "5GHz": True}

def test_get_dashboard():
    mesh_vlan = MeshVLAN()
    mesh_vlan.create_ssid("test_ssid", "test_password")
    dashboard = mesh_vlan.get_dashboard()
    assert dashboard == {"ssids": ["test_ssid"], "radio_settings": {"2.4GHz": True, "5GHz": True}}
