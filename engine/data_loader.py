import os
import json
import yaml


def _get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _get_data_dir():
    return os.path.join(_get_project_root(), 'data')


def load_characters_data():
    """Carrega o catálogo de combatentes e mecânicas defensivas a partir de data/characters.yml."""
    file_path = os.path.join(_get_data_dir(), 'characters.yml')
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_items_data():
    """Carrega o catálogo de equipamentos e consumíveis a partir de data/items.yml."""
    file_path = os.path.join(_get_data_dir(), 'items.yml')
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_campaign_data():
    """Carrega as configurações de campanhas e fases a partir de data/campaign.yml."""
    file_path = os.path.join(_get_data_dir(), 'campaign.yml')
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def create_initial_inventory(consumables_cfg):
    """Cria um dicionário de inventário inicial com base nas quantidades padrão configuradas."""
    return {
        item_id: item_data.get('default_quantity', 1)
        for item_id, item_data in consumables_cfg.items()
    }


def save_game_state(save_data, filename="save.json"):
    """Salva o estado do jogo em JSON. Retorna (bool, dict)."""
    file_path = filename if os.path.isabs(filename) else os.path.join(_get_project_root(), filename)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        return True, {"filename": filename, "file_path": file_path}
    except Exception as e:
        return False, {"reason": "io_error", "msg": str(e)}


def load_game_state(filename="save.json"):
    """Carrega o estado do jogo a partir de save.json. Retorna (dict or None, dict)."""
    file_path = filename if os.path.isabs(filename) else os.path.join(_get_project_root(), filename)
    if not os.path.isfile(file_path):
        return None, {"reason": "file_not_found", "filename": filename}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data, {"filename": filename}
    except json.JSONDecodeError as e:
        return None, {"reason": "corrupted_file", "msg": str(e)}
    except Exception as e:
        return None, {"reason": "io_error", "msg": str(e)}
