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

# Estilos CSS personalizados con la paleta oficial de SaludClic (#0284C7 y #10B981)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0284C7 0%, #10B981 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .main-header h1 {
        color: white !important;
        margin: 0;
        font-size: 2.2rem;
        font-weight: 800;
    }
    .main-header p {
        color: #F8FAFC !important;
        margin-top: 0.4rem;
        font-size: 1.05rem;
    }
    .badge-verificado {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Encabezado Oficial de SaludClic
st.markdown("""
<div class="main-header">
    <h1>🩺 SaludClic</h1>
    <p>Especialistas y cuidado profesional a un clic</p>
</div>
""", unsafe_allow_html=True)

# --- BASE DE DATOS EN MEMORIA (Lista para migrar a Supabase Gratis) ---
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

# Regla oficial de créditos (1 Crédito = $10.000 COP, números enteros, Virtual = -1 crédito, mín 1)
def calcular_creditos(nivel, modalidad):
    if modalidad == "Virtual":
        return max(1, nivel - 1)
    return nivel

# Navegación por pestañas (Mucho más cómoda desde el celular que la barra lateral)
tab_paciente, tab_registro_prof, tab_panel_prof, tab_admin = st.tabs([
    "🔍 Buscar / IA",
    "📝 Registro Profesional",
    "👨‍⚕️ Panel Profesional",
    "🛡️ Admin SaludClic"
])

# ==============================================================================
# PESTAÑA 1: PACIENTE (BUSCADOR + ORIENTADOR IA + RESERVA CON PIN)
# ==============================================================================
with tab_paciente:
    st.subheader("🤖 Orientador Inteligente SaludClic")
    consulta_ia = st.text_input(
        "Cuéntanos qué servicio o especialista buscas (Ej: turno de enfermería en Bello, fisioterapia, psicólogo virtual):",
        placeholder="Escribe aquí lo que necesitas..."
    )
    if consulta_ia:
        txt = consulta_ia.lower()
        if any(p in txt for p in ["turno", "cuidador", "auxiliar", "enfermer", "curacion", "inyect"]):
            st.success("💡 **Sugerencia SaludClic:** Contamos con **Auxiliares de Enfermería y Enfermeros Jefes verificados** para atención a domicilio. Revisa las tarjetas abajo y solicita tu servicio sin costo adicional.")
        elif any(p in txt for p in ["fisio", "terapia", "rehabilita", "fono", "dolor"]):
            st.success("💡 **Sugerencia SaludClic:** Te recomendamos nuestros especialistas en **Fisioterapia y Rehabilitación (Nivel 2)** con las mejores calificaciones verificadas.")
        elif any(p in txt for p in ["psico", "ansiedad", "pareja", "mental"]):
            st.success("💡 **Sugerencia SaludClic:** Puedes agendar con **Psicología Clínica** tanto en modalidad **Virtual** como Presencial.")
        else:
            st.info("💡 **Sugerencia SaludClic:** Aquí tienes nuestros profesionales con sello Verificado ReTHUS ordenados por calificación real de otros pacientes.")

    st.divider()
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filtro_mod = st.selectbox("Modalidad de atención:", ["Todas", "Domicilio", "Virtual", "Consultorio"])
    with col_f2:
        orden = st.selectbox("Ordenar por:", ["Mejor calificados ⭐", "Menor tarifa 💲"])

    lista_profs = [p for p in st.session_state.profesionales if p["verificado"] and p["creditos_disp"] > 0]
    if orden == "Mejor calificados ⭐":
        lista_profs.sort(key=lambda x: x["estrellas"], reverse=True)

    for prof in lista_profs:
        if filtro_mod == "Domicilio" and prof["tarifa_domicilio"] == 0:
            continue
        if filtro_mod == "Virtual" and prof["tarifa_virtual"] == 0:
            continue
        if filtro_mod == "Consultorio" and prof["tarifa_consultorio"] == 0:
            continue

        with st.container(border=True):
            st.markdown(f"### {prof['nombre']} <span class='badge-verificado'>✔️ Verificado ReTHUS</span>", unsafe_allow_html=True)
            st.markdown(f"**{prof['profesion']}** • ⭐ **{prof['estrellas']}** ({prof['resenas']} pacientes atendidos)")
            st.caption(f"📍 Cobertura / Ubicación: {prof['zonas']}")

            precios = []
            modalidades_disp = []
            if prof["tarifa_domicilio"] > 0:
                precios.append(f"🏠 Domicilio: **${prof['tarifa_domicilio']:,}**")
                modalidades_disp.append("Domicilio")
            if prof["tarifa_virtual"] > 0:
                precios.append(f"💻 Virtual: **${prof['tarifa_virtual']:,}**")
                modalidades_disp.append("Virtual")
            if prof["tarifa_consultorio"] > 0:
                precios.append(f"🏥 Consultorio: **${prof['tarifa_consultorio']:,}**")
                modalidades_disp.append("Consultorio")
            st.markdown(" | ".join(precios))

            with st.expander("📅 Solicitar Cita / Servicio"):
                nom_pac = st.text_input("Nombre completo", key=f"nom_{prof['id']}")
                ced_pac = st.text_input("Número de Cédula", key=f"ced_{prof['id']}")
                cel_pac = st.text_input("WhatsApp de contacto", key=f"cel_{prof['id']}")
                mod_sel = st.selectbox("Elige modalidad", modalidades_disp, key=f"mod_{prof['id']}")
                fec_sel = st.text_input("Fecha y hora solicitada (Recuerda: cambios o cancelaciones mín. 24h antes)", placeholder="Ej: Jueves 3:00 PM", key=f"fec_{prof['id']}")

                if st.button("Enviar Solicitud de Cita", key=f"btn_{prof['id']}", type="primary"):
                    if not nom_pac or not ced_pac or not cel_pac or not fec_sel:
                        st.warning("Por favor completa todos tus datos para generar el PIN de seguridad.")
                    elif ced_pac in st.session_state.pacientes_bloqueados:
                        st.error("🚨 Tu cédula tiene una verificación pendiente por una cita previa. Confirma primero qué ocurrió con tu última reserva para poder agendar de nuevo.")
                    else:
                        pin_nuevo = str(random.randint(1000, 9999))
                        cred_cita = calcular_creditos(prof["nivel"], mod_sel)
                        st.session_state.citas.append({
                            "id_cita": len(st.session_state.citas) + 1,
                            "prof_id": prof["id"],
                            "prof_nombre": prof["nombre"],
                            "paciente": nom_pac,
                            "cedula_pac": ced_pac,
                            "celular_pac": cel_pac,
                            "modalidad": mod_sel,
                            "fecha": fec_sel,
                            "creditos": cred_cita,
                            "pin": pin_nuevo,
                            "link_virtual": "",
                            "estado": "Solicitada",
                            "calificado": False
                        })
                        st.success(f"✅ ¡Solicitud enviada a {prof['nombre']}! Guarda tu PIN de atención: **{pin_nuevo}** (Entrégalo al profesional únicamente cuando te atienda para habilitar tu calificación).")

    st.divider()
    st.subheader("⭐ Calificar una Atención Recibida")
    st.caption("Solo habilitado para pacientes con cita confirmada mediante PIN.")
    citas_calificables = [c for c in st.session_state.citas if c["estado"] == "Completada_Con_Pin" and not c["calificado"]]
    if not citas_calificables:
        st.info("Cuando un profesional ingrese tu PIN tras atenderte, aquí aparecerá el formulario para calificarlo.")
    for c in citas_calificables:
        with st.container(border=True):
            st.write(f"Cita #{c['id_cita']} con **{c['prof_nombre']}** (Paciente: {c['paciente']})")
            estrellas_nuevas = st.slider("Calificación", 1, 5, 5, key=f"star_{c['id_cita']}")
            comentario = st.text_input("Comentario sobre la atención", key=f"com_{c['id_cita']}")
            if st.button("Publicar Calificación Verificada", key=f"pub_{c['id_cita']}"):
                c["calificado"] = True
                st.success("¡Gracias! Tu calificación verificada ha sido registrada.")
                st.rerun()

# ==============================================================================
# PESTAÑA 2: REGISTRO DE NUEVOS PROFESIONALES (CON CARGA DE SOPORTES)
# ==============================================================================
with tab_registro_prof:
    st.subheader("Únete a la red de especialistas de SaludClic")
    st.write("Regístrate, valida tu documentación (ReTHUS / Tarjeta Profesional) y recibe pacientes directos.")
    with st.form("form_registro_prof"):
        r_nombre = st.text_input("Nombre completo y título")
        r_cedula = st.text_input("Cédula de ciudadanía")
        r_cel = st.text_input("WhatsApp profesional")
        r_cat = st.selectbox("Categoría / Rol Profesional", [
            "Nivel 1 - Auxiliar de Enfermería / Cuidador (1 Crédito Domicilio)",
            "Nivel 2 - Enfermero Jefe / Médico General / Fisio / Fono / Psicología / Optometría (2 Créd. Presencial | 1 Créd. Virtual)",
            "Nivel 3 - Especialidad Base: Medicina Interna / Pediatría / Ginecología / Ortopedia (3 Créd. Presencial | 2 Créd. Virtual)",
            "Nivel 4 - Subespecialidad: Urología / Cardiología / Dermatología / Psiquiatría (4 Créd. Presencial | 3 Créd. Virtual)"
        ])
        r_zonas = st.text_input("Ciudad y Barrios de cobertura (o dirección de consultorio)")
        c_t1, c_t2, c_t3 = st.columns(3)
        r_t_dom = c_t1.number_input("Tarifa Domicilio ($ COP)", min_value=0, step=5000, value=85000)
        r_t_vir = c_t2.number_input("Tarifa Virtual ($ COP)", min_value=0, step=5000, value=50000)
        r_t_con = c_t3.number_input("Tarifa Consultorio ($ COP)", min_value=0, step=5000, value=0)
        st.file_uploader("Sube tu Foto de Perfil Real (Con uniforme o bata, fondo claro)", type=["jpg", "png", "jpeg"])
        st.file_uploader("Sube tus Soportes en PDF (Cédula, Diploma y Resolución/ReTHUS)", type=["pdf"], accept_multiple_files=True)

        enviado = st.form_submit_button("Enviar Documentos a Verificación")
        if enviado and r_nombre:
            nivel_num = int(r_cat.split(" ")[1])
            st.session_state.profesionales.append({
                "id": len(st.session_state.profesionales) + 1,
                "nombre": r_nombre, "profesion": r_cat.split(" - ")[1].split(" (")[0],
                "nivel": nivel_num, "zonas": r_zonas,
                "tarifa_domicilio": r_t_dom, "tarifa_virtual": r_t_vir, "tarifa_consultorio": r_t_con,
                "creditos_disp": 4, "creditos_ret": 0, "estrellas": 5.0, "resenas": 0, "verificado": False
            })
            st.success("🎉 ¡Registro enviado! El administrador verificará tus documentos en ReTHUS para activar tu perfil con tus créditos de bienvenida.")

# ==============================================================================
# PESTAÑA 3: PANEL DEL PROFESIONAL (BILLETERA DE CRÉDITOS Y GESTIÓN DE CITAS)
# ==============================================================================
with tab_panel_prof:
    st.subheader("Gestión de Agenda y Créditos (1 Crédito = $10.000 COP)")
    nombres_profs = [f"{p['id']} - {p['nombre']} ({p['profesion']})" for p in st.session_state.profesionales]
    sel_prof = st.selectbox("Selecciona tu perfil profesional (Simulación):", nombres_profs)
    id_sel = int(sel_prof.split(" - ")[0])
    prof_actual = next(p for p in st.session_state.profesionales if p["id"] == id_sel)

    m1, m2, m3 = st.columns(3)
    m1.metric("💳 Créditos Disponibles (Vigencia 90 días)", f"{prof_actual['creditos_disp']}")
    m2.metric("⏳ Créditos en Custodia (Citas activas)", f"{prof_actual['creditos_ret']}")
    m3.metric("Estado del Perfil", "✔️ Verificado" if prof_actual["verificado"] else "⏳ En revisión ReTHUS")

    with st.expander("➕ Recargar Paquete de Créditos (Vigencia 90 días)"):
        st.write("• **Paquete Básico (5 Créditos):** $50.000 COP")
        st.write("• **Paquete Pro (10 + 1 Gratis = 11 Créditos):** $100.000 COP")
        st.write("• **Paquete Plus (20 + 3 Gratis = 23 Créditos):** $200.000 COP")
        if st.button("Simular Recarga de 5 Créditos ($50.000 COP)"):
            prof_actual["creditos_disp"] += 5
            st.success("¡Se sumaron 5 créditos a tu billetera!")
            st.rerun()

    st.divider()
    st.markdown("### 📅 Mis Solicitudes de Pacientes")
    mis_citas = [c for c in st.session_state.citas if c["prof_id"] == prof_actual["id"]]
    if not mis_citas:
        st.info("Aún no tienes solicitudes de citas en este perfil.")

    for cita in mis_citas:
        with st.container(border=True):
            st.markdown(f"**Cita #{cita['id_cita']}** | **Paciente:** {cita['paciente']} | **Modalidad:** `{cita['modalidad']}` | **Horario:** {cita['fecha']}")
            st.write(f"Créditos requeridos para aceptar: **{cita['creditos']} Crédito(s)** (${cita['creditos']*10000:,} COP) | Estado: `{cita['estado']}`")

            if cita["estado"] == "Solicitada":
                c_ac, c_re = st.columns(2)
                if c_ac.button("✅ Confirmar Agenda y Aceptar", key=f"ac_{cita['id_cita']}"):
                    if prof_actual["creditos_disp"] >= cita["creditos"]:
                        prof_actual["creditos_disp"] -= cita["creditos"]
                        prof_actual["creditos_ret"] += cita["creditos"]
                        cita["estado"] = "Aceptada_En_Curso"
                        st.rerun()
                    else:
                        st.error("Saldo de créditos insuficiente. Recarga tu billetera para desbloquear este paciente.")
                if c_re.button("❌ Agenda Ocupada (Sin costo)", key=f"re_{cita['id_cita']}"):
                    cita["estado"] = "Rechazada_Por_Agenda"
                    st.rerun()

            elif cita["estado"] == "Aceptada_En_Curso":
                st.success(f"🔓 **Datos del Paciente Desbloqueados:** WhatsApp: **{cita['celular_pac']}** | Cédula: {cita['cedula_pac']}")
                if cita["modalidad"] == "Virtual":
                    link_v = st.text_input("Opcional: Pega aquí el enlace de Google Meet / Zoom para el paciente (o envíaselo por WhatsApp):", value=cita["link_virtual"], key=f"lk_{cita['id_cita']}")
                    if link_v:
                        cita["link_virtual"] = link_v

                pin_ingresado = st.text_input("Ingresa el PIN de 4 dígitos que te entregó el paciente:", key=f"pin_in_{cita['id_cita']}")
                b_pin, b_no = st.columns(2)
                if b_pin.button("✔️ Validar PIN y Completar Cita", key=f"vpin_{cita['id_cita']}"):
                    if pin_ingresado == cita["pin"]:
                        prof_actual["creditos_ret"] -= cita["creditos"]
                        prof_actual["resenas"] += 1
                        cita["estado"] = "Completada_Con_Pin"
                        st.success("¡Atención verificada con éxito! El paciente ya puede calificarte.")
                        st.rerun()
                    else:
                        st.error("El PIN no coincide. Pídele al paciente el código de 4 dígitos que le generó SaludClic.")
                if b_no.button("⚠️ Reportar: Paciente NO contestó / Canceló", key=f"no_{cita['id_cita']}"):
                    cita["estado"] = "En_Auditoria_Paciente_Bloqueado"
                    st.session_state.pacientes_bloqueados.add(cita["cedula_pac"])
                    st.warning("Se bloqueó temporalmente al paciente para verificar qué ocurrió y devolverte tus créditos.")
                    st.rerun()

# ==============================================================================
# PESTAÑA 4: PANEL ADMINISTRADOR (VERIFICACIÓN RETHUS Y AUDITORÍA DE CRÉDITOS)
# ==============================================================================
with tab_admin:
    st.subheader("🛡️ Panel de Control SaludClic (Administrador)")

    st.markdown("#### 1. Profesionales Pendientes de Verificación ReTHUS")
    pendientes = [p for p in st.session_state.profesionales if not p["verificado"]]
    if not pendientes:
        st.info("Todos los profesionales registrados están verificados.")
    for p in pendientes:
        with st.container(border=True):
            st.write(f"**{p['nombre']}** — {p['profesion']} (Nivel {p['nivel']})")
            if st.button(f"✔️ Aprobar ReTHUS y Publicar a {p['nombre']}", key=f"ap_{p['id']}"):
                p["verificado"] = True
                st.rerun()

    st.divider()
    st.markdown("#### 2. Auditoría de Cancelaciones y Pacientes Bloqueados")
    en_auditoria = [c for c in st.session_state.citas if c["estado"] == "En_Auditoria_Paciente_Bloqueado"]
    if not en_auditoria:
        st.info("No hay reportes pendientes de auditoría.")
    for c in en_auditoria:
        with st.container(border=True):
            st.error(f"🚨 Paciente Bloqueado: **{c['paciente']}** (Cédula: `{c['cedula_pac']}` | Tel: `{c['celular_pac']}`)")
            st.write(f"Profesional que reporta: **{c['prof_nombre']}** | Créditos en custodia: **{c['creditos']}**")
            ca1, ca2 = st.columns(2)
            if ca1.button("🔄 Confirmado: Paciente NO asistió (Devolver créditos al profesional)", key=f"dev_c_{c['id_cita']}"):
                prof_rep = next(p for p in st.session_state.profesionales if p["id"] == c["prof_id"])
                prof_rep["creditos_ret"] -= c["creditos"]
                prof_rep["creditos_disp"] += c["creditos"]
                c["estado"] = "Cancelada_Creditos_Devueltos"
                st.rerun()
            if ca2.button("🛑 Paciente demuestra que SÍ fue atendido (Consumir créditos y desbloquear paciente)", key=f"fra_c_{c['id_cita']}"):
                prof_rep = next(p for p in st.session_state.profesionales if p["id"] == c["prof_id"])
                prof_rep["creditos_ret"] -= c["creditos"]
                st.session_state.pacientes_bloqueados.discard(c["cedula_pac"])
                c["estado"] = "Completada_Con_Pin"
                st.rerun()
