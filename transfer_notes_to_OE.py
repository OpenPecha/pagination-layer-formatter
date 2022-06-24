from pathlib import Path
from openpecha.blupdate import PechaBaseUpdate


def transfer_layer(src_opf, trg_opf, src_base_name, trg_base_name):
    pecha_updater = PechaBaseUpdate(src_opf, trg_opf)
    pecha_updater.update_vol(src_base_name, trg_base_name)

if __name__ == "__main__":
    open_id = "O2FCA4A99"
    diplomatic_id = "I4190B39B"
    src_base_name =  "34D1"
    trg_base_name =  "6ABB"
    src_opf = Path(f"./Root-Commentary/{diplomatic_id}/{diplomatic_id}.opf/")
    trg_opf = Path(f"./{open_id}/{open_id}.opf/")
    transfer_layer(src_opf, trg_opf, src_base_name, trg_base_name)