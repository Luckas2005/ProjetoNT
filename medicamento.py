from dados import buscar_interacao_pandas

class Medicamento:
    def __init__(self, nomes: list):
        # Normalização: letras minúsculas e remoção de espaços em branco [cite: 88]
        self.nomes = [nome.strip().lower() for nome in nomes if nome.strip()]

    def verificar_interacoes(self) -> list:
        """Cruza os medicamentos informados e busca alertas no banco de dados[cite: 57, 105]."""
        alertas = []
        n = len(self.nomes)
        
        # Compara todos os medicamentos informados entre si
        for i in range(n):
            for j in range(i + 1, n):
                med1 = self.nomes[i]
                med2 = self.nomes[j]
                
                alerta = buscar_interacao_pandas(med1, med2)
                if alerta:
                    alertas.append(f"ALERTA ({med1} + {med2}): {alerta}")
                    
        return alertas