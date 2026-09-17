Changelog
=========

19.0.1.1.0 (2026-09-17)
-----------------------
* Parchea los ``mail.template`` legados de ``auth_signup`` que almacenan
  ``body_html`` con marca Odoo (Powered by, Odoo Tour, bloque de marketing,
  placeholder ``OdooBot``).
* Renombra el partner del bot interno ``OdooBot`` a ``ERPICO Assistant``.
* Convierte el parcheo en `post_init_hook` + migración ``19.0.1.1.0``
  (reproducible en instalaciones y upgrades).

19.0.1.0.0 (2026-09-17)
-----------------------
* Versión inicial de la suite ERPICO sobre Odoo 19 Community:
  login, settings, portal, emails QWeb, menú de usuario, bloqueo de
  rutas de base de datos y filtro de módulos Enterprise.