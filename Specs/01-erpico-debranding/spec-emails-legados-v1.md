# Spec v1 — Parche de emails legados en `auth_signup`

**Fecha:** 2026-09-17
**Estado:** Implementada y verificada
**Superficie:** S10
**Módulos:** `erpico_debranding` (≥ 19.0.1.1.0)

---

## Problema

En Odoo 19 Community, las plantillas de correo de `auth_signup` tienen
`body_html` **almacenado con marca Odoo**: "Powered by Odoo", "Odoo Tour",
links a odoo.com y placeholder del bot `OdooBot`. La herencia QWeb NO alcanza
los campos almacenados → los correos salen con marca.

## Objetivos

1. Los 4 templates de `auth_signup` (set password, portal set password,
   unregistered, signup account created) muestran exclusivamente marca
   ERPICO al renderizar.
2. El parche es **idempotente** (instalación, upgrade, re-ejecución).
3. El bot interno deja de llamarse `OdooBot`.

## Alcance (criterios de aceptación)

| # | Criterio | Verificación |
|---|---|---|
| 1 | `ERPICO in body_html` para los 4 xmlids | `TestLegacyEmails::test_legacy_bodies_rebranded` |
| 2 | `odoo.com not in body_html` | ídem |
| 3 | `Odoo Tour not in body_html` | ídem |
| 4 | Sin partner llamado `OdooBot` (incl. inactivos) | `TestLegacyEmails::test_bot_partner_renamed` |
| 5 | Re-ejecución del parche → 0 cambios | max_executions (manual) |
| 6 | Render real `_render_field('body_html', {})` → ERPICO, 0 "Odoo" | QA shell |

## Diseño de implementación

### Mecánica (contorno)

```
al instalar (post_init_hook) ──► patch_legacy_emails(env)
al actualizar (post-migrate) ──► idénticos reemplazos inline      (no import! BUG-001)
```

### Estructura de datos (no mutar sin actualizar tests)

```python
LEGACY_EMAIL_XMLIDS = (
    'auth_signup.set_password_email',
    'auth_signup.portal_set_password_email',
    'auth_signup.mail_template_data_unregistered_users',
    'auth_signup.mail_template_user_signup_account_created',
)

_REPLACEMENTS = [
    ('odoo.com', 'erpico.com'),
    ('Odoo Standard', 'ERPICO'),
    ('Odoo includes ... automated processes', _ABOUT_TEXT),
    ('Odoo Tour', 'ERPICO Tour'),
    ('Powered by <a href="https://www.odoo.com" ...>', 'Powered by'),
]
```

### Reglas duras

1. `str()` al inicio de `_clean()` (BUG-002: `Markup.replace`).
2. El reemplazo de "Powered by" es el **último** de la lista (solo sobre
   texto ya saneado).
3. `patch_legacy_emails` recorre los xmlids, compara contra el cuerpo
   esperado y persiste con `env.cr.commit()` (BUG-003).
4. Cualquier extensión de la S10 va **aquí** o en su migración hija.

## Documentos que cierra

- `Decisiones.md` → D-04, D-05.
- `Bugs.md` → BUG-001, BUG-002, BUG-003.
- `TESTS_COVERAGE.md` → TestLegacyEmails (2 tests).

## Pendientes post-release

- [ ] Revisar si los templates del webclient (`mail.template` de descargas)
  requieren el mismo tratamiento.
- [ ] Evaluar si el `_ABOUT_TEXT` debe vivir en `ir.config_parameter`
  (cliente multi-marca).