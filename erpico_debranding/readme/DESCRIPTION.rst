Erpico Debranding
=================

Módulo genérico de debranding Odoo para bases de datos nuevas de cualquier
cliente. Elimina la marca Odoo / Odoo Enterprise de la interfaz, del portal,
del POS y de los emails salientes de Odoo 19 (Community Edition).

La marca del producto es **ERPICO**: la línea "Powered by Odoo" se sustituye
por "Powered by ERPICO" en todas las superficies.

Alcance:

- Página de login: título, favicon, footer y enlaces de marca.
- Footer web y portal.
- Menú Apps: oculta módulos de Odoo Enterprise (``to_buy``) y las tiendas de
  apps.
- Tarjeta "About" de Ajustes y widgets de upgrade.
- Menú de usuario: elimina enlaces Documentation, Support y Odoo.com Account.
- Emails salientes (layouts de correo y plantillas de ``auth_signup``).
- Botón "Connect with your software!" del portal (módulo compañero
  ``erpico_debranding_sale``).
- Recibo de venta POS (módulo compañero ``erpico_debranding_pos``).
- Bloqueo de ``/web/database/manager``.

Depende de módulos core (web, base_setup, portal, mail, auth_signup,
payment) y no modifica el código del seed: todos los cambios se aplican por
herencia y son revertibles con ``-u``.