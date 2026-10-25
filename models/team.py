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
            return False, {"reason": "invalid_index", "target_index": target_index}
        if target_index == self.active_index:
            return False, {"reason": "already_active", "target_index": target_index}
        if not self.members[target_index].is_alive():
            return False, {"reason": "is_dead", "target_index": target_index, "member_name": self.members[target_index].name}

        old_member = self.active_member
        self.active_index = target_index
        new_member = self.active_member
        return True, {
            "old_member": old_member,
            "new_member": new_member,
            "old_name": old_member.name,
            "new_name": new_member.name
        }

    def auto_switch_next_alive(self):
        """Alterna automaticamente para o proximo integrante vivo se o ativo for nocauteado."""
        if self.active_member.is_alive():
            return False, {"reason": "active_is_alive"}
        old_member = self.active_member
        for idx, member in enumerate(self.members):
            if member.is_alive():
                self.active_index = idx
                return True, {
                    "old_member": old_member,
                    "new_member": member,
                    "old_name": old_member.name,
                    "new_name": member.name
                }
        return False, {"reason": "no_alive_members"}
