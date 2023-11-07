import pytest
import typer
from typer.testing import CliRunner

from proceedings_ml.scripts.text_folder_to_jsonl import create_jsonl_from_folder


@pytest.fixture
def tmp_folder(tmp_path):
    tmp_folder = tmp_path / "text_folder"
    tmp_folder.mkdir()
    tmp_file = tmp_folder / "file1.txt"
    tmp_file.write_text("This is file 1")
    tmp_file = tmp_folder / "file2.txt"
    tmp_file.write_text("This is file 2")
    return tmp_folder


@pytest.fixture
def expected_output_file(tmp_path):
    tmp_file = tmp_path / "output.jsonl"
    tmp_file.write_text(
        '{"text": "This is file 1", "meta": {"file_name": "file1.txt"}}\n{"text": "This is file 2", "meta": {"file_name": "file2.txt"}}\n'
    )
    return tmp_file


def test_create_jsonl_from_folder(tmp_folder, expected_output_file):
    output_file = tmp_folder / "output.jsonl"
    create_jsonl_from_folder(tmp_folder, output_file)
    assert output_file.read_text() == expected_output_file.read_text()


app = typer.Typer()
app.command()(create_jsonl_from_folder)
runner = CliRunner()


def test_app(tmp_folder, expected_output_file):
    result = runner.invoke(app, [str(tmp_folder), str(tmp_folder / "output.jsonl")])
    assert result.exit_code == 0
    assert result.stdout == ""
    assert result.stderr_bytes is None
    assert (tmp_folder / "output.jsonl").read_text() == expected_output_file.read_text()
