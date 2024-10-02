import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import urllib.request
import urllib.parse
import json
import os
import traceback
import threading

# Función para consultar la API SLAPHAPI y obtener el correo electrónico
def get_email(name):
    base_url = 'https://bluepages.ibm.com/BpHttpApisv3/slaphapi'
    encoded_name = urllib.parse.quote(name)
    filter = f'(cn={encoded_name})'
    url = f'{base_url}?ibmperson/{filter}.list/byjson?mail'

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode(errors='ignore'))
                if data.get('search') and data['search'].get('entry'):
                    entries = data['search']['entry']
                    if entries and entries[0].get('attribute'):
                        attributes = entries[0]['attribute']
                        for attribute in attributes:
                            if attribute['name'] == 'mail':
                                return '\n'.join(attribute['value'])
    except Exception as e:
        print(f"Error al consultar la API para {name}: {e}")
        traceback.print_exc()
    
    return 'Not found'

# Función para procesar el archivo CSV
def process_csv(input_path, output_path, progress_var, progress_label, count_label):
    try:
        with open(input_path, mode='r', newline='', encoding='utf-8') as infile, \
             open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
            
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            try:
                header = next(reader)
            except StopIteration:
                messagebox.showerror("Error", "El archivo CSV está vacío")
                return

            header.append('e-mail')
            writer.writerow(header)

            rows = list(reader)
            # Filtrar filas vacías en las primeras 7 columnas
            filtered_rows = [row for row in rows if not all(not cell.strip() for cell in row[:7])]
            total_rows = len(filtered_rows)

            processed_rows = 0
            for row in filtered_rows:
                name = row[5]
                email = get_email(name)
                row.append(email)
                writer.writerow(row)

                # Actualizar la barra de progreso
                processed_rows += 1
                progress = (processed_rows / total_rows) * 100
                progress_var.set(progress)
                progress_label.config(text=f"{progress:.2f}%")
                count_label.config(text=f"Filas procesadas: {processed_rows} de {total_rows}")
                root.update_idletasks()
        
        messagebox.showinfo("Éxito", f'Archivo generado: {output_path}')
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        traceback.print_exc()
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Función para seleccionar el archivo de entrada
def select_input_file():
    input_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if input_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, input_path)

# Función para seleccionar la ubicación del archivo de salida
def select_output_file():
    output_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if output_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_path)

# Función para iniciar el procesamiento del archivo CSV en un hilo separado
def start_processing():
    input_path = input_entry.get()
    output_path = output_entry.get()
    
    if not input_path:
        messagebox.showwarning("Advertencia", "Seleccione un archivo de entrada")
        return

    if not output_path:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_processed{ext}"
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_path)

    if not os.path.exists(input_path):
        messagebox.showerror("Error", "El archivo de entrada no existe")
        return
    
    # Contar el número total de filas para la barra de progreso
    try:
        with open(input_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            total_rows = sum(1 for row in reader) - 1  # Excluir la fila del encabezado

        # Iniciar procesamiento del CSV en la ventana principal
        progress_var.set(0)
        progress_label.config(text="0%")
        count_label.config(text="Filas procesadas: 0 de 0")
        root.update_idletasks()
        
        # Crear y comenzar un hilo separado para el procesamiento del CSV
        threading.Thread(target=process_csv, args=(input_path, output_path, progress_var, progress_label, count_label)).start()
    except Exception as e:
        print(f"Ocurrió un error al contar las filas: {e}")
        traceback.print_exc()
        messagebox.showerror("Error", f"Ocurrió un error al contar las filas: {e}")

# Crear la interfaz gráfica con tkinter
root = tk.Tk()
root.title("Procesador de CSV")

tk.Label(root, text="Archivo de entrada:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Seleccionar", command=select_input_file).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Archivo de salida:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Seleccionar", command=select_output_file).grid(row=1, column=2, padx=10, pady=5)

tk.Button(root, text="Procesar", command=start_processing).grid(row=2, column=0, columnspan=3, pady=10)

# Barra de progreso y etiqueta de porcentaje
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, maximum=100, variable=progress_var)
progress_bar.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
progress_label = tk.Label(root, text="0%")
progress_label.grid(row=4, column=0, columnspan=3)

# Etiqueta de contador de filas procesadas
count_label = tk.Label(root, text="Filas procesadas: 0 de 0")
count_label.grid(row=5, column=0, columnspan=3)

root.mainloop()
