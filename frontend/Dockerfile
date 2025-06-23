# Utilisation de Node.js pour un projet React/Vue.js (modifie selon ta stack)
FROM node:18

# Définition du répertoire de travail
WORKDIR /app

# Copie d'abord les fichiers de dépendances
COPY package*.json ./

# Installation des dépendances
RUN npm install
# RUN npm install vue-i18n
# RUN npm install pinia
# RUN npm install chart.js
# RUN npm install axios
# RUN npm install vue-router@next
# RUN npm install chart.js

# Copie des fichiers du projet
COPY . .

# Construction du projet (modifie selon ta stack)
RUN npm run build

# Exposition du port
EXPOSE 3000

# Commande de lancement du frontend
CMD ["npm", "run", "dev"]