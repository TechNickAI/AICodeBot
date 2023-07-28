from aicodebot.config import Session


def test_session_read_write(tmp_path, monkeypatch):
    monkeypatch.setenv("AICODEBOT_SESSION_FILE", str(tmp_path / "session.yaml"))

    assert not Session.get_config_file().exists()

    # Test write
    test_data = {"key": "value"}
    Session.write(test_data)

    # Check that the file was written correctly
    assert Session.get_config_file().exists()

    # Test read
    read_data = Session.read()
    assert read_data == test_data
