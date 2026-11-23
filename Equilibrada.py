import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import time

class MezclaEquilibradaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mezcla Equilibrada - Folios de Facturas")
        self.root.geometry("700x580")
        self.root.config(bg="#1e1e1e")

        tk.Label(root, text="3. Mezcla Equilibrada: Folios de Facturas", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#1abc9c").pack(pady=10)

        frame = tk.LabelFrame(root, text=" Gestión de Lotes de Facturación ", font=("Arial", 10, "bold"), bg="#2d2d2d", fg="white", padx=10, pady=10)
        frame.pack(fill="x", padx=20, pady=5)

        tk.Button(frame, text="1. Ingresar Cantidad y Folios", command=self.pedir_datos, bg="#2980b9", fg="white", font=("Arial", 9, "bold"), padx=10, pady=5).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(frame, text="⚡ Cargar Ejemplo (Facturas)", command=self.ejemplo, bg="#d35400", fg="white", font=("Arial", 9, "bold"), padx=10, pady=5).grid(row=0, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack(pady=10)
        
        self.btn_run = tk.Button(btn_frame, text="2. ▶ Ejecutar Mezcla Equilibrada", command=self.ejecutar, bg="#27ae60", fg="white", font=("Arial", 11, "bold"), padx=15, pady=5)
        self.btn_run.pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="❌ Salir", command=root.quit, bg="#c0392b", fg="white", font=("Arial", 11, "bold"), padx=15, pady=5).pack(side="left", padx=10)

        self.canvas = tk.Canvas(root, width=640, height=160, bg="#111111", highlightthickness=0)
        self.canvas.pack(pady=5)

        self.log = scrolledtext.ScrolledText(root, width=78, height=7, font=("Consolas", 9), bg="#111111", fg="#00ffcc")
        self.log.pack(padx=20, pady=5)
        
        self.ejemplo()

    def pedir_datos(self):
        try:
            cant_str = simpledialog.askstring("Cantidad", "Ingrese la cantidad de facturas:", parent=self.root)
            if not cant_str: return
            cant = int(cant_str)
            if cant <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0.", parent=self.root)
                return

            nums_str = simpledialog.askstring("Folios", f"Ingrese exactamente {cant} folios de facturas (separados por comas):", parent=self.root)
            if not nums_str: return
            
            arr = [int(x) for x in nums_str.replace(",", " ").split()]
            if len(arr) != cant:
                messagebox.showerror("Error de Cantidad", f"Indicó {cant} facturas, pero introdujo {len(arr)}. Operación cancelada.", parent=self.root)
                return

            self.datos_actuales = arr
            self.dibujar(self.datos_actuales, ["#3498db"] * len(self.datos_actuales))
            self.log.delete(1.0, tk.END)
            self.log.insert(tk.END, f"Facturas cargadas: {self.datos_actuales}\nPaso 2: Haga clic en 'Ejecutar Mezcla Equilibrada'.\n")
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar valores numéricos enteros.", parent=self.root)

    def ejemplo(self):
        # Contiene corridas naturales: [12, 35, 60], [18, 42], [9, 55, 80]
        self.datos_actuales = [12, 35, 60, 18, 42, 9, 55, 80]
        self.dibujar(self.datos_actuales, ["#3498db"] * len(self.datos_actuales))
        self.log.delete(1.0, tk.END)
        self.log.insert(tk.END, f"Contexto: Detecta secuencias ordenadas naturales (corridas).\nFacturas cargadas: {self.datos_actuales}\nPaso 2: Haga clic en 'Ejecutar Mezcla Equilibrada'.\n")

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
                self.canvas.create_text(x0 + bw/2, h - 12, text=f"F-{v}", fill="white", font=("Arial", 7, "bold"))
        self.root.update()

    def obtener_corridas(self, arr):
        if not arr: return []
        corridas = []
        actual = [arr[0]]
        for i in range(1, len(arr)):
            if arr[i] >= arr[i - 1]:
                actual.append(arr[i])
            else:
                corridas.append(actual)
                actual = [arr[i]]
        corridas.append(actual)
        return corridas

    def intercalar_dos_listas(self, a, b):
        res = []
        i = j = 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                res.append(a[i])
                i += 1
            else:
                res.append(b[j])
                j += 1
        res.extend(a[i:])
        res.extend(b[j:])
        return res

    def ejecutar(self):
        if not self.datos_actuales: return
        arr = list(self.datos_actuales)
        n = len(arr)
        self.btn_run.config(state="disabled")
        self.log.delete(1.0, tk.END)

        pasada = 1
        while True:
            corridas = self.obtener_corridas(arr)
            self.log.insert(tk.END, f"Pasada {pasada} - Corridas detectadas: {corridas}\n")
            
            # Colorear cada corrida detectada alternando colores
            cols = []
            paleta = ["#1abc9c", "#e67e22", "#9b59b6", "#3498db"]
            for idx_c, c in enumerate(corridas):
                cols.extend([paleta[idx_c % len(paleta)]] * len(c))
            self.dibujar(arr, cols)
            time.sleep(0.4)

            if len(corridas) <= 1:
                break

            # Distribución alterna en Archivo Auxiliar 1 (F1) y Archivo Auxiliar 2 (F2)
            f1 = corridas[0::2]
            f2 = corridas[1::2]
            self.log.insert(tk.END, f"   Archivo F1: {f1} | Archivo F2: {f2}\n")

            # Fusión equilibrada de pares de corridas
            nuevo_arr = []
            max_pares = max(len(f1), len(f2))
            for idx in range(max_pares):
                c1 = f1[idx] if idx < len(f1) else []
                c2 = f2[idx] if idx < len(f2) else []
                nuevo_arr.extend(self.intercalar_dos_listas(c1, c2))

            arr = nuevo_arr
            self.dibujar(arr, ["#f1c40f"] * n)
            time.sleep(0.3)
            pasada += 1

        self.dibujar(arr, ["#2ecc71"] * n)
        self.log.insert(tk.END, f"✔ Folios ordenados en 1 sola corrida: {arr}\n")
        self.btn_run.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    MezclaEquilibradaApp(root)
    root.mainloop()