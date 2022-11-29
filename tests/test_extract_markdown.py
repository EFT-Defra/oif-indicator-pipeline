from pathlib import Path

from oif_indicator_pipeline.extract_markdown import extract_markdown, convert_markdown_to_html

def test_extract_and_convert(shared_datadir: Path) -> None:
    input_path = str(shared_datadir / "databricks-notebook.py")
    with open(shared_datadir / "extracted.html") as file:
        expected_html = file.read()
    markdown = extract_markdown(input_path)
    html = convert_markdown_to_html(markdown)
    assert html == expected_html