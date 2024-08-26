# Use a imagem base do Python
FROM python:3.10

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt /app/

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto
COPY . /app/

# Expõe a porta que o Django usará
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["python", "app/manage.py", "runserver", "0.0.0.0:8000"]
