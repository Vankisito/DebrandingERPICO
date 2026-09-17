# ERPICO Debranding — Suite para Odoo 19

Suite de debranding de marca para Odoo 19 Community Edition. Sustituye la
marca **Odoo / Odoo Enterprise** por **ERPICO** en todas las superficies
visibles (interfaz, portal, emails, POS) y oculta los módulos de pago de Odoo.

## Módulos

| Módulo | Versión | Alcance |
|---|---|---|
| `erpico_debranding` | 19.0.1.1.0 | Núcleo: login, settings, portal, emails (QWeb + mail.template legados), menú de usuario, filtro Enterprise, bloqueo de rutas de BD |
| `erpico_debranding_sale` | 19.0.1.0.0 | Portal de ventas/compra: botón "Connect with your software!" |
| `erpico_debranding_pos` | 19.0.1.0.0 | Recibo de punto de venta: footer "Powered by ERPICO" |

## Documentación

Toda la especificación vive en `Specs/` (estructura copiada del proyecto de
referencia `GpoBCA_Seguros-desarrollo`):

- `Specs/Plan de Desarrollo.md` — plan, decisiones de diseño y checklist.
- `Specs/Decisiones.md` — decisiones técnicas con su porqué (D-01 … D-07).
- `Specs/Changelog.md` — bitácora de sesiones.
- `Specs/Bugs.md` — defectos y hallazgos durante QA.
- `Specs/TESTS_COVERAGE.md` — suite automatizada y manual.
- `Specs/01-erpico-debranding/` — arquitectura, lógica, BDD, diccionario de
  recursos, manual de pruebas y specs de parches.
- `Specs/02-erpico-debranding-sale/`, `Specs/03-erpico-debranding-pos/` —
  specs de los módulos compañeros.

## Estándares

Los tres módulos siguen convenciones **OCA** (Odoo Community Association):

- Manifest con orden canónico de claves y `license: LGPL-3`.
- `readme/` con fragments `DESCRIPTION`, `USAGE`, `CONFIGURE`, `CONTRIBUTORS`,
  `CHANGELOG`.
- Headers de copyright `LGPL-3.0 or later` en todo archivo fuente.
- Suite de tests con `@tagged('erpico_debranding')` + cobertura `HttpCase`.

## Instalación

```bash
odoo -d <base> -i erpico_debranding,erpico_debranding_sale,erpico_debranding_pos
```

## Licencia

LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).