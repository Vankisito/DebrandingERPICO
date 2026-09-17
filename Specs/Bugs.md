# Bugs — Suite `erpico_debranding`

| ID | Estado | Severidad | Resumen |
|---|---|---|---|
| BUG-001 | Pack | Alta | Migración con import de módulo |
| BUG-002 | Pack | Media | `Markup.replace` inconsistente |
| BUG-003 | Pack | Alta | Escrituras del shell descartadas |
| BUG-004 | Pack | Media | `_get_combined_arch` no refleja overrides |
| R-001 | Abierto | Alta | POST de gestión de BD sin intervenir |

---

## BUG-001 — Migración con import de módulo

**Síntoma:** `ModuleNotFoundError` al ejecutar el post-migrate que importaba
`patches/legacy_emails`.

**Causa:** durante una migración el paquete del módulo aún no es importable
desde el entorno de migración (`odoo.tools.misc` / migration script).

**Fix:** migración autocontenida; `_REPLACEMENTS` y `_clean()` duplicados
inline en `migrations/19.0.1.1.0/post-migrate.py`.

---

## BUG-002 — `markupsafe.Markup.replace` inconsistente

**Síntoma:** los reemplazos de marca no se aplicaban en `body_html` aunque
la gestión de strings parecía correcta.

**Causa:** `Markup` de `markupsafe` tiene `replace` que preserva el flag de
markup; al operar cadenas mixtas el resultado se volatiliza o no matchea.

**Fix:** coerción temprana `str(html)` en `_clean()` y reemplazos sobre `str`
puro.

---

## BUG-003 — Escrituras del shell de Odoo descartadas

**Síntoma:** el `OdooBot` renombrado volvía a aparecer como `OdooBot`, y los
templates parcheados se revertían entre sesiones.

**Causa:** `odoo shell` no hace commit automático; sin `env.cr.commit()`
todo cambio se descarta al salir.

**Fix:** `env.cr.commit()` explícito en todo script de una sola escritura.

---

## BUG-004 — `_get_combined_arch` no refleja overrides QWeb

**Síntoma:** la validación "a ojo/`_get_combined_arch`" no mostraba los
cambios de templates planos concernientes al header/footer.

**Causa:** para QWeb planos el combined arch del template en la versión 19
no propaga de forma fiable los overrides.

**Fix:** validar siempre por render real (`ir.ui.view._render`) o HTTP final.

---

## R-001 — Endpoints POST de gestión de BD expuestos

**Síntoma:** `/web/database/manager` y `/web/database/selector` bloqueados,
pero `/web/database/create|drop|backup|restore` (POST) siguen respondiendo.

**Causa:** se decidió (D-06) no tocar los POST para minimizar superficie de
cambio; la autenticación del admin de BD es responsabilidad del deploy.

**Impacto:** en un deploy sin proxy que proteja `create/drop/backup/restore`,
cualquiera con acceso a la red puede intentar operaciones de BD.

**Acción recomendada:** exponer el servicio únicamente en red interna o
detrás de reverse proxy con auth; revisitar si el cliente lo pide.

---

*Estado: `Abierto` / `Pack` / `Won't fix` / `Env ejemplo`.*