from importlib.resources import files

import lcis


def test_package_version_is_exposed():
    assert lcis.__version__ == "0.3.0"


def test_templates_are_packaged():
    template_dir = files("lcis.templates")

    assert (template_dir / "metadata_template.xlsx").is_file()
    assert (template_dir / "bw_exceldb_template.xlsx").is_file()
