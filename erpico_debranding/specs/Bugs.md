# Bitácora de Bugs — Suite `erpico_debranding`

Registro de defectos detectados en la suite `erpico_debranding` (Odoo 19
Community). Cada bug tiene un ID único e **inmutable** (`BUG-XXX`); al
resolverse, el bug se mueve de *Encontrados* a *Resueltos* conservando su ID.

## Leyenda

**Prioridad** (orden sugerido de atención):
- 🔴 **Crítica** — bloquea operación / pérdida de datos / cálculo incorrecto de dinero.
- 🟠 **Alta** — funcionalidad principal rota o ausente; sin workaround razonable.
- 🟡 **Media** — funciona con fricción o hay workaround; afecta la experiencia.
- ⚪ **Baja** — cosmético / configuración / menor.

**Tipo:** `Lógica` (negocio) · `UI/UX` · `Datos` · `Config` · `Seguridad`

**Estado:** `Abierto` · `En progreso` · `Resuelto` · `Pendiente-config`

## Cómo registrar un bug nuevo

Agregar una fila en *Bugs Encontrados* con el próximo `BUG-XXX` libre, fecha,
vista/origen, descripción, tipo y prioridad. Si tiene pasos de reproducción no
obvios, añadir un bloque en *Detalle de bugs abiertos*. Al resolverlo, moverlo a
*Bugs Resueltos* con el commit y la fecha, agrupado por lote de resolución.

---

## Bugs Encontrados (Abiertos)

| ID | Fecha | Vista / Origen | Descripción | Tipo | Prioridad | Estado |
|----|-------|----------------|-------------|------|-----------|--------|
| *(ninguno)* | | | | | | |

---

## Bugs Resueltos

Resuelto el **2026-09-22** (versión `19.0.1.3.0`):

| ID | Vista / Origen | Descripción | Tipo | Prioridad | Solución | Commit |
|----|----------------|-------------|------|-----------|----------|--------|
| BUG-008 | Fuga de marca — Menú de notificaciones (campana) | Al entrar a la BD, pestaña Notificaciones mostraba card "Install Odoo — Come here often? Install the app for quick and easy access!" (getter `installationRequest` en `mail/static/src/core/web/messaging_menu_patch.js`) + badge `counter`. | UI/UX | 🟡 Media | Patch `messaging_menu.js`: `MessagingMenu.prototype.canPromptToInstall = false` (punto único: mata card, badge y `hasPreviews`); push `notificationRequest` intacto. + `remove("install_pwa")` en `user_menu.js`. | `bb4314d` |
| BUG-009 | Fuga de marca — OdooBot (bienvenida y respuestas) | Bot se presentaba como "Odoo's chat helps employees..." (mail_bot `_init_odoobot`) y onboarding mencionaba `@OdooBot`, "Enjoy exploring Odoo!" y links `odoo.com/documentation` `odoo.com/slides`. | UI/UX | 🟡 Media | Override `_init_odoobot()` con texto neutro ERPICO; override `_get_style_dict()` sin links odoo.com; `_get_answer()` post-procesa `@OdooBot`→`@ERPICO Assistant` y "Enjoy exploring Odoo!"→"Enjoy exploring ERPICO!". | `bb4314d` |
| BUG-010 | Fuga de marca — Avatar y nombre del bot | Partner `base.partner_root` con nombre "OdooBot" e imagen `mail/static/src/img/odoobot.png`; icono fallback de notificaciones `odoobot_transparent.png` (`out_of_focus_service.js`). | Datos | ⚪ Baja | `post_init_hook._rebrand_bot_partner` + migración `19.0.1.3.0`: name "ERPICO Assistant", `image_1920` con placeholder `bot_placeholder.png`; patch JS `out_of_focus.js` para icono fallback. | `bb4314d` |
| BUG-011 | Runtime JS — crash total de la webclient | Al entrar, la webclient no cargaba: `Uncaught Error: Cannot add key "res_config_edition" in the "view_widgets" registry: it already exists`. El core `web` ya registra `res_config_edition` en `view_widgets`; `Registry.add()` sin `{ force: true }` lanza `DuplicatedKeyError` y aborta el module loader de `web.assets_backend`. | Lógica | 🔴 Crítica | Registrar con `{ force: true }` en `res_config_edition.js`. Detectado en browser real (CDP/Edge); los tests backend no ejercitan la webclient. | `e8fd8cf` |

