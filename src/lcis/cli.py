"""Command-line entry points for the LCIS package.

This file defines the root Click command group and attaches supported LCIS
subcommands. It depends on Click for command registration and on the inventory
metadata wizard module for the interactive metadata workflow.
"""

import click

@click.group()
def cli():
    """LCIS – Life Cycle Inventory Schema command-line tool."""
    """
    This root command does not perform work by itself. It exists as the
    command-line container where LCIS workflows are registered, so future
    export, import, metadata, or validation commands can be exposed through
    one stable executable entry point.
    """
    pass

from lcis.inventory.metadata_wizard import metadata_wizard
cli.add_command(metadata_wizard)
