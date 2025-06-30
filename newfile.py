import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Calculadora de Média - Bruno Gaia", layout="centered")
st.title("📊 Calculadora de Média - Medicina UNIP | Bruno Gaia")

# Pesos
pesos = {"Tutoria": 3, "Teórica": 3, "Prática": 2, "AEP": 2}

# Entradas
st.markdown("### 📝 Digite suas notas (0 para as que ainda não foram feitas):")
notas = {}
for nome in pesos:
    notas[nome] = st.number_input(f"{nome} (peso {pesos[nome]})", min_value=0.0, max_value=10.0, step=0.1)

pendentes = [k for k in notas if notas[k] == 0.0]

if len(pendentes) != 2:
    st.warning("⚠️ Deixe exatamente 2 avaliações com nota 0 para ativar o cálculo.")
else:
    slider_nome = "Tutoria" if "Tutoria" in pendentes else pendentes[0]
    calculada_nome = [n for n in pendentes if n != slider_nome][0]

    st.markdown(f"### 🎚️ Controle a nota de **{slider_nome}**:")
    slider_valor = st.slider(f"Nota para {slider_nome}", 5.0, 10.0, 10.0, 0.1)
    notas[slider_nome] = slider_valor

    pontos = {n: notas[n] * pesos[n] / 10 for n in notas}
    total = sum(pontos.values())
    faltando = round(6.7 - total, 3)

    if faltando < 0 or faltando > pesos[calculada_nome]:
        st.error("❌ Sem solução com essa combinação.")
    else:
        nota_calc = round((faltando * 10) / pesos[calculada_nome], 2)
        notas[calculada_nome] = nota_calc
        st.success(f"✅ Para média 6.7, tire **{nota_calc}** em **{calculada_nome}**.")

        df_resultado = pd.DataFrame(list(notas.items()), columns=["Avaliação", "Nota"])
        st.markdown("### 📋 Notas atuais:")
        st.dataframe(df_resultado, use_container_width=True)

        # Combinações possíveis
        combinacoes = []
        for x in np.arange(0, 10.1, 0.1):
            for y in np.arange(0, 10.1, 0.1):
                temp = notas.copy()
                temp[slider_nome] = round(x, 1)
                temp[calculada_nome] = round(y, 1)
                pontos_temp = {n: temp[n] * pesos[n] / 10 for n in temp}
                if abs(sum(pontos_temp.values()) - 6.7) < 0.01:
                    combinacoes.append({slider_nome: x, calculada_nome: y})

        if combinacoes:
            df_combos = pd.DataFrame(combinacoes).drop_duplicates().sort_values(by=slider_nome, ascending=False).head(30)
            st.markdown("### 🧮 Primeiras 30 combinações possíveis:")
            st.dataframe(df_combos, use_container_width=True)

            # Gráfico
            x_vals = [c[slider_nome] for c in combinacoes]
            y_vals = [c[calculada_nome] for c in combinacoes]
            fig, ax = plt.subplots()
            ax.scatter(x_vals, y_vals, color='blue', s=10)
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_xticks(np.arange(0, 10.5, 1.0))
            ax.set_yticks(np.arange(0, 10.5, 1.0))
            ax.set_xticks(np.arange(0, 10.5, 0.5), minor=True)
            ax.set_yticks(np.arange(0, 10.5, 0.5), minor=True)
            ax.grid(True, which='major', linestyle='--')
            ax.grid(True, which='minor', linestyle=':', linewidth=0.5)
            ax.set_xlabel(slider_nome)
            ax.set_ylabel(calculada_nome)
            ax.set_title("🔵 Combinações para média 6.7")
            st.pyplot(fig)
        else:
            st.error("❌ Nenhuma combinação encontrada.")



