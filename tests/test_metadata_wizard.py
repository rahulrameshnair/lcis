import json

from lcis.inventory.metadata_template import (
    convert_metadata_workbook,
    load_license_lookup,
    load_metadata_fields,
    read_metadata_workbook,
    write_all_metadata_outputs,
)


def test_template_structure_is_read():
    fields = load_metadata_fields()

    assert fields[0].element == "Dataset"
    assert fields[0].attribute == "name"
    assert fields[0].label == "Name"
    assert any(field.element == "License" for field in fields)


def test_license_lookup_reads_spdx_identifiers():
    licenses = load_license_lookup()

    assert licenses["MIT License"] == "MIT"


def test_metadata_outputs_roundtrip(tmp_path):
    metadata = {
        "Dataset": {
            "name": "demo_dataset",
            "description": "Demo metadata",
            "schema": "LCIS2024",
        },
        "Authors": {
            "name": "Rahul Ramesh Nair",
            "email": "rahul.nair@dlr.de",
        },
        "License": {
            "name": "MIT License",
        },
    }

    paths = write_all_metadata_outputs(metadata, "demo_dataset", tmp_path)

    assert paths["xlsx"].exists()
    assert paths["json"].exists()
    assert paths["csv"].exists()

    with open(paths["json"], encoding="utf-8") as file:
        json_metadata = json.load(file)
    assert json_metadata["Dataset"]["name"] == "demo_dataset"

    workbook_metadata = read_metadata_workbook(paths["xlsx"])
    assert workbook_metadata["Dataset"]["name"] == "demo_dataset"
    assert workbook_metadata["Dataset"]["schema"] == "LCIS2024"
    assert workbook_metadata["License"]["spdx"] == "MIT"


def test_filled_workbook_converts_to_json_and_csv(tmp_path):
    metadata = {
        "Dataset": {
            "name": "demo_dataset",
            "description": "Demo metadata",
            "schema": "LCIS2024",
        },
    }
    paths = write_all_metadata_outputs(metadata, "demo_dataset", tmp_path)

    paths["json"].unlink()
    paths["csv"].unlink()

    converted = convert_metadata_workbook(paths["xlsx"], output_dir=tmp_path)

    assert converted["json"].exists()
    assert converted["csv"].exists()
