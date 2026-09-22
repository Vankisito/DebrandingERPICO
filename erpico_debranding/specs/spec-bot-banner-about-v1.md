# Spec v1 — Bot de chat neutro, banner Install y tarjeta About

**Fecha:** 2026-09-22
**Versión del módulo:** `erpico_debranding` 19.0.1.3.0
**Estado:** Implementado — validación con Docker pendiente
**Superficies nuevas:** S14 (bot neutro), S15 (banner/ítem Install), S16 (About garantizado)

---

## 1. Objetivo

Eliminar la última marca Odoo visible en la UI backend:

1. **Bot de chat** croa interna se presentaba como "Odoo's chat..." y el
   onboarding citaba `@OdooBot`, "Enjoy exploring Odoo!" y links a
   `odoo.com`.
2. **Banner de instalación PWA** ("Install Odoo — Come here often? Install
   the app for quick and easy access!") aparecía en el tab Notificaciones
   del menú de mensajes (campana), con un ítem duplicado "Install App" en
   el menú de usuario.
3. **Tarjeta About** de Ajustes seguía mostrando "Odoo
   `<server_version>` (Community Edition)… Copyright Odoo S.A." a pesar de
   tener un override QWeb previo.

Regla aplicada: **herencia pura**, sin tocar el seed. Textos de marca del
bot (la conversación) se mantienen íntegros salvo las cadenas que citan la
marca (D-12).

---

## 2. Causa raíz (hojografía del seed, Odoo 19.0)

### S15 — Banner "Install Odoo"

- Definición: `mail/static/src/core/web/messaging_menu_patch.js`.
  - Getter `MessagingMenu.prototype.installationRequest` → `displayName:
    _t("Install Odoo")`, `body: _t("Come here often? Install the app for
    quick and easy access!")`, `isShown` true cuando
    `activeTab === "notification" && this.canPromptToInstall`.
  - Getter `counter` suma `+1` cuando `canPromptToInstall`.
  - Getter `hasPreviews` lo incluye.
  - `canPromptToInstall` delega en el servicio `pwa`:
    ideal para neutralizarlo en un solo punto.
- ítem del menú de usuario: `web/static/src/webclient/user_menu/
  user_menu_items.js` → clave `install_pwa`, callback `pwa.show()`,
  es la promoción PWA; compartido con el banner.

### S14 — Textos de marca del bot

- `mail_bot/models/res_users.py::_init_odoobot` → mensaje de bienvenida
  "Odoo's chat helps employees collaborate efficiently. I'm here to help
  you discover its features."
- `mail_bot/models/mail_bot.py::_get_style_dict` → links
  `https://www.odoo.com/documentation` y `https://www.odoo.com/slides`.
- `mail_bot/models/mail_bot.py::_get_answer` → cadenas `@OdooBot` (varias)
  y "Enjoy exploring Odoo!" en el estado `onboarding_canned`.
- `mail/static/src/core/common/out_of_focus_service.js` → icono fallback de
  la notificación del sistema: `/mail/static/src/img/odoobot_transparent.png`.
- Diseño: `mail/static/src/img/odoobot.png` → avatar real del bot.
- Datos: `mail/data/res_partner_data.xml` → `base.partner_root` con
  `name='OdooBot'` y el `image_1920` de `odoobot.png`.

### S16 — Tarjeta About

- Componente: `web/static/src/webclient/settings_form_view/widgets/
  res_config_edition.{js,xml}`.
  - Template `res_config_edition` renderiza `Odoo <serverVersion>
    (Community Edition)` + `Copyright © 2004-... Odoo S.A.` + LGPL.
  - El widget se registra en `registry.category("view_widgets")` con la
    clave `res_config_edition`.
- El override QWeb previo del módulo definía un `<div t-name=
  "res_config_edition">` en un asset; la sobrescritura por mismo nombre
  puede perder ante el orden de los assets del bundle → no garantizado.
- Fix robusto: registrar un componente **propio** bajo la misma clave del
  registry (el add del registry gana al que lo registró primero, por orden
  de carga del bundle) con un template **con nombre único**
  (`erpico_res_config_edition`) → sin colisión de t-name.

---

## 3. Solución implementada

### 3.1 `models/res_users.py` — bienvenida neutra (S14)

`_inherit='res.users'`, override de `_init_odoobot` con el mismo flujo que
el core pero con texto `"ERPICO's chat helps employees collaborate
efficiently. I'm here to help you discover its features."`. Conserva id del
partner, canal, `message_post`, subtipo y `odoobot_state`:
se mantiene el onboarding (D-12).

### 3.2 `models/mail_bot.py` — respuestas neutras (S14)

- `_get_style_dict()`: mismo dict que el core pero
  `document_link_start/end` y `slides_link_start/end` = `Markup('')`
  (quita los links a odoo.com sin romper el formateo).
- `_get_answer()`: tras el `super()`, sobre las respuestas (string o lista)
  reemplaza:
  - `@OdooBot` → `@ERPICO Assistant`
  - `Enjoy exploring Odoo!` → `Enjoy exploring ERPICO!`
  Aplica `Markup` vía `str()` (quirk de `Markup.replace`, cf. BUG-002).

### 3.3 `models/__init__.py` — imports

Añade `mail_bot` y `res_users`.

### 3.4 `__init__.py` — post_init_hook ampliado (S14 datos)

`post_init_hook(env)` ejecuta `patch_legacy_emails(env)` (ya existía) y
`_rebrand_bot_partner(env)`: renombra `base.partner_root` a
"ERPICO Assistant" (si todavía es "OdooBot") y pisa `image_1920` con
`bot_placeholder.png` (leído con `tools.file_open`, base64).

### 3.5 `migrations/19.0.1.3.0/post-migrate.py` (S14 datos, upgrades)

Mismo cambio `_rebrand_bot_partner` para bases que actualizan el módulo
(las migraciones no pueden importar el paquete, cf. BUG-001: autocontenido).

### 3.6 `static/src/img/bot_placeholder.png` (S14)

Placeholder **genérico**: cuadrado 512×512, fondo `#714B67`, letra "E"
blanca (fuente Segoe UI 130). Evita el odoobot de Odoo y no usurpa el
isotipo de ERPICO (D-11).

### 3.7 `static/src/js/messaging_menu.js` (S15)

```js
patch(MessagingMenu.prototype, {
    get canPromptToInstall() {
        return false;
    },
});
```

Punto único: apaga el banner (`installationRequest.isShown`), el `+1` del
`counter` y `hasPreviews`. **No** toca `notificationRequest` (push, D-10).

### 3.8 `static/src/js/user_menu.js` (S15)

Añadido `registry.category("user_menuitems").remove("install_pwa")` a los
removes ya existentes (`support`, `odoo_account`).

### 3.9 `static/src/js/out_of_focus.js` (S14)

`patch(OutOfFocusService.prototype, { async notify(...) })`: réplica del
nitifiable del core con el icono fallback apuntando a
`/erpico_debranding/static/src/img/bot_placeholder.png` en lugar del
`odoobot_transparent.png`. Signature idéntica (mensajes, push, sonido
solo en channels).

### 3.10 `static/src/settings_form_view/res_config_edition.js` + `.xml` (S16)

- `res_config_edition.js`: componente `ErpicoResConfigEdition` con
  `static template = "erpico_res_config_edition"` y
  `static components = { Setting }`; registrado bajo
  `registry.category("view_widgets").add("res_config_edition", {...})`.
- `res_config_edition.xml`: template `erpico_res_config_edition` con el
  card About: `ERPICO` + `Powered by <b>ERPICO</b>` (sin versión, sin
  copyright, sin LGPL de Odoo).

### 3.11 `__manifest__.py`

- `version`: `19.0.1.3.0`
- `depends`: + `mail_bot`
- assets `web.assets_backend`: + `messaging_menu.js`, `out_of_focus.js`,
  `res_config_edition.js` + `.xml`.

### 3.12 `tests/test_debranding.py`

Nueva clase `TestBotWelcomeNeutral`:
- `test_init_odoobot_neutral`: `user._init_odoobot()` → ningún `msg.body`
  contiene "Odoo" ni "odoo.com"; `base.partner_root` = "ERPICO Assistant"
  con `image_1920`.
- `test_get_answer_neutralizes`: `_get_answer(channel, 'help', ..., command
  ='help')` → contiene `@ERPICO Assistant`, sin `OdooBot`.

---

## 4. Archivos afectados

| Archivo | Modo | Cambio |
|---|---|---|
| `__manifest__.py` | A | versión 19.0.1.3.0, dep `mail_bot`, 4 assets nuevos |
| `__init__.py` | A | post_init_hook + `_rebrand_bot_partner` |
| `models/__init__.py` | A | imports mail_bot/res_users |
| `models/res_users.py` | N | `_init_odoobot` neutro |
| `models/mail_bot.py` | N | `_get_style_dict`, `_get_answer` neutro |
| `static/src/img/bot_placeholder.png` | N | avatar genérico |
| `static/src/js/messaging_menu.js` | N | `canPromptToInstall=false` |
| `static/src/js/out_of_focus.js` | N | icono notificación |
| `static/src/js/user_menu.js` | A | remove `install_pwa` |
| `static/src/settings_form_view/res_config_edition.js` | N | widget propio |
| `static/src/settings_form_view/res_config_edition.xml` | A | template único |
| `migrations/19.0.1.3.0/post-migrate.py` | N | bot rebrand upgrade |
| `tests/test_debranding.py` | A | `TestBotWelcomeNeutral` |

---

## 5. Criterios de aceptación (validación pendiente)

Con `-u erpico_debranding --dev=all -d debrand_test` y hard-refresh
(Ctrl+Shift+R):

1. **S14:** crear/abrir chat con "ERPICO Assistant": bienvenida sin "Odoo";
   avatar placeholder; notificaciones del sistema con el placeholder.
2. **S15:** campana → tab Notificaciones: **sin** la card "Install Odoo";
   badge sin `+1` espurio; menú de usuario **sin** "Install App" ni
   "Support"/"Odoo Account"; **con** push "Turn on notifications" (D-10).
3. **S16:** Ajustes → About: "ERPICO / Powered by ERPICO", sin versión
   Community ni Copyright Odoo.
4. Suite: `--test-tags=erpico_debranding` → 22/22.

---

## 6. No resuelto / fuera de alcance

- El banner PWA del **navegador** (prompt nativo) solo aparece si se llama
  `pwa.show()`; ya no queda ningún trigger en la UI, y el ítem se eliminó.
- El push **se mantiene** (D-10): solo debranda la marca, no la funcionalidad.
- El texto de la conversación del bot se conserva (D-12): solo se
  reemplazan las cadenas que citan la marca.