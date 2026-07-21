"""Command-line wrapper for template-driven LCIS metadata collection.

This module connects the reusable metadata-template functions to the Click
command-line interface. It depends on Click for prompts/options, pathlib for
filesystem paths, and :mod:`lcis.inventory.metadata_template` for the actual
template parsing and output writing.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import click

from lcis.inventory.metadata_template import (
    collect_metadata_from_template,
    write_all_metadata_outputs,
)


def collect_metadata(
    *,
    template_path: str | Path | None = None,
    dataset_name: str | None = None,
    schema_version: str = "LCIS2024",
) -> dict[str, dict[str, Any]]:
    """Collect metadata using the packaged Excel template structure."""
    """
    This function prepares the initial values that should already be known
    before the wizard starts. The schema is always seeded, and the dataset
    name is seeded when the caller provides one, so the interactive wizard can
    still let the user confirm or replace those values while preserving the
    LCIS template structure.
    """

    initial_values: dict[tuple[str, str], Any] = {
        ("Dataset", "schema"): schema_version,
    }
    if dataset_name:
        initial_values[("Dataset", "name")] = dataset_name

    return collect_metadata_from_template(
        template_path=template_path,
        initial_values=initial_values,
    )


@click.command("metadata-wizard")
@click.option(
    "--output-dir",
    "-o",
    default=".",
    show_default=True,
    type=click.Path(file_okay=False, writable=True, path_type=Path),
    help="Directory where metadata XLSX, JSON, and CSV files will be written.",
)
@click.option(
    "--dataset-name",
    "-n",
    default=None,
    help="Dataset name. Used as the output file prefix and default metadata value.",
)
@click.option(
    "--schema-version",
    default="LCIS2024",
    show_default=True,
    help="LCIS schema version used as the default Dataset.schema value.",
)
@click.option(
    "--template",
    "template_path",
    default=None,
    type=click.Path(dir_okay=False, exists=True, path_type=Path),
    help="Optional metadata template workbook. Defaults to the packaged LCIS template.",
)
def metadata_wizard(
    output_dir: Path,
    dataset_name: str | None,
    schema_version: str,
    template_path: Path | None,
) -> dict[str, dict[str, Any]]:
    """Interactively collect LCIS metadata and write XLSX, JSON, and CSV."""
    """
    This is the command-line workflow used by ``lcis metadata-wizard``. It
    collects the grouped metadata, chooses a safe output stem from either the
    command option or the collected Dataset.name field, and then delegates all
    file creation to the template module so the workbook, JSON, and CSV stay
    synchronized.
    """

    metadata = collect_metadata(
        template_path=template_path,
        dataset_name=dataset_name,
        schema_version=schema_version,
    )
    stem = dataset_name or metadata.get("Dataset", {}).get("name") or "metadata"
    paths = write_all_metadata_outputs(
        metadata,
        str(stem),
        output_dir,
        template_path=template_path,
    )

    for kind, path in paths.items():
        click.secho(f"  {kind.upper()} written -> {path}", fg="green")

    return metadata


__all__ = ["collect_metadata", "metadata_wizard"]
