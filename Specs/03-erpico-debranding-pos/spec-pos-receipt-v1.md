# Spec v1 — Recibo de punto de venta "Powered by ERPICO"

**Fecha:** 2026-09-17
**Estado:** Implementada y verificada
**Superficie:** S13
**Módulo:** `erpico_debranding_pos` (19.0.1.0.0)

---

## Problema

El recibo térmico del punto de venta de Odoo 19 imprime la línea
"Powered by Odoo". En tienda física es la marca que ve el cliente.

## Objetivo

El recibo de venta POS imprime "Powered by ERPICO" en el pie.

## Alcance (criterios de aceptación)

| # | Criterio | Verificación |
|---|---|---|
| 1 | `point_of_sale.assets_prod` incluye el override | bundle check |
| 2 | Render del recibo (Cliente) contiene "Powered by ERPICO" | QA shell |
| 3 | Sin "Powered by Odoo" en el pie | ídem |

## Diseño de implementación

`static/src/override/order_receipt.xml`:

```xml
<t t-name="erpico_debranding_pos.OrderReceipt"
   t-inherit="point_of_sale.OrderReceipt"
   t-inherit-mode="extension">
    <xpath expr="//div[hasclass('order-info')]/div[last()]/span[1]"
           position="replace">
        <span>Powered by ERPICO</span>
    </xpath>
</t>
```

Se declara exclusivamente en el bundle de producción de POS
(`point_of_sale.assets_prod`) para no afectar el resto de backends.

### Reglas duras

1. El override es **t-name + t-inherit**, no un template nuevo sin
   conexión: el empaquetador del POS en 19 solo mezcla templates con
   `<t t-inherit>`.
2. La línea de poder se sustituye, no se duplica (en el render aparece una
   única marca).
3. `point_of_sale` es dependencia declarada en el manifest.

## Documentos que cierra

- `BDD` → BN-11.
- `TESTS_COVERAGE.md` → QA shell bundle.

## Pendientes post-release

- [ ] Test automatizado QUnit/POS (Selenium de POS ad-hoc del seed) cuando
  el CI lo admita.
- [ ] Verificar impresión real (DYMO/ESC-POS) en tienda piloto.