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

    min_lat = min(muestra[n]['ubicacion'][0] for n in muestra if muestra[n]['ubicacion'])
    max_lat = max(muestra[n]['ubicacion'][0] for n in muestra if muestra[n]['ubicacion'])
    min_lon = min(muestra[n]['ubicacion'][1] for n in muestra if muestra[n]['ubicacion'])
    max_lon = max(muestra[n]['ubicacion'][1] for n in muestra if muestra[n]['ubicacion'])

    for i, (comunidad, nodos) in enumerate(comunidades.items()):
        x, y = [], []
        for nodo in nodos:
            if nodo in muestra and muestra[nodo]['ubicacion']:
                lat, lon = muestra[nodo]['ubicacion']
                x.append(lat)
                y.append(lon)

        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker=dict(
                size=6,
                color=colores[i % len(colores)],
                opacity=0.85
            ),
            name=f"Comunidad {comunidad}"
        ))

    image_path = "world_map.png"
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()

        fig.update_layout(
            images=[dict(
                source="data:image/png;base64," + encoded,
                xref="x",
                yref="y",
                x=min_lat,
                y=max_lon,
                sizex=max_lat - min_lat,
                sizey=max_lon - min_lon,
                sizing="stretch",
                opacity=0.5,
                layer="below"
            )]
        )

    fig.update_layout(
        title="Visualizacion de Comunidades",
        xaxis_title="Latitud",
        yaxis_title="Longitud",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
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
