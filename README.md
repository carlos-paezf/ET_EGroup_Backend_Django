# Entrevista Técnica - Backend

[![wakatime](https://wakatime.com/badge/user/8ef73281-6d0a-4758-af11-fd880ca3009c/project/2cf310ca-7bcb-4db2-94a5-522cbc29f757.svg)](https://wakatime.com/badge/user/8ef73281-6d0a-4758-af11-fd880ca3009c/project/2cf310ca-7bcb-4db2-94a5-522cbc29f757)

## Comando usados

1. Instalar requerimientos para el proyecto:

   ```txt
   $: pip install -r requirements.txt
   ```

2. Levantar contenedor con la base de datos:

   ```txt
   $: docker-compose up -d
   ```

3. Crear nuevo proyecto:

   ```txt
   $: django-admin startproject app
   ```

4. Crear módulo core para centralizar lógica:

   ```txt
   $: python manage.py startapp core
   ```

5. Generar y correr migraciones para modelos definidos en el core:

   ```txt
   $: python manage.py makemigrations core
   ```

   ```txt
   $: python manage.py migrate
   ```

6. Ejecución de test:

   ```txt
   $: python manage.py test
   ```

7. Crear app de usuarios

   ```txt
   $: python manage.py startapp user
   ```

8. Ejecutar proyecto:

   ```txt
   $: python manage.py runserver
   ```
