import re
import json
import subprocess

from pathlib import Path
from github import Github
from datetime import datetime, timezone
from openpecha.core.ids import get_base_id
from openpecha.utils import load_yaml, dump_yaml
from openpecha.core.metadata import PechaMetadata, InitialCreationType

versions_dic = {
    "Derge": {
        "work_id": "bdr:W23703",
        "image_group_id": "1421",
        "total_pages": 79,
        "vol": 105, 
    },
    "Narthang": {
        "work_id": "bdr:W2KG5015",
        "image_group_id": "I2KG212398",
        "total_pages": 75,
        "vol": 114, 
    },
    "Peking": {
        "work_id": "bdr:W1KG13126",
        "image_group_id": "I1KG13283",
        "total_pages": 88,
        "vol": 114, 
    }
}


def create_export_text(type, pecha_path):
    base_paths = list(Path(f"{pecha_path}/{pecha_path.name}.opf/base").iterdir())
    for base_path in base_paths:
        base = base_path.read_text(encoding='utf-8')
        export_base = re.sub(r"\n"," ", base)
    Path(f"./export-lopenling/{type}/བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ་བཞུགས་སོ།.txt").write_text(export_base, encoding='utf-8')
    
    
def get_commits(pecha_path, token):
    pecha_id = pecha_path.name
    g = Github(token)
    repo = g.get_repo(f"Openpecha/{pecha_id}")
    for num, commit in enumerate(repo.get_commits(), 1):
        if num == 1:
            last_commit = commit._identity
        if num == 2:
            second_last_commit = commit._identity
    return last_commit, second_last_commit
        
def get_initial_date(pecha_path, token):
    pecha_id = pecha_path.name
    g = Github(token)
    repo = g.get_repo(f"Openpecha-Data/{pecha_id}")
    for commit in repo.get_commits():
        pass
    import_date = commit.raw_data['commit']['author']['date']
    return import_date
        
def get_source_metadata(type, base_dic):
    base = {}
    curr = {}
    for _, info in base_dic.items():
        new_base = info['new_base']
        curr = {
                'image_group_id': versions_dic[type]['image_group_id'],
                'title': "བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ་བཞུགས་སོ།",
                'total_pages': versions_dic[type]['total_pages'],
                'order': versions_dic[type]['vol'],
                'base_file': f'{new_base}.txt'
        }
        base[new_base]= curr
        curr ={}
    source_metadata = {
        "id": versions_dic[type]['work_id'],
        "base": base
    }
    return source_metadata


def update_meta(pecha_path, type, base_dic, token):
    meta_path = Path(f"{pecha_path}/{pecha_path.name}.opf/meta.yml")
    new_meta = PechaMetadata(
        id = pecha_path.name,
        source = "https://library.bdrc.io",
        source_file = None,
        initial_creation_type = InitialCreationType.input,
        imported = get_initial_date(pecha_path, token),
        last_modified = datetime.now(timezone.utc),
        parser = None,
        source_metadata = get_source_metadata(type,base_dic),
        statistics = {},
        quality = {},
        copyright = None,
        license = None
    )
    
    dump_yaml(json.loads(new_meta.json()), meta_path)

def rename_layers(layers_paths, base_dic):
    layers_paths.sort()
    for layer_path in layers_paths:
        layer_name = layer_path.name
        for _, info in base_dic.items():
            if layer_name == info['old_base']:
                new_base = info['new_base']
                break
        subprocess.run(f'cd {layer_path.parent}; git mv {layer_path.name} {new_base}', shell=True)


def rename_all_base(base_paths):
    curr ={}
    base_dic = {}
    base_paths.sort()
    for num, base_path in enumerate(base_paths,0):
        base_name = base_path.name[:-4]
        new_base_name = get_base_id()
        subprocess.run(f'cd {base_path.parent}; git mv {base_path.name} {new_base_name}.txt', shell=True)
        curr[num] = {
            'old_base': base_name,
            'new_base': new_base_name
        }
        base_dic.update(curr)
        curr = {}
    return base_dic
     
def update_base_name(pecha_path):
    base_paths = list(Path(f"{pecha_path}/{pecha_path.name}.opf/base/").iterdir())
    layers_paths = list(Path(f"{pecha_path}/{pecha_path.name}.opf/layers/").iterdir())
    base_dic = rename_all_base(base_paths)
    rename_layers(layers_paths, base_dic)
    return base_dic
        
        
if __name__ == "__main__":
    token = "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"
    commit_msg = "added the base in the meta"
    pecha_paths = list(Path(f"./Diplomatic_opf").iterdir())
    type = "Peking"
    for pecha_path in pecha_paths:
        base_dic = update_base_name(pecha_path)
        update_meta(pecha_path, type, base_dic, token)
        create_export_text(type, pecha_path)
    
            
            
            
            
# chojuk work 4dba7c9a808a4f5db389c2c9e4bc4b93