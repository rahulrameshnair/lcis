"""Experimental Brightway Excel import helpers.

The import workflow is intentionally not part of the supported LCIS export API
yet. The old notebook-era script had hard-coded project/database names and ran
as soon as it was imported; this placeholder keeps the module import-safe until
the workflow is designed properly. It currently has no runtime dependencies
beyond Python itself.
"""

from __future__ import annotations


def import_excel_inventory(*args, **kwargs):
    """Placeholder for the future supported Excel import workflow."""
    """
    This function intentionally raises instead of attempting a partial import.
    Keeping the placeholder explicit prevents accidental use of an unfinished
    workflow while preserving a stable function name for future development.
    """

    raise NotImplementedError(
        "Excel inventory import is experimental and will be packaged in a "
        "future LCIS release. Use the legacy Imports notebook for now."
    )


__all__ = ["import_excel_inventory"]
