import streamlit as st
import pandas as pd
import random

# Configuración de página optimizada para móvil y escritorio
st.set_page_config(
    page_title="SaludClic | Especialistas y cuidado profesional a un clic",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS avanzados tipo App Pro (Tarjetas flotantes, sombras y bordes redondeados)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 50%, #10B981 100%);
        padding: 2rem 1.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.3);
    }
    .main-header h1 {
        color: white !important;
        margin: 0;
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #F1F5F9 !important;
        margin-top: 0.6rem;
        font-size: 1.1rem;
        font-weight: 400;
    }
    .badge-verificado {
        background-color: #ECFDF5;
        color: #047857;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        border: 1px solid #A7F3D0;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Encabezado Oficial con Marca de Agua / Estética Pro
st.markdown("""
<div class="main-header">
    <h1>🩺 SaludClic</h1>
    <p>Especialistas y cuidado profesional a un clic</p>
</div>
""", unsafe_allow_html=True)

# --- BASE DE DATOS EN MEMORIA ---
if "profesionales" not in st.session_state:
    st.session_state.profesionales = [
        {
            "id": 1, "nombre": "Laura Gómez", "profesion": "Fisioterapeuta", "nivel": 2,
            "zonas": "Bello, Medellín Norte", "tarifa_domicilio": 85000, "tarifa_virtual": 50000, "tarifa_consultorio": 0,
            "creditos_disp": 6, "creditos_ret": 0, "estrellas": 4.9, "resenas": 14, "verificado": True
        },
        {
            "id": 2, "nombre": "Carlos Restrepo", "profesion": "Auxiliar de Enfermería (Turno 12h)", "nivel": 1,
            "zonas": "Bello, Copacabana, Medellín", "tarifa_domicilio": 95000, "tarifa_virtual": 0, "tarifa_consultorio": 0,
            "creditos_disp": 4, "creditos_ret": 0, "estrellas": 5.0, "resenas": 8, "verificado": True
        },
        {
            "id": 3, "nombre": "Dra. Diana Pineda", "profesion": "Psicóloga Clínica", "nivel": 2,
            "zonas": "Medellín (Laureles) / Virtual", "tarifa_domicilio": 100000, "tarifa_virtual": 65000, "tarifa_consultorio": 80000,
            "creditos_disp": 8, "creditos_ret": 0, "estrellas": 4.9, "resenas": 19, "verificado": True
        },
        {
            "id": 4, "nombre": "Dr. Andrés Villa", "profesion": "Médico Internista", "nivel": 3,
            "zonas": "Medellín (El Poblado / Laureles)", "tarifa_domicilio": 180000, "tarifa_virtual": 120000, "tarifa_consultorio": 150000,
            "creditos_disp": 10, "creditos_ret": 0, "estrellas": 4.8, "resenas": 22, "verificado": True
        },
        {
            "id": 5, "nombre": "Dr. Mauricio Rojas", "profesion": "Urólogo", "nivel": 4,
            "zonas": "Medellín (Clínica Medellín / Consultorio)", "tarifa_domicilio": 260000, "tarifa_virtual": 170000, "tarifa_consultorio": 210000,
            "creditos_disp": 12, "creditos_ret": 0, "estrellas": 5.0, "resenas": 11, "verificado": True
        }
    ]

if "citas" not in st.session_state:
    st.session_state.citas = []

if "pacientes_bloqueados" not in st.session_state:
    st.session_state.pacientes_bloqueados = set()

def calcular_creditos(nivel, modalidad):
    if modalidad == "Virtual":
        return max(1, nivel - 1)
    return nivel

# Pestañas de navegación optimizadas para móvil
tab_paciente, tab_registro_prof, tab_panel_prof, tab_admin = st.tabs([
    "🔍 Buscar / IA",
    "📝 Registro",
    "👨‍⚕️ Mi Panel",
    "🛡️ Admin"
])

# ==============================================================================
# PESTAÑA 1: PACIENTE
# ==============================================================================
with tab_paciente:
    st.subheader("🤖 Orientador Inteligente SaludClic")
    consulta_ia = st.text_input(
        "¿Qué servicio o especialista necesitas hoy?",
        placeholder="Ej: Turno de enfermería en Bello, fisio a domicilio, psicólogo..."
    )
    if consulta_ia:
        txt = consulta_ia.lower()
        if any(p in txt for p in ["turno", "cuidador", "auxiliar", "enfermer", "curacion", "inyect"]):
            st.success("💡 **SaludClic te sugiere:** Tenemos **Auxiliares de Enfermería y Cuidadores verificados** listos para turnos o procedimientos en casa.")
        elif any(p in txt for p in ["fisio", "terapia", "rehabilita", "fono", "dolor"]):
            st.success("💡 **SaludClic te sugiere:** Contamos con **Fisioterapeutas profesionales (Nivel 2)** especializados en rehabilitación domiciliaria.")
        elif any(p in txt for p in ["psico", "ansiedad", "pareja", "mental"]):
            st.success("💡 **SaludClic te sugiere:** Encuentra especialistas en **Psicología Clínica** en modalidad virtual o consultorio.")
        else:
            st.info("💡 **SaludClic te sugiere:** Revisa el listado de profesionales verificados con mejor calificación en tu zona.")

    st.divider()
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filtro_mod = st.selectbox("Filtrar modalidad:", ["Todas", "Domicilio", "Virtual", "Consultorio"])
    with col_f2:
        orden = st.selectbox("Ordenar:", ["Mejor calificados ⭐", "Menor tarifa 💲"])

    lista_profs = [p for p in st.session_state.profesionales if p["verificado"] and p["creditos_disp"] > 0]
    if orden == "Mejor calificados ⭐":
        lista_profs.sort(key=lambda x: x["estrellas"], reverse=True)

    for prof in lista_profs:
        if filtro_mod == "Domicilio" and prof["tarifa_domicilio"] == 0: continue
        if filtro_mod == "Virtual" and prof["tarifa_virtual"] == 0: continue
        if filtro_mod == "Consultorio" and prof["tarifa_consultorio"] == 0: continue

        with st.container(border=True):
            st.markdown(f"### {prof['nombre']} <span class='badge-verificado'>✔️ Verificado ReTHUS</span>", unsafe_allow_html=True)
            st.markdown(f"**{prof['profesion']}** • ⭐ **{prof['estrellas']}** ({prof['resenas']} atenciones)")
            st.caption(f"📍 {prof['zonas']}")

            precios = []
            mods_disp = []
            if prof["tarifa_domicilio"] > 0:
                precios.append(f"🏠 Domicilio: **${prof['tarifa_domicilio']:,}**")
                mods_disp.append("Domicilio")
            if prof["tarifa_virtual"] > 0:
                precios.append(f"💻 Virtual: **${prof['tarifa_virtual']:,}**")
                mods_disp.append("Virtual")
            if prof["tarifa_consultorio"] > 0:
                precios.append(f"🏥 Consultorio: **${prof['tarifa_consultorio']:,}**")
                mods_disp.append("Consultorio")
            st.markdown(" | ".join(precios))

            with st.expander("📅 Solicitar Cita o Servicio"):
                nom_pac = st.text_input("Tu Nombre Completo", key=f"nom_{prof['id']}")
                ced_pac = st.text_input("Tu Cédula", key=f"ced_{prof['id']}")
                cel_pac = st.text_input("Tu WhatsApp", key=f"cel_{prof['id']}")
                mod_sel = st.selectbox("Modalidad elegida", mods_disp, key=f"mod_{prof['id']}")
                fec_sel = st.text_input("Fecha y hora deseada", placeholder="Ej: Mañana 3:00 PM", key=f"fec_{prof['id']}")

                if st.button("Confirmar Solicitud", key=f"btn_{prof['id']}", type="primary"):
                    if not nom_pac or not ced_pac or not cel_pac or not fec_sel:
                        st.warning("Completa todos los campos para generar tu PIN.")
                    elif ced_pac in st.session_state.pacientes_bloqueados:
                        st.error("🚨 Tu cédula tiene una verificación pendiente de una cita anterior. Comunícate con soporte.")
                    else:
                        pin_nuevo = str(random.randint(1000, 9999))
                        cred_cita = calcular_creditos(prof["nivel"], mod_sel)
                        st.session_state.citas.append({
                            "id_cita": len(st.session_state.citas) + 1,
                            "prof_id": prof["id"], "prof_nombre": prof["nombre"],
                            "paciente": nom_pac, "cedula_pac": ced_pac, "celular_pac": cel_pac,
                            "modalidad": mod_sel, "fecha": fec_sel, "creditos": cred_cita,
                            "pin": pin_nuevo, "link_virtual": "", "estado": "Solicitada", "calificado": False
                        })
                        st.success(f"✅ ¡Solicitud enviada! Tu PIN de seguridad es: **{pin_nuevo}** (Guárdalo para entregarlo al profesional el día de la atención).")

    st.divider()
    st.subheader("⭐ Calificar Atención Recibida")
    citas_cal = [c for c in st.session_state.citas if c["estado"] == "Completada_Con_Pin" and not c["calificado"]]
    if not citas_cal:
        st.info("Aquí podrás calificar al profesional una vez validado tu PIN de atención.")
    for c in citas_cal:
        with st.container(border=True):
            st.write(f"Cita con **{c['prof_nombre']}**")
            estrellas = st.slider("Calificación (1 a 5)", 1, 5, 5, key=f"st_{c['id_cita']}")
            com = st.text_input("Comentario", key=f"co_{c['id_cita']}")
            if st.button("Enviar Calificación Verificada", key=f"pub_{c['id_cita']}"):
                c["calificado"] = True
                st.success("¡Gracias por calificar en SaludClic!")
                st.rerun()

# ==============================================================================
# PESTAÑA 2: REGISTRO PROFESIONAL
# ==============================================================================
with tab_registro_prof:
    st.subheader("Regístrate en SaludClic")
    st.write("Sube tus documentos para verificación ReTHUS y recibe pacientes directos.")
    with st.form("form_reg"):
        r_nom = st.text_input("Nombre completo y título profesional")
        r_ced = st.text_input("Cédula de ciudadanía")
        r_cel = st.text_input("WhatsApp de contacto")
        r_cat = st.selectbox("Nivel / Categoría Profesional", [
            "Nivel 1 - Auxiliar de Enfermería / Cuidador (1 Crédito)",
            "Nivel 2 - Enfermero Jefe / Médico General / Fisio / Psicología (2 Créd. Presencial | 1 Créd. Virtual)",
            "Nivel 3 - Especialista Base: Internista / Pediatra / Ginecólogo (3 Créd. Presencial | 2 Créd. Virtual)",
            "Nivel 4 - Subespecialista: Urólogo / Cardiólogo / Dermatólogo (4 Créd. Presencial | 3 Créd. Virtual)"
        ])
        r_zon = st.text_input("Zonas de cobertura / Dirección de consultorio")
        c1, c2, c3 = st.columns(3)
        t_dom = c1.number_input("Tarifa Domicilio ($)", min_value=0, step=5000, value=85000)
        t_vir = c2.number_input("Tarifa Virtual ($)", min_value=0, step=5000, value=50000)
        t_con = c3.number_input("Tarifa Consultorio ($)", min_value=0, step=5000, value=0)
        st.file_uploader("Foto de Perfil Real (Bata o uniforme)", type=["jpg", "png"])
        st.file_uploader("Soportes ReTHUS / Diploma (PDF)", type=["pdf"], accept_multiple_files=True)

        if st.form_submit_button("Enviar a Verificación", type="primary") and r_nom:
            nivel_n = int(r_cat.split(" ")[1])
            st.session_state.profesionales.append({
                "id": len(st.session_state.profesionales) + 1, "nombre": r_nom,
                "profesion": r_cat.split(" - ")[1].split(" (")[0], "nivel": nivel_n, "zonas": r_zon,
                "tarifa_domicilio": t_dom, "tarifa_virtual": t_vir, "tarifa_consultorio": t_con,
                "creditos_disp": 4, "creditos_ret": 0, "estrellas": 5.0, "resenas": 0, "verificado": False
            })
            st.success("🎉 ¡Registro exitoso! En breve validaremos tu ReTHUS para activar tus créditos de bienvenida.")

# ==============================================================================
# PESTAÑA 3: PANEL PROFESIONAL
# ==============================================================================
with tab_panel_prof:
    st.subheader("Mi Billetera de Créditos y Agenda")
    nombres = [f"{p['id']} - {p['nombre']} ({p['profesion']})" for p in st.session_state.profesionales]
    sel = st.selectbox("Selecciona tu perfil (Modo prueba):", nombres)
    id_s = int(sel.split(" - ")[0])
    prof = next(p for p in st.session_state.profesionales if p["id"] == id_s)

    m1, m2, m3 = st.columns(3)
    m1.metric("💳 Créditos Disponibles", f"{prof['creditos_disp']}")
    m2.metric("⏳ En Custodia", f"{prof['creditos_ret']}")
    m3.metric("Estado", "✔️ Verificado" if prof["verificado"] else "⏳ En revisión")

    with st.expander("➕ Recargar Créditos (1 Crédito = $10.000 COP)"):
        st.write("• **Paquete Básico (5 Créditos):** $50.000\n• **Paquete Pro (11 Créditos):** $100.000\n• **Paquete Plus (23 Créditos):** $200.000")
        if st.button("Simular Recarga de 5 Créditos"):
            prof["creditos_disp"] += 5
            st.success("¡Recarga simulada exitosa!")
            st.rerun()

    st.divider()
    st.markdown("### 📅 Solicitudes Recibidas")
    mis_c = [c for c in st.session_state.citas if c["prof_id"] == prof["id"]]
    if not mis_c:
        st.info("No tienes solicitudes activas por el momento.")

    for c in mis_c:
        with st.container(border=True):
            st.write(f"**Paciente:** {c['paciente']} | **Modalidad:** {c['modalidad']} | **Fecha:** {c['fecha']}")
            st.write(f"Costo: `{c['creditos']} Crédito(s)` | Estado: `{c['estado']}`")

            if c["estado"] == "Solicitada":
                col_a, col_b = st.columns(2)
                if col_a.button("✅ Aceptar Cita", key=f"ac_{c['id_cita']}"):
                    if prof["creditos_disp"] >= c["creditos"]:
                        prof["creditos_disp"] -= c["creditos"]
                        prof["creditos_ret"] += c["creditos"]
                        c["estado"] = "Aceptada_En_Curso"
                        st.rerun()
                    else:
                        st.error("Créditos insuficientes. Recarga tu billetera.")
                if col_b.button("❌ Rechazar", key=f"re_{c['id_cita']}"):
                    c["estado"] = "Rechazada"
                    st.rerun()

            elif c["estado"] == "Aceptada_En_Curso":
                st.success(f"🔓 **WhatsApp del Paciente:** {c['celular_pac']}")
                if c["modalidad"] == "Virtual":
                    lnk = st.text_input("Enlace Meet / Zoom (Opcional):", value=c["link_virtual"], key=f"lk_{c['id_cita']}")
                    if lnk: c["link_virtual"] = lnk

                pin_i = st.text_input("Ingresa el PIN de 4 dígitos del paciente:", key=f"pi_{c['id_cita']}")
                b1, b2 = st.columns(2)
                if b1.button("✔️ Validar PIN y Finalizar", key=f"vp_{c['id_cita']}"):
                    if pin_i == c["pin"]:
                        prof["creditos_ret"] -= c["creditos"]
                        prof["resenas"] += 1
                        c["estado"] = "Completada_Con_Pin"
                        st.success("¡Cita cerrada con éxito!")
                        st.rerun()
                    else:
                        st.error("PIN incorrecto.")
                if b2.button("⚠️ Reportar No Asistió", key=f"no_{c['id_cita']}"):
                    c["estado"] = "En_Auditoria_Paciente_Bloqueado"
                    st.session_state.pacientes_bloqueados.add(c["cedula_pac"])
                    st.warning("Reporte enviado. Paciente bloqueado temporalmente y créditos en custodia retenidos para auditoría.")
                    st.rerun()

# ==============================================================================
# PESTAÑA 4: ADMINISTRADOR
# ==============================================================================
with tab_admin:
    st.subheader("🛡️ Panel de Control Admin")
    st.markdown("#### 1. Verificación ReTHUS de Profesionales")
    pends = [p for p in st.session_state.profesionales if not p["verificado"]]
    if not pends: st.info("No hay profesionales pendientes.")
    for p in pends:
        with st.container(border=True):
            st.write(f"**{p['nombre']}** — {p['profesion']}")
            if st.button(f"✔️ Aprobar e Habilitar", key=f"ap_{p['id']}"):
                p["verificado"] = True
                st.rerun()

    st.divider()
    st.markdown("#### 2. Auditoría de Cancelaciones")
    audits = [c for c in st.session_state.citas if c["estado"] == "En_Auditoria_Paciente_Bloqueado"]
    if not audits: st.info("Sin auditorías pendientes.")
    for c in audits:
        with st.container(border=True):
            st.error(f"Paciente Bloqueado: **{c['paciente']}** (Cédula: {c['cedula_pac']})")
            a1, a2 = st.columns(2)
            if a1.button("🔄 Devolver créditos al profesional", key=f"dev_{c['id_cita']}"):
                pr = next(p for p in st.session_state.profesionales if p["id"] == c["prof_id"])
                pr["creditos_ret"] -= c["creditos"]
                pr["creditos_disp"] += c["creditos"]
                c["estado"] = "Devuelto"
                st.rerun()
            if a2.button("🛑 Desbloquear paciente (Sí hubo cita)", key=f"des_{c['id_cita']}"):
                pr = next(p for p in st.session_state.profesionales if p["id"] == c["prof_id"])
                pr["creditos_ret"] -= c["creditos"]
                st.session_state.pacientes_bloqueados.discard(c["cedula_pac"])
                c["estado"] = "Completada_Con_Pin"
                st.rerun()
