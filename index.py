import random
import tkinter as tk


MARKET_NEWS = [
    {"headline": "Apple unveils new VR glasses and shakes the market!", "asset": "AAPL", "impact":  0.15},
    {"headline": "Global semiconductor crisis slows down Tesla production.", "asset": "TSLA", "impact": -0.20},
    {"headline": "A European country adopts Bitcoin as legal tender.", "asset": "BTC",  "impact":  0.30},
    {"headline": "Rumors of new government regulations crush cryptocurrencies.",  "asset": "BTC",  "impact": -0.25},
    {"headline": "Massive Apple server failure leaves millions without service.", "asset": "AAPL", "impact": -0.10},
    {"headline": "Tesla breaks electric vehicle sales record.", "asset": "TSLA", "impact":  0.12},
    {"headline": "Google announces a strategic alliance with Apple.","asset": "AAPL", "impact":  0.08},
    {"headline": "Chinese government bans Bitcoin transactions.","asset": "BTC",  "impact": -0.18},
    {"headline": "Tesla launches new battery with record-breaking range.","asset": "TSLA", "impact":  0.22},
]

# paleta de colores del tema oscuro
BG       = "#0d1117"
BG_CARD  = "#161b22"
BORDER   = "#30363d"
TEXT     = "#e6edf3"
MUTED    = "#8b949e"
GOLD     = "#e3b341"
GREEN    = "#3fb950"
RED      = "#f85149"
BLUE     = "#388bfd"
BTN_BG   = "#21262d"


def apply_fluctuations(assets):
    # guardamos los precios del mes anterior para calcular el % de cambio real
    previous_prices = dict(assets)

    # variacion aleatoria mensual para todos los activos
    for asset in assets:
        assets[asset] *= (1 + random.uniform(-0.05, 0.05))

    # impacto extra de la noticia del mes sobre un activo concreto
    news = random.choice(MARKET_NEWS)
    assets[news["asset"]] *= (1 + news["impact"])

    changes = {a: (assets[a] / previous_prices[a]) - 1 for a in assets}
    return news, changes


# ── helpers de estilo ──────────────────────────────────────────────────────

def make_card(parent):
    """Frame con fondo de tarjeta y borde sutil."""
    return tk.Frame(parent, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)


def make_separator(parent):
    """Linea horizontal separadora."""
    return tk.Frame(parent, bg=BORDER, height=1)


def style_option_menu(menu):
    """Aplica el tema oscuro al widget OptionMenu."""
    menu.config(
        bg=BTN_BG, fg=TEXT, activebackground=BORDER, activeforeground=TEXT,
        relief="flat", font=("Courier New", 10),
        highlightthickness=1, highlightbackground=BORDER, highlightcolor=BLUE,
    )
    menu["menu"].config(
        bg=BG_CARD, fg=TEXT,
        activebackground=BLUE, activeforeground="white",
        font=("Courier New", 10),
    )


# ── aplicacion principal ───────────────────────────────────────────────────

