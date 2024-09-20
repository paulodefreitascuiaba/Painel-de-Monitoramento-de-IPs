import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import time
import json

# Carregando os IPs e nomes a partir de um arquivo JSON
with open('config.json', 'r') as f:
    config = json.load(f)

# Função para verificar o status de um IP e tempo de resposta
def check_ip(ip, indicator):
    while True:
        try:
            # Comando ping com timeout de 1 segundo e apenas 1 pacote enviado
            response = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], stdout=subprocess.PIPE, text=True)
            if response.returncode == 0:
                # Extrai o tempo de resposta em milissegundos
                ms_line = next((line for line in response.stdout.splitlines() if "tempo=" in line), None)
                if ms_line:
                    ms = ms_line.split("tempo=")[1].split("ms")[0].strip()
                    indicator.set_status("online", ms)
                else:
                    indicator.set_status("online", "N/A")
            else:
                indicator.set_status("offline", "N/A")
        except Exception:
            indicator.set_status("offline", "N/A")    # Caso haja erro, considera como offline
        time.sleep(5)  # Espera 5 segundos antes de verificar novamente

# Classe para o indicador de status visual
class StatusIndicator(tk.Frame):
    def __init__(self, master, ip, nome, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.ip = ip
        self.status = "offline"  # Status inicial
        self.ms = "N/A"
        self.configure(bg="#2C2F33", padx=3, pady=3, bd=1, relief="solid")

        # Label do Nome
        self.name_label = tk.Label(self, text=nome, font=("Arial", 12), fg="white", bg="#2C2F33", width=17, anchor="w")
        self.name_label.grid(row=0, column=0, padx=(5, 10))

        # Label do IP
        self.label = tk.Label(self, text=ip, font=("Arial", 12), fg="white", bg="#2C2F33", width=13, anchor="w")
        self.label.grid(row=0, column=1, padx=(5, 10))

        # Label do tempo de resposta em ms
        self.ms_label = tk.Label(self, text=self.ms, font=("Arial", 12), fg="white", bg="#2C2F33", width=5)
        self.ms_label.grid(row=0, column=2, padx=(5, 10))

        # Indicador de status
        self.status_label = tk.Label(self, width=2, height=1, bg="red")
        self.status_label.grid(row=0, column=3, padx=(5, 10))

    def set_status(self, status, ms):
        self.status = status
        self.ms = ms
        # Atualiza a cor imediatamente para online (verde) ou offline (vermelho) e atualiza o ms
        self.ms_label.config(text=self.ms)
        if status == "online":
            self.status_label.config(bg="#28A745")  # Verde para online
        else:
            self.status_label.config(bg="#DC3545")  # Vermelho para offline

# Função principal para configurar a interface
def main():
    root = tk.Tk()
    root.title("Painel de Monitoramento de IPs")
    root.configure(bg="#1E2124")

    # Variável para controlar o modo tela cheia
    fullscreen = False

    # Função para alternar entre modo tela cheia e janela normal
    def toggle_fullscreen(event=None):
        nonlocal fullscreen
        fullscreen = not fullscreen
        root.attributes("-fullscreen", fullscreen)

    # Exibe a janela maximizada, mas com barra de título
    root.state('zoomed')
    root.bind("<F>", toggle_fullscreen)  # Pressione "F" para alternar o modo tela cheia

    # Estilo
    style = ttk.Style()
    style.configure("TLabel", background="#1E2124", foreground="white", font=("Arial", 12))

    header = tk.Label(root, text="Monitoramento de IPs", font=("Arial", 18, "bold"), bg="#1E2124", fg="white")
    header.pack(pady=20)

    # Frame para os indicadores de status organizados em 3 colunas
    indicators_frame = tk.Frame(root, bg="#1E2124")
    indicators_frame.pack(fill="both", expand=True, padx=20)

    # Cria StatusIndicators para cada IP e nome, organizados em 3 colunas
    col_count = 3
    for i, item in enumerate(config["devices"]):
        nome = item["nome"]
        ip = item["ip"]
        indicator = StatusIndicator(indicators_frame, ip, nome)
        indicator.grid(row=i // col_count, column=i % col_count, padx=10, pady=5, sticky="ew")
        threading.Thread(target=check_ip, args=(ip, indicator), daemon=True).start()

    # Fecha o programa ao pressionar ESC
    root.bind("<Escape>", lambda e: root.destroy())

    root.mainloop()

if __name__ == "__main__":
    main()
