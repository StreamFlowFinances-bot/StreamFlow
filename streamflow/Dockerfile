FROM python:3.10-slim

# Setează folderul de lucru
WORKDIR /app

# Copiază fișierul de dependențe
COPY requirements.txt .

# Instalează bibliotecile necesare
RUN pip install --no-cache-dir -r requirements.txt

# Copiază tot restul codului
COPY . .

# Expune portul pe care îl folosește Render
EXPOSE 10000

# Comanda de start
CMD ["python", "main.py"]
