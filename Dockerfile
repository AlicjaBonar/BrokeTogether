# Wersja stabilna Pythona (nie beta!)
FROM python:3.11-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie pliku z zależnościami
COPY requirements.txt .

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie całej aplikacji do kontenera
COPY . .

# Domyślna komenda startująca serwer
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
