
# Utilisation de Python avec FastAPI
FROM python:3.12.7

# Définition du répertoire de travail
WORKDIR /app

# Copie d'abord les fichiers de dépendances pour profiter du cache Docker
COPY requirements.txt ./

# Installation des dépendances
RUN pip install -r requirements.txt

# Installation de netcat pour wait-for
RUN apt-get update && apt-get install -y netcat-openbsd

# Ajout du script wait-for
ADD https://raw.githubusercontent.com/eficode/wait-for/master/wait-for /wait-for
RUN chmod +x /wait-for

# Copie des fichiers de l'application
COPY . .

# Exposition du port
EXPOSE 8084

# Commande de lancement du backend
CMD ["/wait-for", "db_ch:5432", "--timeout=60", "--", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8084"]