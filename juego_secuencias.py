import tkinter as tk
from tkinter import messagebox
import random


class JuegoSecuencias:

    def __init__(self, root):
        """Configura ventana y variables principales del juego."""
        self.root = root
        self.root.title("Juego de Secuencias Numéricas")
        self.root.geometry("550x420")
        self.root.resizable(False, False)

        # Tiempo mínimo de juego: 5 minutos (300 segundos)
        self.tiempo_total = 300
        self.tiempo_restante = self.tiempo_total

        # Variables del juego
        self.puntaje = 0
        self.respuesta_correcta = None
        self.juego_activo = False

        self.crear_interfaz()


    # ---------------------------------------------------------
    # Interfaz gráfica
    # ---------------------------------------------------------
    def crear_interfaz(self):
        """Crea componentes de la interfaz."""
        titulo = tk.Label(self.root, text="Adivina la Secuencia",
                          font=("Arial", 22, "bold"))
        titulo.pack(pady=10)

        self.temporizador = tk.Label(self.root, text="Tiempo: 5:00",
                                     font=("Arial", 16))
        self.temporizador.pack()

        self.label_secuencia = tk.Label(self.root,
                                        text="Presiona 'Iniciar' para comenzar",
                                        font=("Arial", 16))
        self.label_secuencia.pack(pady=30)

        self.entrada = tk.Entry(self.root, font=("Arial", 16), width=10, justify="center")
        self.entrada.pack()

        self.boton_responder = tk.Button(self.root, text="Responder",
                                         font=("Arial", 14),
                                         command=self.verificar_respuesta,
                                         state="disabled")
        self.boton_responder.pack(pady=15)

        self.label_puntaje = tk.Label(self.root,
                                      text="Puntaje: 0",
                                      font=("Arial", 14))
        self.label_puntaje.pack()

        self.boton_iniciar = tk.Button(self.root, text="Iniciar Juego",
                                       font=("Arial", 16, "bold"),
                                       command=self.iniciar_juego)
        self.boton_iniciar.pack(pady=20)


    # ---------------------------------------------------------
    # Lógica del juego
    # ---------------------------------------------------------
    def iniciar_juego(self):
        """Reinicia valores y activa el juego."""
        self.puntaje = 0
        self.tiempo_restante = self.tiempo_total
        self.juego_activo = True

        self.boton_responder.config(state="normal")
        self.boton_iniciar.config(state="disabled")

        self.nueva_secuencia()
        self.actualizar_puntaje()
        self.actualizar_tiempo()


    # ---------------------------------------------------------
    # Generación de secuencias
    # ---------------------------------------------------------
    def generar_secuencia(self):
        """
        Genera una secuencia numérica simple pero variada.
        Tipos incluidos:
        1. Aritmética:      2, 5, 8, 11, ...
        2. Geométrica:      3, 6, 12, 24, ...
        3. Fibonacci:       1, 1, 2, 3, 5, ...
        4. Alternante:      2, 4, 2, 4, ...
        5. Cuadrados:       1, 4, 9, 16, ...
        """
        tipo = random.choice(["arit", "geom", "fibo", "alt", "cuad"])

        if tipo == "arit":
            a = random.randint(1, 10)
            d = random.randint(1, 10)
            sec = [a + i * d for i in range(4)]
            respuesta = a + 4 * d

        elif tipo == "geom":
            a = random.randint(1, 5)
            r = random.randint(2, 4)
            sec = [a * (r ** i) for i in range(4)]
            respuesta = a * (r ** 4)

        elif tipo == "fibo":
            f1 = random.randint(1, 5)
            f2 = random.randint(1, 5)
            sec = [f1, f2, f1 + f2, f1 + 2*f2]
            respuesta = sec[-1] + sec[-2]

        elif tipo == "alt":
            x = random.randint(1, 9)
            y = random.randint(1, 9)
            sec = [x, y, x, y]
            respuesta = x

        else:  # cuadrados
            n = random.randint(1, 5)
            sec = [(n + i)**2 for i in range(4)]
            respuesta = (n + 4)**2

        return sec, respuesta


    def nueva_secuencia(self):
        """Carga una nueva secuencia en pantalla."""
        secuencia, respuesta = self.generar_secuencia()
        self.respuesta_correcta = respuesta
        texto = ", ".join(str(n) for n in secuencia)
        self.label_secuencia.config(text=f"Secuencia: {texto}, ...")
        self.entrada.delete(0, tk.END)


    # ---------------------------------------------------------
    # Verificación
    # ---------------------------------------------------------
    def verificar_respuesta(self):
        """Valida la respuesta del jugador."""
        if not self.juego_activo:
            return

        try:
            valor = int(self.entrada.get())
        except ValueError:
            messagebox.showwarning("Error", "Debes escribir un número válido.")
            return

        if valor == self.respuesta_correcta:
            self.puntaje += 1
        else:
            messagebox.showinfo("Incorrecto",
                                f"La respuesta correcta era: {self.respuesta_correcta}")

        self.actualizar_puntaje()
        self.nueva_secuencia()


    # ---------------------------------------------------------
    # Temporizador
    # ---------------------------------------------------------
    def actualizar_puntaje(self):
        self.label_puntaje.config(text=f"Puntaje: {self.puntaje}")

    def actualizar_tiempo(self):
        """Controla el tiempo del juego."""
        if self.tiempo_restante > 0 and self.juego_activo:
            minutos = self.tiempo_restante // 60
            segundos = self.tiempo_restante % 60
            self.temporizador.config(text=f"Tiempo: {minutos}:{segundos:02d}")
            self.tiempo_restante -= 1
            self.root.after(1000, self.actualizar_tiempo)
        else:
            self.terminar_juego()


    # ---------------------------------------------------------
    # Fin del juego
    # ---------------------------------------------------------
    def terminar_juego(self):
        """Termina el juego cuando llega a 0 segundos."""
        self.juego_activo = False
        self.boton_responder.config(state="disabled")
        self.boton_iniciar.config(state="normal")
        messagebox.showinfo("Fin del juego",
                            f"Tiempo terminado.\nPuntaje final: {self.puntaje}")


# ---------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# ---------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoSecuencias(root)
    root.mainloop()
