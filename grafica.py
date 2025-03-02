import json
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import firebase_admin
from firebase_admin import credentials, db
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Credenciales de Firebase
firebase_config = {
    "type": "service_account",
    "project_id": "velocidad-en-carretera",
    "private_key_id": "8fb69995fc5a0fc2351ca0cef66a13c595e12e56",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDO9EuHUWzIIkW+\ndoiffbymQrVjH4lggCY9tic+s2kTW3hLCpuxsxiiv/6BoAM4fbOmgZ/ptOfO3p1N\nR6kz8g5HsufbyK+wPi5l1wfMytzNliLTLs0Cdwccz7KcPxXIPzh2ME6KL52XWRuS\njjKhsi1JYzsXyIertx298FUXnhQSp+1ZziB9WQ04bUqhUJUdumuRYWIkkFcXMHqZ\n+hGINYWY0pGAKvTdIq/N9Eu0yY7emBBlnAocfaslNKawzdDpuIDg39tRTJij952j\nLsT5dz1lUHaimilonjAmAHQpkKGPBu4LXMf4eLVsiS7zJ6+iKcK0KqEvcn24LmAH\nmo6/2XQnAgMBAAECggEAIakI99NojAyhp17ZeIds6DswDBU/CjENseUvRjrMEQKZ\nnYBLiSrbYO01VJlVV29/3snKhqqOjCPCa1AH1z5m0DFAa4udTQnFZiRZTRfZs0ku\nFNx8f7V4X1lGGwpaXUgwbhi2otx9F0wTo1H5g48wCnWspiukKsENLK2ASZJugAdW\nkAxTXUUiNXF+qdFUpz+ZDEGCgrhi1C4vue5iytM4l82iFsr2wIZst0bPPYpuh23y\niZNGwBsKD1Imgu4R9ZTSn8Nm8jesUvZ+DZpUkQpVAkfI5n3ysFqj3xNgseLH7+NX\nUYw3YbAN2fjBVCVcw+F+S5PkHurTW1XMvw+h8I+9MQKBgQDrtYU+qNdmR+ZYQrEG\nGE7+SSFWGozvBpezsKBa+Hw96aN9E77rJMNti7r+podokyEdBbIKkNDMpeNaILCN\nVib39xOpGjlW0iExCPHHocmCX5Uqg53i8HBZaBqf2xo2b+/TDGhG/cPHX3YZ35gh\nu8oiNhN/C4AsEl1CgOWxJyYl2wKBgQDgxRX/TNE1EkkT4ZPTymGKfWSxnpLsitUb\n1MHxhFLW7RvqzPmiXYugppecA3mP3+xcNc9AhGEZ355lZu+gk6VRyhAtiHXXAs/J\ni0pvTtXBw6rLLYDJOV4z4ngMH17rJTlKwFz8QBiT1BOo1hwkHgmgqLDxPUkHKSCb\nqAATygGKpQKBgEui1f0DZQtXKx1LWU7hYgfLI71ji7Hv5aItnWdTsVqUrHeobG08\nQNHYMssgWPc/rzKG71jgm3/wA4KaVs0jxiFv0YlD9v5bM3durVcoHWeOkGkyDuoR\nyZuHAnQldMXfKZAJvTR6neZORbGLxF+eyQAtZhgwcpKx2edLQWmVbHJdAoGBAIAX\nUOXg/Qhll0fBMeFsYBHwS8X9PHWY2MG3iZ79bcgV7+brUQf6j2vKBHRgdpJLZgNW\nlvmJd1yrVzUqaDz2ZywpHvcT4TPa4ldVDeJI5wA5ZcfL8qy6CLlAwnEGH62Z1QCI\nh3Upgdgc7+czvW3HwGzSNaQE7O0rvu113DVq1V4RAoGAYgyxyP6CrssrCEBqSznz\nx4VqqkyHePjLPv2Nl0g8ynmLrQU46kUtSVoQ952ogL7zssYNFo7abu9Pu6x1Z2Os\nB/fpGRaqd03VcQ7y7iclnX+6fV6JDundISvWKuT2c+3HOvUyFlc5GQQEO0vIPdIB\nS4HIv2dN8w/U2fVQyc0zgPM=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-fbsvc@velocidad-en-carretera.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.googleapis.com/token"
}

cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://velocidad-en-carretera-default-rtdb.europe-west1.firebasedatabase.app"
})

# Crear ventana principal
root = tk.Tk()
root.title("Filtro de Velocidad")
root.state("zoomed")

# Frames principales
frame_top = tk.Frame(root)
frame_top.pack(fill="x", padx=10, pady=10)

frame_counts = tk.Frame(root)
frame_counts.pack(fill="x", pady=10)

frame_graph = tk.Frame(root)
frame_graph.pack(side="left", fill="both", expand=True, padx=10, pady=10)

frame_listado = tk.Frame(root)
frame_listado.pack(side="right", fill="y", padx=10, pady=10)

