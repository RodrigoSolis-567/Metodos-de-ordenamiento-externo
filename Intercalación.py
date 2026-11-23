import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import time

class IntercalacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intercalación - Fusión de Pedidos de Sucursales")
        self.root.geometry("700x580")
        self.root.config(bg="#1e1e1e")

        tk.Label(root, text="1. Intercalación: Fusión de Pedidos (Folios)", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#e67e22").pack(pady=10)

        frame = tk.LabelFrame(root, text=" Gestión de Flujos de Pedidos ", font=("Arial", 10, "bold"), bg="#2d2d2d", fg="white", padx=10, pady=10)
        frame.pack(fill="x", padx=20, pady=5)

        tk.Button(frame, text="1. Ingresar Cantidad y Folios (2 Sucursales)", command=self.pedir_datos, bg="#2980b9", fg="white", font=("Arial", 9, "bold"), padx=10, pady=5).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(frame, text="⚡ Cargar Ejemplo (Sucursales)", command=self.ejemplo, bg="#d35400", fg="white", font=("Arial", 9, "bold"), padx=10, pady=5).grid(row=0, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack(pady=10)
        
        self.btn_run = tk.Button(btn_frame, text="2. ▶ Intercalar Pedidos", command=self.ejecutar, bg="#27ae60", fg="white", font=("Arial", 11, "bold"), padx=15, pady=5)
        self.btn_run.pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="❌ Salir", command=root.quit, bg="#c0392b", fg="white", font=("Arial", 11, "bold"), padx=15, pady=5).pack(side="left", padx=10)

        self.canvas = tk.Canvas(root, width=640, height=160, bg="#111111", highlightthickness=0)
        self.canvas.pack(pady=5)

        self.log = scrolledtext.ScrolledText(root, width=78, height=7, font=("Consolas", 9), bg="#111111", fg="#00ffcc")
        self.log.pack(padx=20, pady=5)
        
        self.ejemplo()

    def pedir_datos(self):
        try:
            c1_str = simpledialog.askstring("Sucursal A", "Cantidad de pedidos en Sucursal A:", parent=self.root)
            if not c1_str: return
            c1 = int(c1_str)
            if c1 <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0.", parent=self.root)
                return

            f1_str = simpledialog.askstring("Folios Sucursal A", f"Ingrese los {c1} folios de Sucursal A (separados por comas):", parent=self.root)
            if not f1_str: return
            arr1 = [int(x) for x in f1_str.replace(",", " ").split()]
            if len(arr1) != c1:
                messagebox.showerror("Error de Cantidad", f"Indicó {c1} folios, pero introdujo {len(arr1)}. Operación cancelada.", parent=self.root)
                return

            c2_str = simpledialog.askstring("Sucursal B", "Cantidad de pedidos en Sucursal B:", parent=self.root)
            if not c2_str: return
            c2 = int(c2_str)
            if c2 <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0.", parent=self.root)
                return

            f2_str = simpledialog.askstring("Folios Sucursal B", f"Ingrese los {c2} folios de Sucursal B (separados por comas):", parent=self.root)
            if not f2_str: return
            arr2 = [int(x) for x in f2_str.replace(",", " ").split()]
            if len(arr2) != c2:
                messagebox.showerror("Error de Cantidad", f"Indicó {c2} folios, pero introdujo {len(arr2)}. Operación cancelada.", parent=self.root)
                return

            # La intercalación requiere que las fuentes individuales estén ordenadas
            self.lista_a = sorted(arr1)
            self.lista_b = sorted(arr2)
            
            combinado = self.lista_a + self.lista_b
            colores = ["#3498db"] * len(self.lista_a) + ["#9b59b6"] * len(self.lista_b)
            self.dibujar(combinado, colores)
            
            self.log.delete(1.0, tk.END)
            self.log.insert(tk.END, f"Sucursal A (ordenada): {self.lista_a}\nSucursal B (ordenada): {self.lista_b}\nPaso 2: Haga clic en 'Intercalar Pedidos'.\n")
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar únicamente números enteros para los folios.", parent=self.root)

    def ejemplo(self):
        self.lista_a = [105, 210, 340, 480]
        self.lista_b = [120, 250, 310, 520]
        combinado = self.lista_a + self.lista_b
        colores = ["#3498db"] * len(self.lista_a) + ["#9b59b6"] * len(self.lista_b)
        self.dibujar(combinado, colores)
        self.log.delete(1.0, tk.END)
        self.log.insert(tk.END, f"Contexto: Fusión de 2 archivos ordenados de pedidos.\nSucursal A (Azul): {self.lista_a}\nSucursal B (Morado): {self.lista_b}\nPaso 2: Haga clic en 'Intercalar Pedidos'.\n")

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
                self.canvas.create_text(x0 + bw/2, h - 12, text=f"#{v}", fill="white", font=("Arial", 7, "bold"))
        self.root.update()

    def ejecutar(self):
        self.btn_run.config(state="disabled")
        self.log.delete(1.0, tk.END)
        self.log.insert(tk.END, "Iniciando intercalación externa...\n")
        
        i = j = 0
        resultado = []
        a, b = self.lista_a, self.lista_b
        
        while i < len(a) and j < len(b):
            if a[i] < b[j]:
                resultado.append(a[i])
                self.log.insert(tk.END, f" -> Toma #{a[i]} de Sucursal A\n")
                i += 1
            else:
                resultado.append(b[j])
                self.log.insert(tk.END, f" -> Toma #{b[j]} de Sucursal B\n")
                j += 1
            
            pendientes = a[i:] + b[j:]
            vista = resultado + pendientes
            cols = ["#2ecc71"] * len(resultado) + ["#3498db"] * len(a[i:]) + ["#9b59b6"] * len(b[j:])
            self.dibujar(vista, cols)
            time.sleep(0.25)

        while i < len(a):
            resultado.append(a[i])
            i += 1
            vista = resultado + a[i:]
            cols = ["#2ecc71"] * len(resultado) + ["#3498db"] * len(a[i:])
            self.dibujar(vista, cols)
            time.sleep(0.2)

        while j < len(b):
            resultado.append(b[j])
            j += 1
            vista = resultado + b[j:]
            cols = ["#2ecc71"] * len(resultado) + ["#9b59b6"] * len(b[j:])
            self.dibujar(vista, cols)
            time.sleep(0.2)

        self.dibujar(resultado, ["#2ecc71"] * len(resultado))
        self.log.insert(tk.END, f"✔ Archivo maestro fusionado: {resultado}\n")
        self.btn_run.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    IntercalacionApp(root)
    root.mainloop()