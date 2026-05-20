from dados import buscar_interacao_pandas
import re

class Medicamento:
    def __init__(self, nomes: list):
        # Limpeza e normalização de dados: conversão para minúsculas e remoção de espaços [cite: 88]
        self.nomes = [nome.strip().lower() for nome in nomes if nome.strip()]

    def validar_entrada(self) -> bool:
        """Valida se há caracteres não permitidos nas strings de medicamentos[cite: 89]."""
        texto_completo = " ".join(self.nomes)
        if re.search(r'[^a-zA-Z0-9\sãáàâéêíóôõúç-]', texto_completo, re.IGNORECASE):
            return False
        return True

    def verificar_interacoes(self) -> list:
        """Cruza os medicamentos no banco de dados e retorna alertas[cite: 14, 111]."""
        if not self.validar_entrada():
            return ["ERRO_VALIDACAO"]

        alertas = []
        n = len(self.nomes)
        
        for i in range(n):
            for j in range(i + 1, n):
                med1 = self.nomes[i]
                med2 = self.nomes[j]
                
                alerta = buscar_interacao_pandas(med1, med2)
                if alerta:
                    alertas.append(f"({med1} + {med2}): {alerta}")
                    
        return alertas