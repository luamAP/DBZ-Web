class Team:
    """Gerencia composicao, estado e trocas de uma equipe de combate (Tag Team)."""
    def __init__(self, name, members):
        if not members:
            raise ValueError("Uma equipe deve possuir ao menos um integrante.")
        self.name = name
        self.members = list(members)
        self.active_index = 0

    @property
    def active_member(self):
        return self.members[self.active_index]

    def has_alive_members(self):
        return any(m.is_alive() for m in self.members)

    def get_bench_members(self):
        """Retorna tuplas (indice_original, membro) de lutadores vivos na reserva."""
        return [
            (idx, m) for idx, m in enumerate(self.members)
            if idx != self.active_index and m.is_alive()
        ]

    def switch_member(self, target_index):
        if target_index < 0 or target_index >= len(self.members):
            return False, "Indice de lutador invalido."
        if target_index == self.active_index:
            return False, "Este lutador ja esta em combate!"
        if not self.members[target_index].is_alive():
            return False, "Nao e possivel selecionar um combatente derrotado!"

        old_member = self.active_member
        self.active_index = target_index
        new_member = self.active_member
        return True, f"Troca realizada! {old_member.name} recua e {new_member.name} assume a arena!"

    def auto_switch_next_alive(self):
        """Alterna automaticamente para o proximo integrante vivo se o ativo for nocauteado."""
        if self.active_member.is_alive():
            return False
        for idx, member in enumerate(self.members):
            if member.is_alive():
                self.active_index = idx
                return True
        return False
