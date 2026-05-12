import pandas as pd

# Dicionário de dados simulados conforme definido no escopo [cite: 85, 86]
dados_simulados = [
    {"med1": "ibuprofeno", "med2": "varfarina", "alerta": "Risco de sangramento crasso. Encaminhar para avaliação médica."},
    {"med1": "paracetamol", "med2": "alcool", "alerta": "Risco de toxicidade hepática grave."},
    {"med1": "omeprazol", "med2": "clopidogrel", "alerta": "Redução da eficácia do clopidogrel. Risco cardiovascular."}
]

# Transformando o dicionário em um DataFrame Pandas para tratamento e consulta [cite: 105]
df_interacoes = pd.DataFrame(dados_simulados)

def buscar_interacao_pandas(med1: str, med2: str) -> str:
    """Busca interações entre dois medicamentos usando Pandas."""
    # Máscara para buscar a combinação de medicamentos em qualquer ordem
    mascara = ((df_interacoes['med1'] == med1) & (df_interacoes['med2'] == med2)) | \
              ((df_interacoes['med1'] == med2) & (df_interacoes['med2'] == med1))
    
    resultado = df_interacoes[mascara]
    
    if not resultado.empty:
        return resultado.iloc[0]['alerta']
    return ""