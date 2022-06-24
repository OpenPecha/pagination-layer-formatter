
import json
from pathlib import Path

from openpecha.core.layer import LayerEnum
from openpecha.core.pecha import OpenPechaFS


def get_base_names(opf_path):
    base_names = []
    for base_path in list((opf_path / "base").iterdir()):
        base_names.append(base_path.stem)
    return base_names

def get_img_link(ann):
    img_fn = ann['reference'].strip()
    img_grp_id = img_fn[:-8]
    img_link = f"iiif.bdrc.io/bdr:{img_grp_id}::{img_fn}/full/max/0/default.jpg"
    return img_link

def get_text2image_alignment(pecha_id, pagination_layer):
    text2image_alignment = {
        'id': pecha_id,
        'type': "image",
        'alignment' : []
    }
    alignments = []
    for _, ann in pagination_layer['annotations'].items():
        img_link = get_img_link(ann)
        cur_alignment = {
            'source_segment': {
                'start': ann['span']['start'],
                'end': ann['span']['end']
            },
            'target_segment': img_link
        }
        alignments.append(cur_alignment)
    text2image_alignment['alignment'] = alignments
    return text2image_alignment



def serialize_pagination_layer_to_json(opf_id, opf_path, json_path):
    pecha = OpenPechaFS(opf_id, opf_path)
    base_names = get_base_names(pecha.opf_path)
    for base_name in base_names:
        pagination_layer = pecha.read_layers_file(base_name, LayerEnum.pagination.value)
        text2image_alignment = get_text2image_alignment(opf_id, pagination_layer)
        text2image_alignment = json.dumps(text2image_alignment, ensure_ascii=False)
        json_path.write_text(text2image_alignment, encoding='utf-8')


if __name__ == "__main__":
    opf_path = Path('./data/opfs/OC579B0AC/OC579B0AC.opf')
    pecha_id = opf_path.stem
    json_path = Path(f'./data/json/{pecha_id}.json')
    serialize_pagination_layer_to_json(pecha_id, opf_path, json_path)

