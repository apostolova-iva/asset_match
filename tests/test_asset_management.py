import os
import json
from unittest.mock import patch, mock_open
from services.asset_management import AssetProcessor


@patch("os.listdir")
def test_list_json_files(mock_listdir):
    """
    Test that list_json_files returns the correct list of JSON files in the directory.
    """
    mock_listdir.return_value = ["file1.json", "file2.json", "not_json.txt"]
    processor = AssetProcessor("dummy_dir")
    files = processor.list_json_files()

    # Normalize the paths to account for OS differences
    expected_files = [
        os.path.join("dummy_dir", "file1.json"),
        os.path.join("dummy_dir", "file2.json"),
    ]

    assert len(files) == 2
    assert files == expected_files


@patch("os.listdir")
def test_list_json_files_empty(mock_listdir):
    """
    Test that list_json_files returns an empty list if no JSON files are present.
    """
    mock_listdir.return_value = []
    processor = AssetProcessor("dummy_dir")
    files = processor.list_json_files()

    assert files == []


@patch("os.listdir")
def test_list_json_files_non_existent_directory(mock_listdir):
    """
    Test that list_json_files handles the case where the directory does not exist.
    """
    mock_listdir.side_effect = FileNotFoundError
    processor = AssetProcessor("dummy_dir")
    files = processor.list_json_files()

    assert files == []


@patch("os.listdir")
def test_list_json_files_permission_denied(mock_listdir):
    """
    Test that list_json_files handles the case where directory access is denied.
    """
    mock_listdir.side_effect = PermissionError
    processor = AssetProcessor("dummy_dir")
    files = processor.list_json_files()

    assert files == []


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"assets": [{"name": "Test Asset"}]}',
)
@patch("json.load")
def test_read_json_file(mock_json_load, mock_open):
    """
    Test that read_json_file correctly reads and yields assets from a JSON file.
    """
    mock_json_load.return_value = {"assets": [{"name": "Test Asset"}]}
    processor = AssetProcessor("dummy_dir")
    assets = list(processor.read_json_file("dummy_file.json"))

    assert len(assets) == 1
    assert assets[0]["name"] == "Test Asset"


@patch("builtins.open", new_callable=mock_open, read_data='{"assets": []}')
@patch("json.load")
def test_read_json_file_empty(mock_json_load, mock_open):
    """
    Test that read_json_file handles an empty assets list in the JSON file.
    """
    mock_json_load.return_value = {"assets": []}
    processor = AssetProcessor("dummy_dir")
    assets = list(processor.read_json_file("dummy_file.json"))

    assert assets == []


@patch("builtins.open", new_callable=mock_open, read_data='{"wrong_key": []}')
@patch("json.load")
def test_read_json_file_unexpected_format(mock_json_load, mock_open):
    """
    Test that read_json_file handles a JSON file with an unexpected format.
    """
    mock_json_load.return_value = {"wrong_key": []}
    processor = AssetProcessor("dummy_dir")
    assets = list(processor.read_json_file("dummy_file.json"))

    assert assets == []  # No assets should be returned if the format is unexpected


@patch("builtins.open", new_callable=mock_open)
@patch("json.load")
def test_read_json_file_json_decode_error(mock_json_load, mock_open):
    """
    Test that read_json_file handles JSON decoding errors.
    """
    mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
    processor = AssetProcessor("dummy_dir")
    assets = list(processor.read_json_file("dummy_file.json"))

    assert assets == []


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"assets": [{"name": "Test Asset"}]}',
)
@patch("json.load")
def test_read_json_file_file_not_found(mock_json_load, mock_open):
    """
    Test that read_json_file handles the case where the JSON file is not found.
    """
    mock_open.side_effect = FileNotFoundError
    processor = AssetProcessor("dummy_dir")
    assets = list(processor.read_json_file("dummy_file.json"))

    assert assets == []


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"assets": [{"name": "Test Asset"}]}',
)
@patch("json.load")
def test_read_json_file_permission_denied(mock_json_load, mock_open):
    """
    Test that read_json_file handles the case where file access is denied.
    """
    mock_open.side_effect = PermissionError
    processor = AssetProcessor("dummy_dir")
    assets = list(processor.read_json_file("dummy_file.json"))

    assert assets == []


def test_extract_asset_info_complete():
    """
    Test that extract_asset_info correctly extracts all necessary fields from an asset.
    """
    processor = AssetProcessor("dummy_dir")
    asset = {"name": "Test Asset", "model": "Model X", "ip_address": "192.168.1.1"}
    extracted = processor.extract_asset_info(asset)

    assert extracted is not None
    assert extracted["Name"] == "Test Asset"
    assert extracted["Model"] == "Model X"
    assert extracted["IP Address"] == "192.168.1.1"


def test_extract_asset_info_incomplete():
    """
    Test that extract_asset_info returns None if any necessary field is missing.
    """
    processor = AssetProcessor("dummy_dir")

    asset_missing_name = {"model": "Model X", "ip_address": "192.168.1.1"}
    asset_missing_model = {"name": "Test Asset", "ip_address": "192.168.1.1"}
    asset_missing_ip = {"name": "Test Asset", "model": "Model X"}

    assert processor.extract_asset_info(asset_missing_name) is None
    assert processor.extract_asset_info(asset_missing_model) is None
    assert processor.extract_asset_info(asset_missing_ip) is None


def test_extract_asset_info_alternative_keys():
    """
    Test that extract_asset_info correctly extracts fields using alternative keys.
    """
    processor = AssetProcessor("dummy_dir")

    asset = {"name_snmp": "Test Asset", "asset-model": "Model X", "ipv4": "192.168.1.1"}
    extracted = processor.extract_asset_info(asset)

    assert extracted is not None
    assert extracted["Name"] == "Test Asset"
    assert extracted["Model"] == "Model X"
    assert extracted["IP Address"] == "192.168.1.1"


def test_extract_asset_info_unexpected_format():
    """
    Test that extract_asset_info handles unexpected asset formats.
    """
    processor = AssetProcessor("dummy_dir")

    asset_unexpected = {"unexpected_key": "unexpected_value"}
    extracted = processor.extract_asset_info(asset_unexpected)

    assert extracted is None  # Should return None if required fields are missing
