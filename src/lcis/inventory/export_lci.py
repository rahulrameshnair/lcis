"""Export Brightway inventories to LCIS files.

This module is intentionally import-safe: it defines functions only, and does
not prompt, select Brightway projects, or write files until a public function is
called. It depends on Brightway/BW2IO at export time, pathlib/shutil/json for
file handling, the LCIS validation helpers for naming checks, and the metadata
template modules for metadata sidecar creation.
"""

from __future__ import annotations

import json
import pprint
import shutil
from pathlib import Path
from typing import Any

from lcis.inventory.validate import (
    is_valid_dataset_name,
    is_valid_dataset_version,
    is_valid_schema_version,
)


def _require_valid_export_inputs(
    output_stem: str,
    schema_version: str,
    dataset_version: str,
) -> None:
    """Raise ``ValueError`` when export names or versions are not LCIS-safe."""
    """
    Export writes several files using the dataset stem and embeds schema and
    dataset versions in the properties output. Centralizing validation here
    keeps bad filenames and malformed version strings from propagating into
    the generated LCIS file set.
    """

    if not is_valid_dataset_name(output_stem):
        raise ValueError(
            f"Invalid dataset name: {output_stem!r}. Use letters, digits, "
            "hyphens, or underscores only, with a maximum length of 250."
        )
    if not is_valid_schema_version(schema_version):
        raise ValueError(
            f"Invalid schema version: {schema_version!r}. Expected a value "
            "such as 'LCIS2024'."
        )
    if not is_valid_dataset_version(dataset_version):
        raise ValueError(
            f"Invalid dataset version: {dataset_version!r}. Expected semantic "
            "version format such as '1.0.0'."
        )


def _copy_exported_file(source: str | Path, destination: Path) -> Path:
    """Copy an exporter-created file into the requested LCIS output folder."""
    """
    Brightway exporters may write to their own default location. This helper
    normalizes the final file placement by creating the destination directory
    and copying the generated file into the user-selected output directory.
    """

    source_path = Path(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, destination)
    return destination


def _formatted_excel_path(source: Path) -> Path:
    """Return the filename used for the formatted Excel copy."""
    """
    The raw BW2IO Excel export is preserved, while LCIS writes a formatted
    workbook as a separate file. Existing ``.xlsx`` files get a
    ``_formatted`` suffix; non-xlsx paths are normalized to an xlsx suffix.
    """

    if source.suffix.lower() == ".xlsx":
        return source.with_name(f"{source.stem}_formatted.xlsx")
    return source.with_suffix(".xlsx")


def ensure_metadata(
    output_stem: str,
    output_dir: str | Path = ".",
    *,
    prompt_if_missing: bool = True,
    schema_version: str = "LCIS2024",
) -> dict[str, Any] | None:
    """Load or create metadata files for an LCIS export.

    If ``<output_stem>_metadata.xlsx`` already exists, it is read and JSON/CSV
    are regenerated from it. Otherwise, if JSON exists it is loaded. If no
    metadata exists and prompting is enabled, the template-driven wizard
    collects values and writes XLSX, JSON, and CSV files.
    """
    """
    This helper makes metadata generation idempotent around an export. A
    filled workbook is treated as the richest source, existing JSON is
    normalized and expanded into all formats, and only a missing metadata set
    triggers the interactive wizard when prompting is allowed.
    """

    from lcis.inventory.metadata_template import (
        read_metadata_workbook,
        write_all_metadata_outputs,
        write_metadata_csv,
        write_metadata_json,
    )
    from lcis.inventory.metadata_wizard import collect_metadata

    output_dir = Path(output_dir)
    xlsx_path = output_dir / f"{output_stem}_metadata.xlsx"
    json_path = output_dir / f"{output_stem}_metadata.json"
    csv_path = output_dir / f"{output_stem}_metadata.csv"

    if xlsx_path.exists():
        metadata = read_metadata_workbook(xlsx_path)
        write_metadata_json(metadata, json_path)
        write_metadata_csv(metadata, csv_path, template_path=xlsx_path)
        return metadata

    if json_path.exists():
        with open(json_path, encoding="utf-8") as f:
            metadata = _normalize_metadata_json(json.load(f), output_stem, schema_version)
        write_all_metadata_outputs(metadata, output_stem, output_dir)
        return metadata

    if not prompt_if_missing:
        return None

    metadata = collect_metadata(
        dataset_name=output_stem,
        schema_version=schema_version,
    )
    write_all_metadata_outputs(metadata, output_stem, output_dir)

    return metadata


