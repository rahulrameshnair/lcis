import builtins
import importlib


def test_export_module_import_does_not_prompt_or_export(monkeypatch):
    def fail_input(*args, **kwargs):
        raise AssertionError("module import should not prompt for input")

    monkeypatch.setattr(builtins, "input", fail_input)
    module = importlib.import_module("lcis.inventory.export_lci")

    assert hasattr(module, "export_inventory")


def test_network_module_import_does_not_prompt_or_export(monkeypatch):
    def fail_input(*args, **kwargs):
        raise AssertionError("module import should not prompt for input")

    monkeypatch.setattr(builtins, "input", fail_input)
    module = importlib.import_module("lcis.inventory.lci_network")

    assert hasattr(module, "export_network")


def test_network_plotly_module_import_does_not_require_plotly_or_prompt(monkeypatch):
    def fail_input(*args, **kwargs):
        raise AssertionError("module import should not prompt for input")

    monkeypatch.setattr(builtins, "input", fail_input)
    module = importlib.import_module("lcis.inventory.network_plotly")

    assert hasattr(module, "plot_network")


def test_experimental_import_module_is_import_safe():
    module = importlib.import_module("lcis.imports.import_excel_inventory")

    assert hasattr(module, "import_excel_inventory")
