# Spec v1 — Portal de ventas/compra sin "Connect with your software!"

**Fecha:** 2026-09-17
**Estado:** Implementada y verificada
**Superficie:** S12
**Módulo:** `erpico_debranding_sale` (19.0.1.0.0)

---

## Problema

El portal de Odoo 19 añade a las páginas públicas de cotizaciones y órdenes
de compra el bloque "Connect with your software!" (`portal.portal_content_boot`
y `sale.portal_content_boot`) con un modal de ficheros EDI. Hace referencia
al ecosistema Odoo y a Odoo Account.

## Objetivo

Ningún cliente externo que abra una cotización o una orden de compra
publicada ve el botón ni su modal.

## Alcance (criterios de aceptación)

| # | Criterio | Verificación |
|---|---|---|
| 1 | Template `sale.portal_content_boot` sin el botón | render manual |
| 2 | Template `purchase.portal_content_boot` idem | render manual |
| 3 | Sin referencias a `odoo.com` en la página de la cotización | QA shell |

## Diseño de implementación

`views/sale_portal_templates.xml`:

```xml
<template id="sale_portal_remove_connect"
          inherit_id="sale.portal_content_boot"
          name="Remove Odoo connect for sale portal">
    <xpath expr="//a[hasclass('o_portal_connect_button')]/.."
           position="replace"/>
</template>
```

Mismo patrón para `purchase.portal_content_boot` desde
`erpico_debranding_sale` reutilizando el objeto Apache (QWeb hereda por
`inherit_id` de `purchase.portal_content_boot`).

### Reglas duras

1. El XPath usa `replace` completo del nodo botón (más robusto que `t-if`).
2. Si `erpico_debranding_sale` se instala sin `sale` o `purchase`, el
   install falla → la dependencia es declarada en el manifest.
3. No mover botones; solo eliminar la referencia de marca.

## Documentos que cierra

- `BDD` → BN-10.
- `TESTS_COVERAGE.md` → QA manual.

## Pendientes post-release

- [ ] Test automatizado con `HttpCase` del portal (requiere cotización
  publicada).
- [ ] Revisar `digest` (envío de resumen de ventas) que también renderiza
  botón de marca.