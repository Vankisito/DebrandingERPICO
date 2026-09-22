# Arquitectura — `erpico_debranding` (núcleo)

Cuando un humano o un agente IA mira este módulo, **esto es lo que hay que
ver**: de qué dependen los cambios, dónde vive cada override y qué artefacto
consumidor los recoge. No es un manual de setup (va en `readme/`).

---

## 1. Capa de datos (más vieja, más estable)

| Componente | Qué hace | Quién lo consume |
|---|---|---|
| `data/ir_ui_menu.xml` | infijo `ir.ui.menu`: 3 menús de tiendas reparent bajo `menu_ir_property` | La parte donde los menús de apps viven; evita pasarelas de venta públicas |
| `demo/` | — | No uses demo aquí; el debranding no necesita datasets |
| `migrations/19.0.1.1.0/post-migrate.py` | Reemplazos de marca en `mail.template.body_html` de auth_signup + renombra el bot | Bases que **ya tenían** datos antes del upgrade |

## 2. Capa de negocio (modelos)

| Modelo | Método | Qué hace |
|---|---|---|
| `models/base.py` — `Base` (`_inherit='base'`) | `search_fetch(drilldown)` / `search_count(domain)` | Filtra `ir.module.module` por `to_buy=False` (solo los módulos instalables Community), escape por contexto `debranding_show_enterprise`; igual para `payment.provider.module_to_buy` |
| `models/res_config_settings.py` | `get_views(views)` | **lxml** remueve `widget="upgrade_boolean"` de los archs de settings antes de devolverlos |
| `models/base.py` — `Models` generales | — | Sin otros hooks; la herencia se limita a lo listado |

Detalle de `models/base.py` (el meollo del filtro Enterprise):

```python
@api.model
def search_fetch(self, domain, field_names=None, **kwargs):
    if self._name == 'ir.module.module' \
            and not self.env.context.get('debranding_show_enterprise'):
        domain = [*domain, ('to_buy', '=', False)]
    elif self._name == 'payment.provider' \
            and not self.env.context.get('debranding_show_enterprise'):
        domain = [*domain, ('module_to_buy', '=', False)]
    return super().search_fetch(domain, field_names=field_names, **kwargs)
```

Regla del dominio: **AND por concatenación de listas**, nunca
`odoo.osv.expression` (el API 19 lo deprecó).

## 3. Capa de presentación (lo que ve el usuario)

| Superficie | Artefacto | Template/JS |
|---|---|---|
| Login | QWeb `web.login_layout` / `web.layout` | título, favicon, `footer Powered by ERPICO`, logo isotipo, sin link de DB |
| Web genérica | `web.layout` | 404, errores, etc. |
| Portal | `portal.portal_record_sidebar` | footer + branding en páginas públicas |
| Ajustes | `res_config_edition.xml` (OWL) | tarjeta About ERPICO, sin menú de upgrade |
| Menú usuario | `user_menu.js` (OWL registry) | quita `support` y `odoo_account` |

Los assets se declaran en `assets` del manifest (backend y frontend) y se
recogen en `web.assets_backend` / `web.assets_frontend`. **Nunca** inyectes
CSS/JS por `web.assets_%s.py` heredado.

## 4. Capa de servicios (controllers)

| Ruta | Controller | Respuesta |
|---|---|---|
| `/web/database/manager` | `Forbidden` a mano (no `@http.route` de db) | 403 |
| `/web/database/selector` | misma técnica | 403 |

El resto del `db` controller del seed queda intacto (riesgo R-001).

## 5. Arranque: `post_init_hook`

`__init__.py` hace `from . import controllers, models` (nada más).

```python
def post_init_hook(cr, registry):
    from odoo.addons.erpico_debranding.patches.legacy_emails import (
        patch_legacy_emails)
    env = api.Environment(cr, SUPERUSER_ID, Context())
    patched = patch_legacy_emails(env)
    _logger.info("[erpico_debranding] legacy emails patched: %r", patched)
```

Esto solo dispara en **instalaciones nuevas** (dependencias ya cargadas);
las bases existentes llegan por la migración.

## 6. Flujo de un upgrade

```
odoo -u erpico_debranding → -u aplica migración 19.0.1.1.0
  1. reemplazos body_html (4 templates)
  2. renombra OdooBot → ERPICO Assistant
  3. commitea (transaction)
→ vistas/controllers/assets recargados → suite tests opcional
--test-enable
```

## 7. Límites del módulo

- NO toca: `point_of_sale` ni portal sale/purchase (vas a los módulos
  compañeros).
- NO toca: endpoints POST de BD (R-001), webservice/API de Odoo (x2).
- El debranding es **visual y de navegación**; el código del seed nunca
  cambia.