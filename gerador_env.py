import os
import secrets

def gerar_secret_key():
    """Gera uma SECRET_KEY segura de 50 caracteres compatível com o Django."""
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(50))

def criar_arquivo_env():
    """Gera o arquivo .env com as configurações do Django e Supabase."""
    caminho_env = os.path.join(os.getcwd(), '.env')

    if os.path.exists(caminho_env):
        resposta = input("⚠️  O arquivo .env já existe. Deseja sobrescrevê-lo? (s/N): ").strip().lower()
        if resposta != 's':
            print("❌ Operação cancelada. O arquivo .env original foi mantido.")
            return

    secret_key = gerar_secret_key()

    conteudo_env = f"""# ==============================================================================
# CONFIGURAÇÕES SECRETAS DO DJANGO - ARMÁRIO INTELIGENTE
# ==============================================================================

# Segredo do Django (Nunca compartilhe ou envie para o GitHub)
SECRET_KEY='{secret_key}'

# Modo de Desenvolvimento (True para dev local, False para produção)
DEBUG=True

# Hosts Permitidos (Separados por vírgula)
ALLOWED_HOSTS=*

# ==============================================================================
# CONEXÃO COM O BANCO DE DADOS POSTGRESQL (SUPABASE)
# ==============================================================================
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=SUA_SENHA_DO_SUPABASE_AQUI
DB_HOST=[suspicious link removed]
DB_PORT=5432
DB_SSLMODE=require
"""

    with open(caminho_env, 'w', encoding='utf-8') as file:
        file.write(conteudo_env)

    print("✅ Arquivo .env gerado com sucesso na raiz do projeto!")
    print(f"🔑 SECRET_KEY gerada: {secret_key[:10]}... (mascarada)")
    print("👉 Lembre-se de substituir 'SUA_SENHA_DO_SUPABASE_AQUI' e '[suspicious link removed]' com os dados reais do seu projeto no Supabase.")

if __name__ == '__main__':
    criar_arquivo_env()