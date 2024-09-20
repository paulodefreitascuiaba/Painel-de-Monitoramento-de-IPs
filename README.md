# README - Painel de Monitoramento de IPs

## Descrição

Este projeto é um painel de monitoramento de IPs desenvolvido em Python, utilizando a biblioteca Tkinter para a interface gráfica. O painel permite que os usuários monitorem o status de dispositivos em uma rede local, exibindo se estão online ou offline, juntamente com o tempo de resposta em milissegundos.

## Objetivo

O objetivo deste projeto é fornecer uma ferramenta simples e eficiente para administradores de rede que desejam acompanhar a conectividade de dispositivos em tempo real. Através deste painel, é possível verificar rapidamente o status de múltiplos dispositivos sem a necessidade de utilizar o terminal ou ferramentas externas.

## Requisitos

### Software Necessário

- **Python 3.x**: O código foi desenvolvido e testado em Python 3.x. Certifique-se de que a versão mais recente está instalada em seu sistema. Você pode baixar o Python em [python.org](https://www.python.org/downloads/).

### Bibliotecas Necessárias

As bibliotecas utilizadas são padrão do Python, portanto não é necessário instalar pacotes adicionais. As bibliotecas incluem:
- `tkinter`: Para criar a interface gráfica.
- `subprocess`: Para executar comandos do sistema.
- `json`: Para manipulação de arquivos JSON.

## Estrutura do Código

O código é organizado em várias funções e classes, cada uma responsável por uma parte específica da aplicação:

### 1. Importação de Módulos

O código começa com a importação das bibliotecas necessárias:

```python
import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import time
import json
2. Carregamento de Configurações
Os IPs e nomes dos dispositivos são carregados a partir de um arquivo JSON:

with open('config.json', 'r') as f:
    config = json.load(f)
3. Função check_ip
Esta função é responsável por verificar o status de um IP. Ela executa um comando de ping e atualiza o status do dispositivo:

def check_ip(ip, indicator):
    while True:
        try:
            response = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], stdout=subprocess.PIPE, text=True)
            if response.returncode == 0:
                ms_line = next((line for line in response.stdout.splitlines() if "tempo=" in line), None)
                if ms_line:
                    ms = ms_line.split("tempo=")[1].split("ms")[0].strip()
                    indicator.set_status("online", ms)
                else:
                    indicator.set_status("online", "N/A")
            else:
                indicator.set_status("offline", "N/A")
        except Exception:
            indicator.set_status("offline", "N/A")    
        time.sleep(5)  # Espera 5 segundos antes de verificar novamente
4. Classe StatusIndicator
Esta classe representa cada dispositivo a ser monitorado na interface gráfica. Ela exibe o nome do dispositivo, o IP, o tempo de resposta e o status (online/offline):

class StatusIndicator(tk.Frame):
    def __init__(self, master, ip, nome, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.ip = ip
        self.status = "offline"  # Status inicial
        self.ms = "N/A"
        self.configure(bg="#2C2F33", padx=3, pady=3, bd=1, relief="solid")
        ...
    
    def set_status(self, status, ms):
        self.status = status
        self.ms = ms
        self.ms_label.config(text=self.ms)
        if status == "online":
            self.status_label.config(bg="#28A745")  # Verde para online
        else:
            self.status_label.config(bg="#DC3545")  # Vermelho para offline
5. Função main
A função main configura a interface gráfica principal do aplicativo, define a aparência da janela e inicia as threads para monitorar cada IP:

def main():
    root = tk.Tk()
    root.title("Painel de Monitoramento de IPs")
    root.configure(bg="#1E2124")
    ...
    
    for i, item in enumerate(config["devices"]):
        nome = item["nome"]
        ip = item["ip"]
        indicator = StatusIndicator(indicators_frame, ip, nome)
        indicator.grid(row=i // col_count, column=i % col_count, padx=10, pady=5, sticky="ew")
        threading.Thread(target=check_ip, args=(ip, indicator), daemon=True).start()
6. Encerramento do Programa
O programa pode ser encerrado pressionando a tecla ESC, que chama a função de destruição da janela principal.

Configuração do Arquivo JSON
Para configurar o painel, é necessário criar um arquivo config.json no mesmo diretório do script. O formato do arquivo deve ser o seguinte:

{
  "devices": [
    { "nome": "SERVIDOR 1", "ip": "192.168.1.1" },
    { "nome": "SERVIDOR 2", "ip": "192.168.1.2" }
  ]
}
Você pode adicionar quantos dispositivos quiser, seguindo a mesma estrutura.

Como Executar o Programa
Salve o arquivo Python (por exemplo, monitoramento.py) e o arquivo config.json no mesmo diretório.

Abra o terminal ou prompt de comando.

Navegue até o diretório onde os arquivos estão salvos.

Execute o script usando o seguinte comando:

python monitoramento.py

Funcionalidades
Monitoramento em Tempo Real: O painel faz ping a cada 5 segundos para verificar o status dos dispositivos.
Atualização Visual: A interface gráfica é atualizada automaticamente para mostrar o status atual e o tempo de resposta.
Interface Intuitiva: Os dispositivos são exibidos de forma organizada, facilitando a visualização.
Contribuições
Se você deseja contribuir com o projeto, sinta-se à vontade para fazer melhorias ou correções. Crie um fork do repositório e envie suas alterações por meio de um pull request.

Licença
Este projeto é de código aberto. Você é livre para utilizar, modificar e distribuir o código, desde que forneça os devidos créditos.
