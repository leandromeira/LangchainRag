from langchain_google_genai import ChatGoogleGenerativeAI
from search import search_prompt
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    print("=== CHAT RAG - Sistema de Perguntas e Respostas ===")
    print("Digite 'sair', 'quit' ou 'exit' para encerrar o chat\n")
    
    # Inicializar o modelo uma única vez
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )
    print("✓ Modelo carregado com sucesso!\n")
    
    # Loop principal do chat
    while True:
        try:
            # Obter pergunta do usuário
            user_input = input("PERGUNTA: ").strip()
            
            # Verificar comandos de saída
            if user_input.lower() in ['sair', 'quit', 'exit', 'q']:
                print("\n👋 Encerrando o chat. Até logo!")
                break
            
            # Verificar se a pergunta não está vazia
            if not user_input:
                print("⚠️  Por favor, digite uma pergunta válida.\n")
                continue
            
            print(f"\n🔍 Processando sua pergunta...")
            
            # Criar chain: busca + prompt + modelo
            chain = search_prompt(user_input) | model

            # Invocar chain
            result = chain.invoke({})
            
            # Exibir resposta
            print("="*60)
            print(f"RESPOSTA: {result.content}")
            print("="*60)
            print()  # Linha em branco para separar as conversas
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrompido. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            print("Tente novamente com uma pergunta diferente.\n")


if __name__ == "__main__":
    main()
