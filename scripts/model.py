"""Shared helpers: load/save the data file and resolve its layers into the view model."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "services.json"

TF_KINDS = {"resource": "resources", "data_source": "data-sources"}


def load(path=DATA):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(data, path=DATA):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def deep_merge(base, over):
    """Dicts merge key by key; anything else in `over` replaces `base`."""
    if isinstance(base, dict) and isinstance(over, dict):
        out = dict(base)
        for k, v in over.items():
            out[k] = deep_merge(base[k], v) if k in base else v
        return out
    return over


def version_key(v):
    return tuple(int(p) for p in re.findall(r"\d+", v))


def tf_docs_url(providers, provider, kind, type_name):
    p = providers[provider]
    short = type_name[len(provider) + 1:] if type_name.startswith(provider + "_") else type_name
    return f"https://registry.terraform.io/providers/{p['namespace']}/{p['name']}/latest/docs/{TF_KINDS[kind]}/{short}"


def tf_status(resources, gaps, arm_types, override=None):
    """full | partial | listed | azapi-only | none | unchecked | unknown (see docs/data-model.md).

    "full" is only ever set by a human (manual.terraform.status); the pipeline can only prove that
    the tracked resources exist, which is "listed".
    """
    if override:
        return override
    if not resources:
        return "azapi-only" if arm_types else "unknown"
    if any(r["exists"] is None for r in resources):
        return "unchecked"
    found = [r for r in resources if r["exists"]]
    if not found:
        return "azapi-only" if arm_types else "none"
    return "partial" if gaps or len(found) < len(resources) else "listed"


def resolve_terraform(data, svc, merged):
    providers = data["terraform_providers"]
    tracked = svc["tracking"]["terraform"]
    checked = {r["type"]: r for r in svc["fetched"].get("terraform", {}).get("resources", [])}
    resources = []
    for t in tracked:
        got = checked.get(t["type"], {})
        resources.append({
            "provider": t["provider"], "kind": t["kind"], "type": t["type"],
            "docs_url": tf_docs_url(providers, t["provider"], t["kind"], t["type"]),
            "exists": got.get("exists"), "since": got.get("since"),
        })
    manual = merged.get("terraform", {})
    gaps = manual.get("gaps", [])
    sinces = [r["since"] for r in resources if r["exists"] and r["since"]]
    all_since = all(r["since"] for r in resources if r["exists"])
    arm_types = svc["tracking"]["arm_types"]
    fallback = None
    if arm_types:
        docs = providers["azapi"]["docs_url"] + "/resources/"
        checked_arm = {a["type"]: a["documented"] for a in svc["fetched"].get("terraform", {}).get("arm_types", [])}
        fallback = {
            "provider": "azapi", "resource": "azapi_resource", "docs_url": docs + "resource",
            "arm_types": [{
                "type": a, "documented": checked_arm.get(a),
                "docs_url": docs + a.replace("/", "_") if checked_arm.get(a) else None,
            } for a in arm_types],
        }
    return {
        "status": tf_status(resources, gaps, arm_types, manual.get("status")),
        "resources": resources,
        "first_supported": min(sinces, key=version_key) if sinces and all_since else None,
        "fully_supported_since": max(sinces, key=version_key) if sinces and all_since else None,
        "gaps": gaps,
        "content": manual.get("content", []),
        "compared": manual.get("compared"),
        "fallback": fallback,
        "note": manual.get("note", ""),
        "changed_at": svc["fetched"].get("terraform", {}).get("changed_at"),
    }


def resolve(data):
    """Merge fetched + manual per service and derive Terraform status. Output has no layers."""
    tiers = {t["tier"]: t["label"] for t in data["tiers"]}
    services = []
    for svc in data["services"]:
        merged = deep_merge(svc["fetched"], svc["manual"])
        fresh = svc["freshness"]
        services.append({
            "id": svc["id"], "name": svc["name"], "tier": svc["tier"], "tier_label": tiers[svc["tier"]],
            "category": svc["category"],
            "purpose": merged.get("purpose", ""),
            "facts": merged.get("facts", []),
            "cloud_native": merged.get("cloud_native", {"level": "unrated", "note": ""}),
            "cost": merged.get("cost", {"level": "unrated", "confirmed": False, "note": "", "billed": "", "sources": [], "checked_at": None}),
            "docs": [{"url": u} for u in svc["tracking"]["learn_urls"]],
            "review": svc["review"],
            "freshness": {"status": fresh["status"], "changed_at": fresh["changed_at"]},
            "terraform": resolve_terraform(data, svc, merged),
        })
    return {
        "schema_version": data["schema_version"],
        "scope": data["scope"],
        "tiers": data["tiers"],
        "categories": data["categories"],
        "cloud_native_scale": data["cloud_native_scale"],
        "cost_scale": data["cost_scale"],
        "comparisons": data["comparisons"],
        "edge_types": data["edge_types"],
        "edge_group_order": data["edge_group_order"],
        "terraform_providers": data["terraform_providers"],
        "services": services,
        "stubs": data["stubs"],
        "edges": data["edges"],
    }
