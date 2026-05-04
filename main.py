import requests
import time
import os
import sys
from datetime import datetime

class FinTrace:
    """
    FINTRACE // Terminal-based financial asset tracker.
    Developed by NathnF or (Galaxy).
    """
    def __init__(self):
        # Adicionei Ouro (XAU) e Ethereum (ETH) à sua API
        self.url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL,ETH-BRL,XAU-BRL"
        self.p = "\033[38;5;141m" 
        self.d = "\033[2m"        
        self.b = "\033[1m"        
        self.r = "\033[0m"        
        self.g = "\033[92m"       
        self.red = "\033[91m"     
        self.start_time = datetime.now().strftime('%H:%M:%S')

    def fetch_data(self):
        try:
            return requests.get(self.url, timeout=5).json()
        except:
            return None

    def render(self, data):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"{self.p}{self.b}/// FINTRACE_{self.r} {self.d}v1.1.0{self.r}")
        print(f"{self.d}————————————————————————————————————————————————————————————{self.r}")
        print(f"STATUS: {self.g}ACTIVE{self.r}  |  BASE: {self.p}BRL{self.r}  |  TIME: {datetime.now().strftime('%H:%M:%S')}")
        print(f"{self.d}————————————————————————————————————————————————————————————{self.r}\n")
        
        # Mapeamento expandido de ativos
        assets = [
            ("BITCOIN", data["BTCBRL"]),
            ("ETHEREUM", data["ETHBRL"]),
            ("OURO (g)", data["XAUBRL"]), # Preço do grama do ouro
            ("DOLAR", data["USDBRL"]),
            ("EURO", data["EURBRL"])
        ]

        print(f"   {self.d}IDENTIFIER      │      VALUE (BRL)      │      CHANGE{self.r}")
        print(f"   {self.d}————————————————│———————————————————————│————————————{self.r}")

        for name, info in assets:
            val = float(info['bid'])
            pct = float(info['pctChange'])
            c_color = self.g if pct >= 0 else self.red
            
            # Formatação inteligente para diferentes escalas de preço
            if val > 10000:
                v_str = f"{val:,.0f}"
            elif val > 100:
                v_str = f"{val:,.2f}"
            else:
                v_str = f"{val:,.2f}"

            print(f"   {self.b}{name:<13}{self.r} {self.d}│{self.r}  {v_str:>17}  {self.d}│{self.r}  {c_color}{pct:>+9}%{self.r}")

        print(f"\n{self.d}————————————————————————————————————————————————————————————{self.r}")
        print(f"   {self.p}>>{self.r} {self.d}Press CTRL+C to decouple session...{self.r}")

    def exit_gracefully(self):
        print(f"\n\n   {self.p}[SIGTERM]{self.r} {self.b}Severing FINTRACE connection...{self.r}")
        time.sleep(0.5)
        print(f"   {self.d}>> Session start: {self.start_time}{self.r}")
        print(f"   {self.d}>> Session end:   {datetime.now().strftime('%H:%M:%S')}{self.r}")
        print(f"   {self.d}>> Status: All nodes synchronized and logged.{self.r}")
        print(f"   {self.p}>> Goodbye.{self.r}\n")
        sys.exit(0)

    def start(self):
        try:
            while True:
                payload = self.fetch_data()
                if payload:
                    self.render(payload)
                time.sleep(15)
        except KeyboardInterrupt:
            self.exit_gracefully()

if __name__ == "__main__":
    app = FinTrace()
    app.start()