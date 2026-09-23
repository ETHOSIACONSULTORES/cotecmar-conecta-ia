import json
import os
import re
from collections import Counter

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5")

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "sector": {"type": "string"},
        "provider_summary": {"type": "string"},
        "categories": {"type": "array", "items": {"type": "string"}},
        "products": {"type": "array", "items": {"type": "string"}},
        "services": {"type": "array", "items": {"type": "string"}},
        "capabilities": {"type": "array", "items": {"type": "string"}},
        "certifications": {"type": "array", "items": {"type": "string"}},
        "keywords": {"type": "array", "items": {"type": "string"}},
        "overall_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "classification": {"type": "string", "enum": ["Alta afinidad", "Afinidad media", "Baja afinidad", "Información insuficiente"]},
        "executive_assessment": {"type": "string"},
        "strengths": {"type": "array", "items": {"type": "string"}},
        "gaps": {"type": "array", "items": {"type": "string"}},
        "recommended_next_step": {"type": "string"},
        "matches": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "need_id": {"type": "integer"},
                    "need_title": {"type": "string"},
                    "score": {"type": "integer", "minimum": 0, "maximum": 100},
                    "rationale": {"type": "string"},
                    "evidence": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["need_id", "need_title", "score", "rationale", "evidence"]
            }
        }
    },
    "required": ["sector", "provider_summary", "categories", "products", "services", "capabilities", "certifications", "keywords", "overall_score", "classification", "executive_assessment", "strengths", "gaps", "recommended_next_step", "matches"]
}

def _clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", s or " ").strip()

def analyze_with_openai(provider: dict, needs: list[dict]) -> dict:
    from openai import OpenAI
    client = OpenAI()
    needs_text = "\n".join(
        f"NECESIDAD {n['id']} | {n['title']} | Categoría: {n['category']} | {n['description']}"
        for n in needs
    )
    portfolio = _clean_text(provider.get("portfolio_summary", ""))
    doc = _clean_text(provider.get("extracted_text", ""))[:42000]
    prompt = f"""
Analiza un proveedor para apoyar el proceso de abastecimiento de COTECMAR. El resultado es una herramienta de priorización para revisión humana, no una decisión de contratación.

DATOS DEL PROVEEDOR
Empresa: {provider['company_name']}
Ciudad: {provider['city']}
Tamaño declarado: {provider['company_size']}
Resumen ingresado: {portfolio}
Texto extraído del portafolio: {doc if doc else '[Sin documento legible]'}

NECESIDADES ACTIVAS DE COTECMAR
{needs_text}

Instrucciones:
- Identifica sector, productos, servicios, capacidades y certificaciones únicamente con evidencia disponible.
- Cruza capacidades contra TODAS las necesidades y devuelve en matches solo las 5 con mayor relación.
- El score debe medir pertinencia técnica/comercial aparente, no reputación ni elegibilidad jurídica.
- Penaliza ausencia de evidencia. No inventes experiencia, clientes, certificaciones ni capacidades.
- En evidence usa fragmentos muy breves o hechos presentes en el texto; si no hay evidencia, indícalo.
- La recomendación debe ser operativa: priorizar revisión, solicitar información, mantener en base o baja prioridad.
"""
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": "Eres analista de abastecimiento y clasificación de proveedores. Sé preciso, explicable y conservador."}]},
            {"role": "user", "content": [{"type": "input_text", "text": prompt}]},
        ],
        text={"format": {"type": "json_schema", "name": "provider_match", "strict": True, "schema": SCHEMA}},
    )
    return json.loads(response.output_text)

def analyze_fallback(provider: dict, needs: list[dict]) -> dict:
    source = " ".join([provider.get("portfolio_summary", ""), provider.get("extracted_text", "")]).lower()
    tokens = [x for x in re.findall(r"[a-záéíóúñ0-9]{4,}", source) if x not in {"para", "como", "desde", "esta", "este", "empresa", "servicio", "servicios", "productos", "soluciones"}]
    common = [w for w, _ in Counter(tokens).most_common(12)]
    matches = []
    for n in needs:
        need_tokens = set(re.findall(r"[a-záéíóúñ0-9]{4,}", (n["title"] + " " + n["description"]).lower()))
        hits = sorted(set(tokens) & need_tokens)
        score = min(95, len(hits) * 13)
        if score:
            matches.append({"need_id": n["id"], "need_title": n["title"], "score": score, "rationale": "Coincidencia léxica preliminar; requiere validación humana.", "evidence": hits[:5]})
    matches = sorted(matches, key=lambda x: x["score"], reverse=True)[:5]
    overall = int(sum(m["score"] for m in matches[:3]) / max(1, min(3, len(matches)))) if matches else 10
    classification = "Alta afinidad" if overall >= 75 else "Afinidad media" if overall >= 45 else "Baja afinidad"
    return {
        "sector": "Por validar",
        "provider_summary": provider.get("portfolio_summary", "")[:500],
        "categories": common[:5],
        "products": [],
        "services": [],
        "capabilities": common[:8],
        "certifications": [],
        "keywords": common,
        "overall_score": overall,
        "classification": classification,
        "executive_assessment": "Análisis de contingencia basado en coincidencias de texto. Configure OPENAI_API_KEY para análisis semántico completo.",
        "strengths": ["Portafolio capturado y disponible para clasificación"],
        "gaps": ["Análisis semántico no ejecutado porque no hay proveedor de IA configurado"],
        "recommended_next_step": "Configurar el motor de IA y reanalizar el proveedor.",
        "matches": matches,
    }

def analyze_provider(provider: dict, needs: list[dict]) -> dict:
    if os.getenv("OPENAI_API_KEY"):
        return analyze_with_openai(provider, needs)
    return analyze_fallback(provider, needs)
