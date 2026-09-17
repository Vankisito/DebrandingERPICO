# Changelog — Suite `erpico_debranding`

Bitácora versionada por sesiones. Semana (año-semana), decisiones y cambios
relevantes. Documento vivo.

---

## 2026-09-17 — Sesión 1: implementación de la suite

**Entorno:** Odoo 19.0 FINAL build, Docker Compose (`odoo_debrand_test` app
+ `db` postgres), base `debrand_test`.

- Montaje del scaffold de los 3 módulos y sus assets estáticos (isotipo,
  SCSS) bajo `Custom_addons/`.
- Implementadas las 13 superficies del plan (S1–S13):
  - QWeb `web.login_layout` / `web.layout` (título, favicon, footer).
  - Filtros `search_fetch`/`search_count` en `base` para `to_buy`
    (módulos) y `module_to_buy` (payment providers).
  - `res.config.settings.get_views` stripping de `upgrade_boolean`.
  - Registry JS: fuera `support` y `odoo_account`.
  - Reparent de 3 menús de tienda.
  - Footer de portal y correo; layouts de email y reset password.
  - Rutas `/web/database/*` → 403 (UI).
  - `erpico_debranding_sale`: portal ventas/compras sin "Connect with your
    software!".
  - `erpico_debranding_pos`: recibo POS "Powered by ERPICO".
- Activación completa con `-u` de los 3 módulos: 0 errores, 66 módulos
  cargados.
- Instalación verificada por HTTP: login 5783 bytes, 404 con ERPICO y sin
  odoo.com, rutas de BD 403, favicon isotipo, contadores de apps
  coherentes.
- Riesgo R-001 detectado (POST de BD sin intervenir) → decisión D-06.

## 2026-09-17 — Sesión 2: fix de emails legados

- Detectado: los 4 `mail.template` de `auth_signup` con `body_html`
  almacenado seguían mostrando marca Odoo.
- Implementado `patches/legacy_emails.py` + `post_init_hook` +
  migración `19.0.1.1.0`.
  1ª tentativa: la migración intentó importar el paquete de módulo →
  `ModuleNotFoundError` (el paquete no existe durante la migración).
  Reescrito como **migración autocontenida** (reemplazos inline).
- Quirk descubierto: `markupsafe.Markup.replace` se comporta mal con
  substrings; mitigado con `str()` al inicio del `_clean()`.
- Quirk descubierto: el shell de Odoo **no auto-commitea** → las replicas
  manuales se descartaban; forzado `env.cr.commit()`.
- Verificación final: render real de los 4 templates (lens 4145/4533/3789,
  ERPICO dentro, 0 "Odoo"), idempotencia del parche, renombrado del partner
  `OdooBot` → `ERPICO Assistant` persistido.
- Suite HTTP final PASS (login, 404, manager/selector 403, isotipo).

## 2026-09-17 — Sesión 3: publicación Git + OCA + documentación

- Creado el repo GitHub `Vankisito/DebrandingERPICO`; inicializado con
  raíz en `Custom_addons/` (corrección: el repo debe vivir dentro del
  árbol de módulos, no en la raíz del workspace).
- `git init`, `.gitignore`, commit inicial (26 archivos, 413
  inserciones), `push -u origin main` → HEAD `5178073`.
- Pasados los 3 módulos a convenciones OCA: headers, manifests,
  `readme/` fragments, suite de tests `tests/test_debranding.py`.
- Documentada la suite completa en `Specs/`.

## 2026-09-17 — Sesión 4: fixes de módulo + autor

- Autor de los 3 módulos cambiado a **Habitat Digital** (manifests, headers
  ©, readme `CONTRIBUTORS`, `Specs/`) — commit `ba167eb`.
- Auditoría del código encontró 2 desviaciones + 1 bug fatal introducido al
  corregirlas (documentados en `Bugs.md`):
  - **BUG-005:** `get_views` eliminaba el `<field>` completo con widget
    `upgrade_boolean` (contra D-07) → fix: `node.attrib.pop('widget')`.
  - **BUG-006:** filtro Enterprise no cubría `.search()` plano →
    override de `search()` en `base.py` + tests de `search()`/escape.
  - **BUG-007:** `search(count=...)` no existe en ORM 19 → `TypeError` en
    registry; firma sin `count`.
- Suite completa re-validada: `-u` de los 3 módulos con
  `--test-enable --test-tags=/erpico_debranding` → **0 failed, 0 errors,
  11 tests, 66 módulos** — commit `58367ba`.
- `Specs/Bugs.md` y `Specs/TESTS_COVERAGE.md` actualizados.

---

*Próxima sesión 2026-09-18 o posterior: pendientes de `Specs/Bugs.md` y
revisión de R-001.*