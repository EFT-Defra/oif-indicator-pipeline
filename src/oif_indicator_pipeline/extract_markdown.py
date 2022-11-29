from typing import List, Optional

from pandoc import read, write

COMMAND_SEPARATOR = "# COMMAND ----------\n\n"
MAGIC_IDENTIFIER = "# MAGIC "
MARKDOWN_MAGIC_IDENTIFIER = f"{MAGIC_IDENTIFIER}%md "

def _get_text(path: str) -> str:
    with open(path) as file:
        text = file.read()
    return text


def _get_markdown_commands(
    text: str,
    command_separator: str = COMMAND_SEPARATOR,
    markdown_magic_identifier: str = MARKDOWN_MAGIC_IDENTIFIER,
) -> str:
    return "".join(command for command in text.split(command_separator) if command.startswith(markdown_magic_identifier))


def _clean_markdown_commands(
    markdown_commands: str,
    magic_identifier: str = MAGIC_IDENTIFIER,
    markdown_magic_identifier: str = MARKDOWN_MAGIC_IDENTIFIER,
) -> str:
    return (
        markdown_commands
        .replace(markdown_magic_identifier, "")
        .replace(magic_identifier, "")
    )


def extract_markdown(path: str) -> str:
    text = _get_text(path)
    markdown_commands = _get_markdown_commands(text)
    return _clean_markdown_commands(markdown_commands)


def convert_markdown_to_html(
    markdown: str,
    file: Optional[str] = None,
    options: Optional[List[str]] = None    
) -> Optional[str]:
    _options = options if options else ["--section-divs"]
    doc = read(markdown)
    return write(
        doc=doc, 
        file=file, 
        format="html", 
        options=_options
    )