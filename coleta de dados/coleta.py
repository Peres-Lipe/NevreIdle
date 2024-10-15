import psutil
import time
import requests
import json
import platform

# URL da sua API no backend
API_URL = "http://your-backend-api-url.com/api/metrics"

# Função para coletar métricas de CPU, Memória e Disco
def collect_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)  # Uso de CPU em %
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.used / 1024 / 1024  # Uso de memória em MB
    disk_usage = psutil.disk_usage('/').percent   # Uso de disco em %

    # Outras informações úteis (opcional)
    system_info = {
        "os": platform.system(),
        "hostname": platform.node(),
        "cpu_cores": psutil.cpu_count(logical=True),
    }

    # Dados de métricas
    metrics = {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "system_info": system_info,
        "timestamp": int(time.time())  # Timestamp atual
    }

    return metrics

# Função para enviar as métricas para a API do backend
def send_metrics(metrics):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(API_URL, data=json.dumps(metrics), headers=headers)
        if response.status_code == 201:
            print("Métricas enviadas com sucesso!")
        else:
            print(f"Erro ao enviar métricas: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")

# Função principal para executar a coleta e envio em loop
def main():
    while True:
        metrics = collect_metrics()
        print("Métricas coletadas:", metrics)  # Opcional: apenas para ver as métricas coletadas no terminal
        send_metrics(metrics)
        time.sleep(10)  # Intervalo de 10 segundos entre coletas

if __name__ == "__main__":
    main()
