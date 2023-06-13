FROM mcr.microsoft.com/playwright/python:v1.34.0-jammy

LABEL application=win-patch-download

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the default command to the script with no additional arguments
ENTRYPOINT ["python", "win-patch-download.py"]

# Set the default argument(s) for the script
CMD []