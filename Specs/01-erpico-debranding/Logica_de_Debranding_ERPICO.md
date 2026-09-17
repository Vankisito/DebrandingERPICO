# Lógica de Debranding — `erpico_debranding`

Documento de referencia para comprender **qué decisión mueve cada línea de
código**. Se mantiene al día con el código; los humanos y los agentes IA
deben leerlo antes de modificar el módulo.

---

## 1. Modelo mental

**Del lado servidor:**

```
petición → middleware → controllers del seed
             │
             ├─ get_views(settings)      → strip upgrade_boolean
             ├─ search_fetch (apps)      → to_buy=False
             ├─ search_fetch (providers) → module_to_buy=False
             ├─ registro de menús        → reparent theme_store/x/third_party
             └─ render de templates      → QWeb con pointers ERPICO
```

**En el arranque (instalación/upgrade):**

```
post_init_hook o migración → patch_legacy_emails(env)
   ├─ 4 mail.template.body_html reemplazados (str-safe)
   └─ res.partner OdooBot → ERPICO Assistant
```

## 2. Reglas de oro del filtro de módulos

1. El filtro se aplica **en ORM** (`search_fetch`, `search_count`), no en
   vistas: así PHP/JS/anyclient recibe lo mismo.
2. `domain + [('to_buy','=',False)]` es AND — nunca `DomainAnd` (deprecado
   en 19).
3. El contexto `debranding_show_enterprise=True` **desactiva** el filtro
   (escape para auditoría). Es la única "configuración" del módulo; por
   diseño no es un `ir.config_parameter`.

**Ojo:** los parches de email/corporate **NO** pasan por este filtro:
aplican siempre (son datos).

## 3. Qué se SILENCIA y qué se EDITA

| Caso | Modo | Dónde |
|---|---|---|
| `to_buy` en módulos | ORM filter | `models/base.py` |
| `module_to_buy` en providers | ORM filter | `models/base.py` |
| widgets `upgrade_boolean` | lxml strip | `models/res_config_settings.py` |
| menús de tienda | infijo reparent | `data/ir_ui_menu.xml` |
| botón "Connect with your software!" | QWeb override | `views/templates.xml` |
| textos fijos de marca | QWeb override + parche | `views/*` + `patches/legacy_emails.py` |

## 4. Flujo de decisión (para un agente)

```
Pregunta: ¿aparece marca Odoo en X?
├─ ¿Proviene de un template render dinámico?  → override QWeb
├─ ¿Proviene de un campo almacenado?          → patch + migración
├─ ¿Es una ruta/aplicación entera?            → controller o filter ORM
└─ ¿Es un widget JS de la UI admin?           → JS registry / lxml strip
```

## 5. Notas técnicas que evitan bugs

- `search_fetch` en 19 acepta `field_names` → llamar con kwargs posicionales
  cuidando la firma (`super().search_fetch(domain, field_names=field_names,
  **kwargs)`).
- `get_views` strip: usar `lxml.etree` con XPath
  `//field[@widget='upgrade_boolean']`; re-serializar el arch y devolver
  `result['views'][str(view_id)]['arch']` actualizado. Si el campo no existe
  en ese arch, no rompe.
- Patcheo de emails: SIEMPRE `str(html)` antes de `str.replace`; `Markup`
  rompe el matching (BUG-002).
- Idempotencia: el parche comprueba antes de reemplazar (si ya fue
  patcheado en migración → 0 patcheos).

## 6. Referencia rápida de nombres

| Símbolo | Dónde |
|---|---|
| `patch_legacy_emails` | `patches/legacy_emails.py` |
| `_REPLACEMENTS` | `patches/legacy_emails.py` |
| `LEGACY_EMAIL_XMLIDS` | `patches/legacy_emails.py` |
| `restrict_database_routes` | `controllers/main.py` |
| `post_init_hook` | `__init__.py` del módulo |
| `erpico_debranding` tests | `tests/test_debranding.py` |
| isotipo | `static/src/img/erpico-isotipo.png` |
| recibo POS | `erpico_debranding_pos/static/src/override/order_receipt.xml` |