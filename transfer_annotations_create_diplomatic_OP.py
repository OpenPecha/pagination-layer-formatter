import re
from pathlib import Path
from antx import transfer
from openpecha.formatters.hfml import HFMLFormatter
from openpecha.core.ids import get_diplomatic_id

def transfer_annotations(source_text, target_text):
    target_text = re.sub(r"\n", " ", target_text)
    annotations = [['reference', r"(〔[\d+].+)"],['line_break', r"(\n)"]]
    result = transfer(source_text, annotations, target_text, output="txt")
    return result



def hfml_to_opf(hfml_name, pecha_output_path):
    pecha_id = get_diplomatic_id()
    text_path = Path(f"./annotation_transfered/{hfml_name}")
    formatter = HFMLFormatter(output_path=pecha_output_path)
    formatter.create_opf(text_path, pecha_id)
    pecha_path = Path(f"{pecha_output_path}/{pecha_id}")
    return pecha_path

if __name__ == "__main__":
    types = ['narthang', 'derge', 'peking']
    for text_type in types:
        source_text = Path(f"./serialized/{text_type}/{text_type}.txt").read_text(encoding='utf-8')
        target_text = Path(f"./D3871/{text_type}.txt").read_text(encoding='utf-8')
        result = transfer_annotations(source_text, target_text)
        Path(f"./annotation_transfered/{text_type}/{text_type}.txt").write_text(result, encoding='utf-8')
        pecha_path = hfml_to_opf(text_type, "Diplomatic_opf")