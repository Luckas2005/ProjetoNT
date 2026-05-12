class Triagem:
    def __init__(self, sintomas: list):
        self.sintomas = sintomas # [cite: 53]

    def classificar_risco(self) -> str:
        """Classifica o risco baseado nos sintomas informados[cite: 56]."""
        sintomas_str = " ".join(self.sintomas).lower().strip()
        
        # Testes de unidade esperados da Fase 2 [cite: 114, 115]
        if "falta de ar" in sintomas_str or "dor no peito" in sintomas_str or "hemorragia" in sintomas_str:
            return "VERMELHO (Alto Risco)"
        elif "febre" in sintomas_str or "dor intensa" in sintomas_str:
            return "AMARELO (Risco Moderado)"
        elif sintomas_str == "":
            return "INVÁLIDO"
        else:
            return "VERDE (Baixo Risco)"