Resuelto el **2026-09-17** (hot-fix posterior a `19.0.1.1.0`, sin bump de
versión; verificado con `-u` de los 3 módulos + `--test-enable
--test-tags=/erpico_debranding` → **11/11 tests, 0 failures, 0 errors**, 66
módulos):

| ID | Vista / Origen | Descripción | Tipo | Prioridad | Solución | Commit |
|----|----------------|-------------|------|-----------|----------|--------|
| BUG-005 | Ajustes → `get_views` | `node.getparent().remove(node)` eliminaba el `<field>` completo con `widget="upgrade_boolean"`, en vez de solo quitar el widget (contraviene D-07). | UI/UX | 🟡 Media | `node.attrib.pop('widget', None)` en `models/res_config_settings.py`; el campo permanece. Test `TestSettingsView` valida strip + arch >1000 chars. | `58367ba` |
| BUG-006 | Buscador de apps, wizards/API | El filtro `to_buy`/`module_to_buy` aplicaba solo en `search_fetch`/`search_count`; `.search()` plano (wizards, API server-side) seguía viendo Enterprise. | Lógica | 🟡 Media | Override de `search()` en `models/base.py` (`ir.module.module` + `payment.provider`) con escape `debranding_show_enterprise`; tests extendidos en `TestEnterpriseHidden`. | `58367ba` |
| BUG-007 | Registry (init de `ir.config_parameter`) | `TypeError: BaseModel.search() got an unexpected keyword argument 'count'`; el parámetro `count` de `search()` fue retirado en Odoo 17+. | Lógica | 🟠 Alta | Firma `(self, domain, offset=0, limit=None, order=None)` sin `count` en `Base.search` y `PaymentProvider.search`. | `58367ba` |

Resuelto el **2026-09-17** (versión `19.0.1.1.0`):

| ID | Vista / Origen | Descripción | Tipo | Prioridad | Solución | Commit |
|----|----------------|-------------|------|-----------|----------|--------|
| BUG-001 | Upgrade del módulo (migración) | `ModuleNotFoundError` en el post-migrate que importaba `patches/legacy_emails`: el paquete del módulo no existe durante la migración. | Lógica | 🟠 Alta | Migración autocontenida: `_REPLACEMENTS`/`_clean()` duplicados inline en `migrations/19.0.1.1.0/post-migrate.py`. | `5178073` |
| BUG-002 | Parche de emails legados | `markupsafe.Markup.replace` no matcheaba substrings de marca en `body_html`; los reemplazos se volatilizaban. | Datos | 🟡 Media | Coerción temprana `str(html)` en `_clean()` y reemplazos sobre `str` puro. | `5178073` |
| BUG-003 | Sesiones de validación (shell) | Las escrituras de `odoo shell` se descartaban al salir (sin `env.cr.commit()`); el renombrado del bot y los patcheos se revertían. | Config | 🟠 Alta | `env.cr.commit()` explícito en todo script de una sola escritura. Verificación: bot `OdooBot` → `ERPICO Assistant` persistido tras re-sesiones. | `5178073` |
| BUG-004 | Validación de overrides QWeb | `_get_combined_arch` no reflejaba los overrides de templates; validaciones "a ojo" daban falsos negativos. | Lógica | 🟡 Media | Proceso/QA: validar siempre por render real (`ir.ui.view._render`) o HTTP final; canonizado en `Manual_Pruebas_Testing.md`. | `f333dea` (docs) |

---

*Estado: `Abierto` · `En progreso` · `Resuelto` · `Pendiente-config`.*