# Plan de Desarrollo — Suite `erpico_debranding`

**Proyecto:** Debranding ERPICO — Odoo 19 Community
**Plataforma:** Odoo 19.0 (build 20260619), Docker Compose
**Autor:** Habitat Digital
**Audiencia:** Desarrolladores humanos y agentes IA
**Estado:** Documento vivo — actualizar al cerrar cada sesión

> **Estructura de `Specs/`:** transversales en la raíz (`Plan de Desarrollo.md`,
> `Decisiones.md`, `Changelog.md`, `Bugs.md`, `TESTS_COVERAGE.md`).
> Módulo núcleo en `Specs/01-erpico-debranding/`; ventas/compras en
> `Specs/02-erpico-debranding-sale/`; POS en `Specs/03-erpico-debranding-pos/`.

---

## 1. Cómo usar este documento

### Para un humano desarrollador
Lee las secciones 2–4 para el alcance y las reglas. Revisa el checklist §5
antes de cerrar cualquier sesión.

### Para un agente IA
1. **Lee** `Specs/Decisiones.md` antes de tocar código: hay decisiones ya
   tomadas (D-01…D-07) que no deben revertirse.
2. **Odoo 19:** OWL 3.x, `invisible=` directo (no `attrs`), `SQL()` para SQL
   crudo, type hints en métodos nuevos.
3. **No generes código de memoria.** Aplican los patrones del skill
   `odoo-development-skill` (índice de patrones).
4. **Marca `[x]`** cuando una tarea pase su checklist.

---

## 2. Objetivo

Llevar una base de Odoo 19 **Community** a una presentación de marca
**ERPICO**: sin "Powered by Odoo", sin módulos Enterprise de pago visibles en
Apps, sin widgets de upgrade en Ajustes, sin gestión de base de datos expuesta
y con emails y portal íntegramente debranded.

**Regla de oro:** todos los cambios se aplican **por herencia** (XML, QWeb,
JS, SCSS) y **nunca se modifica el código del seed**. Todo es revertible con
`-u <módulo>`.

**Regla de oro 2:** donde el core expone textos de marca en **campos
almacenados** (ej. `mail.template.body_html`), no basta el QWeb: se aplica
parche en `post_init_hook` + migración versionada.

---

## 3. Superficies cubiertas

| # | Superficie | Mecanismo | Módulo |
|---|---|---|---|
| S1 | Página de login (`/web/login`) | QWeb `web.login_layout` + `web.layout` | núcleo |
| S2 | Error 404 / otras páginas web | `web.layout` (título, favicon, footer) | núcleo |
| S3 | Apps (buscador/contadores) | `base.search_fetch` / `search_count` filtro `to_buy` | núcleo |
| S4 | Provider de pago (módulos a comprar) | `payment.provider.search_fetch` filtro `module_to_buy` | núcleo |
| S5 | Ajustes → tarjeta About / upgrades | `res.config.settings.get_views` strip `upgrade_boolean` + OWL `res_config_edition` | núcleo |
| S6 | Menú de usuario | eliminación `support` / `odoo_account` (registry) | núcleo |
| S7 | Menús de tiendas de apps | infijo `ir.ui.menu` reparent bajo `menu_ir_property` | núcleo |
| S8 | Footer web/portal | QWeb `web.brand_promotion_message` + `portal.portal_record_sidebar` | núcleo |
| S9 | Emails QWeb (layouts + reset password) | `mail.mail_notification_layout`, `mail.mail_notification_light`, `auth_signup.reset_password_email` | núcleo |
| S10 | Emails `mail.template` legados (auth_signup) | parche `body_html` (post_init_hook + migración) | núcleo |
| S11 | Rutas de gestión de BD | `Forbidden` en `/web/database/manager` y `/web/database/selector` | núcleo |
| S12 | Portal ventas/compras | QWeb: ocultar "Connect with your software!" | sale |
| S13 | Recibo POS | QWeb `order_receipt.xml` (footer ERPICO) | pos |

---

## 4. Reglas técnicas (no negociables)

1. Jamás editar el seed. Solo herencia.
2. Todo `ref` propio con prefijo de módulo (aunque el seed use ids nativos,
   los datos se referencian por xmlid completo).
3. Un solo bloque `<data>` por archivo XML.
4. Ruby del filtro Enterprise: dominio AND `('to_buy','=',False)`, con escape
   por contexto `debranding_show_enterprise` para auditorías.
5. Emails legados: reemplazos quirúrgicos con `str()` (evita el quirk de
   `markupsafe.Markup.replace`), idempotencia garantizada.
6. Bot de Odoo: el partner `OdooBot` se renombra a `ERPICO Assistant` (dato DB
   visible en renders/chatter).
7. Odoo shell no auto-commit: toda escritura manual requiere
   `env.cr.commit()`.
8. Validación de QWeb: render real (`ir.ui.view._render`) o HTTP — nunca
   `_get_combined_arch` (no refleja overrides en templates planos).

---

## 5. Checklist de instalación y verificación final

```
INSTALACIÓN
[x] odoo -u erpico_debranding,erpico_debranding_sale,erpico_debranding_pos → 0 errores
[x] post_init_hook + migración 19.0.1.1.0 parchean los 4 mail.template legados
[x] Suite tests --test-enable --test-tags /erpico_debranding → verde

SUPERFICIES
[x] /web/login: título ERPICO, favicon isotipo, footer "Powered by ERPICO",
    sin "Manage Databases"
[x] /web/database/manager y /web/database/selector → 403
[x] Apps: módulos Enterprise ocultos (to_buy), contadores coherentes
[x] Ajustes: sin widget upgrade_boolean, tarjeta About ERPICO
[x] Menús theme_store/menu_theme_store/menu_third_party bajo menu_ir_property
[x] Footer web/portal: "Powered by ERPICO", sin odoo.com
[x] Emails QWeb render: ERPICO dentro, odoo.com fuera
[x] Emails legados render (4 xmlids): ERPICO dentro, Odoo fuera
[x] Bundle web.assets_web.min.js incluye user_menu.js + res_config_edition
[x] Bundle point_of_sale.assets_prod incluye order_receipt.xml
[x] Login HTTP: 5783 bytes, ERPICO, sin odoo.com visible
```

---

*Elaborado por Habitat Digital. Desviaciones de esta
documentación deben validarse antes de implementarse.*