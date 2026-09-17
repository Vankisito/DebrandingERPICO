# Diccionario de Recursos — `erpico_debranding`

Catálogo verbatim de todos los recursos que consume o entrega la suite
(referencias de XML/QWeb, assets, xmlids de parche). Convención de nombres:
`prefix_` = prefijo del módulo.

---

## 1. Estructura de archivos del núcleo

```
erpico_debranding/
├── __init__.py                 (post_init_hook)
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── main.py                 (403 en /web/database/*)
├── data/
│   └── ir_ui_menu.xml          (reparent)
├── migrations/
│   └── 19.0.1.1.0/
│       └── post-migrate.py
├── models/
│   ├── __init__.py
│   ├── base.py                 (filtros to_buy)
│   └── res_config_settings.py  (strip upgrade_boolean)
├── patches/
│   ├── __init__.py
│   └── legacy_emails.py        (parche idempotente)
├── readme/
│   ├── DESCRIPTION.rst
│   ├── USAGE.rst
│   ├── CONFIGURE.rst
│   ├── CONTRIBUTORS.rst
│   └── CHANGELOG.rst
├── static/src/
│   ├── img/erpico-isotipo.png
│   ├── js/user_menu.js
│   ├── scss/debranding.scss
│   └── settings_form_view/res_config_edition.xml
├── tests/
│   ├── __init__.py
│   └── test_debranding.py
└── views/
    ├── templates.xml
    ├── emails.xml
    └── portal.xml
```

## 2. Xmlids definidos en views

| Xmlid | Tipo | Uso |
|---|---|---|
| `erpico_debranding.web_login_layout_erpico` | template QWeb | login |
| `erpico_debranding.web_layout_erpico_footer` | template QWeb | footer web |
| `erpico_debranding.portal_record_sidebar_erpico` | template QWeb | sidebar portal |
| `erpico_debranding.email_layouts_rebrand` | template QWeb | layouts de email |
| `erpico_debranding.reset_password_rebrand` | template QWeb | reset password |
| `erpico_debranding.res_config_edition_erpico` | template OWL (assets) | tarjeta About |
| `erpico_debranding.user_menu_items_erpico` | JS registry entry | menú de usuario |

## 3. Templados heredados (seed) que se sobreescriben

| Template seed | Módulo padre | Override en |
|---|---|---|
| `web.login_layout` | web | `views/templates.xml` |
| `web.layout` | web | `views/templates.xml` |
| `web.brand_promotion_message` | web | `views/templates.xml` |
| `portal.portal_record_sidebar` | portal | `views/portal.xml` |
| `mail.mail_notification_layout` | mail | `views/emails.xml` |
| `mail.mail_notification_light` | mail | `views/emails.xml` |
| `auth_signup.reset_password_email` | auth_signup | `views/emails.xml` |
| `sale.portal_content_boot` | sale | `erpico_debranding_sale/views/sale_portal_templates.xml` |
| `purchase.portal_content_boot` | purchase | `erpico_debranding_sale/views/sale_portal_templates.xml` |
| `point_of_sale.OrderReceipt` (order_receipt.xml) | point_of_sale | `erpico_debranding_pos/static/src/override/order_receipt.xml` |

## 4. Menús tocados (data/ir_ui_menu.xml)

| Xmlid seed | Operación |
|---|---|
| `base.theme_store` | parent_id → `base.menu_ir_property` |
| `base.menu_theme_store` | parent_id → `base.menu_ir_property` |
| `base.menu_third_party` | parent_id → `base.menu_ir_property` |

## 5. Email templates legados parcheados (LEGACY_EMAIL_XMLIDS)

| Xmlid | Plantilla | Estado post-parche |
|---|---|---|
| `auth_signup.set_password_email` | Set Password | ERPICO, sin odoo.com |
| `auth_signup.portal_set_password_email` | Portal Set Password | ídem |
| `auth_signup.mail_template_data_unregistered_users` | Unregistered | ídem |
| `auth_signup.mail_template_user_signup_account_created` | Signup | ídem |

Todos: `body_html` reescrito con `_REPLACEMENTS` (str-safe), idempotente.

## 6. Registros de datos (seed) no tocados pero relevantes

| Registro | Por qué importa |
|---|---|
| partner `OdooBot` (inactivo) | renombrado a `ERPICO Assistant` |
| `payment.provider` con `module_to_buy=True` | ocultos por filtro |
| `ir.module.module` con `to_buy=True` | ocultos por filtro |

## 7. Assets declarados en manifest

### `erpico_debranding`
```
web.assets_backend:
  erpico_debranding/static/src/js/user_menu.js
  erpico_debranding/static/src/scss/debranding.scss
  erpico_debranding/static/src/settings_form_view/res_config_edition.xml
web.assets_frontend:
  erpico_debranding/static/src/scss/debranding.scss
```

### `erpico_debranding_pos`
```
point_of_sale.assets_prod:
  erpico_debranding_pos/static/src/override/order_receipt.xml
```

### `erpico_debranding_sale`
```
data: [views/sale_portal_templates.xml]
```

## 8. Assets de marca importados (estáticos)

| Asset | Procedencia |
|---|---|
| `erpico-isotipo.png` | logo isotipo ERPICO (PNG) |
| `debranding.scss` | SCSS de los overrides del layout |