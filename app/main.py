import csv
import io
import json
import os
import uuid
from datetime import date, datetime
from pathlib import Path

import qrcode
from fastapi import BackgroundTasks, Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .ai import analyze_provider
from .auth import create_session_token, require_admin, verify_password
from .db import Base, SessionLocal, engine, get_db
from .document import DocumentError, extract_text
from .models import Event, Need, Provider
from .seed import seed

BASE_DIR = Path(__file__).resolve().parent
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "8"))
PRIVACY_URL = os.getenv(
    "COTECMAR_PRIVACY_URL",
    "https://www.cotecmar.com/en/descargas/corporate/politica-corporativa-de-tratamiento-de-datos-personales",
)
AI_AUTO_ANALYZE = os.getenv("AI_AUTO_ANALYZE", "true").lower() == "true"

app = FastAPI(title="COTECMAR Conecta IA", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.middleware("http")
async def pilot_no_cache(request: Request, call_next):
    response = await call_next(request)
    if request.url.path in {"/", "/admin", "/admin/login", "/static/public.js", "/static/admin.js", "/static/login.js", "/static/app.css"}:
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
    return response

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


def provider_dict(p: Provider) -> dict:
    return {
        "id": p.id,
        "company_name": p.company_name,
        "contact_name": p.contact_name,
        "contact_role": p.contact_role,
        "phone": p.phone,
        "email": p.email,
        "website": p.website,
        "linkedin": p.linkedin,
        "city": p.city,
        "company_size": p.company_size,
        "portfolio_summary": p.portfolio_summary,
        "document_name": p.document_name,
        "extracted_text": p.extracted_text or "",
    }


def need_dict(n: Need) -> dict:
    return {"id": n.id, "title": n.title, "category": n.category, "description": n.description, "source": n.source}


def run_provider_analysis(provider_id: int):
    db = SessionLocal()
    try:
        p = db.get(Provider, provider_id)
        if not p:
            return
        p.analysis_status = "processing"
        db.commit()
        needs = db.query(Need).filter(Need.active.is_(True)).all()
        try:
            result = analyze_provider(provider_dict(p), [need_dict(n) for n in needs])
            p.analysis_json = json.dumps(result, ensure_ascii=False)
            p.overall_score = int(result.get("overall_score", 0))
            p.classification = result.get("classification")
            p.sector = result.get("sector")
            p.analysis_status = "done"
        except Exception as exc:
            p.analysis_status = "error"
            p.analysis_json = json.dumps({"error": str(exc)}, ensure_ascii=False)
        db.commit()
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def public_form(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "privacy_url": PRIVACY_URL})


@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse(request=request, name="admin.html", context={"request": request})


@app.get("/admin/login", response_class=HTMLResponse)
def admin_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})


@app.get("/health")
def health():
    return {"status": "ok", "service": "COTECMAR Conecta IA"}


@app.get("/api/public/event")
def public_event(code: str | None = None, db: Session = Depends(get_db)):
    if code:
        event = db.query(Event).filter(Event.public_code == code, Event.active.is_(True)).first()
    else:
        event = db.query(Event).filter(Event.active.is_(True)).order_by(Event.event_date.desc(), Event.id.desc()).first()
    if not event:
        raise HTTPException(status_code=404, detail="No hay un evento activo")
    return {
        "name": event.name,
        "city": event.city,
        "venue": event.venue,
        "date": event.event_date.isoformat() if event.event_date else None,
        "code": event.public_code,
    }


