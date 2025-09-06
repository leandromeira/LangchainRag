from langchain_google_genai import ChatGoogleGenerativeAI
from search import search_prompt
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )
    
    user_input = input("Faça sua pergunta:\n\nPERGUNTA: ")

    # Criar chain: busca + prompt + modelo
    chain = search_prompt(user_input) | model

    # Invocar chain (não precisa passar parâmetros, pois a pergunta já está no chain)
    result = chain.invoke({})
    print("="*30) 
    print(f"RESPOSTA: {result.content}")


if __name__ == "__main__":
    main()