import re
from pathlib import Path
from openpecha.formatters.hfml import HFMLFormatter
from openpecha.core.ids import get_open_pecha_id

def hfml_to_opf(hfml_name, pecha_output_path):
    pecha_id = get_open_pecha_id()
    text_path = Path(f"./new_OE/{hfml_name}")
    formatter = HFMLFormatter(output_path=pecha_output_path)
    formatter.create_opf(text_path, pecha_id)
    pecha_path = Path(f"{pecha_output_path}/{pecha_id}")
    return pecha_path

def remove_line_break():
    text = Path(f"./new_OE/with_line_break/with_line_break.txt").read_text(encoding='utf-8')
    new_text = re.sub(r"\n", " ", text)
    Path(f"./new_OE/no_line_break/no_line_break.txt").write_text(new_text, encoding='utf-8')

if __name__ == "__main__":
    for num in range(0,3):
        hfml_name = "with_line_break"
        hfml_to_opf(hfml_name, "with_line_break_OE")
