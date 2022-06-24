from pathlib import Path
from openpecha.utils import load_yaml



def get_base_name(layers_path, image_group_id):
    for layer_path in layers_path:
        pagination_layer = load_yaml(Path(f"{layer_path}/Pagination.yml"))
        annotations = pagination_layer['annotations']
        for _, ann_info in annotations.items():
            if ann_info['reference'][:9] == image_group_id:
                return layer_path.name
            else:
                break



if __name__ == "__main__":
    derge_pecha_id = "P000800"
    narthang_pecha_id = "IF6EAA761"
    chone_pecha_id = "I1417FAF4"
    peking_pecha_id = "I647D7CBC"
    image_group_id = "I1GS66136"
    opf_path = Path(f"./pechas/{chone_pecha_id}/{chone_pecha_id}.opf")
    layers_path = list(Path(f"{opf_path}/layers").iterdir())
    base_name = get_base_name(layers_path, image_group_id)
    print(base_name)