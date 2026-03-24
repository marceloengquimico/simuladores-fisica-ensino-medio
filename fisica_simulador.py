"""
Simulador de Física — Ensino Médio  v2.0
Queda Livre · Lançamento Vertical · Horizontal · Oblíquo

Novidades v2.0:
  • Gravidade: g=10 (simplificado), g=9,81 (Terra) ou outro planeta
  • Câmera lenta (até 0,05×)
  • Painel de equações horárias por modo
  • Comparação Terra × Planeta na mesma tela

Build: pyinstaller --onefile --windowed fisica_simulador.py
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ─── PALETA ───────────────────────────────────────────────────────
BG      = "#0d1117"
PANEL   = "#161b22"
PANEL2  = "#1c2128"
BORDER  = "#21262d"
ACCENT  = "#58a6ff"
GREEN   = "#3fb950"
ORANGE  = "#f78166"
YELLOW  = "#e3b341"
PURPLE  = "#bc8cff"
CYAN    = "#39d0d8"
PINK    = "#ff7eb6"
TEXT    = "#e6edf3"
MUTED   = "#7d8590"
LABEL   = "#8b949e"
ENTRY   = "#0d1117"

# ─── GRAVIDADES ───────────────────────────────────────────────────
GRAVITY_PRESETS = {
    "g = 10  (simplificado)": 10.0,
    "g = 9,81  (Terra real)": 9.81,
}

PLANETS = {
    "☿  Mercúrio":  3.70,
    "♀  Vênus":     8.87,
    "🌍  Terra":    9.81,
    "🌙  Lua":      1.62,
    "♂  Marte":    3.72,
    "♃  Júpiter": 24.79,
    "♄  Saturno":  10.44,
    "⛢  Urano":    8.69,
    "♆  Netuno":   11.15,
    "✦  Plutão":    0.62,
}

PLANET_COLORS = {
    "☿  Mercúrio": "#aaaaaa",
    "♀  Vênus":    "#f5c842",
    "🌍  Terra":   "#3fb950",
    "🌙  Lua":     "#c8d0d8",
    "♂  Marte":   "#f78166",
    "♃  Júpiter": "#e8c07a",
    "♄  Saturno":  "#d4b483",
    "⛢  Urano":   "#7de8e8",
    "♆  Netuno":  "#5b8fe8",
    "✦  Plutão":   "#bc8cff",
}

MODES = ["Queda Livre", "Lançamento Vertical", "Lançamento Horizontal", "Lançamento Oblíquo"]
MODE_COLORS = {
    "Queda Livre":           ORANGE,
    "Lançamento Vertical":   GREEN,
    "Lançamento Horizontal": ACCENT,
    "Lançamento Oblíquo":    PURPLE,
}

# ─── EQUAÇÕES HORÁRIAS (texto didático) ───────────────────────────
EQUATIONS = {
    "Queda Livre": [
        ("Posição",    "y(t) = h₀ − ½·g·t²"),
        ("Velocidade", "v(t) = g·t  (↓)"),
        ("Tempo",      "t = √(2·h₀/g)"),
        ("V impacto",  "v = √(2·g·h₀)"),
    ],
    "Lançamento Vertical": [
        ("Posição",    "y(t) = h₀ + v₀·t − ½·g·t²"),
        ("Velocidade", "v(t) = v₀ − g·t"),
        ("H máxima",   "H = h₀ + v₀²/(2g)"),
        ("T subida",   "t_s = v₀/g"),
    ],
    "Lançamento Horizontal": [
        ("Horizontal", "x(t) = v₀·t"),
        ("Vertical",   "y(t) = h₀ − ½·g·t²"),
        ("Alcance",    "R = v₀·√(2·h₀/g)"),
        ("V impacto",  "v = √(v₀² + 2·g·h₀)"),
    ],
    "Lançamento Oblíquo": [
        ("x(t)",       "x = v₀·cos θ · t"),
        ("y(t)",       "y = h₀ + v₀·sen θ·t − ½g·t²"),
        ("H máxima",   "H = h₀ + (v₀·sen θ)²/(2g)"),
        ("Alcance",    "R = v₀²·sen(2θ)/g  (h₀=0)"),
    ],
}

# ─── FÍSICA ───────────────────────────────────────────────────────
def simulate(mode, h0, v0, angle_deg, g, dt=0.02):
    angle = np.radians(angle_deg)
    if mode == "Queda Livre":
        vx0, vy0 = 0.0, 0.0
    elif mode == "Lançamento Vertical":
        vx0, vy0 = 0.0, float(v0)
    elif mode == "Lançamento Horizontal":
        vx0, vy0 = float(v0), 0.0
    else:
        vx0 = v0 * np.cos(angle)
        vy0 = v0 * np.sin(angle)

    t_l, x_l, y_l, vx_l, vy_l = [], [], [], [], []
    t, x, y, vx, vy = 0.0, 0.0, float(h0), vx0, vy0

    for _ in range(20000):
        t_l.append(t); x_l.append(x); y_l.append(y)
        vx_l.append(vx); vy_l.append(vy)
        if y <= 0 and t > 0:
            break
        vy_new = vy - g * dt
        x  += vx * dt
        y  += vy * dt - 0.5 * g * dt**2
        if y < 0: y = 0.0
        vy  = vy_new
        t  += dt

    return (np.array(t_l), np.array(x_l),
            np.array(y_l), np.array(vx_l), np.array(vy_l))


# ─── APP ──────────────────────────────────────────────────────────
class PhysicsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Física — Ensino Médio  v2.0")
        self.configure(bg=BG)
        self.geometry("1280x760")
        self.minsize(1050, 640)
        self.resizable(True, True)

        # variáveis
        self.mode        = tk.StringVar(value=MODES[0])
        self.var_h0      = tk.DoubleVar(value=50.0)
        self.var_v0      = tk.DoubleVar(value=20.0)
        self.var_angle   = tk.DoubleVar(value=45.0)
        self.var_speed   = tk.DoubleVar(value=1.0)

        # gravidade
        self.grav_mode   = tk.StringVar(value="g = 10  (simplificado)")
        self.planet_var  = tk.StringVar(value="🌍  Terra")
        self._g          = 10.0

        # animação
        self._frame   = 0
        self._data    = None
        self._running = False

        self._build_ui()
        self._run_simulation()

    # ─────────────────────────────────────────────────────────────
    def _current_g(self):
        gm = self.grav_mode.get()
        if gm in GRAVITY_PRESETS:
            return GRAVITY_PRESETS[gm]
        # planeta
        return PLANETS.get(self.planet_var.get(), 9.81)

    # ── CONSTRUÇÃO DA UI ─────────────────────────────────────────
    def _build_ui(self):
        # ── HEADER ──
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(12, 0))
        tk.Label(hdr, text="Simulador de Física",
                 bg=BG, fg=TEXT, font=("Courier", 17, "bold")).pack(side="left")
        tk.Label(hdr, text="ENSINO MÉDIO · CINEMÁTICA",
                 bg=BG, fg=MUTED, font=("Courier", 9)).pack(side="left", padx=14, pady=(5,0))
        tk.Label(hdr, text=" v2.0 ",
                 bg="#1e3a5f", fg=ACCENT, font=("Courier", 9, "bold"), padx=6).pack(side="right", pady=4)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=14, pady=8)

        # ── SIDEBAR ──
        sb = tk.Frame(body, bg=BG, width=280)
        sb.pack(side="left", fill="y", padx=(0, 10))
        sb.pack_propagate(False)

        # — Tipo de lançamento —
        self._section(sb, "TIPO DE LANÇAMENTO")
        for m in MODES:
            c = MODE_COLORS[m]
            tk.Radiobutton(
                sb, text=m, variable=self.mode, value=m,
                bg=PANEL, fg=TEXT, selectcolor=c,
                activebackground=PANEL, activeforeground=TEXT,
                font=("Courier", 10), indicatoron=False,
                relief="flat", padx=10, pady=6, width=25,
                cursor="hand2", command=self._on_mode_change
            ).pack(fill="x", pady=2)

        # — Gravidade —
        self._section(sb, "GRAVIDADE")
        grav_frame = tk.Frame(sb, bg=PANEL,
                              highlightbackground=BORDER, highlightthickness=1)
        grav_frame.pack(fill="x", pady=2)

        for gkey in GRAVITY_PRESETS:
            col = GREEN if "10" in gkey else CYAN
            tk.Radiobutton(
                grav_frame, text=gkey, variable=self.grav_mode, value=gkey,
                bg=PANEL, fg=TEXT, selectcolor=col,
                activebackground=PANEL, activeforeground=TEXT,
                font=("Courier", 9), indicatoron=False,
                relief="flat", padx=8, pady=4, width=26,
                cursor="hand2", command=self._on_grav_change
            ).pack(fill="x", padx=4, pady=2)

        # Separador "Outro planeta"
        sep_row = tk.Frame(grav_frame, bg=PANEL)
        sep_row.pack(fill="x", padx=4, pady=(4, 2))
        tk.Frame(sep_row, bg=BORDER, height=1).pack(fill="x")

        planet_rb = tk.Radiobutton(
            grav_frame, text="Outro planeta ↓", variable=self.grav_mode, value="planeta",
            bg=PANEL, fg=TEXT, selectcolor=ORANGE,
            activebackground=PANEL, activeforeground=TEXT,
            font=("Courier", 9), indicatoron=False,
            relief="flat", padx=8, pady=4, width=26,
            cursor="hand2", command=self._on_grav_change
        )
        planet_rb.pack(fill="x", padx=4, pady=(0, 2))

        # Dropdown de planetas
        style = ttk.Style()
        style.theme_use("default")
        style.configure("P.TCombobox",
                        background=PANEL, fieldbackground=ENTRY,
                        foreground=TEXT, selectbackground=BORDER,
                        font=("Courier", 9))
        self.planet_combo = ttk.Combobox(
            grav_frame, textvariable=self.planet_var,
            values=list(PLANETS.keys()),
            state="readonly", width=22,
            style="P.TCombobox"
        )
        self.planet_combo.pack(padx=8, pady=(0, 8), fill="x")
        self.planet_combo.bind("<<ComboboxSelected>>", self._on_planet_change)

        # Label g atual
        self.lbl_g = tk.Label(sb, text="",
                              bg=BG, fg=YELLOW,
                              font=("Courier", 10, "bold"), anchor="w")
        self.lbl_g.pack(fill="x", pady=(4, 0))
        self._update_g_label()

        # — Parâmetros —
        self._section(sb, "PARÂMETROS")
        self.sl_h0    = self._slider(sb, "Altura inicial  h₀ (m)",     self.var_h0,    0,  200, 1)
        self.sl_v0    = self._slider(sb, "Velocidade inicial  v₀ (m/s)", self.var_v0,  0,   80, 1)
        self.sl_angle = self._slider(sb, "Ângulo  θ (°)",               self.var_angle, 1,   89, 1)

        # — Velocidade da animação (inclui câmera lenta) —
        self._section(sb, "VELOCIDADE DA ANIMAÇÃO")
        speed_frame = tk.Frame(sb, bg=PANEL,
                               highlightbackground=BORDER, highlightthickness=1)
        speed_frame.pack(fill="x", pady=2)

        speed_inner = tk.Frame(speed_frame, bg=PANEL)
        speed_inner.pack(fill="x", padx=8, pady=6)

        self.lbl_speed = tk.Label(speed_inner, text="1,00×",
                                   bg=ENTRY, fg=YELLOW,
                                   font=("Courier", 11, "bold"),
                                   width=7, anchor="e", padx=4)
        self.lbl_speed.pack(side="right")

        self.sl_speed = tk.Scale(speed_inner, from_=0.05, to=5.0,
                                  resolution=0.05,
                                  orient="horizontal", variable=self.var_speed,
                                  command=self._on_speed_change,
                                  bg=PANEL, fg=TEXT,
                                  troughcolor=BORDER,
                                  activebackground=YELLOW,
                                  highlightthickness=0, sliderrelief="flat",
                                  sliderlength=14, showvalue=False, length=155)
        self.sl_speed.pack(side="left", fill="x", expand=True)

        # Botões de atalho de velocidade
        btn_row = tk.Frame(speed_frame, bg=PANEL)
        btn_row.pack(fill="x", padx=8, pady=(0, 6))
        speed_shortcuts = [("🐢 0,1×", 0.1), ("🐌 0,25×", 0.25),
                           ("▶ 1×", 1.0), ("⚡ 3×", 3.0)]
        for label, val in speed_shortcuts:
            tk.Button(btn_row, text=label,
                      bg=PANEL2, fg=LABEL,
                      font=("Courier", 7), relief="flat",
                      cursor="hand2", padx=4, pady=2,
                      command=lambda v=val: self._set_speed(v)
                      ).pack(side="left", expand=True, fill="x", padx=1)

        # — Botões —
        btn_outer = tk.Frame(sb, bg=BG)
        btn_outer.pack(fill="x", pady=(10, 0))

        self.btn_play = tk.Button(btn_outer, text="▶  Iniciar",
                                   bg=GREEN, fg=BG,
                                   font=("Courier", 11, "bold"),
                                   relief="flat", padx=10, pady=8,
                                   cursor="hand2",
                                   command=self._toggle_play)
        self.btn_play.pack(fill="x", pady=(0, 5))

        tk.Button(btn_outer, text="↺  Reiniciar",
                  bg=PANEL, fg=TEXT,
                  font=("Courier", 10),
                  relief="flat", padx=10, pady=5,
                  cursor="hand2",
                  command=self._run_simulation).pack(fill="x")

        # — Resultados —
        self._section(sb, "RESULTADOS")
        res_f = tk.Frame(sb, bg=PANEL,
                         highlightbackground=BORDER, highlightthickness=1)
        res_f.pack(fill="x")
        self.lbl_info = tk.Label(res_f, text="",
                                  bg=PANEL, fg=TEXT,
                                  font=("Courier", 9),
                                  justify="left", anchor="w",
                                  padx=10, pady=8)
        self.lbl_info.pack(fill="x")

        # ── COLUNA CENTRAL: gráfico + mini-charts ──
        center = tk.Frame(body, bg=BG)
        center.pack(side="left", fill="both", expand=True)

        self.fig_main = Figure(figsize=(5.2, 3.6), facecolor=BG)
        self.ax_main  = self.fig_main.add_subplot(111)
        self._style_ax(self.ax_main)
        self.canvas_main = FigureCanvasTkAgg(self.fig_main, master=center)
        self.canvas_main.get_tk_widget().pack(fill="both", expand=True)

        mini_row = tk.Frame(center, bg=BG)
        mini_row.pack(fill="x", pady=(6, 0))

        for attr, title, col in [
            ("fig_vy", "Vy × t (m/s)", ORANGE),
            ("fig_ht", "h × t (m)",    ACCENT),
            ("fig_vx", "Vx × t (m/s)", PURPLE),
        ]:
            fig = Figure(figsize=(2.2, 1.6), facecolor=BG)
            ax  = fig.add_subplot(111)
            self._style_ax(ax, tiny=True)
            canvas = FigureCanvasTkAgg(fig, master=mini_row)
            canvas.get_tk_widget().pack(side="left", fill="both",
                                         expand=True, padx=(0, 4))
            setattr(self, attr, fig)
            setattr(self, attr.replace("fig_", "ax_"), ax)
            setattr(self, attr.replace("fig_", "canvas_"), canvas)

        # ── COLUNA DIREITA: equações + planeta ──
        right = tk.Frame(body, bg=BG, width=230)
        right.pack(side="left", fill="y", padx=(10, 0))
        right.pack_propagate(False)

        self._section(right, "EQUAÇÕES HORÁRIAS")
        self.eq_frame = tk.Frame(right, bg=PANEL,
                                  highlightbackground=BORDER,
                                  highlightthickness=1)
        self.eq_frame.pack(fill="x")

        self._section(right, "COMPARAR PLANETAS")
        cmp_frame = tk.Frame(right, bg=PANEL,
                              highlightbackground=BORDER, highlightthickness=1)
        cmp_frame.pack(fill="x")
        tk.Label(cmp_frame,
                 text="Tempo de queda de h₀\n(para o modo atual)",
                 bg=PANEL, fg=MUTED, font=("Courier", 7),
                 justify="left").pack(anchor="w", padx=8, pady=(6, 2))
        self.planet_cmp = tk.Text(cmp_frame, bg=PANEL, fg=TEXT,
                                   font=("Courier", 8),
                                   height=12, width=26,
                                   relief="flat", state="disabled",
                                   highlightthickness=0)
        self.planet_cmp.pack(padx=6, pady=(0, 6))

    # ─── HELPERS ─────────────────────────────────────────────────
    def _section(self, parent, title):
        tk.Label(parent, text=title,
                 bg=BG, fg=MUTED,
                 font=("Courier", 8, "bold"),
                 anchor="w").pack(fill="x", pady=(10, 3))

    def _slider(self, parent, label, var, lo, hi, res, fmt="{:.0f}"):
        grp = tk.Frame(parent, bg=PANEL,
                       highlightbackground=BORDER, highlightthickness=1)
        grp.pack(fill="x", pady=2)
        row = tk.Frame(grp, bg=PANEL)
        row.pack(fill="x", padx=8, pady=4)
        tk.Label(row, text=label, bg=PANEL, fg=LABEL,
                 font=("Courier", 7)).pack(anchor="w")
        r2 = tk.Frame(row, bg=PANEL)
        r2.pack(fill="x")
        val_lbl = tk.Label(r2, text=fmt.format(var.get()),
                           bg=ENTRY, fg=TEXT,
                           font=("Courier", 10, "bold"),
                           width=7, anchor="e", padx=4)
        val_lbl.pack(side="right")

        def _cmd(v, lbl=val_lbl, f=fmt, variable=var):
            variable.set(float(v))
            lbl.config(text=f.format(float(v)))
            if not self._running:
                self._run_simulation()

        sl = tk.Scale(r2, from_=lo, to=hi, resolution=res,
                      orient="horizontal", variable=var,
                      command=_cmd, bg=PANEL, fg=TEXT,
                      troughcolor=BORDER, activebackground=ACCENT,
                      highlightthickness=0, sliderrelief="flat",
                      sliderlength=14, showvalue=False, length=150)
        sl.pack(side="left", fill="x", expand=True)
        return sl

    def _style_ax(self, ax, tiny=False):
        ax.set_facecolor(BG)
        ax.figure.patch.set_facecolor(BG)
        for sp in ax.spines.values():
            sp.set_edgecolor(BORDER)
        fs = 6 if tiny else 8
        ax.tick_params(colors=MUTED, labelsize=fs)
        ax.xaxis.label.set_color(MUTED)
        ax.yaxis.label.set_color(MUTED)
        ax.grid(True, color=BORDER, lw=0.5, ls="--")

    def _update_g_label(self):
        g = self._current_g()
        gm = self.grav_mode.get()
        if gm == "planeta":
            pname = self.planet_var.get().split("  ")[-1]
            self.lbl_g.config(text=f"  g = {g:.2f} m/s²  ({pname})")
        else:
            self.lbl_g.config(text=f"  g = {g:.2f} m/s²")

    # ─── EVENTOS ─────────────────────────────────────────────────
    def _on_mode_change(self):
        m = self.mode.get()
        self.sl_v0.config(state="disabled" if m == "Queda Livre" else "normal")
        self.sl_angle.config(state="normal" if m == "Lançamento Oblíquo" else "disabled")
        self._update_equations()
        self._run_simulation()

    def _on_grav_change(self):
        # Habilita combo apenas se "planeta" estiver selecionado
        gm = self.grav_mode.get()
        self.planet_combo.config(state="readonly" if gm == "planeta" else "disabled")
        self._g = self._current_g()
        self._update_g_label()
        if not self._running:
            self._run_simulation()

    def _on_planet_change(self, event=None):
        self.grav_mode.set("planeta")
        self.planet_combo.config(state="readonly")
        self._g = self._current_g()
        self._update_g_label()
        if not self._running:
            self._run_simulation()

    def _on_speed_change(self, v):
        val = float(v)
        self.var_speed.set(val)
        self.lbl_speed.config(text=f"{val:.2f}×")

    def _set_speed(self, val):
        self.var_speed.set(val)
        self.sl_speed.set(val)
        self.lbl_speed.config(text=f"{val:.2f}×")

    # ─── PAINEL DE EQUAÇÕES ───────────────────────────────────────
    def _update_equations(self):
        for w in self.eq_frame.winfo_children():
            w.destroy()
        mode = self.mode.get()
        eqs  = EQUATIONS.get(mode, [])
        g    = self._current_g()

        tk.Label(self.eq_frame, text=f"[ {mode} ]",
                 bg=PANEL, fg=MODE_COLORS[mode],
                 font=("Courier", 9, "bold"),
                 anchor="w").pack(fill="x", padx=8, pady=(8, 4))

        for name, formula in eqs:
            row = tk.Frame(self.eq_frame, bg=PANEL2)
            row.pack(fill="x", padx=6, pady=2)
            tk.Label(row, text=f"  {name}:",
                     bg=PANEL2, fg=LABEL,
                     font=("Courier", 7),
                     width=10, anchor="w").pack(side="left")
            tk.Label(row, text=formula,
                     bg=PANEL2, fg=YELLOW,
                     font=("Courier", 8, "bold"),
                     anchor="w").pack(side="left", padx=4)

        # Valor de g em uso
        tk.Frame(self.eq_frame, bg=BORDER, height=1).pack(fill="x", padx=6, pady=6)
        tk.Label(self.eq_frame,
                 text=f"  g = {g:.2f} m/s²  em uso",
                 bg=PANEL, fg=CYAN,
                 font=("Courier", 8, "bold"),
                 anchor="w").pack(fill="x", padx=6, pady=(0, 8))

    # ─── TABELA COMPARATIVA DE PLANETAS ───────────────────────────
    def _update_planet_table(self):
        h0    = self.var_h0.get()
        v0    = self.var_v0.get()
        mode  = self.mode.get()

        self.planet_cmp.config(state="normal")
        self.planet_cmp.delete("1.0", "end")

        # Header
        self.planet_cmp.insert("end", f"{'Planeta':<14} {'g':>5}  {'t(s)':>6}\n")
        self.planet_cmp.insert("end", "─" * 28 + "\n")

        for planet, g in PLANETS.items():
            pname = planet.split("  ")[-1]
            if mode == "Queda Livre" and h0 > 0:
                t_val = np.sqrt(2 * h0 / g)
            elif mode == "Lançamento Vertical" and v0 > 0:
                t_val = (2 * v0 / g) + np.sqrt(2 * h0 / g) if h0 > 0 else 2 * v0 / g
            elif mode == "Lançamento Horizontal" and h0 > 0:
                t_val = np.sqrt(2 * h0 / g)
            else:
                t_val = None

            marker = " ◀" if planet == self.planet_var.get() and self.grav_mode.get() == "planeta" else ""
            if t_val is not None:
                line = f"{pname:<13} {g:>5.2f}  {t_val:>6.2f}{marker}\n"
            else:
                line = f"{pname:<13} {g:>5.2f}     —\n"
            self.planet_cmp.insert("end", line)

        self.planet_cmp.config(state="disabled")

    # ─── SIMULAÇÃO ────────────────────────────────────────────────
    def _run_simulation(self):
        self._stop_anim()
        self._running = False
        self.btn_play.config(text="▶  Iniciar", bg=GREEN)

        mode  = self.mode.get()
        h0    = self.var_h0.get()
        v0    = self.var_v0.get()
        angle = self.var_angle.get()
        g     = self._current_g()

        self._update_equations()
        self._update_planet_table()

        t, x, y, vx, vy = simulate(mode, h0, v0, angle, g)
        self._data  = (t, x, y, vx, vy)
        self._frame = 0
        color = MODE_COLORS[mode]

        # ── Gráfico principal ──
        ax = self.ax_main
        ax.cla()
        self._style_ax(ax)
        ax.plot(x, y, color=color, alpha=0.25, lw=1.5, ls="--")
        ax.set_xlabel("x  (m)", fontsize=8)
        ax.set_ylabel("y  (m)", fontsize=8)

        # Título com g
        g_label = f"g = {g:.2f} m/s²"
        ax.set_title(f"{mode}  ·  {g_label}",
                     color=color, fontsize=10, fontweight="bold", pad=6)

        xlim_r = max(x.max() + x.max() * 0.12, 3)
        ax.set_xlim(x.min() - 1, xlim_r)
        ax.set_ylim(-3, max(y.max() * 1.18, h0 * 1.1, 6))

        ax.axhline(0, color=MUTED, lw=1.0)
        ax.fill_between([x.min()-2, xlim_r + 5], [-3, -3], [0, 0],
                        color="#21262d", alpha=0.5)

        self._traj_line, = ax.plot([], [], color=color, lw=2)
        self._ball,      = ax.plot([], [], "o", color=color, ms=13,
                                   markeredgecolor="white", markeredgewidth=1.5, zorder=10)
        self._vel_arrow  = None
        self._time_text  = ax.text(
            0.02, 0.97, "", transform=ax.transAxes,
            color=TEXT, fontsize=9, fontfamily="monospace", va="top",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=PANEL, alpha=0.7)
        )
        self.fig_main.tight_layout(pad=1.1)
        self.canvas_main.draw()

        # ── Mini charts ──
        configs = [
            (self.ax_vy, self.fig_vy, self.canvas_vy, t, vy, ORANGE,  "Vy × t  (m/s)"),
            (self.ax_ht, self.fig_ht, self.canvas_ht, t, y,  ACCENT,  "h × t   (m)"),
            (self.ax_vx, self.fig_vx, self.canvas_vx, t, vx, PURPLE,  "Vx × t  (m/s)"),
        ]
        self._mini_dots = []
        for ax_m, fig_m, cv_m, tx, ty, col, title in configs:
            ax_m.cla()
            self._style_ax(ax_m, tiny=True)
            ax_m.plot(tx, ty, color=col, lw=1.5)
            if title.startswith("Vy") or title.startswith("Vx"):
                ax_m.axhline(0, color=MUTED, lw=0.7)
            ax_m.set_title(title, color=col, fontsize=7, pad=3)
            dot, = ax_m.plot([], [], "o", color=col, ms=5)
            self._mini_dots.append((dot, tx, ty))
            fig_m.tight_layout(pad=0.7)
            cv_m.draw()

        # ── Resultados ──
        t_total = t[-1]
        h_max   = y.max()
        v_imp   = np.sqrt(vx[-1]**2 + vy[-1]**2)
        x_max   = x[-1]
        self.lbl_info.config(text=(
            f"  Tempo total:  {t_total:.2f} s\n"
            f"  Altura máx:   {h_max:.2f} m\n"
            f"  Alcance:      {x_max:.2f} m\n"
            f"  V impacto:    {v_imp:.2f} m/s\n"
            f"  g usado:      {g:.2f} m/s²"
        ))

    # ─── ANIMAÇÃO ────────────────────────────────────────────────
    def _toggle_play(self):
        if self._running:
            self._stop_anim()
            self._running = False
            self.btn_play.config(text="▶  Continuar", bg=GREEN)
        else:
            self._running = True
            self.btn_play.config(text="⏸  Pausar", bg=YELLOW)
            self._start_anim()

    def _start_anim(self):
        t, x, y, vx, vy = self._data
        color = MODE_COLORS[self.mode.get()]

        def _loop():
            if not self._running:
                return
            speed = self.var_speed.get()
            i = self._frame

            if i >= len(t):
                self._stop_anim()
                self._running = False
                self.btn_play.config(text="↺  Assistir novamente", bg=GREEN)
                return

            # Bola e trajetória
            self._traj_line.set_data(x[:i+1], y[:i+1])
            self._ball.set_data([x[i]], [y[i]])

            # Texto em tempo real
            v_total = np.sqrt(vx[i]**2 + vy[i]**2)
            spd_label = f"  🐢 {speed:.2f}×" if speed < 0.5 else f"  {speed:.2f}×"
            self._time_text.set_text(
                f"t = {t[i]:.2f} s\n"
                f"y = {y[i]:.2f} m\n"
                f"|v| = {v_total:.2f} m/s"
                + (f"\n{spd_label}" if speed < 0.8 else "")
            )

            # Vetor velocidade
            if self._vel_arrow:
                try: self._vel_arrow.remove()
                except: pass
            xlim = self.ax_main.get_xlim()
            scale = max((xlim[1] - xlim[0]) * 0.035, 0.4)
            self._vel_arrow = self.ax_main.annotate(
                "", xy=(x[i] + vx[i]*scale, y[i] + vy[i]*scale),
                xytext=(x[i], y[i]),
                arrowprops=dict(arrowstyle="->", color=YELLOW, lw=2, mutation_scale=14)
            )

            # Mini dots
            for (dot, tx, ty), cv in zip(self._mini_dots,
                                          [self.canvas_vy, self.canvas_ht, self.canvas_vx]):
                dot.set_data([tx[i]], [ty[i]])
                cv.draw_idle()

            self.canvas_main.draw_idle()

            # Avanço de frames: câmera lenta = skip=1, rápido = skip>1
            skip = max(1, int(speed * 2))
            self._frame = min(i + skip, len(t))

            # Intervalo real: câmera lenta aumenta o delay entre frames
            # speed=0.05 → interval=800ms; speed=1 → interval=40ms
            interval = max(10, int(40 / speed))
            self._after_id = self.after(interval, _loop)

        self._after_id = self.after(10, _loop)

    def _stop_anim(self):
        if hasattr(self, "_after_id"):
            try: self.after_cancel(self._after_id)
            except: pass

    def on_close(self):
        self._stop_anim()
        self.destroy()


# ─── MAIN ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = PhysicsApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
