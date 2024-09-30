import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

def get_recommendations(location, care_type, start_date, end_date, special_needs, level_of_care, amenities, openai_api_key):
    if not openai_api_key:
        st.error("Please enter an OpenAI API key to proceed.")
        return []

    llm = ChatOpenAI(model="gpt-4o", api_key=openai_api_key)
    
    prompt = PromptTemplate.from_template("""
    Com base nos seguintes critérios, gere 3 recomendações fictícias de cuidados para idosos:

    - Localização: {location}
    - Tipo de cuidado: {care_type}
    - Data de início: {start_date}
    - Data de término: {end_date}
    - Necessidades especiais: {special_needs}
    - Nível de cuidado: {level_of_care}
    - Comodidades desejadas: {amenities}

    Para cada recomendação, forneça:
    1. Nome do local ou serviço
    2. Localização específica
    3. Breve descrição dos serviços (2-3 frases)

    Formato da resposta:
    Nome: [Nome do local]
    Localização: [Localização específica]
    Descrição: [Breve descrição]

    ---
    """)

    query = prompt.format(
        location=location,
        care_type=care_type,
        start_date=start_date.strftime('%d/%m/%Y'),
        end_date=end_date.strftime('%d/%m/%Y') if end_date else "Tempo indeterminado",
        special_needs=', '.join(special_needs) if special_needs else 'Nenhuma específica',
        level_of_care=level_of_care,
        amenities=', '.join(amenities) if amenities else 'Nenhuma específica'
    )

    response = llm.predict(query)
    
    recommendations = []
    for rec in response.split('---'):
        if rec.strip():
            lines = rec.strip().split('\n')
            recommendations.append({
                'name': lines[0].split(': ', 1)[1] if len(lines) > 0 else 'Nome não especificado',
                'location': lines[1].split(': ', 1)[1] if len(lines) > 1 else 'Localização não especificada',
                'description': lines[2].split(': ', 1)[1] if len(lines) > 2 else 'Descrição não fornecida'
            })
    
    return recommendations