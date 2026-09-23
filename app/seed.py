from datetime import date
import uuid
from sqlalchemy.orm import Session
from .models import Event, Need

DEFAULT_NEEDS = [
    ("Astillero 4.0: automatización, integración e IA", "Tecnología", "Capacidades para automatización industrial, integración de sistemas, datos, analítica, inteligencia artificial, control de producción, inspección y gestión documental.", "Contexto estratégico COTECMAR / Astillero 4.0"),
    ("Material de aislamiento", "Industrial", "Suministro de materiales de aislamiento para aplicaciones navales e industriales.", "Proceso ADM 004-2026"),
    ("Accesorios navales", "Industrial", "Suministro de accesorios navales y elementos afines para proyectos de construcción, reparación y mantenimiento.", "Invitación ADM-015-2026"),
    ("Energía no regulada", "Servicios", "Suministro de energía no regulada para la operación de Planta Mamonal.", "Invitación ADM-058-2026"),
    ("Ingeniería para control de inundaciones", "Ingeniería", "Ingeniería de detalle e implementación de soluciones que mitiguen y controlen inundaciones en infraestructura de COTECMAR.", "Invitación ADM-066-2026"),
    ("Outsourcing de ofimática y mesa de ayuda", "Tecnología", "Servicios de ofimática, mesa de ayuda, mantenimiento preventivo y correctivo de equipos de cómputo, con informes para toma de decisiones.", "Invitación ADM-043-2026"),
    ("Gases industriales", "Industrial", "Suministro de gases industriales para operaciones en Planta Mamonal y Planta Bocagrande.", "Proceso ADM 006-2026"),
    ("Abrasivos, soldaduras y accesorios", "Industrial", "Suministro de abrasivos, soldaduras, accesorios de soldadura y elementos afines.", "Invitación ADM-014-2026"),
]

def seed(db: Session):
    if db.query(Event).count() == 0:
        db.add(Event(name="Encuentro de Proveedores – Bucaramanga", city="Bucaramanga", venue="Cámara de Comercio de Bucaramanga", event_date=date(2026, 9, 24), public_code=str(uuid.uuid4()), active=True))
    if db.query(Need).count() == 0:
        for title, category, description, source in DEFAULT_NEEDS:
            db.add(Need(title=title, category=category, description=description, source=source, active=True))
    db.commit()
