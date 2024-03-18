from langchain_core.prompts import PromptTemplate


template = """Вы помощник для задач по ответам на вопросы. Используйте следующие фрагменты извлеченного контекста, чтобы ответить на вопрос. Если вы не знаете ответа, просто скажите, что не знаете. Используйте не более трех предложений и сохраняйте ответ кратким.
Вопрос: {question} 
Контекст: {context} 
Ответ:
"""
# custom_rag_prompt = PromptTemplate.from_template(template)
custom_rag_prompt = PromptTemplate(
    template=template,
    input_variables=["question", "context"]
)
