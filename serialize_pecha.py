import re
from pathlib import Path

from openpecha.serializers import HFMLSerializer
from openpecha.utils import load_yaml

def get_hfml_text(opf_path):
    serializer = HFMLSerializer(opf_path, layers=['Pagination', 'Durchen'])
    serializer.apply_layers()
    hfml_text = serializer.get_result()
    return hfml_text

def save_volwise(hfml_text, output_path, type):
    for vol_num, hfml in hfml_text.items():
        Path(f'{output_path}/{type}/{type}.txt').write_text(hfml, encoding="utf-8")
        print(f'{vol_num} done')

def create_volwise(opf_path, type):
    output_path = f"./serialized/"
    text_hfml = get_hfml_text(opf_path)
    save_volwise(text_hfml, output_path, type)

if __name__ == "__main__":
    derge_pecha_id = "P000002"
    peking_pecha_id = "I647D7CBC"
    narthang_pecha_id = "IF6EAA761"
    chone_pecha_id = "I1417FAF4"
    
    opf_path = Path(f"./pechas/{chone_pecha_id}/{chone_pecha_id}.opf")
    create_volwise(opf_path, "chone")