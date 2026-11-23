import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import time

class MezclaDirectaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mezcla Directa - Transacciones Bancarias")
        self.root.geometry("700x580")
        self.root.config(bg="#1e1e1e")

        tk.Label(root, text="2. Mezcla Directa: Montos de Transacciones ($)", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#3498db").pack(pady=10)

        frame = tk.LabelFrame(root, text=" Gestión de Lotes Bancarios ", font=("Arial", 10, "bold"), bg="#2d2d2d", fg="white", padx=10, pady=10)
        frame.pack(fill="x", padx=20, pady=5)

        tk.Button(frame, text="1. Ingresar Cantidad y Montos", command=self.pedir_datos, bg="#2980b9", fg="white", font=("Arial", 9, "bold"), padx=10, pady=5).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(frame, text="⚡ Cargar Ejemplo (Montos)", command=self.ejemplo, bg="#d35400", fg="white", font=("Arial", 9, "bold"), padx=10, pady=5).grid(row=0, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack(pady=10)
        
        self.btn_run = tk.Button(btn_frame, text="2. ▶ Ejecutar Mezcla Directa", command=self.ejecutar, bg="#27ae60", fg="white", font=("Arial", 11, "bold"), padx=15, pady=5)
        self.btn_run.pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="❌ Salir", command=root.quit, bg="#c0392b", fg="white", font=("Arial", 11, "bold"), padx=15, pady=5).pack(side="left", padx=10)

        self.canvas = tk.Canvas(root, width=640, height=160, bg="#111111", highlightthickness=0)
        self.canvas.pack(pady=5)

        self.log = scrolledtext.ScrolledText(root, width=78, height=7, font=("Consolas", 9), bg="#111111", fg="#00ffcc")
        self.log.pack(padx=20, pady=5)
        
        self.ejemplo()

    def pedir_datos(self):
        try:
            cant_str = simpledialog.askstring("Cantidad", "Ingrese la cantidad de transacciones:", parent=self.root)
            if not cant_str: return
            cant = int(cant_str)
            if cant <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0.", parent=self.root)
                return

            nums_str = simpledialog.askstring("Montos", f"Ingrese exactamente {cant} montos en $ (separados por comas):", parent=self.root)
            if not nums_str: return
            
            arr = [int(x) for x in nums_str.replace(",", " ").split()]
            if len(arr) != cant:
                messagebox.showerror("Error de Cantidad", f"Indicó {cant} transacciones, pero introdujo {len(arr)}. Operación cancelada.", parent=self.root)
                return

            self.datos_actuales = arr
            self.dibujar(self.datos_actuales, ["#3498db"] * len(self.datos_actuales))
            self.log.delete(1.0, tk.END)
            self.log.insert(tk.END, f"Transacciones cargadas: ${self.datos_actuales}\nPaso 2: Haga clic en 'Ejecutar Mezcla Directa'.\n")
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar valores numéricos enteros.", parent=self.root)

    def ejemplo(self):
        self.datos_actuales = [850, 120, 430, 95, 670, 310, 540, 200]
        self.dibujar(self.datos_actuales, ["#3498db"] * len(self.datos_actuales))
        self.log.delete(1.0, tk.END)
        self.log.insert(tk.END, f"Contexto: Ordenamiento externo por bloques de tamaño 2^k.\nLote cargado: ${self.datos_actuales}\nPaso 2: Haga clic en 'Ejecutar Mezcla Directa'.\n")

    def dibujar(self, arr, cols):
        self.canvas.delete("all")
        if not arr: return
        w, h = 640, 160
        bw = max(5, (w / len(arr)) - 5)
        mx = max(arr) if max(arr) > 0 else 1
        for i, v in enumerate(arr):
            x0 = i * (bw + 5) + 10
            yh = (v / mx) * 100
            self.canvas.create_rectangle(x0, h - yh - 25, x0 + bw, h - 25, fill=cols[i], outline="")
            if len(arr) <= 16:
                self.canvas.create_text(x0 + bw/2, h - 12, text=f"${v}", fill="white", font=("Arial", 7, "bold"))
        self.root.update()

    def ejecutar(self):
        if not self.datos_actuales: return
        arr = list(self.datos_actuales)
        n = len(arr)
        self.btn_run.config(state="disabled")
        self.log.delete(1.0, tk.END)

        # Mezcla directa iterativa (bottom-up) con bloques de tamaño 1, 2, 4, 8...
        part = 1
        pasada = 1
        while part < n:
            self.log.insert(tk.END, f"Pasada {pasada} (bloques de tamaño {part}):\n")
            for start in range(0, n, 2 * part):
                mid = min(start + part, n)
                end = min(start + 2 * part, n)
                
                izq = arr[start:mid]
                der = arr[mid:end]
                
                # Intercalación de los dos bloques actuales
                i = j = 0
                k = start
                while i < len(izq) and j < len(der):
                    if izq[i] <= der[j]:
                        arr[k] = izq[i]
                        i += 1
                    else:
                        arr[k] = der[j]
                        j += 1
                    k += 1
                while i < len(izq):
                    arr[k] = izq[i]
                    i += 1
                    k += 1
                while j < len(der):
                    arr[k] = der[j]
                    j += 1
                    k += 1

                cols = ["#3498db"] * n
                for idx in range(start, end):
                    cols[idx] = "#f1c40f"
                self.dibujar(arr, cols)
                time.sleep(0.25)
                
            self.log.insert(tk.END, f"   Resultado parcial: ${arr}\n")
            part *= 2
            pasada += 1

        self.dibujar(arr, ["#2ecc71"] * n)
        self.log.insert(tk.END, f"✔ Transacciones ordenadas: ${arr}\n")
        self.btn_run.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    MezclaDirectaApp(root)
    root.mainloop()