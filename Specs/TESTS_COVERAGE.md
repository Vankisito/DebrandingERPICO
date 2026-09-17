# TESTS_COVERAGE.md — Suite `erpico_debranding`

Matriz de trazabilidad: superficie → prueba → resultado. Dos familias:
**automatizados** (tests Odoo `--test-enable`) y **manuales/HTTP** (sesión
de QA final).

---

## 1. Suite automatizada — `erpico_debranding/tests/test_debranding.py`

Ejecución:

```bash
odoo -d debrand_test -u erpico_debranding \
  --test-enable --test-tags=/erpico_debranding
```

| Clase | Caso | Superficie | Assert clave | Resultado |
|---|---|---|---|---|
| `TestLegacyEmails` | `test_legacy_bodies_rebranded` | S10 | 4 xmlids: `ERPICO` in body; `odoo.com`/`Odoo Tour` out | ✅ |
| `TestLegacyEmails` | `test_bot_partner_renamed` | D-05 | sin partner `OdooBot` (incl. inactivos) | ✅ |
| `TestEnterpriseHidden` | `test_module_to_buy_hidden_from_search_fetch` | S3 | `search`/`search_fetch`/`search_count` filtran; escape `debranding_show_enterprise` | ✅ |
| `TestEnterpriseHidden` | `test_payment_provider_module_to_buy_hidden` | S4 | provider `module_to_buy=True` oculto en `search`/`search_fetch`; contexto escape | ✅ |
| `TestSettingsView` | `test_get_views_strips_upgrade_boolean` | S5 | arch sin `upgrade_boolean`, campo conservado | ✅ |
| `TestMenus` | `test_store_menus_reparented` | S7 | 3 menús padre = `menu_ir_property` | ✅ |
| `TestBrandedRenders` | `test_brand_promotion_message` | S8 | ERPICO in, Odoo/odoo.com out | ✅ |
| `TestBrandedRenders` | `test_mail_layout_render` | S9 | `mail_notification_layout` ERPICO in, odoo.com out | ✅ |
| `TestDebrandingHttp` | `test_database_manager_blocked` | S11 | 403 | ✅ |
| `TestDebrandingHttp` | `test_database_selector_blocked` | S11 | 403 | ✅ |
| `TestDebrandingHttp` | `test_login_debranded` | S1/S2/S8 | 200; ERPICO footer; sin manager link; favicon isotipo | ✅ |

> Desde `58367ba` (BUG-006): la cobertura de S3/S4 incluye `.search()` plano,
> no solo `search_fetch`/`search_count`.

## 2. QA manual / HTTP (sesión final reportada)

| Caso | Comando / método | Esperado | Resultado |
|---|---|---|---|
| Login HTML size | `curl -L /web/login` | ≈5783 bytes | ✅ |
| Logo isotipo | `GET /erpico_debranding/static/src/img/erpico-isotipo.png` | 200 | ✅ |
| 404 page | `curl -L /inexistente` | code 404 + ERPICO + no odoo.com | ✅ |
| Manager/Selector UI | `curl /web/database/manager`, `/web/database/selector` | 403 | ✅ |
| Contadores de apps | UI `Inicio → Ajustes` (contadores) | sin módulos Enterprise | ✅ |
| Renders email legados | shell `_render_field('body_html')` | ERPICO in, 0 "Odoo" | ✅ |
| Idempotencia parche | re-llamada `patch_legacy_emails` | 0 nuevos patcheos | ✅ |
| Renombrado bot | `res.partner` search `OdooBot` | 0 resultados | ✅ |
| Recibo POS | render `order_receipt.xml` (punto de venta) | "Powered by ERPICO" | ✅ |
| Portal sale/purchase | render QWeb `portal_content_boot` overrides | sin "Connect with your software!" | ✅ |

## 3. Resultado global

- **Automatizados:** 11/11 ✅ (`--test-tags=/erpico_debranding`, 2026-09-17)
- **QA manual/HTTP:** 10/10 ✅ (misma fecha)
- **Riesgo abierto:** R-001 (POST de BD) → ver `Bugs.md`.

---

*Actualizar este documento en cada sesión de QA.*