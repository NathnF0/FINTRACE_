from flask import Flask, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

def get_financial_data():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL,ETH-BRL,XAU-BRL"
    try:
        response = requests.get(url, timeout=5).json()
        assets = []
        names = {"USDBRL": "DÓLAR", "EURBRL": "EURO", "BTCBRL": "BITCOIN", "ETHBRL": "ETHEREUM", "XAUBRL": "OURO (g)"}
        
        for key, item in response.items():
            val = float(item['bid'])
            pct = float(item['pctChange'])
            assets.append({
                "name": names.get(key, item['name'].split('/')[0].upper()),
                "val": f"{val:,.2f}" if val < 10000 else f"{val:,.0f}",
                "pct": f"{pct:+.2f}%",
                "is_up": pct >= 0
            })
        return assets, datetime.now().strftime('%H:%M:%S')
    except:
        return [], "--:--:--"

# --- DESIGN PREMIUM V2 (COM INDICADORES LIVE) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="30"> <!-- AUTO-REFRESH A CADA 30s -->
    <title>FINTRACE // Market Telemetry</title>
    <style>
        :root {
            --bg: #0a0a0b;
            --card: #141416;
            --accent: #8e44ad;
            --text-main: #e1e1e6;
            --text-dim: #7c7c8a;
            --up: #00ff88;
            --down: #ff4757;
        }

        body { 
            background: var(--bg); 
            color: var(--text-main); 
            font-family: 'Inter', -apple-system, sans-serif; 
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container { width: 100%; max-width: 480px; padding: 20px; }

        header { text-align: center; margin-bottom: 30px; }
        h1 { font-size: 1.2rem; letter-spacing: 4px; color: var(--accent); margin: 0; font-weight: 800; }
        .subtitle { font-size: 0.7rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px; }

        /* STATUS LIVE PULSANDO */
        .status-live {
            font-size: 0.6rem;
            color: var(--up);
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        .dot {
            height: 6px;
            width: 6px;
            background-color: var(--up);
            border-radius: 50%;
            display: inline-block;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(0, 255, 136, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
        }

        .card {
            background: var(--card);
            border: 1px solid #29292e;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .asset-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 24px;
            border-bottom: 1px solid #29292e;
            transition: background 0.2s;
        }
        .asset-row:hover { background: #1c1c1f; }
        .asset-row:last-child { border-bottom: none; }

        .name { font-weight: 600; font-size: 0.9rem; }
        .price { font-family: 'JetBrains Mono', monospace; font-size: 1rem; }
        .change { font-size: 0.8rem; font-weight: 700; padding: 4px 8px; border-radius: 4px; background: rgba(0,0,0,0.2); }
        .up { color: var(--up); }
        .down { color: var(--down); }

        .sync-info {
            text-align: center;
            margin-top: 15px;
            font-size: 0.65rem;
            color: var(--text-dim);
            font-family: 'JetBrains Mono', monospace;
        }

        .btn-refresh {
            display: block;
            width: 100%;
            margin-top: 20px;
            padding: 14px;
            background: var(--accent);
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.8rem;
            letter-spacing: 1px;
            transition: all 0.2s;
        }
        .btn-refresh:hover { filter: brightness(1.2); transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>FINTRACE_</h1>
            <div class="subtitle">Market Telemetry Engine</div>
            <div class="status-live"><span class="dot"></span> SYSTEM ACTIVE</div>
        </header>

        <div class="card">
            {% for asset in assets %}
            <div class="asset-row">
                <div class="name">{{ asset.name }}</div>
                <div class="price">R$ {{ asset.val }}</div>
                <div class="change {{ 'up' if asset.is_up else 'down' }}">
                    {{ asset.pct }}
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="sync-info">LAST DATA STREAM: {{ time }}</div>

        <a href="/" class="btn-refresh">FORCE SYNCHRONIZE</a>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    dados, hora = get_financial_data()
    return render_template_string(HTML_TEMPLATE, assets=dados, time=hora)

if __name__ == "__main__":
    app.run(debug=True)