"""
Aplicación financiera monolítica en Streamlit.

Características:
- Un solo archivo: no necesita funciones_financieras.py.
- Conserva los datos al cambiar de módulo mediante st.session_state.
- Interfaz empresarial personalizada con HTML, CSS y JavaScript.
- Oculta la apariencia visual estándar de Streamlit.
- Incluye interés simple, interés compuesto y pago mensual.

Ejecución:
    streamlit run app_financiera_monolitica.py
"""

# ============================================================
# 1. IMPORTACIONES
# ============================================================

import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# 2. CONFIGURACIÓN GENERAL DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Finanzas Pro",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "Aplicación financiera empresarial con Session State.",
    },
)


# ============================================================
# 3. ESTILOS CSS EMPRESARIALES
# ============================================================

st.markdown(
    """
    <style>
        /* ----------------------------------------------------
           PALETA EMPRESARIAL
        ---------------------------------------------------- */
        :root {
            --azul-noche: #071A2B;
            --azul-profundo: #0B2A46;
            --azul-corporativo: #1464A5;
            --azul-claro: #2D9CDB;
            --turquesa: #00B8A9;
            --verde-exito: #19B37A;
            --dorado: #F4B942;
            --rojo-alerta: #E65A5A;
            --blanco: #FFFFFF;
            --gris-claro: #EAF0F6;
            --gris-texto: #6D7B8A;
            --sombra: 0 20px 55px rgba(2, 18, 34, 0.16);
        }

        /* ----------------------------------------------------
           OCULTAR ELEMENTOS NATIVOS VISIBLES DE STREAMLIT
        ---------------------------------------------------- */
        #MainMenu,
        footer,
        header,
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        [data-testid="collapsedControl"],
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        /* ----------------------------------------------------
           FONDO GENERAL
        ---------------------------------------------------- */
        html,
        body,
        [data-testid="stAppViewContainer"],
        .stApp {
            background:
                radial-gradient(circle at 10% 10%, rgba(45, 156, 219, 0.14), transparent 30%),
                radial-gradient(circle at 90% 15%, rgba(0, 184, 169, 0.12), transparent 28%),
                linear-gradient(135deg, #F7FAFD 0%, #EEF4F9 48%, #F8FBFD 100%) !important;
            color: var(--azul-noche);
            font-family: Inter, "Segoe UI", Arial, sans-serif;
        }

        [data-testid="stMain"] {
            background: transparent;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.35rem;
            padding-bottom: 2.5rem;
        }

        /* ----------------------------------------------------
           TEXTOS GENERALES
        ---------------------------------------------------- */
        h1, h2, h3, h4, h5, h6, p, label, span {
            font-family: Inter, "Segoe UI", Arial, sans-serif;
        }

        .section-title {
            margin: 1.2rem 0 0.35rem 0;
            color: var(--azul-noche);
            font-size: 1.55rem;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .section-subtitle {
            margin: 0 0 1.25rem 0;
            color: var(--gris-texto);
            font-size: 0.96rem;
            line-height: 1.65;
        }

        .module-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.42rem 0.78rem;
            margin-bottom: 0.65rem;
            border-radius: 999px;
            background: rgba(20, 100, 165, 0.10);
            border: 1px solid rgba(20, 100, 165, 0.15);
            color: var(--azul-corporativo);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        /* ----------------------------------------------------
           NAVEGACIÓN TIPO SEGMENTED CONTROL
        ---------------------------------------------------- */
        div[role="radiogroup"] {
            display: grid !important;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.8rem;
            width: 100%;
            margin: 0.3rem 0 1.4rem 0;
        }

        div[role="radiogroup"] > label {
            margin: 0 !important;
            padding: 0.95rem 1rem !important;
            border-radius: 15px !important;
            border: 1px solid rgba(11, 42, 70, 0.10) !important;
            background: rgba(255, 255, 255, 0.82) !important;
            box-shadow: 0 10px 28px rgba(2, 18, 34, 0.08);
            cursor: pointer;
            transition: transform 0.25s ease, box-shadow 0.25s ease,
                        border-color 0.25s ease, background 0.25s ease;
        }

        div[role="radiogroup"] > label:hover {
            transform: translateY(-3px);
            border-color: rgba(20, 100, 165, 0.40) !important;
            box-shadow: 0 16px 35px rgba(2, 18, 34, 0.12);
        }

        div[role="radiogroup"] > label:has(input:checked) {
            background: linear-gradient(135deg, var(--azul-profundo), var(--azul-corporativo)) !important;
            border-color: transparent !important;
            box-shadow: 0 16px 34px rgba(20, 100, 165, 0.28);
        }

        div[role="radiogroup"] > label:has(input:checked) p {
            color: var(--blanco) !important;
        }

        div[role="radiogroup"] [data-testid="stMarkdownContainer"] p {
            margin: 0;
            color: var(--azul-profundo);
            font-weight: 750;
            text-align: center;
        }

        div[role="radiogroup"] input,
        div[role="radiogroup"] [data-testid="stRadio"] > div:first-child {
            display: none !important;
        }

        /* ----------------------------------------------------
           TARJETAS DE CONTENIDO
        ---------------------------------------------------- */
        .content-card {
            padding: 1.35rem 1.45rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(11, 42, 70, 0.08);
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.90);
            box-shadow: var(--sombra);
            backdrop-filter: blur(14px);
        }

        .formula-card {
            padding: 1rem 1.15rem;
            margin: 0.25rem 0 1.15rem 0;
            border-left: 4px solid var(--turquesa);
            border-radius: 12px;
            background: linear-gradient(90deg, rgba(0, 184, 169, 0.09), rgba(45, 156, 219, 0.04));
            color: var(--azul-profundo);
            font-size: 0.92rem;
            line-height: 1.55;
        }

        .formula-card strong {
            color: var(--azul-corporativo);
        }

        /* ----------------------------------------------------
           CAMPOS NUMÉRICOS
        ---------------------------------------------------- */
        [data-testid="stNumberInput"] {
            padding: 0.3rem 0.2rem;
        }

        [data-testid="stNumberInput"] label p {
            color: var(--azul-profundo) !important;
            font-size: 0.89rem !important;
            font-weight: 750 !important;
            letter-spacing: 0.01em;
        }

        [data-testid="stNumberInput"] > div > div {
            min-height: 3.15rem;
            border: 1.5px solid rgba(11, 42, 70, 0.13) !important;
            border-radius: 13px !important;
            background: #FFFFFF !important;
            box-shadow: 0 7px 20px rgba(2, 18, 34, 0.05);
            transition: border-color 0.22s ease, box-shadow 0.22s ease,
                        transform 0.22s ease;
        }

        [data-testid="stNumberInput"] > div > div:focus-within {
            border-color: var(--azul-claro) !important;
            box-shadow: 0 0 0 4px rgba(45, 156, 219, 0.13),
                        0 12px 25px rgba(2, 18, 34, 0.07);
            transform: translateY(-1px);
        }

        [data-testid="stNumberInput"] input {
            color: var(--azul-noche) !important;
            background: transparent !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
        }

        [data-testid="stNumberInputStepUp"],
        [data-testid="stNumberInputStepDown"] {
            color: var(--azul-corporativo) !important;
            background: rgba(20, 100, 165, 0.06) !important;
            border-left: 1px solid rgba(11, 42, 70, 0.08) !important;
        }

        /* ----------------------------------------------------
           BOTONES EMPRESARIALES ANIMADOS
        ---------------------------------------------------- */
        div[data-testid="stButton"] > button {
            position: relative;
            width: 100%;
            min-height: 3.15rem;
            overflow: hidden;
            border: 0 !important;
            border-radius: 13px !important;
            color: var(--blanco) !important;
            background: linear-gradient(110deg, var(--azul-profundo), var(--azul-corporativo), var(--azul-claro)) !important;
            background-size: 220% 100% !important;
            box-shadow: 0 13px 28px rgba(20, 100, 165, 0.28) !important;
            font-size: 0.96rem !important;
            font-weight: 800 !important;
            letter-spacing: 0.01em;
            transition: transform 0.22s ease, box-shadow 0.22s ease,
                        filter 0.22s ease;
            animation: buttonGradient 5s ease infinite;
        }

        div[data-testid="stButton"] > button::before {
            content: "";
            position: absolute;
            top: 0;
            left: -120%;
            width: 70%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.34), transparent);
            transform: skewX(-22deg);
            transition: left 0.55s ease;
        }

        div[data-testid="stButton"] > button:hover {
            transform: translateY(-3px) scale(1.01);
            box-shadow: 0 18px 34px rgba(20, 100, 165, 0.34) !important;
            filter: saturate(1.08);
        }

        div[data-testid="stButton"] > button:hover::before {
            left: 145%;
        }

        div[data-testid="stButton"] > button:active {
            transform: translateY(0) scale(0.99);
        }

        div[data-testid="stButton"] > button p {
            color: var(--blanco) !important;
            font-weight: 800 !important;
        }

        @keyframes buttonGradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Botón secundario: se aplica al segundo botón de cada fila. */
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stButton"] > button {
            color: var(--azul-profundo) !important;
            background: rgba(255, 255, 255, 0.92) !important;
            border: 1.5px solid rgba(20, 100, 165, 0.18) !important;
            box-shadow: 0 10px 24px rgba(2, 18, 34, 0.08) !important;
            animation: none;
        }

        div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stButton"] > button p {
            color: var(--azul-profundo) !important;
        }

        /* ----------------------------------------------------
           TARJETAS DE RESULTADO
        ---------------------------------------------------- */
        .results-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
            margin: 1.15rem 0 0.8rem 0;
        }

        .result-card {
            position: relative;
            overflow: hidden;
            min-height: 128px;
            padding: 1.05rem 1.1rem;
            border-radius: 16px;
            border: 1px solid rgba(11, 42, 70, 0.08);
            background: linear-gradient(145deg, #FFFFFF 0%, #F5FAFD 100%);
            box-shadow: 0 13px 32px rgba(2, 18, 34, 0.09);
            animation: resultEntry 0.48s ease both;
        }

        .result-card::after {
            content: "";
            position: absolute;
            right: -24px;
            bottom: -28px;
            width: 95px;
            height: 95px;
            border-radius: 50%;
            background: rgba(45, 156, 219, 0.08);
        }

        .result-label {
            position: relative;
            z-index: 1;
            margin-bottom: 0.55rem;
            color: var(--gris-texto);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .result-value {
            position: relative;
            z-index: 1;
            color: var(--azul-noche);
            font-size: clamp(1.35rem, 2.4vw, 2rem);
            font-weight: 850;
            letter-spacing: -0.04em;
        }

        .result-note {
            position: relative;
            z-index: 1;
            margin-top: 0.45rem;
            color: var(--verde-exito);
            font-size: 0.78rem;
            font-weight: 750;
        }

        @keyframes resultEntry {
            from { opacity: 0; transform: translateY(12px) scale(0.98); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        /* ----------------------------------------------------
           PANEL SESSION STATE
        ---------------------------------------------------- */
        [data-testid="stExpander"] {
            margin-top: 1.35rem;
            border: 1px solid rgba(11, 42, 70, 0.09) !important;
            border-radius: 17px !important;
            background: rgba(255, 255, 255, 0.86) !important;
            box-shadow: 0 13px 34px rgba(2, 18, 34, 0.08);
            overflow: hidden;
        }

        [data-testid="stExpander"] summary {
            padding: 0.85rem 1rem !important;
            color: var(--azul-profundo) !important;
            font-weight: 800 !important;
        }

        .state-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.8rem;
            padding: 0.35rem 0 0.65rem 0;
        }

        .state-card {
            padding: 0.9rem;
            border-radius: 13px;
            background: rgba(234, 240, 246, 0.62);
            border: 1px solid rgba(11, 42, 70, 0.07);
        }

        .state-card h4 {
            margin: 0 0 0.55rem 0;
            color: var(--azul-corporativo);
            font-size: 0.9rem;
        }

        .state-row {
            display: flex;
            justify-content: space-between;
            gap: 0.8rem;
            padding: 0.25rem 0;
            color: var(--gris-texto);
            font-size: 0.82rem;
        }

        .state-row strong {
            color: var(--azul-noche);
        }

        .footer-app {
            margin-top: 1.7rem;
            padding: 0.85rem 0;
            text-align: center;
            color: var(--gris-texto);
            font-size: 0.78rem;
        }

        /* ----------------------------------------------------
           DISEÑO RESPONSIVO
        ---------------------------------------------------- */
        @media (max-width: 760px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            div[role="radiogroup"],
            .results-grid,
            .state-grid {
                grid-template-columns: 1fr;
            }

            div[role="radiogroup"] > label {
                padding: 0.8rem !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. CABECERA HTML + CSS + JAVASCRIPT
# ============================================================

# Este bloque se ejecuta dentro de un iframe independiente.
# JavaScript actualiza la hora y genera partículas decorativas.
hero_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { box-sizing: border-box; }

            html, body {
                margin: 0;
                padding: 0;
                overflow: hidden;
                background: transparent;
                font-family: Inter, "Segoe UI", Arial, sans-serif;
            }

            .hero {
                position: relative;
                min-height: 184px;
                overflow: hidden;
                padding: 28px 32px;
                border-radius: 24px;
                color: #FFFFFF;
                background:
                    radial-gradient(circle at 80% 20%, rgba(45,156,219,0.32), transparent 30%),
                    radial-gradient(circle at 15% 85%, rgba(0,184,169,0.22), transparent 28%),
                    linear-gradient(125deg, #071A2B 0%, #0B2A46 52%, #1464A5 100%);
                box-shadow: 0 22px 55px rgba(2,18,34,0.26);
            }

            .grid {
                position: absolute;
                inset: 0;
                opacity: 0.18;
                background-image:
                    linear-gradient(rgba(255,255,255,0.10) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,0.10) 1px, transparent 1px);
                background-size: 32px 32px;
                mask-image: linear-gradient(to right, transparent 0%, black 40%, black 100%);
            }

            .content {
                position: relative;
                z-index: 3;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 24px;
            }

            .eyebrow {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 7px 12px;
                border: 1px solid rgba(255,255,255,0.17);
                border-radius: 999px;
                background: rgba(255,255,255,0.08);
                color: #CFE9F9;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 0.12em;
                text-transform: uppercase;
            }

            .dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #00B8A9;
                box-shadow: 0 0 0 6px rgba(0,184,169,0.12);
                animation: pulse 1.8s ease-in-out infinite;
            }

            h1 {
                margin: 13px 0 7px 0;
                font-size: clamp(28px, 4vw, 46px);
                line-height: 1;
                letter-spacing: -0.05em;
            }

            p {
                max-width: 620px;
                margin: 0;
                color: #C3D5E4;
                font-size: 14px;
                line-height: 1.6;
            }

            .status {
                min-width: 215px;
                padding: 17px 18px;
                border: 1px solid rgba(255,255,255,0.14);
                border-radius: 17px;
                background: rgba(255,255,255,0.08);
                backdrop-filter: blur(12px);
            }

            .status-label {
                margin-bottom: 7px;
                color: #9EC8E1;
                font-size: 10px;
                font-weight: 800;
                letter-spacing: 0.12em;
                text-transform: uppercase;
            }

            #clock {
                color: #FFFFFF;
                font-size: 25px;
                font-weight: 850;
                letter-spacing: -0.03em;
            }

            #date {
                margin-top: 3px;
                color: #B8D0DF;
                font-size: 11px;
                text-transform: capitalize;
            }

            .particle {
                position: absolute;
                z-index: 1;
                width: 4px;
                height: 4px;
                border-radius: 50%;
                background: rgba(255,255,255,0.45);
                animation: float linear infinite;
            }

            @keyframes pulse {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(0.72); opacity: 0.65; }
            }

            @keyframes float {
                from { transform: translateY(210px) translateX(0); opacity: 0; }
                15% { opacity: 0.7; }
                to { transform: translateY(-30px) translateX(26px); opacity: 0; }
            }

            @media (max-width: 700px) {
                .hero { padding: 23px 22px; }
                .content { align-items: flex-start; }
                .status { display: none; }
                p { font-size: 12px; }
            }
        </style>
    </head>
    <body>
        <section class="hero" id="hero">
            <div class="grid"></div>
            <div class="content">
                <div>
                    <div class="eyebrow">
                        <span class="dot"></span>
                        Session State activo
                    </div>
                    <h1>Finanzas Pro</h1>
                    <p>
                        Simule escenarios financieros, cambie de módulo y conserve
                        automáticamente cada dato durante la sesión.
                    </p>
                </div>

                <div class="status">
                    <div class="status-label">Hora local</div>
                    <div id="clock">--:--:--</div>
                    <div id="date">Cargando fecha...</div>
                </div>
            </div>
        </section>

        <script>
            const clockElement = document.getElementById("clock");
            const dateElement = document.getElementById("date");
            const hero = document.getElementById("hero");

            function updateClock() {
                const now = new Date();

                clockElement.textContent = now.toLocaleTimeString("es-EC", {
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit"
                });

                dateElement.textContent = now.toLocaleDateString("es-EC", {
                    weekday: "long",
                    day: "2-digit",
                    month: "long",
                    year: "numeric"
                });
            }

            function createParticles() {
                for (let i = 0; i < 18; i++) {
                    const particle = document.createElement("span");
                    particle.className = "particle";
                    particle.style.left = Math.random() * 100 + "%";
                    particle.style.animationDuration = (5 + Math.random() * 7) + "s";
                    particle.style.animationDelay = (-Math.random() * 8) + "s";
                    particle.style.opacity = 0.2 + Math.random() * 0.5;
                    hero.appendChild(particle);
                }
            }

            updateClock();
            createParticles();
            setInterval(updateClock, 1000);
        </script>
    </body>
    </html>
    """

# Streamlit moderno permite ejecutar JavaScript directamente con st.html.
# El bloque alternativo mantiene compatibilidad con versiones anteriores.
try:
    st.html(
        hero_html,
        width="stretch",
        unsafe_allow_javascript=True,
    )
except (TypeError, AttributeError):
    components.html(
        hero_html,
        height=205,
        scrolling=False,
    )


# ============================================================
# 5. VARIABLES PERMANENTES EN SESSION STATE
# ============================================================

# Estas variables guardan los datos aunque el usuario cambie de módulo.

# Interés simple.
if "simple_capital" not in st.session_state:
    st.session_state["simple_capital"] = 1000.0

if "simple_tasa" not in st.session_state:
    st.session_state["simple_tasa"] = 5.0

if "simple_meses" not in st.session_state:
    st.session_state["simple_meses"] = 12

if "simple_resultado" not in st.session_state:
    st.session_state["simple_resultado"] = None


# Interés compuesto.
if "compuesto_capital" not in st.session_state:
    st.session_state["compuesto_capital"] = 1000.0

if "compuesto_tasa" not in st.session_state:
    st.session_state["compuesto_tasa"] = 5.0

if "compuesto_anios" not in st.session_state:
    st.session_state["compuesto_anios"] = 5

if "compuesto_resultado" not in st.session_state:
    st.session_state["compuesto_resultado"] = None


# Pago mensual.
if "pago_monto" not in st.session_state:
    st.session_state["pago_monto"] = 10000.0

if "pago_tasa" not in st.session_state:
    st.session_state["pago_tasa"] = 10.0

if "pago_anios" not in st.session_state:
    st.session_state["pago_anios"] = 3

if "pago_resultado" not in st.session_state:
    st.session_state["pago_resultado"] = None


# ============================================================
# 6. NAVEGACIÓN PRINCIPAL
# ============================================================

st.markdown(
    """
    <div class="section-title">Centro de simulación financiera</div>
    <div class="section-subtitle">
        Seleccione un módulo. Los valores permanecerán almacenados aunque navegue
        entre las diferentes calculadoras.
    </div>
    """,
    unsafe_allow_html=True,
)

modulo = st.radio(
    "Seleccione un módulo",
    [
        "📈 Interés simple",
        "🚀 Interés compuesto",
        "🏦 Pago mensual",
    ],
    horizontal=True,
    label_visibility="collapsed",
    key="modulo_activo",
)


# ============================================================
# 7. MÓDULO DE INTERÉS SIMPLE
# ============================================================

if modulo == "📈 Interés simple":

    st.markdown(
        """
        <div class="module-badge">01 · Crecimiento lineal</div>
        <div class="section-title">Interés simple</div>
        <div class="section-subtitle">
            Calcule el rendimiento generado cuando el interés se aplica únicamente
            sobre el capital inicial.
        </div>
        <div class="formula-card">
            <strong>Fórmula:</strong> Interés = Capital × Tasa anual × Tiempo en años.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Cada widget utiliza una clave temporal.
    # El valor también se copia a una clave permanente de session_state.
    columna_1, columna_2, columna_3 = st.columns(3, gap="large")

    with columna_1:
        capital_simple = st.number_input(
            "Capital inicial ($)",
            min_value=0.0,
            step=100.0,
            value=float(st.session_state["simple_capital"]),
            key="widget_simple_capital",
        )
        st.session_state["simple_capital"] = capital_simple

    with columna_2:
        tasa_simple = st.number_input(
            "Tasa anual (%)",
            min_value=0.0,
            step=0.5,
            value=float(st.session_state["simple_tasa"]),
            key="widget_simple_tasa",
        )
        st.session_state["simple_tasa"] = tasa_simple

    with columna_3:
        meses_simple = st.number_input(
            "Tiempo en meses",
            min_value=1,
            step=1,
            value=int(st.session_state["simple_meses"]),
            key="widget_simple_meses",
        )
        st.session_state["simple_meses"] = meses_simple

    boton_calcular, boton_limpiar = st.columns([2.2, 1], gap="large")

    with boton_calcular:
        calcular_simple = st.button(
            "Calcular interés simple  →",
            key="boton_calcular_simple",
            use_container_width=True,
        )

    with boton_limpiar:
        limpiar_simple = st.button(
            "Restablecer",
            key="boton_limpiar_simple",
            use_container_width=True,
        )

    if calcular_simple:
        tasa_decimal = tasa_simple / 100
        tiempo_anios = meses_simple / 12
        interes = capital_simple * tasa_decimal * tiempo_anios
        monto_final = capital_simple + interes

        st.session_state["simple_resultado"] = {
            "interes": interes,
            "monto_final": monto_final,
            "rendimiento": (interes / capital_simple * 100) if capital_simple > 0 else 0,
        }

    if limpiar_simple:
        st.session_state["simple_capital"] = 1000.0
        st.session_state["simple_tasa"] = 5.0
        st.session_state["simple_meses"] = 12
        st.session_state["simple_resultado"] = None

        for clave in [
            "widget_simple_capital",
            "widget_simple_tasa",
            "widget_simple_meses",
        ]:
            if clave in st.session_state:
                del st.session_state[clave]

        st.rerun()

    if st.session_state["simple_resultado"] is not None:
        resultado_simple = st.session_state["simple_resultado"]

        st.markdown(
            f"""
            <div class="results-grid">
                <div class="result-card">
                    <div class="result-label">Interés generado</div>
                    <div class="result-value">${resultado_simple['interes']:,.2f}</div>
                    <div class="result-note">Ganancia financiera estimada</div>
                </div>
                <div class="result-card">
                    <div class="result-label">Monto final</div>
                    <div class="result-value">${resultado_simple['monto_final']:,.2f}</div>
                    <div class="result-note">Capital más rendimiento</div>
                </div>
                <div class="result-card">
                    <div class="result-label">Rendimiento</div>
                    <div class="result-value">{resultado_simple['rendimiento']:,.2f}%</div>
                    <div class="result-note">Respecto al capital inicial</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# 8. MÓDULO DE INTERÉS COMPUESTO
# ============================================================

elif modulo == "🚀 Interés compuesto":

    st.markdown(
        """
        <div class="module-badge">02 · Crecimiento acumulativo</div>
        <div class="section-title">Interés compuesto</div>
        <div class="section-subtitle">
            Proyecte el crecimiento de una inversión cuando los intereses se
            reinvierten y generan nuevos intereses.
        </div>
        <div class="formula-card">
            <strong>Fórmula:</strong> Monto final = Capital × (1 + Tasa)<sup>Años</sup>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    columna_1, columna_2, columna_3 = st.columns(3, gap="large")

    with columna_1:
        capital_compuesto = st.number_input(
            "Capital inicial ($)",
            min_value=0.0,
            step=100.0,
            value=float(st.session_state["compuesto_capital"]),
            key="widget_compuesto_capital",
        )
        st.session_state["compuesto_capital"] = capital_compuesto

    with columna_2:
        tasa_compuesta = st.number_input(
            "Tasa anual (%)",
            min_value=0.0,
            step=0.5,
            value=float(st.session_state["compuesto_tasa"]),
            key="widget_compuesto_tasa",
        )
        st.session_state["compuesto_tasa"] = tasa_compuesta

    with columna_3:
        anios_compuesto = st.number_input(
            "Tiempo en años",
            min_value=1,
            step=1,
            value=int(st.session_state["compuesto_anios"]),
            key="widget_compuesto_anios",
        )
        st.session_state["compuesto_anios"] = anios_compuesto

    boton_calcular, boton_limpiar = st.columns([2.2, 1], gap="large")

    with boton_calcular:
        calcular_compuesto = st.button(
            "Calcular interés compuesto  →",
            key="boton_calcular_compuesto",
            use_container_width=True,
        )

    with boton_limpiar:
        limpiar_compuesto = st.button(
            "Restablecer",
            key="boton_limpiar_compuesto",
            use_container_width=True,
        )

    if calcular_compuesto:
        tasa_decimal = tasa_compuesta / 100
        monto_final = capital_compuesto * (1 + tasa_decimal) ** anios_compuesto
        interes = monto_final - capital_compuesto

        st.session_state["compuesto_resultado"] = {
            "interes": interes,
            "monto_final": monto_final,
            "crecimiento": (interes / capital_compuesto * 100) if capital_compuesto > 0 else 0,
        }

    if limpiar_compuesto:
        st.session_state["compuesto_capital"] = 1000.0
        st.session_state["compuesto_tasa"] = 5.0
        st.session_state["compuesto_anios"] = 5
        st.session_state["compuesto_resultado"] = None

        for clave in [
            "widget_compuesto_capital",
            "widget_compuesto_tasa",
            "widget_compuesto_anios",
        ]:
            if clave in st.session_state:
                del st.session_state[clave]

        st.rerun()

    if st.session_state["compuesto_resultado"] is not None:
        resultado_compuesto = st.session_state["compuesto_resultado"]

        st.markdown(
            f"""
            <div class="results-grid">
                <div class="result-card">
                    <div class="result-label">Interés acumulado</div>
                    <div class="result-value">${resultado_compuesto['interes']:,.2f}</div>
                    <div class="result-note">Rendimiento total generado</div>
                </div>
                <div class="result-card">
                    <div class="result-label">Monto final</div>
                    <div class="result-value">${resultado_compuesto['monto_final']:,.2f}</div>
                    <div class="result-note">Valor futuro estimado</div>
                </div>
                <div class="result-card">
                    <div class="result-label">Crecimiento</div>
                    <div class="result-value">{resultado_compuesto['crecimiento']:,.2f}%</div>
                    <div class="result-note">Sobre el capital inicial</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# 9. MÓDULO DE PAGO MENSUAL
# ============================================================

else:

    st.markdown(
        """
        <div class="module-badge">03 · Financiamiento</div>
        <div class="section-title">Pago mensual de préstamo</div>
        <div class="section-subtitle">
            Estime la cuota mensual fija, el total pagado y los intereses de un
            préstamo amortizado.
        </div>
        <div class="formula-card">
            <strong>Modelo:</strong> cuota fija calculada con tasa mensual y número
            total de pagos. También admite préstamos con tasa de 0%.
        </div>
        """,
        unsafe_allow_html=True,
    )

    columna_1, columna_2, columna_3 = st.columns(3, gap="large")

    with columna_1:
        monto_prestamo = st.number_input(
            "Monto del préstamo ($)",
            min_value=0.01,
            step=500.0,
            value=float(st.session_state["pago_monto"]),
            key="widget_pago_monto",
        )
        st.session_state["pago_monto"] = monto_prestamo

    with columna_2:
        tasa_prestamo = st.number_input(
            "Tasa anual (%)",
            min_value=0.0,
            step=0.5,
            value=float(st.session_state["pago_tasa"]),
            key="widget_pago_tasa",
        )
        st.session_state["pago_tasa"] = tasa_prestamo

    with columna_3:
        plazo_prestamo = st.number_input(
            "Plazo en años",
            min_value=1,
            step=1,
            value=int(st.session_state["pago_anios"]),
            key="widget_pago_anios",
        )
        st.session_state["pago_anios"] = plazo_prestamo

    boton_calcular, boton_limpiar = st.columns([2.2, 1], gap="large")

    with boton_calcular:
        calcular_pago = st.button(
            "Calcular pago mensual  →",
            key="boton_calcular_pago",
            use_container_width=True,
        )

    with boton_limpiar:
        limpiar_pago = st.button(
            "Restablecer",
            key="boton_limpiar_pago",
            use_container_width=True,
        )

    if calcular_pago:
        tasa_mensual = (tasa_prestamo / 100) / 12
        numero_pagos = plazo_prestamo * 12

        if tasa_mensual == 0:
            cuota = monto_prestamo / numero_pagos
        else:
            cuota = (
                monto_prestamo
                * tasa_mensual
                * (1 + tasa_mensual) ** numero_pagos
                / ((1 + tasa_mensual) ** numero_pagos - 1)
            )

        total_pagado = cuota * numero_pagos
        total_intereses = total_pagado - monto_prestamo

        st.session_state["pago_resultado"] = {
            "cuota": cuota,
            "total_pagado": total_pagado,
            "total_intereses": total_intereses,
        }

    if limpiar_pago:
        st.session_state["pago_monto"] = 10000.0
        st.session_state["pago_tasa"] = 10.0
        st.session_state["pago_anios"] = 3
        st.session_state["pago_resultado"] = None

        for clave in [
            "widget_pago_monto",
            "widget_pago_tasa",
            "widget_pago_anios",
        ]:
            if clave in st.session_state:
                del st.session_state[clave]

        st.rerun()

    if st.session_state["pago_resultado"] is not None:
        resultado_pago = st.session_state["pago_resultado"]

        st.markdown(
            f"""
            <div class="results-grid">
                <div class="result-card">
                    <div class="result-label">Cuota mensual</div>
                    <div class="result-value">${resultado_pago['cuota']:,.2f}</div>
                    <div class="result-note">Pago fijo estimado</div>
                </div>
                <div class="result-card">
                    <div class="result-label">Total pagado</div>
                    <div class="result-value">${resultado_pago['total_pagado']:,.2f}</div>
                    <div class="result-note">Capital más intereses</div>
                </div>
                <div class="result-card">
                    <div class="result-label">Total de intereses</div>
                    <div class="result-value">${resultado_pago['total_intereses']:,.2f}</div>
                    <div class="result-note">Costo del financiamiento</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# 10. VISUALIZACIÓN DE LOS DATOS GUARDADOS
# ============================================================

with st.expander("🧠 Ver memoria de la aplicación · session_state"):

    st.markdown(
        f"""
        <div class="state-grid">
            <div class="state-card">
                <h4>📈 Interés simple</h4>
                <div class="state-row"><span>Capital</span><strong>${st.session_state['simple_capital']:,.2f}</strong></div>
                <div class="state-row"><span>Tasa</span><strong>{st.session_state['simple_tasa']:,.2f}%</strong></div>
                <div class="state-row"><span>Meses</span><strong>{st.session_state['simple_meses']}</strong></div>
            </div>

            <div class="state-card">
                <h4>🚀 Interés compuesto</h4>
                <div class="state-row"><span>Capital</span><strong>${st.session_state['compuesto_capital']:,.2f}</strong></div>
                <div class="state-row"><span>Tasa</span><strong>{st.session_state['compuesto_tasa']:,.2f}%</strong></div>
                <div class="state-row"><span>Años</span><strong>{st.session_state['compuesto_anios']}</strong></div>
            </div>

            <div class="state-card">
                <h4>🏦 Pago mensual</h4>
                <div class="state-row"><span>Monto</span><strong>${st.session_state['pago_monto']:,.2f}</strong></div>
                <div class="state-row"><span>Tasa</span><strong>{st.session_state['pago_tasa']:,.2f}%</strong></div>
                <div class="state-row"><span>Años</span><strong>{st.session_state['pago_anios']}</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 11. PIE DE PÁGINA
# ============================================================

st.markdown(
    """
    <div class="footer-app">
        Finanzas Pro · Aplicación monolítica desarrollada con Python, Streamlit,
        HTML, CSS y JavaScript.
    </div>
    """,
    unsafe_allow_html=True,
)
