# Bugs — Suite `erpico_debranding`

| ID | Estado | Severidad | Resumen |
|---|---|---|---|
| BUG-001 | Pack | Alta | Migración con import de módulo |
| BUG-002 | Pack | Media | `Markup.replace` inconsistente |
| BUG-003 | Pack | Alta | Escrituras del shell descartadas |
| BUG-004 | Pack | Media | `_get_combined_arch` no refleja overrides |
| BUG-005 | Pack | Media | `get_views` eliminaba el campo entero con widget |
| BUG-006 | Pack | Media | Filtro Enterprise no cubría `search()` plano |
| BUG-007 | Pack | Alta | `search(count=...)` inexistente en ORM 19 |
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

## BUG-005 — `get_views` eliminaba el campo entero con widget de upgrade

**Síntoma:** los `<field widget="upgrade_boolean">` desaparecían de la vista
de Ajustes por completo, en vez de perder solo el widget.

**Causa:** `res_config_settings.py` usaba `node.getparent().remove(node)`
contraviniendo lo documentado (D-07: solo quitar el atributo).

**Fix:** `node.attrib.pop('widget', None)`.

**Resuelto en:** commit `58367ba`. Validación: suite `--test-enable` 11/11
verde + HTTP Ajustes sin cambio funcional.

---

## BUG-006 — Filtro Enterprise no cubría `search()` plano

**Síntoma:** el debranding de `to_buy`/`module_to_buy` aplicaba vía
`search_fetch`/`search_count` pero no en `.search()` plano (wizards,
API server-side).

**Causa:** el override original solo interceptaba `search_fetch` y
`search_count`; `search()` pasaba el dominio sin filtrar.

**Fix:** override de `search()` en `base.py` (modelos `ir.module.module` y
`payment.provider`) con el mismo dominio y escape por contexto
`debranding_show_enterprise`; tests extendidos en `TestEnterpriseHidden`
(`search()` plano + escape en ambos modelos).

**Resuelto en:** commit `58367ba`. Validación: `TestEnterpriseHidden` → PASS.

---

## BUG-007 — `search(count=...)` inexistente en ORM 19

**Síntoma:** `TypeError: BaseModel.search() got an unexpected keyword
argument 'count'` en el registry (init de `ir.config_parameter`).

**Causa:** el parámetro `count` de `search()` fue retirado en Odoo 17+; el
override inicial lo re-enviaba a `super().search()` con `count=count`.

**Fix:** firma `(self, domain, offset=0, limit=None, order=None)` sin `count`
(en `Base.search` y `PaymentProvider.search`).

**Resuelto en:** commit `58367ba`. Validación: `-u` de los 3 módulos →
registry carga OK, 66 módulos, 0 errores.

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