@app.post("/api/providers")
async def create_provider(
    background_tasks: BackgroundTasks,
    event_code: str = Form(...),
    company_name: str = Form(...),
    contact_name: str = Form(...),
    contact_role: str = Form(""),
    phone: str = Form(...),
    email: str = Form(...),
    website: str = Form(""),
    linkedin: str = Form(""),
    city: str = Form(...),
    company_size: str = Form(...),
    portfolio_summary: str = Form(...),
    consent: bool = Form(False),
    document: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
):
    if not consent:
        raise HTTPException(status_code=400, detail="Debe autorizar el tratamiento de datos personales")
    if len(portfolio_summary.strip()) < 20:
        raise HTTPException(status_code=400, detail="Describa brevemente el portafolio de la empresa")
    event = db.query(Event).filter(Event.public_code == event_code, Event.active.is_(True)).first()
    if not event:
        raise HTTPException(status_code=400, detail="El evento no es válido o ya no está activo")

    filename = None
    mime = None
    file_bytes = None
    extracted = ""
    if document and document.filename:
        filename = Path(document.filename).name[:255]
        suffix = Path(filename).suffix.lower()
        if suffix not in {".pdf", ".docx"}:
            raise HTTPException(status_code=400, detail="Adjunte un archivo PDF o DOCX")
        file_bytes = await document.read()
        if len(file_bytes) > MAX_UPLOAD_MB * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"El archivo supera el límite de {MAX_UPLOAD_MB} MB")
        mime = document.content_type or "application/octet-stream"
        try:
            extracted = extract_text(filename, file_bytes)
        except DocumentError as exc:
            extracted = f"[Documento almacenado, extracción no disponible: {exc}]"

    p = Provider(
        event_id=event.id,
        company_name=company_name.strip()[:180],
        contact_name=contact_name.strip()[:160],
        contact_role=contact_role.strip()[:160] or None,
        phone=phone.strip()[:80],
        email=email.strip()[:180],
        website=website.strip()[:300] or None,
        linkedin=linkedin.strip()[:300] or None,
        city=city.strip()[:120],
        company_size=company_size.strip()[:80],
        portfolio_summary=portfolio_summary.strip(),
        document_name=filename,
        document_mime=mime,
        document_bytes=file_bytes,
        extracted_text=extracted,
        consent=True,
        consent_at=datetime.utcnow(),
        analysis_status="pending",
    )
    db.add(p)
    db.commit()
    db.refresh(p)

    if AI_AUTO_ANALYZE:
        background_tasks.add_task(run_provider_analysis, p.id)

    return {"ok": True, "provider_id": p.id, "analysis_status": p.analysis_status, "message": "Registro recibido correctamente"}


@app.post("/api/admin/login")
async def admin_login(request: Request):
    data = await request.json()
    if not verify_password(data.get("password", "")):
        raise HTTPException(status_code=401, detail="Clave incorrecta")
    response = JSONResponse({"ok": True})
    response.set_cookie(
        "cotecmar_session",
        create_session_token(),
        max_age=60 * 60 * 12,
        httponly=True,
        secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        samesite="strict",
    )
    return response


@app.post("/api/admin/logout")
def admin_logout(_: bool = Depends(require_admin)):
    response = JSONResponse({"ok": True})
    response.delete_cookie("cotecmar_session")
    return response


@app.get("/api/admin/summary")
def admin_summary(_: bool = Depends(require_admin), db: Session = Depends(get_db)):
    providers = db.query(Provider).order_by(Provider.created_at.desc()).all()
    events = db.query(Event).order_by(Event.event_date.desc(), Event.id.desc()).all()
    needs = db.query(Need).filter(Need.active.is_(True)).order_by(Need.id).all()
    scores = [p.overall_score for p in providers if p.overall_score is not None]

    def counts(items):
        out = {}
        for x in items:
            if x:
                out[x] = out.get(x, 0) + 1
        return sorted([{"name": k, "count": v} for k, v in out.items()], key=lambda z: z["count"], reverse=True)

    provider_rows = []
    for p in providers[:250]:
        provider_rows.append({
            "id": p.id,
            "company_name": p.company_name,
            "contact_name": p.contact_name,
            "email": p.email,
            "phone": p.phone,
            "city": p.city,
            "company_size": p.company_size,
            "sector": p.sector,
            "score": p.overall_score,
            "classification": p.classification,
            "analysis_status": p.analysis_status,
            "document_name": p.document_name,
            "event": p.event.name if p.event else "",
            "created_at": p.created_at.isoformat(),
        })

    event_rows = [{
        "id": e.id,
        "name": e.name,
        "city": e.city,
        "venue": e.venue,
        "date": e.event_date.isoformat() if e.event_date else None,
        "public_code": e.public_code,
        "active": e.active,
        "providers": len(e.providers),
    } for e in events]

    return {
        "kpis": {
            "providers": len(providers),
            "analyzed": sum(1 for p in providers if p.analysis_status == "done"),
            "pending": sum(1 for p in providers if p.analysis_status in {"pending", "processing"}),
            "avg_score": round(sum(scores) / len(scores), 1) if scores else 0,
            "high_affinity": sum(1 for p in providers if p.classification == "Alta afinidad"),
            "cities": len(set(p.city for p in providers if p.city)),
        },
        "cities": counts([p.city for p in providers])[:10],
        "sizes": counts([p.company_size for p in providers]),
        "sectors": counts([p.sector for p in providers])[:10],
        "providers": provider_rows,
        "events": event_rows,
        "needs": [need_dict(n) | {"active": n.active} for n in needs],
    }


