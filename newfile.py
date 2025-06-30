import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculadora de Média", layout="centered")
st.title("📊 Calculadora de Média - Medicina UNIP | Bruno Gaia")

# Pesos das avaliações
pesos = {"Tutoria": 3, "Teórica": 3, "Prática": 2, "EAP": 2}

# Entradas de nota
st.markdown("### 📝 Digite suas notas (0 para as que ainda não foram feitas):")
notas = {}
for nome in pesos:
    notas[nome] = st.number_input(f"{nome} (peso {pesos[nome]})", min_value=0.0, max_value=10.0, step=0.1)

# Identificar avaliações ainda não feitas
pendentes = [k for k in notas if notas[k] == 0.0]

if len(pendentes) != 2:
    st.warning("⚠️ Deixe exatamente 2 avaliações com nota 0 para o cálculo funcionar.")
else:
    slider_nome = pendentes[0]
    calculada_nome = pendentes[1]

    st.markdown(f"### 🎚️ Escolha uma nota para **{slider_nome}**:")
    slider_valor = st.slider(f"Nota para {slider_nome}", min_value=5.0, max_value=10.0, value=7.0, step=0.1)
    notas[slider_nome] = slider_valor

    # Calcular pontos totais
    pontos = {n: notas[n] * pesos[n] / 10 for n in notas}
    total = sum(pontos.values())
    faltando = round(6.7 - total, 3)

    if faltando < 0 or faltando > pesos[calculada_nome]:
        st.error("❌ Sem solução com essa combinação. Tente outra nota.")
    else:
        nota_calc = round((faltando * 10) / pesos[calculada_nome], 2)
        notas[calculada_nome] = nota_calc

        st.success(f"✅ Para média 6.7, você deve tirar **{nota_calc}** em **{calculada_nome}**.")

        # Tabela
        df_resultado = pd.DataFrame(list(notas.items()), columns=["Avaliação", "Nota"])
        st.markdown("### 📋 Notas calculadas:")
        st.dataframe(df_resultado, use_container_width=True)

        # Gráfico
        fig, ax = plt.subplots()
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_xlabel(slider_nome)
        ax.set_ylabel(calculada_nome)
        ax.set_title("🎯 Combinação para média 6.7")
        ax.grid(True)
        ax.scatter(notas[slider_nome], nota_calc, color='blue')
        st.pyplot(fig)
