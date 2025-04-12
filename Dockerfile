FROM python:3.9

# Crée et définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie le fichier des dépendances
COPY requirements.txt .

# Installe les dépendances Python
RUN pip install -r requirements.txt

# Copie tout le code de l'application
COPY . .

# Expose le port 8000 pour l'application
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]