from pathlib import Path
from openpecha import github_utils





def pecha_publish(pecha_path):
    github_utils.github_publish(
        pecha_path,
        message="initial commit",
        not_includes=[],
        layers=[],
        org="Openpecha-Data",
        token="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"
    )
    
if __name__ == "__main__":
    pecha_paths = list(Path(f"./Diplomatic_opf/").iterdir())
    for pecha_path in pecha_paths:
       pecha_publish(pecha_path)