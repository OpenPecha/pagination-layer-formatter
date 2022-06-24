from pathlib import Path
from  openpecha import github_utils
from openpecha.core.ids import get_base_id

def pecha_publish(pecha_path):
    github_utils.github_publish(
        pecha_path,
        message="initial commit",
        not_includes=[],
        layers=[],
        org="Openpecha-Data",
        token="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"
    )

if __name__=='__main__':
    pecha_paths = list(Path(f"./Open-Edition/").iterdir())
    for pecha_path in pecha_paths:
        pecha_publish(pecha_path)
        print(f'published {pecha_path.stem}')


# D1793x