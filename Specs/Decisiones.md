# Decisiones — Suite `erpico_debranding`

Registro de decisiones técnicas. Cada una: ¿qué?, ¿por qué?, ¿alternativas
rechazadas?, ¿impacto?

Estado de cada registro: `[x]` aceptada, `[ ]` propuesta, `[!]` revocada.

---

## D-01 — Marca dura "ERPICO" como brand del seed

- **Estado:** `[x]`
- **Qué:** todos los textos de marca se sustituyen por "ERPICO" fijo
  (hardcoded en overrides y en los reemplazos del parche de emails).
- **Por qué:** single-tenant sin necesidad de configuración; símbolos web,
  favicon e isotipo de ERPICO ya importados como assets estáticos.
- **Alternativas rechazadas:** variable de entorno / `ir.config_parameter`
  por marca (`brand_name`…) — más superficie de test sin necesidad real.
- **Impacto:** para otro cliente habría que derivar este módulo.

---

## D-02 — Logo de login estático (assets), no `company_logo`

- **Estado:** `[x]`
- **Qué:** el logo del login es un asset estático (`erpico-isotipo.png` +
  CSS), no el logo de la compañía de la UI.
- **Por qué:** la página de login no razona con la compañía/logo de forma
  uniforme en 19 Community; un asset es determinista, cacheable y
  reproducible en todas las tenant.
- **Impacto:** el `company_logo` de cada compañía no se refleja en el login.
  Documentado, asumido.

---

## D-03 — Menús de tiendas: reparent, no delete

- **Estado:** `[x]`
- **Qué:** `base.theme_store`, `base.menu_theme_store` y
  `base.menu_third_party` se mueven bajo `base.menu_ir_property` (fuera de
  cualquier raíz visible de apps). No se eliminan registros.
- **Por qué:** eliminar registros del seed rompe dependencias y complica
  upgrades; reparent es reversible y seguro.
- **Impacto:** visibles a administradores que expandan la jerarquía raw;
  asumido.

---

## D-04 — Emails legados: parche en `post_init_hook` + migración

- **Estado:** `[x]`
- **Qué:** los 4 `mail.template` de `auth_signup` con `body_html` almacenado
  con marca Odoo se reescriben con reemplazos quirúrgicos en
  `patches/legacy_emails.py`:
  ```python
  _REPLACEMENTS = [
      ('odoo.com', 'erpico.com'),
      ('Odoo Standard', 'ERPICO'),
      ('Odoo includes ... automated processes', _ABOUT_TEXT),
      ('Odoo Tour', 'ERPICO Tour'),
      ('Powered by <a href="https://www.odoo.com" ...>', 'Powered by'),
  ]
  ```
  La lógica vive en `patches/` (reutilizable) y se dispara desde
  `post_init_hook` del manifest + migración `19.0.1.1.0/post-migrate.py`
  (upgrade de bases ya instaladas).
- **Por qué:** son campos almacenados; el QWeb solo debranda lo dinámico.
- **Alternativas rechazadas:** regenerar los templates desde XML con
  `force_create` / retrocompat bad; cambiar el correo por completo rompe
  el body del cliente.
- **Impacto:** parche idempotente (2ª ejecución = 0 patcheos), mantiene
  estructura original del body. El contenido 100% personalizado sigue siendo
  del cliente.

---

## D-05 — Renombrar partner `OdooBot` → `ERPICO Assistant`

- **Estado:** `[x]`
- **Qué:** en el mismo parche se localiza el partner del bot interno de Odoo
  y se renombra.
- **Por qué:** aparece como autor/remitente en chatter, emails y archivos.
- **Detalle:** el partner del bot está marcado `active=False`; las búsquedas
  por defecto no lo ven (`ERPICO Assistant` no aparece en search normal hasta
  el cambio).

---

## D-06 — Rutas de BD: 403 en UI, POST no intervenido

- **Estado:** `[x]` (+ riesgo asumido)
- **Qué:** `/web/database/manager` y `/web/database/selector` → `Forbidden`
  (403). Los endpoints **POST** `/web/database/{create,drop,backup,restore}`
  quedan intactos.
- **Por qué:** con DB public domain público y auth de admin de BD externo,
  bloquear la UI quita la exposición superficial; intervenir los POST añade
  superficie de test y riesgo de efecto colateral en tools de
  backup/restore.
- **Riesgo:** ver `Bugs.md` **R-001**.

---

## D-07 — `get_views` strip de `upgrade_boolean` en settings

- **Estado:** `[x]`
- **Qué:** `res.config.settings.get_views` recorre los archs form de
  res.config.settings y elimina `widget="upgrade_boolean"` con lxml
  (XPath por atributo), antes de devolverlos.
- **Por qué:** en Community los widgets de "Upgrade" apuntan a la tienda de
  Odoo; debranding exige quitarlos de la UI.
- **Alternativas rechazadas:** editar views del seed (prohibido), JS de
  stripping en cliente (frágil y visible en flash de UI).
- **Impacto:** ninguna propiedad del arch se pierde; solo se elimina el
  atributo del widget.

---

## D-08 — Suite de tests en el módulo núcleo

- **Estado:** `[x]`
- **Qué:** `erpico_debranding/tests/` con clases `@tagged('erpico_debranding')`
  (TransactionCase + HttpCase) que cubren todas las superficies S1–S11.
- **Por qué:** validación reproducible fuera de sesiones HTTP manuales;
  requisito de calidad OCA.
- **Impacto:** la suite es el oráculo de regresión tras cualquier cambio.

---

## D-09 — Metadatos OCA

- **Estado:** `[x]`
- **Qué:** manifests con orden canónico de claves OCA, `license: LGPL-3`,
  `author: 'ERPICO, Santiago Vásquez'`, `website` apuntando al repo GitHub.
  `readme/` con fragments `DESCRIPTION`, `USAGE`, `CONFIGURE`,
  `CONTRIBUTORS`, `CHANGELOG`. Headers de copyright y licencia en todo
  archivo fuente.
- **Por qué:** compatibilidad con pipelines OCA/`oca-addons-repo-template`,
  Pylint de la comunidad y consumo humano/agentes del `readme/`.
- **Impacto:** el proyecto es publicable tal cual.