FROM python:3.12-slim

# Fijar el directorio de trabajo
WORKDIR /app

# Copia todos los archivos al contenedor
COPY . /app

# Avoid writing .pyc files to the container's filesystem
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure that Python logs output directly (no buffering)
ENV PYTHONUNBUFFERED=1

# Copiar los requirements e instalamos las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto con el cual nos comunicaremos con la maquina a través de la API
EXPOSE 5000

ENV PYTHONPATH="${PYTHONPATH}:/app"

# Override CMD to run your custom script
CMD ["python", "-m", "api.run"]