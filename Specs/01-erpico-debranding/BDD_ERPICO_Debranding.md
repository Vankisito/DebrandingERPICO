# BDD — Especificación por comportamiento — `erpico_debranding`

Formato Gherkin. Cada historia se mapea a una superficie S# y a un caso de
`tests/test_debranding.py` (T#) o a QA manual.

---

## BN-01 — Login totalmente ERPICO

```gherkin
Funcionalidad: Página de login con marca ERPICO
  Como usuario final
  Quiero no ver ninguna referencia a Odoo en /web/login
  Para que la identidad de la instalación sea ERPICO

  Escenario: login por defecto
    Dado una base Community 19 con el módulo erpico_debranding instalado
    Cuando solicito GET /web/login
    Entonces el código de estado es 200
    Y el título es "ERPICO"
    Y el favicon es erpico-isotipo.png
    Y el footer contiene "Powered by <b>ERPICO</b>"
    Y no existe el enlace "Manage Databases"
    Y el body no contiene "odoo.com"
```

## BN-02 — Apps sin módulos Enterprise

```gherkin
Funcionalidad: Ocultar módulos de pago del listado de apps
  Como administrador
  Quiero no ver los módulos de Odoo Enterprise en el buscador
  Para no promocionar compras de módulos

  Escenario: filtro por defecto
    Dado el módulo M con to_buy=True
    Cuando busco M en el buscador de apps
    Entonces M no aparece
    Y el contador de apps no incluye M

  Escenario: escape de auditoría
    Dado el contexto debranding_show_enterprise=True
    Cuando busco M en el buscador de apps
    Entonces M aparece
```

## BN-03 — Provider de pago de pago (módulos a comprar) oculto

```gherkin
Funcionalidad: Ocultar providers module_to_buy
  Como vendedor
  Quiero no ver los métodos de pago de módulos de pago en el sistema
  Para no ofrecer compras desde la UI

  Escenario: filtro y escape
    Dado payment.provider P con module_to_buy=True
    Cuando busco P con search_fetch
    Entonces P no aparece en el resultado
    Y con contexto debranding_show_enterprise=True P aparece
```

## BN-04 — Ajustes sin widgets de upgrade

```gherkin
Funcionalidad: Ajustes sin upgrade_boolean
  Como usuario con permisos de settings
  Quiero no ver los campos marcados como upgrade
  Para no hacer referencia a productos de pago

  Escenario: vista de settings
    Dado la vista V de res.config.settings con field widget='upgrade_boolean'
    Cuando uso get_views(V)
    Entonces el arch devuelto no contiene 'upgrade_boolean'
    Y el campo sigue existiendo en el arch
```

## BN-05 — Menús de tiendas recolocados

```gherkin
Funcionalidad: Menús de tiendas de apps fuera de la raíz visible
  Como usuario común
  Quiero no ver menús de marcas de apps en la navegación
  Para que la jerarquía sea ERPICO

  Escenario: reparent
    Dado el módulo instalado
    Cuando miro ir.ui.menu
    Entonces theme_store, menu_theme_store y menu_third_party
    Y su parent_id es base.menu_ir_property
```

## BN-06 — Footer / brand promotion ERPICO

```gherkin
Funcionalidad: Texto de promoción de marca
  Como usuario cualquiera
  Quiero ver "Powered by ERPICO" en el footer y en las páginas públicas
  Para reforzar la marca

  Escenario: render dinámico
    Cuando renderizo web.brand_promotion_message
    Entonces el texto contiene "ERPICO" y no contiene "Odoo" ni "odoo.com"
```

## BN-07 — Emails QWeb debranded

```gherkin
Funcionalidad: Layouts de correo sin marca Odoo
  Como destinatario de emails
  Quiero no recibir ninguna página web de correo con marca Odoo

  Escenario: render de mail_notification_layout
    Cuando renderizo mail.mail_notification_layout
    Entonces el texto contiene "ERPICO"
    Y no contiene "odoo.com"
```

## BN-08 — Emails legados con body_html almacenado (patcheados)

```gherkin
Funcionalidad: Templates de correo legados de auth_signup ERPICO
  Como destinatario de emails de registro
  Quiero que los correos pre-almacenados no muestren marca Odoo

  Escenario: parche tras instalación/upgrade
    Dado que los 4 mail.template de auth_signup tienen body_html
    Cuando se instala o actualiza el módulo
    Entonces cada body_html contiene "ERPICO"
    Y no contiene "odoo.com" ni "Odoo Tour"
    Y el patcheo es idempotente (segunda ejecución = 0 cambios)

  Escenario: bot interno
    Dado el partner OdooBot
    Cuando se instala o actualiza el módulo
    Entonces su nombre es "ERPICO Assistant"
```

## BN-09 — Gestión de base de datos bloqueada en UI

```gherkin
Funcionalidad: Bloquear la consola de BD
  Como usuario web
  Quiero no poder abrir /web/database/manager ni /web/database/selector
  Para no exponer operaciones de administración de la base

  Escenario: rutas bloqueadas
    Cuando solicito GET /web/database/manager
    Entonces el código de estado es 403
    Cuando solicito GET /web/database/selector
    Entonces el código de estado es 403
```

## BN-10 — Portal de ventas/compra sin botón de conectarse

```gherkin
Funcionalidad: Portal sale/purchase debranded
  Como cliente con cotización/orden de compra publicada
  Quiero no ver el botón "Connect with your software!"
  Para no hacer referencia al ecosistema de Odoo

  Escenario: render del portal
    Dado erpico_debranding_sale instalado
    Cuando renderizo el portal de una cotización
    Entonces no aparece el botón ni el modal de conexión
```

## BN-11 — Recibo POS "Powered by ERPICO"

```gherkin
Funcionalidad: Recibo de venta sin marca Odoo
  Como cajero
  Quiero que el recibo impreso lleve "Powered by ERPICO"
  Para consistencia de marca en tienda

  Escenario: override del recibo
    Dado erpico_debranding_pos instalado
    Cuando un pedido POS genera el recibo
    Entonces la línea de marca es "Powered by ERPICO"
```

---

## Trazabilidad

| Historia | Superficie | Test automatizado | QA manual/HTTP |
|---|---|---|---|
| BN-01 | S1, S2 | `TestDebrandingHttp::test_login_debranded` | login 5783 bytes |
| BN-02 | S3 | `TestEnterpriseHidden::test_module_to_buy_hidden_*` | contadores apps |
| BN-03 | S4 | `TestEnterpriseHidden::test_payment_provider_*` | — |
| BN-04 | S5 | `TestSettingsView::test_get_views_strips_upgrade_boolean` | — |
| BN-05 | S7 | `TestMenus::test_store_menus_reparented` | — |
| BN-06 | S8 | `TestBrandedRenders::test_brand_promotion_message` | — |
| BN-07 | S9 | `TestBrandedRenders::test_mail_layout_render` | renders shell |
| BN-08 | S10 | `TestLegacyEmails::*` | renders + idempotencia |
| BN-09 | S11 | `TestDebrandingHttp::test_database_*` | curl 403 |
| BN-10 | S12 | — (manual) | render portal |
| BN-11 | S13 | — (manual) | render recibo |