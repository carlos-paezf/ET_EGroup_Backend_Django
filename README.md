# Entrevista Técnica - Backend

[![wakatime](https://wakatime.com/badge/user/8ef73281-6d0a-4758-af11-fd880ca3009c/project/2cf310ca-7bcb-4db2-94a5-522cbc29f757.svg)](https://wakatime.com/badge/user/8ef73281-6d0a-4758-af11-fd880ca3009c/project/2cf310ca-7bcb-4db2-94a5-522cbc29f757)

## Comando usados

1. Instalar requerimientos para el proyecto:

   ```txt
   $: pip install -r requirements.txt
   ```

2. Crear nuevo proyecto:

   ```txt
   $: django-admin startproject app
   ```

3. Crear módulo core para centralizar lógica:

   ```txt
   $: python manage.py startapp core
   ```

4. Instalar paquete Pillow para gestión de imágenes:

   ```txt
   $: python -m pip install Pillow
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