def run_metadata_wizard(
    output_dir: str | Path = ".",
    dataset_name: str | None = None,
) -> dict[str, Any]:
    """Collect LCIS metadata from the user and write XLSX, JSON, and CSV."""
    """
    This public helper exposes the metadata wizard without running a full
    inventory export. It is useful when a researcher wants to prepare or edit
    metadata before the Brightway export step is performed.
    """

    from lcis.inventory.metadata_wizard import collect_metadata

    output_dir = Path(output_dir)
    metadata = collect_metadata(dataset_name=dataset_name)
    stem = dataset_name or metadata.get("Dataset", {}).get("name") or "metadata"

    from lcis.inventory.metadata_template import write_all_metadata_outputs

    write_all_metadata_outputs(metadata, str(stem), output_dir)
    return metadata


def export_inventory(
    project_name: str,
    database_name: str,
    output_stem: str,
    schema_version: str = "LCIS2024",
    dataset_version: str = "1.0.0",
    output_dir: str | Path = ".",
    *,
    print_properties: bool = True,
) -> dict[str, Path]:
    """Export a Brightway database to the LCIS inventory file set.

    Outputs are written to ``output_dir`` and use ``output_stem`` as their
    prefix:

    - ``<output_stem>.csv``
    - ``<output_stem>.xlsx``
    - ``<output_stem>_properties.csv``
    """
    """
    The export flow validates LCIS names, selects the Brightway project,
    produces raw CSV and Excel exports through BW2IO, formats the Excel file,
    then writes a properties CSV that combines identifying metadata, database
    counts, and detected database dependencies.
    """

    _require_valid_export_inputs(output_stem, schema_version, dataset_version)

    import bw2data as bw
    import bw2io as bwio

    from lcis.inventory import excel
    from lcis.inventory import metadata as md

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    bw.projects.set_current(project_name)
    bw.Database(database_name)

    csv_source = bwio.export.csv.write_lci_csv(database_name)
    csv_path = _copy_exported_file(csv_source, output_dir / f"{output_stem}.csv")

    excel_source = Path(bwio.export.excel.write_lci_excel(database_name))
    formatted_source = _formatted_excel_path(excel_source)
    excel.excel_format(excel_source, formatted_source)
    xlsx_path = _copy_exported_file(formatted_source, output_dir / f"{output_stem}.xlsx")

    dbprops = md.Dbprops(project_name, database_name)
    database_properties = dbprops.identifying_info(schema_version, dataset_version)
    database_properties |= dbprops.gen_info()
    database_properties["Dataset dependencies"] = dbprops.db_dependencies()

    if print_properties:
        pprint.pprint(database_properties)

    properties_path = output_dir / f"{output_stem}_properties.csv"
    md.Dbprops.csv(properties_path, database_properties)

    return {
        "csv": csv_path,
        "xlsx": xlsx_path,
        "properties_csv": properties_path,
    }


__all__ = ["ensure_metadata", "export_inventory", "run_metadata_wizard"]


def _normalize_metadata_json(
    metadata: dict[str, Any],
    output_stem: str,
    schema_version: str,
) -> dict[str, dict[str, Any]]:
    """Convert old flat metadata JSON to the new template-grouped structure."""
    """
    Older LCIS metadata was stored as one flat JSON object. The template
    workflow expects metadata grouped by LCIS element, so this adapter maps
    legacy keys into the current nested structure while preserving values that
    users may already have created.
    """

    if "Dataset" in metadata:
        return metadata

    def _join(value: Any) -> Any:
        if isinstance(value, list):
            return " | ".join(str(item) for item in value)
        return value

    license_value = metadata.get("license")
    normalized: dict[str, dict[str, Any]] = {
        "Dataset": {
            "name": metadata.get("name") or output_stem,
            "description": metadata.get("description"),
            "language": metadata.get("language"),
            "keywords": _join(metadata.get("keywords")),
            "model": metadata.get("lci_type"),
            "boundary": metadata.get("system_boundary"),
            "fu": metadata.get("functional_unit"),
            "region": metadata.get("region"),
            "assumptions": metadata.get("modelling_assumptions"),
            "schema": metadata.get("schema_version") or schema_version,
        },
        "Authors": {
            "name": _join(metadata.get("authors")),
            "email": metadata.get("contact"),
            "affliation": metadata.get("affiliation"),
        },
        "Background": {
            "name": metadata.get("background_database"),
        },
        "License": {
            "name": license_value,
            "spdx": license_value,
            "attribution": metadata.get("license_attribution"),
        },
        "Primary data": {
            "comments": _join(metadata.get("primary_data_sources")),
        },
        "Secondary data": {
            "comments": _join(metadata.get("secondary_data_sources")),
        },
        "Glossary": {
            "abbreviations": _join(metadata.get("abbreviations")),
        },
    }

    return normalized
