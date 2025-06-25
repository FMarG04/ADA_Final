# -*- coding: utf-8 -*-
import customtkinter as ctk
import threading
import plotly.graph_objects as go
import os
import base64
import gc
import sys
from ADA_Proyecto import main

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("900x700")
app.title("Analisis de Grafo")

frame = ctk.CTkFrame(app)
frame.pack(pady=10, padx=10, fill="both", expand=True)

output_text = ctk.CTkTextbox(frame, wrap="word", font=("Consolas", 12))
output_text.pack(expand=True, fill="both", padx=10, pady=10)

# Redirigir salida a la interfaz
def redirect_print(textbox):
    class StdoutRedirector:
        def write(self, s):
            textbox.insert("end", s)
            textbox.see("end")
        def flush(self):
            pass
    sys.stdout = StdoutRedirector()
    sys.stderr = StdoutRedirector()

redirect_print(output_text)

# Variables globales
grafo_global = {}
muestra_global = {}
comunidades_global = {}

def ejecutar():
    global grafo_global, muestra_global, comunidades_global
    output_text.delete("1.0", "end")
    grafo, muestra, comunidades = main()
    grafo_global = grafo
    muestra_global = muestra
    comunidades_global = comunidades

boton_ejecutar = ctk.CTkButton(app, text="Ejecutar Analisis", command=lambda: threading.Thread(target=ejecutar).start())
boton_ejecutar.pack(pady=10)

import plotly.graph_objects as go

def visualizar_comunidades():
    muestra = muestra_global
    comunidades = comunidades_global

    fig = go.Figure()

    colores = [
        "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
        "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
        "#008080", "#e6beff", "#9a6324", "#fffac8", "#800000",
        "#aaffc3", "#808000", "#ffd8b1", "#000075", "#808080"
    ]

    comunidades_items = list(comunidades.items())
    comunidad_id_map = {orig_id: idx for idx, (orig_id, _) in enumerate(comunidades_items)}

    for orig_id, nodos in comunidades_items:
        idx = comunidad_id_map[orig_id]
        lats, lons = [], []

        for nodo in nodos:
            if nodo in muestra and muestra[nodo]['ubicacion']:
                lat, lon = muestra[nodo]['ubicacion']
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    lats.append(lat)
                    lons.append(lon)

        fig.add_trace(go.Scattergeo(
            lat=lats,
            lon=lons,
            mode='markers',
            marker=dict(
                size=4,
                color=colores[idx % len(colores)],
                opacity=0.85
            ),
            name=f"Comunidad {idx + 1}"
        ))

    fig.update_layout(
        title='Visualizacion de Comunidades',
        geo=dict(
            projection_type='natural earth',  
            showland=True,
            landcolor='rgb(40, 40, 40)',
            showocean=True,
            oceancolor='rgb(10, 80, 150)',
            showlakes=True,
            lakecolor='rgb(80, 150, 240)',
            coastlinecolor='white',
            lataxis=dict(range=[-90, 90]),
            lonaxis=dict(range=[-180, 180])
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black')
    )

    fig.show()

 

boton_comunidades = ctk.CTkButton(app, text="Ver Comunidades", command=lambda: threading.Thread(target=visualizar_comunidades).start())
boton_comunidades.pack(pady=10)

# Boton para salir
def salir():
    output_text.insert("end", "\nCerrando y limpiando recursos...\n")
    global grafo_global, muestra_global, comunidades_global
    grafo_global = None
    muestra_global = None
    comunidades_global = None
    gc.collect()
    app.destroy()

boton_salir = ctk.CTkButton(app, text="Salir", fg_color="red", hover_color="#aa0000", command=salir)
boton_salir.pack(pady=10)

app.mainloop()
