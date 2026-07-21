"""Validation helpers for LCIS dataset names and versions.

This module contains small regular-expression checks used before export files
are written. It depends only on Python's ``re`` module and keeps LCIS naming
rules in one place for the export workflow.
"""

import re

def is_valid_dataset_name(name):
    """Validates dataset name per LCIS schema §3.2.1.
    Only Latin letters, digits, hyphens, underscores allowed. Max 250 characters."""
    """
    Dataset names become filename stems during export, so the rule is kept
    deliberately strict: short enough for filesystems and limited to portable
    ASCII characters that will behave consistently across platforms.
    """
    if len(name) > 250:
        return False
    pattern = r'^[A-Za-z0-9_-]+$'
    return bool(re.match(pattern, name))

def is_valid_schema_version(version):
    """Validates schema version per LCIS schema §3.2.1.
    Must follow format LCIS + 4-digit year e.g. LCIS2024."""
    """
    The schema version is treated as a compact identifier rather than free
    text. Matching ``LCIS`` plus a four-digit year keeps exported metadata
    aligned with the schema naming convention.
    """
    pattern = r'^LCIS\d{4}$'
    return bool(re.match(pattern, version))

def is_valid_dataset_version(version):
    """Validates dataset version per LCIS schema §3.2.1.
    Must follow semantic versioning e.g. 1.0.1."""
    """
    Dataset versions use a simple semantic-version shape so revisions can be
    compared and cited clearly in LCIS properties and metadata files.
    """
    pattern = r'^\d+\.\d+\.\d+$'
    return bool(re.match(pattern, version))
