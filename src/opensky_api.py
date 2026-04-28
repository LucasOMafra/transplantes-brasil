"""
opensky_api.py
Integração com a OpenSky Network API (gratuita, sem autenticação).
Rastreia aeronaves em tempo real sobre o território brasileiro.
Documentação: https://openskynetwork.github.io/opensky-api/
"""

import json
import math
import urllib.request
import urllib.error
from datetime import datetime
from typing import Optional

BRASIL_BBOX = {
    "lat_min": -33.75,
    "lat_max":   5.27,
    "lon_min": -73.99,
    "lon_max": -28.85,
}

CENTROS_TRANSPLANTE = {
    "HC-SP (USP)":              (-23.557, -46.669),
    "HCFMUSP Coração":          (-23.558, -46.671),
    "Santa Casa-RS":            (-30.035, -51.219),
    "HC-UFPR":                  (-25.411, -49.265),
    "HGF-CE":                   (-3.7318, -38.548),
    "HUPES-BA":                 (-12.973, -38.501),
    "Hospital Albert Einstein": (-23.601, -46.717),
    "INCA-RJ":                  (-22.896, -43.184),
}

BASE_URL = "https://opensky-network.org/api"


def _get(endpoint: str, params: dict = None, timeout: int = 15) -> Optional[dict]:
    url = f"{BASE_URL}{endpoint}"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query}"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "transplantes-brasil-research/1.0"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  [OpenSky] HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"  [OpenSky] Conexão falhou: {e.reason}")
    except Exception as e:
        print(f"  [OpenSky] Erro inesperado: {e}")
    return None


def buscar_aeronaves_brasil() -> list[dict]:
    params = {
        "lamin": BRASIL_BBOX["lat_min"],
        "lamax": BRASIL_BBOX["lat_max"],
        "lomin": BRASIL_BBOX["lon_min"],
        "lomax": BRASIL_BBOX["lon_max"],
    }
    data = _get("/states/all", params)
    if not data or "states" not in data or not data["states"]:
        return []

    campos = [
        "icao24", "callsign", "origin_country", "time_position",
        "last_contact", "longitude", "latitude", "baro_altitude",
        "on_ground", "velocity", "true_track", "vertical_rate",
        "sensors", "geo_altitude", "squawk", "spi", "position_source"
    ]
    aeronaves = []
    for s in data["states"]:
        av = dict(zip(campos, s))
        av["callsign"] = (av.get("callsign") or "").strip()
        aeronaves.append(av)
    return aeronaves


def _centro_mais_proximo(lat: float, lon: float) -> dict:
    melhor = {"nome": "Desconhecido", "distancia_km": 9999}
    for nome, (clat, clon) in CENTROS_TRANSPLANTE.items():
        dlat = math.radians(lat - clat)
        dlon = math.radians(lon - clon)
        a = (math.sin(dlat / 2) ** 2
             + math.cos(math.radians(clat))
             * math.cos(math.radians(lat))
             * math.sin(dlon / 2) ** 2)
        dist = 6371 * 2 * math.asin(math.sqrt(a))
        if dist < melhor["distancia_km"]:
            melhor = {"nome": nome, "distancia_km": round(dist, 1)}
    return melhor


def filtrar_candidatos_orgaos(aeronaves: list[dict]) -> list[dict]:
    candidatos = []
    for av in aeronaves:
        alt = av.get("baro_altitude") or 0
        vel = av.get("velocity") or 0
        no_solo = not av.get("on_ground", True)
        lat = av.get("latitude")
        lon = av.get("longitude")

        if no_solo and 50 <= alt <= 12000 and 20 <= vel <= 250 and lat and lon:
            av["centro_mais_proximo"] = _centro_mais_proximo(lat, lon)
            candidatos.append(av)
    return candidatos


def estatisticas_snapshot(aeronaves: list[dict]) -> dict:
    if not aeronaves:
        return {"total": 0}
    em_voo = [a for a in aeronaves if not a.get("on_ground")]
    altitudes = [a["baro_altitude"] for a in em_voo if a.get("baro_altitude")]
    velocidades = [a["velocity"] for a in em_voo if a.get("velocity")]
    paises = {}
    for a in aeronaves:
        p = a.get("origin_country", "Desconhecido")
        paises[p] = paises.get(p, 0) + 1
    return {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total_aeronaves": len(aeronaves),
        "em_voo": len(em_voo),
        "em_solo": len(aeronaves) - len(em_voo),
        "altitude_media_m": round(sum(altitudes) / len(altitudes), 0) if altitudes else 0,
        "velocidade_media_ms": round(sum(velocidades) / len(velocidades), 1) if velocidades else 0,
        "top_paises": sorted(paises.items(), key=lambda x: -x[1])[:5],
    }


def imprimir_snapshot(aeronaves: list[dict], candidatos: list[dict]) -> None:
    stats = estatisticas_snapshot(aeronaves)
    sep = "─" * 55
    print(f"\n{'═'*55}")
    print("  OPENSKY NETWORK — SNAPSHOT BRASIL")
    print(f"  {stats.get('timestamp', 'N/A')}")
    print(f"{'═'*55}")
    print(f"  Total de aeronaves detectadas : {stats['total_aeronaves']:>6}")
    print(f"  Em voo                        : {stats['em_voo']:>6}")
    print(f"  Em solo                       : {stats['em_solo']:>6}")
    print(f"  Altitude média (em voo)       : {stats['altitude_media_m']:>6.0f} m")
    print(f"  Velocidade média              : {stats['velocidade_media_ms']:>6.1f} m/s")
    print(f"\n  Top países de origem:")
    print(sep)
    for pais, qtd in stats.get("top_paises", []):
        print(f"    {pais:<30} {qtd:>4} aeronaves")
    print(f"\n  Candidatos a voos de transporte: {len(candidatos)}")
    print(sep)
    if candidatos:
        for av in candidatos[:10]:
            cs = av["callsign"] or "(sem callsign)"
            alt = av.get("baro_altitude", 0) or 0
            vel = (av.get("velocity") or 0) * 3.6
            centro = av.get("centro_mais_proximo", {})
            print(f"    {cs:<10} | Alt {alt:>6.0f}m | {vel:>5.0f} km/h"
                  f" | ↔ {centro.get('nome','?')} ({centro.get('distancia_km','?')} km)")
    else:
        print("    Nenhum candidato encontrado no momento.")
    print(f"\n{'═'*55}\n")
