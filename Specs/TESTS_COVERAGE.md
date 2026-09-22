# TESTS_COVERAGE.md — Suite `erpico_debranding`

Matriz de trazabilidad: superficie → prueba → resultado. Dos familias:
**automatizados** (tests Odoo `--test-enable`) y **manuales/HTTP** (sesión
de QA final).

---

## 1. Suite automatizada — suite completa (3 módulos)

Ejecución:

```bash
odoo -d debrand_test -u erpico_debranding,erpico_debranding_sale,erpico_debranding_pos \
  --test-enable --test-tags=erpico_debranding
```

> **Nota de sintaxis:** `--test-tags=erpico_debranding` (tag plano, sin `/`).
> `--test-tags=/erpico_debranding` restringe al módulo exacto
> `erpico_debranding` (el `/` implica `standard` + filtro de módulo) y deja
> fuera los tests de `_sale`/`_pos`.

| Clase | Caso | Superficie | Assert clave | Resultado |
|---|---|---|---|---|
| `TestLegacyEmails` | `test_legacy_bodies_rebranded` | S10 | 4 xmlids: `ERPICO` in body; `odoo.com`/`Odoo Tour` out | ✅ |
| `TestLegacyEmails` | `test_bot_partner_renamed` | D-05 | sin partner `OdooBot` (incl. inactivos) | ✅ |
| `TestEnterpriseHidden` | `test_module_to_buy_hidden_from_search_fetch` | S3 | `search`/`search_fetch`/`search_count` filtran; escape `debranding_show_enterprise` | ✅ |
| `TestEnterpriseHidden` | `test_payment_provider_module_to_buy_hidden` | S4 | provider `module_to_buy=True` oculto en `search`/`search_fetch`; contexto escape | ✅ |
| `TestEnterpriseHidden` | `test_search_handles_legacy_domains` | S3/S4 | domains `None`/tuple no rompen; filtro sigue activo | ✅ |
| `TestSettingsView` | `test_get_views_strips_upgrade_boolean` | S5 | arch sin `upgrade_boolean`, campo conservado | ✅ |
| `TestMenus` | `test_store_menus_reparented` | S7 | 3 menús padre = `menu_ir_property` | ✅ |
| `TestBrandedRenders` | `test_brand_promotion_message` | S8 | ERPICO in, Odoo/odoo.com out | ✅ |
| `TestBrandedRenders` | `test_mail_layout_render` | S9 | `mail_notification_layout` ERPICO in, odoo.com out | ✅ |
| `TestPatchMigrationParity` | `test_replacements_parity` | S10 | paridad `_REPLACEMENTS`/xmlids/patterns patch ↔ migración | ✅ |
| `TestPatchMigrationParity` | `test_patch_idempotent` | S10 | 2ª ejecución del parche = 0 patcheos | ✅ |
| `TestDebrandingHttp` | `test_database_manager_blocked` | S11 | 403 | ✅ |
| `TestDebrandingHttp` | `test_database_selector_blocked` | S11 | 403 | ✅ |
| `TestDebrandingHttp` | `test_login_debranded` | S1/S2/S8 | 200; ERPICO footer; sin manager link; favicon isotipo | ✅ |
| `TestDebrandingHttp` | `test_database_post_endpoints_blocked` | S11/R-001 | 6 POST de BD → 403 | ✅ |
| `TestSalePortalDebranding` (sale) | `test_sale_order_portal_hides_connect_software` | S12 | portal `/my/orders` sin "Connect with your software!" ni modal | ✅ |
| `TestSalePortalDebranding` (sale) | `test_purchase_order_portal_hides_connect_software` | S12 | portal `/my/purchase` sin "Connect with your software!" ni modal | ✅ |
| `TestSalePortalOverride` (sale) | `test_sale_override_templates_registered` | S12 | los 2 overrides QWeb existen | ✅ |
| `TestPosReceiptDebranding` (pos) | `test_override_registered_in_assets` | S13 | `order_receipt.xml` en `point_of_sale.assets_prod` (`_get_asset_paths`) | ✅ |
| `TestPosReceiptDebranding` (pos) | `test_override_targets_order_receipt` | S13 | t-inherit `OrderReceipt` + footer ERPICO, sin "Powered by Odoo" | ✅ |

| `TestBotWelcomeNeutral` | `test_init_odoobot_neutral` | S-bot (2026-09-22) | bienvenida `_init_odoobot` sin "Odoo"/odoo.com; partner = ERPICO Assistant con imagen | ⏳ |
| `TestBotWelcomeNeutral` | `test_get_answer_neutralizes` | S-bot (2026-09-22) | `_get_answer('help')` → `@ERPICO Assistant`, sin `OdooBot` | ⏳ |

> Desde `58367ba` (BUG-006): la cobertura de S3/S4 incluye `.search()` plano.
> Desde `19.0.1.2.0`: cobertura R-001 (POST), paridad parche/migración,
> domains legacy, S12 y S13 automatizados.
> Desde `19.0.1.3.0`: `TestBotWelcomeNeutral` (bot neutro y respuestas)
> pendiente de correr en la validación con Docker.

## 2. QA manual / HTTP (sesión final reportada)

| Caso | Comando / método | Esperado | Resultado |
|---|---|---|---|
| Login HTML size | `curl -L /web/login` | ≈5783 bytes | ✅ |
| Logo isotipo | `GET /erpico_debranding/static/src/img/erpico-isotipo.png` | 200 | ✅ |
| 404 page | `curl -L /inexistente` | code 404 + ERPICO + no odoo.com | ✅ |
| Manager/Selector UI | `curl /web/database/manager`, `/web/database/selector` | 403 | ✅ |
| POST de BD real | `POST /web/database/create` (body cualquiera) | 403 | ✅ (2026-09-18, server 8070) |
| Contadores de apps | UI `Inicio → Ajustes` (contadores) | sin módulos Enterprise | ✅ |
| Renders email legados | shell `_render_field('body_html')` | ERPICO in, 0 "Odoo" | ✅ |
| Idempotencia parche | re-llamada `patch_legacy_emails` | 0 nuevos patcheos | ✅ |
| Renombrado bot | `res.partner` search `OdooBot` | 0 resultados | ✅ |
| Recibo POS | render `order_receipt.xml` (punto de venta) | "Powered by ERPICO" | ✅ |
| Portal sale/purchase | render QWeb `portal_content_boot` overrides | sin "Connect with your software!" | ✅ |

## 3. Resultado global

- **Automatizados:** 20/20 ✅ (`--test-tags=erpico_debranding`, 2026-09-18) + 2 nuevos pendientes de validación con Docker
- **QA manual/HTTP:** 11/11 ✅ (2026-09-17 + POST real 2026-09-18)
- **Riesgo residual:** `/web/database/list` JSON-RPC activo (compat móvil) →
  mitigable en deploy con `list_db = False` + proxy.

---

*Actualizar este documento en cada sesión de QA.*