class MarketSimulator(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Financial Market Simulator")
        self.configure(bg=BG)
        self.resizable(False, False)

        # estado del juego
        self.assets = {"AAPL": 150.0, "TSLA": 100.0, "BTC": 500.0}
        self.portfolio = {"AAPL": 0.0, "TSLA": 0.0, "BTC": 0.0}
        self.capital = 10000.0
        self.initial_capital = 10000.0
        self.month = 0
        self.news = None
        self.changes = {a: 0.0 for a in self.assets}

        self._build_ui()
        self._advance_month()

    # ── construccion de la interfaz ────────────────────────────────────────

    def _build_ui(self):
        PAD = 12

        # titulo
        tk.Label(
            self, text="FINANCIAL MARKET SIMULATOR",
            bg=BG, fg=GOLD, font=("Courier New", 16, "bold"),
        ).pack(pady=(PAD, 4))

        # linea de mes y efectivo
        self.lbl_header = tk.Label(self, text="", bg=BG, fg=MUTED, font=("Courier New", 10))
        self.lbl_header.pack()

        make_separator(self).pack(fill="x", padx=PAD, pady=6)

        # tarjeta: noticia del mes
        news_card = make_card(self)
        news_card.pack(fill="x", padx=PAD, pady=(0, 6))

        tk.Label(news_card, text="EVENT OF THE MONTH", bg=BG_CARD, fg=MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w", padx=10, pady=(8, 2))

        self.lbl_headline = tk.Label(
            news_card, text="", bg=BG_CARD, fg=TEXT,
            font=("Courier New", 10), wraplength=560, justify="left",
        )
        self.lbl_headline.pack(anchor="w", padx=10, pady=(0, 4))

        self.lbl_news_detail = tk.Label(news_card, text="", bg=BG_CARD, fg=MUTED,
                                        font=("Courier New", 9))
        self.lbl_news_detail.pack(anchor="w", padx=10, pady=(0, 8))

        # tarjeta: precios del mercado
        prices_card = make_card(self)
        prices_card.pack(fill="x", padx=PAD, pady=(0, 6))

        tk.Label(prices_card, text="MARKET PRICES  (locked this month)",
                 bg=BG_CARD, fg=MUTED, font=("Courier New", 8, "bold")).pack(anchor="w", padx=10, pady=(8, 4))

        self.price_labels = {}
        for asset in self.assets:
            row = tk.Frame(prices_card, bg=BG_CARD)
            row.pack(fill="x", padx=10, pady=2)

            tk.Label(row, text=asset, bg=BG_CARD, fg=TEXT,
                     font=("Courier New", 11, "bold"), width=6).pack(side="left")

            lbl_price = tk.Label(row, text="", bg=BG_CARD, fg=TEXT,
                                 font=("Courier New", 11), width=12, anchor="e")
            lbl_price.pack(side="left")

            lbl_chg = tk.Label(row, text="", bg=BG_CARD,
                               font=("Courier New", 10), width=10, anchor="e")
            lbl_chg.pack(side="left")

            self.price_labels[asset] = (lbl_price, lbl_chg)

        tk.Label(prices_card, text="", bg=BG_CARD, height=1).pack()

        # tarjeta: cartera
        portfolio_card = make_card(self)
        portfolio_card.pack(fill="x", padx=PAD, pady=(0, 6))

        tk.Label(portfolio_card, text="YOUR PORTFOLIO", bg=BG_CARD, fg=MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w", padx=10, pady=(8, 4))

        # este frame se vacia y reconstruye en cada actualizacion
        self.portfolio_frame = tk.Frame(portfolio_card, bg=BG_CARD)
        self.portfolio_frame.pack(fill="x", padx=10)

        self.lbl_networth = tk.Label(portfolio_card, text="", bg=BG_CARD, fg=GOLD,
                                     font=("Courier New", 10, "bold"))
        self.lbl_networth.pack(anchor="e", padx=10, pady=(4, 8))

        # tarjeta: operaciones
        trade_card = make_card(self)
        trade_card.pack(fill="x", padx=PAD, pady=(0, 6))

        tk.Label(trade_card, text="TRADE", bg=BG_CARD, fg=MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w", padx=10, pady=(8, 6))

        controls = tk.Frame(trade_card, bg=BG_CARD)
        controls.pack(padx=10, pady=(0, 10))

        tk.Label(controls, text="Asset:", bg=BG_CARD, fg=TEXT,
                 font=("Courier New", 10)).pack(side="left", padx=(0, 6))

        self.selected_asset = tk.StringVar(value="AAPL")
        asset_menu = tk.OptionMenu(controls, self.selected_asset, *self.assets.keys())
        style_option_menu(asset_menu)
        asset_menu.pack(side="left", padx=(0, 16))

        tk.Label(controls, text="Amount:", bg=BG_CARD, fg=TEXT,
                 font=("Courier New", 10)).pack(side="left", padx=(0, 6))

        self.entry_amount = tk.Entry(
            controls, font=("Courier New", 10), bg=BTN_BG, fg=TEXT,
            insertbackground=TEXT, relief="flat", width=10,
            highlightthickness=1, highlightbackground=BORDER, highlightcolor=BLUE,
        )
        self.entry_amount.pack(side="left", padx=(0, 16))

        self.btn_buy = tk.Button(
            controls, text="BUY", font=("Courier New", 10, "bold"),
            bg="#1f4f2a", fg=GREEN, activebackground="#2ea043", activeforeground="white",
            relief="flat", padx=14, pady=4, cursor="hand2",
            command=self._handle_buy,
        )
        self.btn_buy.pack(side="left", padx=(0, 6))

        self.btn_sell = tk.Button(
            controls, text="SELL", font=("Courier New", 10, "bold"),
            bg="#4a1b1b", fg=RED, activebackground="#da3633", activeforeground="white",
            relief="flat", padx=14, pady=4, cursor="hand2",
            command=self._handle_sell,
        )
        self.btn_sell.pack(side="left")

        # mensaje de feedback tras cada operacion
        self.lbl_feedback = tk.Label(self, text="", bg=BG, fg=MUTED,
                                     font=("Courier New", 9), wraplength=580)
        self.lbl_feedback.pack(pady=(2, 4))

        make_separator(self).pack(fill="x", padx=PAD, pady=4)

        # boton para avanzar al siguiente mes
        self.btn_next = tk.Button(
            self, text="Next Month  →",
            font=("Courier New", 11, "bold"),
            bg=BLUE, fg="white", activebackground="#58a6ff", activeforeground="white",
            relief="flat", padx=20, pady=8, cursor="hand2",
            command=self._advance_month,
        )
        self.btn_next.pack(pady=(4, 14))

    # ── logica del juego ───────────────────────────────────────────────────

    def _advance_month(self):
        self.month += 1

        if self.month > 12:
            self._show_final_results()
            return

        # fase 1: el mercado se mueve solo, precios quedan fijos hasta el proximo mes
        self.news, self.changes = apply_fluctuations(self.assets)
        self._refresh_display()
        self._set_feedback("")

        # en el ultimo mes cambiamos el texto del boton para indicar que termina
        if self.month == 12:
            self.btn_next.config(text="Finish Game")

    def _handle_buy(self):
        asset = self.selected_asset.get()
        raw = self.entry_amount.get().strip()

        try:
            amount = float(raw)
        except ValueError:
            self._set_feedback("Amount must be a number.  Example: 5  or  0.5", error=True)
            return

        if amount <= 0:
            self._set_feedback("Amount must be greater than zero.", error=True)
            return

        cost = amount * self.assets[asset]
        if cost > self.capital:
            # no dejamos que el usuario se quede en negativo
            self._set_feedback(
                f"Insufficient funds. You need ${cost:.2f} but only have ${self.capital:.2f}", error=True
            )
            return

        self.capital -= cost
        self.portfolio[asset] += amount
        self.entry_amount.delete(0, "end")
        self._set_feedback(
            f"Purchase complete: {amount:.4f} {asset} for ${cost:.2f}   Remaining cash: ${self.capital:.2f}", ok=True
        )
        self._refresh_display()

    def _handle_sell(self):
        asset = self.selected_asset.get()
        raw = self.entry_amount.get().strip()

        try:
            amount = float(raw)
        except ValueError:
            self._set_feedback("Amount must be a number.  Example: 2  or  0.25", error=True)
            return

        if amount <= 0:
            self._set_feedback("Amount must be greater than zero.", error=True)
            return

        if amount > self.portfolio[asset]:
            # tampoco dejamos vender lo que no tienes
            self._set_feedback(
                f"Insufficient shares. You only have {self.portfolio[asset]:.4f} units of {asset}.", error=True
            )
            return

        profit = amount * self.assets[asset]
        self.capital += profit
        self.portfolio[asset] -= amount
        self.entry_amount.delete(0, "end")
        self._set_feedback(
            f"Sale complete: {amount:.4f} {asset} for ${profit:.2f}   Current cash: ${self.capital:.2f}", ok=True
        )
        self._refresh_display()

    # ── actualizacion de la pantalla ───────────────────────────────────────

    def _refresh_display(self):
        # linea de mes y efectivo
        self.lbl_header.config(
            text=f"Month {self.month} / 12                 Cash: ${self.capital:,.2f}"
        )

        # noticia del mes
        self.lbl_headline.config(text=self.news["headline"])
        sign = "+" if self.news["impact"] >= 0 else ""
        color = GREEN if self.news["impact"] >= 0 else RED
        self.lbl_news_detail.config(
            text=f"Asset affected: {self.news['asset']}   Extra impact: {sign}{self.news['impact']*100:.1f}%",
            fg=color,
        )

        # precios con su variacion del mes
        for asset, (lbl_price, lbl_chg) in self.price_labels.items():
            lbl_price.config(text=f"${self.assets[asset]:,.2f}")
            chg = self.changes[asset]
            sign = "+" if chg >= 0 else ""
            color = GREEN if chg >= 0 else RED
            lbl_chg.config(text=f"{sign}{chg*100:.1f}%", fg=color)

        # cartera: vaciamos y reconstruimos las filas dinamicamente
        for widget in self.portfolio_frame.winfo_children():
            widget.destroy()

        has_assets = False
        for asset, amount in self.portfolio.items():
            if amount > 0:
                has_assets = True
                value = amount * self.assets[asset]
                row = tk.Frame(self.portfolio_frame, bg=BG_CARD)
                row.pack(fill="x", pady=1)
                tk.Label(row, text=f"{asset:<6}", bg=BG_CARD, fg=TEXT,
                         font=("Courier New", 10, "bold"), width=6).pack(side="left")
                tk.Label(row, text=f"{amount:.4f} units", bg=BG_CARD, fg=MUTED,
                         font=("Courier New", 10), width=16).pack(side="left")
                tk.Label(row, text=f"= ${value:,.2f}", bg=BG_CARD, fg=TEXT,
                         font=("Courier New", 10)).pack(side="left")

        if not has_assets:
            tk.Label(self.portfolio_frame, text="(no assets in portfolio)", bg=BG_CARD,
                     fg=MUTED, font=("Courier New", 10, "italic")).pack(anchor="w")

        # patrimonio total (efectivo + cartera)
        portfolio_value = sum(self.portfolio[a] * self.assets[a] for a in self.assets)
        net_worth = self.capital + portfolio_value
        diff = net_worth - self.initial_capital
        sign = "+" if diff >= 0 else ""
        color = GREEN if diff > 0 else (RED if diff < 0 else GOLD)
        self.lbl_networth.config(
            text=f"Net worth: ${net_worth:,.2f}   ({sign}${diff:,.2f})",
            fg=color,
        )

    def _set_feedback(self, msg, error=False, ok=False):
        color = RED if error else (GREEN if ok else MUTED)
        self.lbl_feedback.config(text=msg, fg=color)

    # ── pantalla de resultados finales ─────────────────────────────────────

    def _show_final_results(self):
        # limpiamos todos los widgets y construimos la pantalla de cierre
        for widget in self.winfo_children():
            widget.destroy()

        portfolio_value = sum(self.portfolio[a] * self.assets[a] for a in self.assets)
        net_worth = self.capital + portfolio_value
        gain = net_worth - self.initial_capital
        pct = (gain / self.initial_capital) * 100
        PAD = 16

        tk.Label(self, text="FINAL RESULTS", bg=BG, fg=GOLD,
                 font=("Courier New", 18, "bold")).pack(pady=(PAD, 4))
        tk.Label(self, text="12 Months Complete", bg=BG, fg=MUTED,
                 font=("Courier New", 10)).pack(pady=(0, PAD))

        make_separator(self).pack(fill="x", padx=PAD, pady=4)

        results_card = make_card(self)
        results_card.pack(fill="x", padx=PAD, pady=8)

        # filas del balance
        rows = [
            ("Starting capital", f"${self.initial_capital:,.2f}", TEXT),
            ("Remaining cash", f"${self.capital:,.2f}", TEXT),
        ]
        for asset, amount in self.portfolio.items():
            if amount > 0:
                value = amount * self.assets[asset]
                rows.append((f"  {asset} ({amount:.4f} units)", f"${value:,.2f}", MUTED))

        rows.append(("Portfolio value", f"${portfolio_value:,.2f}", TEXT))
        rows.append(("─" * 28, "─" * 12, BORDER))

        gain_color = GREEN if gain >= 0 else RED
        sign = "+" if gain >= 0 else ""
        rows.append(("Total net worth", f"${net_worth:,.2f}", GOLD))
        rows.append(("Net result", f"{sign}${gain:,.2f}  ({sign}{pct:.1f}%)", gain_color))

        for label, value, color in rows:
            row = tk.Frame(results_card, bg=BG_CARD)
            row.pack(fill="x", padx=16, pady=3)
            tk.Label(row, text=label, bg=BG_CARD, fg=MUTED,
                     font=("Courier New", 10), width=28, anchor="w").pack(side="left")
            tk.Label(row, text=value, bg=BG_CARD, fg=color,
                     font=("Courier New", 10, "bold"), anchor="e").pack(side="right")

        tk.Label(results_card, text="", bg=BG_CARD, height=1).pack()

        # mensaje personalizado segun el rendimiento
        if net_worth >= self.initial_capital * 1.30:
            msg = "Outstanding. You outperformed the market by a wide margin."
        elif net_worth >= self.initial_capital * 1.10:
            msg = "Good job. You finished clearly in the green."
        elif net_worth > self.initial_capital:
            msg = "You closed positive, though barely. Not bad for a first year."
        elif net_worth == self.initial_capital:
            msg = "Right where you started. Maybe be bolder next time."
        else:
            msg = "The market won this time. Analyze the news better next year."

        make_separator(self).pack(fill="x", padx=PAD, pady=8)

        tk.Label(self, text=msg, bg=BG, fg=TEXT,
                 font=("Courier New", 10, "italic"), wraplength=560).pack(pady=(0, PAD))

        tk.Button(
            self, text="Play Again",
            font=("Courier New", 11, "bold"),
            bg=BLUE, fg="white", activebackground="#58a6ff", activeforeground="white",
            relief="flat", padx=20, pady=8, cursor="hand2",
            command=self._restart,
        ).pack(pady=(0, PAD))

    def _restart(self):
        # reiniciamos el estado por completo y reconstruimos la interfaz
        self.assets = {"AAPL": 150.0, "TSLA": 100.0, "BTC": 500.0}
        self.portfolio = {"AAPL": 0.0, "TSLA": 0.0, "BTC": 0.0}
        self.capital = 10000.0
        self.initial_capital = 10000.0
        self.month = 0
        self.news = None
        self.changes = {a: 0.0 for a in self.assets}

        for widget in self.winfo_children():
            widget.destroy()

        self._build_ui()
        self._advance_month()


if __name__ == "__main__":
    app = MarketSimulator()
    app.mainloop()
