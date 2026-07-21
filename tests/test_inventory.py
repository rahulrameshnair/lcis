import os
import csv
import tempfile
from lcis.inventory.metadata import Dbprops
import openpyxl
from lcis.inventory.metadata import Metadata

from lcis.inventory.validate import (
    is_valid_dataset_name,
    is_valid_schema_version,
    is_valid_dataset_version
)

class TestDatasetNaming:

    def test_valid_name(self):
        assert is_valid_dataset_name("aviation-fuel-production") == True

    def test_valid_name_with_underscore(self):
        assert is_valid_dataset_name("aviation_fuel_production") == True

    def test_valid_name_with_numbers(self):
        assert is_valid_dataset_name("aviation-fuel-2024") == True

    def test_rejects_special_characters(self):
        assert is_valid_dataset_name("aviation#fuel") == False

    def test_rejects_spaces(self):
        assert is_valid_dataset_name("aviation fuel") == False

    def test_rejects_percent(self):
        assert is_valid_dataset_name("fuel%production") == False

    def test_rejects_at_symbol(self):
        assert is_valid_dataset_name("aviation@fuel") == False

    def test_rejects_dot(self):
        assert is_valid_dataset_name("aviation.fuel") == False

    def test_rejects_slash(self):
        assert is_valid_dataset_name("aviation/fuel") == False

    def test_rejects_over_250_characters(self):
        assert is_valid_dataset_name("a" * 251) == False

    def test_accepts_exactly_250_characters(self):
        assert is_valid_dataset_name("a" * 250) == True

class TestSchemaVersion:

    def test_valid_schema_version(self):
        assert is_valid_schema_version("LCIS2024") == True

    def test_rejects_wrong_prefix(self):
        assert is_valid_schema_version("LCI2024") == False

    def test_rejects_missing_year(self):
        assert is_valid_schema_version("LCIS") == False

    def test_rejects_lowercase(self):
        assert is_valid_schema_version("lcis2024") == False

class TestDatasetVersion:

    def test_valid_version(self):
        assert is_valid_dataset_version("1.0.0") == True

    def test_valid_version_multidigit(self):
        assert is_valid_dataset_version("1.0.1") == True

    def test_rejects_missing_patch(self):
        assert is_valid_dataset_version("1.0") == False

    def test_rejects_text(self):
        assert is_valid_dataset_version("v1.0.0") == False
        
class TestDbpropsCSV:

    def test_csv_creates_file(self):
        """CSV file is created at the specified path."""
        with tempfile.TemporaryDirectory() as tmp:
            output_file = os.path.join(tmp, "test_props.csv")
            Dbprops.csv(output_file, {"Dataset Name": "aviation-fuel"})
            assert os.path.exists(output_file)

    def test_csv_has_header_row(self):
        """CSV file contains the correct header: Property, Value."""
        with tempfile.TemporaryDirectory() as tmp:
            output_file = os.path.join(tmp, "test_props.csv")
            Dbprops.csv(output_file, {"Dataset Name": "aviation-fuel"})
            with open(output_file) as f:
                reader = csv.reader(f)
                header = next(reader)
            assert header == ["Property", "Value"]

    def test_csv_writes_key_value_pairs(self):
        """CSV rows correctly reflect the input dictionary."""
        with tempfile.TemporaryDirectory() as tmp:
            output_file = os.path.join(tmp, "test_props.csv")
            Dbprops.csv(output_file, {"Schema Version": "LCIS2024"})
            with open(output_file) as f:
                reader = csv.reader(f)
                next(reader)
                row = next(reader)
            assert row == ["Schema Version", "LCIS2024"]

    def test_csv_joins_list_values(self):
        """List values are joined into a comma-separated string."""
        with tempfile.TemporaryDirectory() as tmp:
            output_file = os.path.join(tmp, "test_props.csv")
            Dbprops.csv(output_file, {"Dependencies": ["ecoinvent", "biosphere3"]})
            with open(output_file) as f:
                reader = csv.reader(f)
                next(reader)
                row = next(reader)
            assert row == ["Dependencies", "ecoinvent, biosphere3"]

    def test_csv_handles_multiple_properties(self):
        """All dictionary entries are written as separate rows."""
        with tempfile.TemporaryDirectory() as tmp:
            output_file = os.path.join(tmp, "test_props.csv")
            props = {
                "Dataset Name": "aviation-fuel",
                "Schema Version": "LCIS2024",
                "Dataset Version": "1.0.0"
            }
            Dbprops.csv(output_file, props)
            with open(output_file) as f:
                rows = list(csv.reader(f))
            assert len(rows) == 4
            
class TestMetadataExcelToCSV:

    def test_csv_file_is_created(self):
        """CSV file is created from a valid Excel file."""
        with tempfile.TemporaryDirectory() as tmp:
            excel_file = os.path.join(tmp, "test.xlsx")
            csv_file = os.path.join(tmp, "test.csv")
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["Name", "Value"])
            ws.append(["aviation-fuel", "1.0.0"])
            wb.save(excel_file)
            Metadata.excel_to_csv(excel_file, csv_file)
            assert os.path.exists(csv_file)

    def test_csv_contains_correct_headers(self):
        """CSV headers match the Excel column headers."""
        with tempfile.TemporaryDirectory() as tmp:
            excel_file = os.path.join(tmp, "test.xlsx")
            csv_file = os.path.join(tmp, "test.csv")
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["Name", "Value"])
            ws.append(["aviation-fuel", "1.0.0"])
            wb.save(excel_file)
            Metadata.excel_to_csv(excel_file, csv_file)
            with open(csv_file) as f:
                reader = csv.reader(f)
                header = next(reader)
            assert header == ["Name", "Value"]

    def test_csv_contains_correct_data(self):
        """CSV data row matches the Excel data row."""
        with tempfile.TemporaryDirectory() as tmp:
            excel_file = os.path.join(tmp, "test.xlsx")
            csv_file = os.path.join(tmp, "test.csv")
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["Name", "Value"])
            ws.append(["aviation-fuel", "1.0.0"])
            wb.save(excel_file)
            Metadata.excel_to_csv(excel_file, csv_file)
            with open(csv_file) as f:
                reader = csv.reader(f)
                next(reader)
                row = next(reader)
            assert row == ["aviation-fuel", "1.0.0"]

    def test_csv_handles_multiple_rows(self):
        """All data rows from Excel are written to CSV."""
        with tempfile.TemporaryDirectory() as tmp:
            excel_file = os.path.join(tmp, "test.xlsx")
            csv_file = os.path.join(tmp, "test.csv")
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["Name", "Version"])
            ws.append(["aviation-fuel", "1.0.0"])
            ws.append(["hydrogen", "1.0.1"])
            ws.append(["electrolysis", "2.0.0"])
            wb.save(excel_file)
            Metadata.excel_to_csv(excel_file, csv_file)
            with open(csv_file) as f:
                rows = list(csv.reader(f))
            assert len(rows) == 4

    def test_raises_error_on_missing_file(self):
        """A missing Excel file raises an error."""
        with tempfile.TemporaryDirectory() as tmp:
            csv_file = os.path.join(tmp, "test.csv")
            try:
                Metadata.excel_to_csv("nonexistent.xlsx", csv_file)
                assert False, "Expected an error but none was raised"
            except Exception:
                pass