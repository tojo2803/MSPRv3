FROM nginx:latest

# Copie de la configuration vers le dossier Nginx
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]