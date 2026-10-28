import os
import yaml


def _get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))


def load_characters_data():
    """Carrega o catálogo de combatentes e mecânicas defensivas a partir de characters.yml."""
    file_path = os.path.join(_get_base_dir(), 'characters.yml')
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_items_data():
    """Carrega o catálogo de equipamentos e consumíveis a partir de items.yml."""
    file_path = os.path.join(_get_base_dir(), 'items.yml')
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_campaign_data():
    """Carrega as configurações de campanhas e fases a partir de campaign.yml."""
    file_path = os.path.join(_get_base_dir(), 'campaign.yml')
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def create_initial_inventory(consumables_cfg):
    """Cria um dicionário de inventário inicial com base nas quantidades padrão configuradas."""
    return {
        item_id: item_data.get('default_quantity', 1)
        for item_id, item_data in consumables_cfg.items()
    }
