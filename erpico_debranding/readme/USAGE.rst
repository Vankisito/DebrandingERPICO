Usage
=====

Instalar el módulo en una base Community 19:

.. code-block:: bash

    odoo -d <base> -i erpico_debranding

El debranding es inmediato tras la instalación:

- Página de login: título y favicon **ERPICO**, logo isotipo, footer
  "Powered by ERPICO" y sin enlace a gestión de bases de datos.
- Apps: los módulos de Odoo Enterprise (``to_buy``) dejan de listarse en el
  buscador y en los contadores.
- Ajustes: la tarjeta "About" y los widgets de upgrade desaparecen.
- Portal/web: footer "Powered by ERPICO".
- Emails: los layouts de correo y las plantillas de ``auth_signup`` muestran
  "Powered by ERPICO" (la migración ``19.0.1.1.0`` parchea los `mail.template`
  que almacenan ``body_html`` con marca Odoo).
- Las rutas ``/web/database/manager`` y ``/web/database/selector`` devuelven
  403.

Para el portal de ventas/compra y el recibo POS, instalar además los módulos
compañeros:

.. code-block:: bash

    odoo -d <base> -i erpico_debranding_sale
    odoo -d <base> -i erpico_debranding_pos

Para volver a mostrar los módulos Enterprise (auditorías), activar el
contexto ``debranding_show_enterprise=True`` en las búsquedas.