# Agregar scrollbar para la lista de velocidades
scrollbar = tk.Scrollbar(frame_listado)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(frame_listado, font=("Arial", 12), width=40, height=20, yscrollcommand=scrollbar.set)
listbox.pack(fill="both", expand=True)
scrollbar.config(command=listbox.yview)

# Filtros de fecha, hora y velocidad mínima
hoy = datetime.datetime.today().strftime('%d/%m/%Y')

cal_inicio = DateEntry(frame_top, date_pattern='dd/MM/yyyy', font=("Arial", 14))
cal_inicio.set_date(hoy)
cal_inicio.pack(side="left", padx=5, pady=5)

hora_inicio = ttk.Entry(frame_top, width=12, font=("Arial", 14))
hora_inicio.insert(0, "00:00:00")
hora_inicio.pack(side="left", padx=5, pady=5)

cal_fin = DateEntry(frame_top, date_pattern='dd/MM/yyyy', font=("Arial", 14))
cal_fin.set_date(hoy)
cal_fin.pack(side="left", padx=5, pady=5)

hora_fin = ttk.Entry(frame_top, width=12, font=("Arial", 14))
hora_fin.insert(0, "23:59:59")
hora_fin.pack(side="left", padx=5, pady=5)

velocidad_slider = tk.Scale(frame_top, from_=13, to=140, orient="horizontal", font=("Arial", 12), label="Velocidad Mínima")
velocidad_slider.pack(side="left", padx=5, pady=5)

# Variables de conteo
count_0_30 = count_30_40 = count_40_50 = count_50_70 = count_70_plus = 0

def obtener_datos(filtro_rango=None):
    global count_0_30, count_30_40, count_40_50, count_50_70, count_70_plus
    count_0_30 = count_30_40 = count_40_50 = count_50_70 = count_70_plus = 0

    fecha_inicio = datetime.datetime.strptime(cal_inicio.get() + " " + hora_inicio.get(), "%d/%m/%Y %H:%M:%S")
    fecha_fin = datetime.datetime.strptime(cal_fin.get() + " " + hora_fin.get(), "%d/%m/%Y %H:%M:%S")
    velocidad_min = velocidad_slider.get()

    ref = db.reference("/lecturas")
    snapshot = ref.get()

    timestamps = []
    max_velocities = []

    # Limpiar listbox antes de agregar nuevos datos
    listbox.delete(0, tk.END)

    for key, entry in snapshot.items():
        timestamp = datetime.datetime.strptime(entry["timestamp"], "%d/%m/%Y %H:%M:%S")
        velocity_values = list(map(float, entry["velocidades"].split(";")))
        velocity_values = [v for v in velocity_values if 13 <= v <= 140 and v >= velocidad_min]

        if not velocity_values or not (fecha_inicio <= timestamp <= fecha_fin):
            continue

        max_value = max(velocity_values)
        if filtro_rango and not (filtro_rango[0] <= max_value < filtro_rango[1]):
            continue

        max_velocities.append(max_value)
        timestamps.append(timestamp)

        listbox.insert(tk.END, f"{timestamp.strftime('%d/%m/%Y %H:%M:%S')} - {max_value} km/h")

        if 0 <= max_value < 30:
            count_0_30 += 1
        elif 30 <= max_value < 40:
            count_30_40 += 1
        elif 40 <= max_value < 50:
            count_40_50 += 1
        elif 50 <= max_value < 70:
            count_50_70 += 1
        else:
            count_70_plus += 1

    # Graficar los datos
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(timestamps, max_velocities, linestyle="-", color="red", linewidth=2, label="Máximo")
    ax.set_xlabel("Fecha y Hora", fontsize=14)
    ax.set_ylabel("Velocidad (KM/H)", fontsize=14)
    ax.set_title("Máximo de Velocidades", fontsize=16, fontweight="bold")
    ax.tick_params(axis='x', rotation=45, labelsize=12)
    ax.legend(fontsize=12)
    fig.tight_layout()

    for widget in frame_graph.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Botones de conteo
    for widget in frame_counts.winfo_children():
        widget.destroy()
    
    headers = [("0-30 km/h", (0, 30)), ("30-40 km/h", (30, 40)), ("40-50 km/h", (40, 50)), 
               ("50-70 km/h", (50, 70)), ("70+ km/h", (70, 140))]
    counts = [count_0_30, count_30_40, count_40_50, count_50_70, count_70_plus]
    colors = ["#4CAF50", "#FF9800", "#FF9800", "#F44336", "#F44336"]
    
    for i, ((header, rango), count, color) in enumerate(zip(headers, counts, colors)):
        btn = tk.Button(frame_counts, text=f"{header}: {count}", font=("Arial", 14), bg=color, fg="white", 
                        padx=10, pady=5, borderwidth=2, relief="solid", 
                        command=lambda r=rango: obtener_datos(filtro_rango=r))
        btn.pack(side="left", padx=5, pady=5, fill="x", expand=True)

# Botón para generar datos
btn_generar = ttk.Button(frame_top, text="Generar Gráfica", command=obtener_datos)
btn_generar.pack(side="left", padx=5, pady=5)

# Ejecutar la interfaz
tk.mainloop()
