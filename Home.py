import streamlit as st
from datetime import datetime, timedelta
from utils import get_recommendations

def display_casa_repouso_fields():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Data de entrada", min_value=datetime.today())
    with col2:
        indefinite_stay = st.checkbox("Tempo indeterminado")
        if not indefinite_stay:
            duration = st.number_input("Duração da estadia (em dias)", min_value=1, value=30)
            end_date = start_date + timedelta(days=duration)
            st.info(f"Data de saída prevista: {end_date.strftime('%d/%m/%Y')}")
        else:
            end_date = None
            st.info("Estadia por tempo indeterminado")
    
    special_needs = st.multiselect("Necessidades especiais", 
                                   ["Alzheimer", "Parkinson", "Mobilidade reduzida", "Diabetes", "Hipertensão"])
    level_of_care = st.select_slider("Nível de cuidado necessário", 
                                     options=["Básico", "Intermediário", "Avançado"])
    amenities = st.multiselect("Comodidades desejadas", 
                               ["Jardim", "Atividades recreativas", "Fisioterapia", "Terapia ocupacional", "Nutricionista"])
    return start_date, end_date, special_needs, level_of_care, amenities

def display_cuidador_fields():
    frequency = st.selectbox("Frequência do cuidado", 
                             ["Diário", "Semanal", "Quinzenal", "Mensal", "Sob demanda"])
    hours_per_day = st.number_input("Horas por dia", min_value=1, max_value=24, value=8)
    start_date = st.date_input("Data de início", min_value=datetime.today())
    duration = st.number_input("Duração do contrato (em dias)", min_value=1, value=30)
    end_date = start_date + timedelta(days=duration)
    st.info(f"Data final do contrato: {end_date.strftime('%d/%m/%Y')}")
    
    special_skills = st.multiselect("Habilidades especiais necessárias", 
                                    ["Primeiros socorros", "Cuidados com Alzheimer", "Fisioterapia básica", "Cuidados paliativos"])
    return frequency, hours_per_day, start_date, end_date, special_skills

def main():
    st.set_page_config(page_title="Care Next: Encontre Cuidados para Idosos", layout="wide")

    st.title("🏡 Care Next: Encontre o Melhor Cuidado para Idosos")
    st.write("Selecione o tipo de cuidado e preencha os campos específicos para encontrar as melhores opções.")

    location = st.text_input("Onde", placeholder="Cidade ou região")
    care_type = st.selectbox("Tipo de cuidado", ["", "Casa de Repouso", "Cuidador Domiciliar"])

    if care_type:
        if care_type == "Casa de Repouso":
            start_date, end_date, special_needs, level_of_care, amenities = display_casa_repouso_fields()
        else:  # Cuidador Domiciliar
            frequency, hours_per_day, start_date, end_date, special_skills = display_cuidador_fields()

        if st.button('Buscar Recomendações', use_container_width=True):
            if not location:
                st.warning("Por favor, informe a localização desejada.")
            else:
                with st.spinner("Buscando as melhores opções para você..."):
                    if care_type == "Casa de Repouso":
                        results = get_recommendations(location, care_type, start_date, end_date, special_needs, level_of_care, amenities)
                    else:  # Cuidador Domiciliar
                        results = get_recommendations(location, care_type, start_date, end_date, special_skills, frequency, hours_per_day)
                
                st.subheader("Recomendações Personalizadas")
                for result in results:
                    with st.expander(f"{result['name']} - {result['location']}"):
                        st.write(f"**Descrição:** {result['description']}")

if __name__ == '__main__':
    main()




    ## decidi que nao vou usar base de dados coisa nenhuma, vou pedir pro chatgpt gerar ao vivo ali 5 recomendações aleatórias de acordo com o que a pessoa precisa 