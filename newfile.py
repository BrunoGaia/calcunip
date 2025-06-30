import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Calculadora de Média - Bruno Gaia", layout="centered")
st.title("📊 Calculadora de Média - Medicina UNIP | Bruno Gaia")

# Pesos das avaliações
pesos = {"Tutoria": 3, "Teórica": 3, "Prática": 2, "AEP": 2}

# Entradas de nota
st.markdown("### 📝 Digite suas notas (0 para as que ainda não foram feitas):")
notas = {}
for nome in pesos:
    notas[nome] = st.number_input(f"{nome} (peso {pesos[nome]})", min_value=0.0, max_value=10.0, step=0.1)

# Identificar avaliações ainda não feitas
pendentes = [k for k in notas if notas[k] == 0.0]

if len(pendentes) != 2:
    st.warning("⚠️ Deixe exatamente 2 avaliações com nota 0 para gerar combinações.")
else:
    aval1, aval2 = pendentes
    combinacoes = []
    for x in np.arange(0, 10.1, 0.1):
        for y in np.arange(0, 10.1, 0.1):
            notas_testadas = notas.copy()
            notas_testadas[aval1] = round(x, 1)
            notas_testadas[aval2] = round(y, 1)

            pontos = {n: notas_testadas[n] * pesos[n] / 10 for n in notas_testadas}
            total = round(sum(pontos.values()), 2)

            if abs(total - 6.7) < 0.01:
                combinacoes.append({aval1: round(x, 1), aval2: round(y, 1)})

    if combinacoes:
        st.success(f"✅ {len(combinacoes)} combinações encontradas que resultam em média 6.7.")

        # Mostrar tabela com as 20 primeiras
        df_resultado = pd.DataFrame(combinacoes).drop_duplicates().head(20)
        st.markdown("### 📋 Primeiras combinações possíveis:")
        st.dataframe(df_resultado, use_container_width=True)

        # Gráfico com todos os pontos válidos
        x_vals = [d[aval1] for d in combinacoes]
        y_vals = [d[aval2] for d in combinacoes]
        fig, ax = plt.subplots()
        ax.scatter(x_vals, y_vals, color='blue', s=10)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_xlabel(aval1)
        ax.set_ylabel(aval2)
        ax.set_title("🔵 Combinações para média 6.7")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.error("❌ Nenhuma combinação encontrada para média 6.7. Verifique suas outras notas.")