@app.get("/api/admin/providers/{provider_id}")
def provider_detail(provider_id: int, _: bool = Depends(require_admin), db: Session = Depends(get_db)):
    p = db.get(Provider, provider_id)
    if not p:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    analysis = None
    if p.analysis_json:
        try:
            analysis = json.loads(p.analysis_json)
        except json.JSONDecodeError:
            analysis = {"raw": p.analysis_json}
    return provider_dict(p) | {
        "event": p.event.name if p.event else None,
        "analysis_status": p.analysis_status,
        "overall_score": p.overall_score,
        "classification": p.classification,
        "sector": p.sector,
        "analysis": analysis,
        "created_at": p.created_at.isoformat(),
        "consent_at": p.consent_at.isoformat() if p.consent_at else None,
    }


@app.post("/api/admin/providers/{provider_id}/analyze")
def analyze_now(provider_id: int, background_tasks: BackgroundTasks, _: bool = Depends(require_admin), db: Session = Depends(get_db)):
    p = db.get(Provider, provider_id)
    if not p:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    p.analysis_status = "pending"
    db.commit()
    background_tasks.add_task(run_provider_analysis, provider_id)
    return {"ok": True, "status": "pending"}


@app.get("/api/admin/providers/{provider_id}/document")
def provider_document(provider_id: int, _: bool = Depends(require_admin), db: Session = Depends(get_db)):
    p = db.get(Provider, provider_id)
    if not p or not p.document_bytes:
        raise HTTPException(status_code=404, detail="Documento no disponible")
    headers = {"Content-Disposition": f'attachment; filename="{p.document_name or "portafolio"}"'}
    return Response(content=p.document_bytes, media_type=p.document_mime or "application/octet-stream", headers=headers)


@app.post("/api/admin/needs")
async def create_need(request: Request, _: bool = Depends(require_admin), db: Session = Depends(get_db)):
    data = await request.json()
    title = (data.get("title") or "").strip()
    category = (data.get("category") or "").strip()
    description = (data.get("description") or "").strip()
    if not title or not category or not description:
        raise HTTPException(status_code=400, detail="Título, categoría y descripción son obligatorios")
    n = Need(title=title[:220], category=category[:120], description=description, source=(data.get("source") or "Carga administrativa")[:300], active=True)
    db.add(n)
    db.commit()
    db.refresh(n)
    return {"ok": True, "need": need_dict(n)}


@app.post("/api/admin/events")
async def create_event(request: Request, _: bool = Depends(require_admin), db: Session = Depends(get_db)):
    data = await request.json()
    name = (data.get("name") or "").strip()
    city = (data.get("city") or "").strip()
    if not name or not city:
        raise HTTPException(status_code=400, detail="Nombre y ciudad son obligatorios")
    event_date = None
    if data.get("date"):
        try:
            event_date = date.fromisoformat(data["date"])
        except ValueError:
            raise HTTPException(status_code=400, detail="Fecha inválida")
    e = Event(name=name[:180], city=city[:120], venue=(data.get("venue") or "")[:180] or None, event_date=event_date, public_code=str(uuid.uuid4()), active=True)
    db.add(e)
    db.commit()
    db.refresh(e)
    return {"ok": True, "event": {"id": e.id, "name": e.name, "public_code": e.public_code}}


@app.get("/api/admin/events/{event_id}/qr.png")
def event_qr(event_id: int, request: Request, _: bool = Depends(require_admin), db: Session = Depends(get_db)):
    e = db.get(Event, event_id)
    if not e:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    base = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
    if not base:
        proto = request.headers.get("x-forwarded-proto") or request.url.scheme
        host = request.headers.get("host") or request.url.netloc
        base = f"{proto}://{host}"
    target = f"{base}/?event={e.public_code}"
    img = qrcode.make(target)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return Response(content=buf.getvalue(), media_type="image/png", headers={"X-QR-Target": target})


@app.get("/api/admin/export.csv")
def export_csv(_: bool = Depends(require_admin), db: Session = Depends(get_db)):
    providers = db.query(Provider).order_by(Provider.created_at.desc()).all()
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["ID", "Evento", "Empresa", "Contacto", "Correo", "Teléfono", "Ciudad", "Tamaño", "Sector", "Afinidad", "Clasificación", "Fecha"])
    for p in providers:
        w.writerow([p.id, p.event.name if p.event else "", p.company_name, p.contact_name, p.email, p.phone, p.city, p.company_size, p.sector or "", p.overall_score if p.overall_score is not None else "", p.classification or "", p.created_at.isoformat()])
    data = buf.getvalue().encode("utf-8-sig")
    return StreamingResponse(io.BytesIO(data), media_type="text/csv; charset=utf-8", headers={"Content-Disposition": "attachment; filename=cotecmar_proveedores.csv"})
