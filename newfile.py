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
    st.warning("⚠️ Deixe exatamente 2 avaliações com nota 0 para ativar o cálculo.")
else:
    # Priorizar Tutoria como controle de slider se estiver entre os pendentes
    if "Tutoria" in pendentes:
        slider_nome = "Tutoria"
        calculada_nome = [n for n in pendentes if n != "Tutoria"][0]
    else:
        slider_nome, calculada_nome = pendentes

    st.markdown(f"### 🎚️ Controle a nota de **{slider_nome}**:")
    slider_valor = st.slider(f"Nota para {slider_nome}", min_value=5.0, max_value=10.0, value=10.0, step=0.1)
    notas[slider_nome] = slider_valor

    # Calcular nota necessária na outra avaliação
    pontos = {n: notas[n] * pesos[n] / 10 for n in notas}
    total = sum(pontos.values())
    faltando = round(6.7 - total, 3)

    if faltando < 0 or faltando > pesos[calculada_nome]:
        st.error("❌ Sem solução com essa combinação. Tente outro valor no slider.")
    else:
        nota_calc = round((faltando * 10) / pesos[calculada_nome], 2)
        notas[calculada_nome] = nota_calc

        st.success(f"✅ Para média 6.7, você deve tirar **{nota_calc}** em **{calculada_nome}**.")

        # Mostrar tabela com notas atuais
        df_resultado = pd.DataFrame(list(notas.items()), columns=["Avaliação", "Nota"])
        st.markdown("### 📋 Notas atuais:")
        st.dataframe(df_resultado, use_container_width=True)

        # Gerar todas as combinações possíveis fixas para gráfico
        combinacoes = []
        for x in np.arange(0, 10.1, 0.1):
            for y in np.arange(0, 10.1, 0.1):
                temp_notas = notas.copy()
                temp_notas[slider_nome] = round(x, 1)
                temp_notas[calculada_nome] = round(y, 1)

                pontos_temp = {n: temp_notas[n] * pesos[n] / 10 for n in temp_notas}
                total_temp = round(sum(pontos_temp.values()), 2)

                if abs(total_temp - 6.7) < 0.01:
                    combinacoes.append({slider_nome: round(x, 1), calculada_nome: round(y, 1)})

        if combinacoes:
            df_combos = pd.DataFrame(combinacoes).drop_duplicates().sort_values(by=slider_nome, ascending=False).head(30)
            st.markdown("### 🧮 Primeiras 30 combinações possíveis (fixas):")
            st.dataframe(df_combos, use_container_width=True)

            # Gráfico com os pontos com escala 0.5
            x_vals = [d[slider_nome] for d in combinacoes]
            y_vals = [d[calculada_nome] for d in combinacoes]
            fig, ax = plt.subplots()
            ax.scatter(x_vals, y_vals, color='blue', s=10)
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_xticks(np.arange(0, 10.5, 0.5))
            ax.set_yticks(np.arange(0, 10.5, 0.5))
            ax.set_xlabel(slider_nome)
            ax.set_ylabel(calculada_nome)
            ax.set_title("🔵 Combinações possíveis para média 6.7")
            ax.grid(True)
            st.pyplot(fig)
        else:
            st.error("❌ Nenhuma combinação possível para média 6.7 com as notas fornecidas.")



