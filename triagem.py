import re

class Triagem:
    def __init__(self, sintomas: list):
        self.sintomas = sintomas

    def validar_entrada(self, texto: str) -> bool:
        """Bloqueia caracteres especiais e valida a entrada[cite: 89]."""
        # Permite apenas letras (incluindo acentos), números, espaços e vírgulas
        if re.search(r'[^a-zA-Z0-9\s,ãáàâéêíóôõúç]', texto, re.IGNORECASE):
            return False
        return True

    def classificar_risco(self) -> str:
        """Retorna o nível de urgência baseado nos sintomas informados[cite: 109, 110]."""
        sintomas_str = " ".join(self.sintomas).lower().strip()
        
        if not self.validar_entrada(sintomas_str):
            return "ERRO_VALIDACAO"

        # Lógica de classificação baseada nos testes de aceitação [cite: 114, 115]
        if "falta de ar" in sintomas_str or "dor no peito" in sintomas_str or "hemorragia" in sintomas_str:
            return "VERMELHO (Alto Risco)"
        elif "febre" in sintomas_str or "dor intensa" in sintomas_str:
            return "AMARELO (Risco Moderado)"
        elif not sintomas_str:
            return "INVÁLIDO"
        else:
            return "VERDE (Baixo Risco)"