# Spec v1 — Ocultar módulos Enterprise y widgets de upgrade

**Fecha:** 2026-09-17
**Estado:** Implementada y verificada
**Superficie:** S3, S4, S5
**Módulos:** `erpico_debranding`

---

## Problema

En Community, los módulos de Odoo Enterprise (`ir.module.module.to_buy=True`)
y los proveedores/payment de pago (`payment.provider.module_to_buy=True`)
aparecen igualmente en el UI (buscador de Apps, contadores, settings).
Además, los views de `res.config.settings` exponen widgets `upgrade_boolean`
que apuntan a la tienda de Odoo ("Upgrade").

## Objetivos

Sin tocar el seed y sin perder funcionalidad:

1. El buscador de apps y los contadores **no muestran** módulos Enterprise.
2. Los `payment.provider` con `module_to_buy=True` no aparecen.
3. Los settings **no renderizan** `widget="upgrade_boolean"`.
4. Escape para auditorías: contexto `debranding_show_enterprise=True`
   restaura la vista completa.

## Alcance (criterios de aceptación)

| # | Criterio | Verificación |
|---|---|---|
| 1 | `search_fetch` de `ir.module.module` omite registros `to_buy` | `TestEnterpriseHidden::test_module_to_buy_hidden_*` |
| 2 | `search_count` coherente (mismo filtro) | ídem |
| 3 | Contexto escape muestra todo | ídem |
| 4 | Provider `module_to_buy` omitido idem | `TestEnterpriseHidden::test_payment_provider_*` |
| 5 | `get_views` arch sin `upgrade_boolean` | `TestSettingsView::test_get_views_strips_upgrade_boolean` |
| 6 | Vista de Ajustes no muestra campos "Upgrade" | QA humano UI |

## Diseño de implementación

### Filtro ORM (`models/base.py`)

```python
class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def search_fetch(self, domain, field_names=None, **kwargs):
        if self._name == 'ir.module.module' \
                and not self.env.context.get('debranding_show_enterprise'):
            domain = [*domain, ('to_buy', '=', False)]
        elif self._name == 'payment.provider' \
                and not self.env.context.get('debranding_show_enterprise'):
            domain = [*domain, ('module_to_buy', '=', False)]
        return super().search_fetch(
            domain, field_names=field_names, **kwargs)

    @api.model
    def search_count(self, domain, **kwargs):
        # mismo patrón
        ...
```

### Strip lxml (`models/res_config_settings.py`)

```python
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def get_views(self, views, options=None):
        res = super().get_views(views, options=options)
        for view_id_str, info in res['views'].items():
            arch = etree.fromstring(info['arch'].encode('utf-8'))
            for node in arch.xpath("//field[@widget='upgrade_boolean']"):
                node.attrib.pop('widget', None)
            info['arch'] = etree.tostring(arch, encoding='unicode')
        return res
```

### Reglas duras

1. Nunca `DomainAnd` ni `odoo.osv.expression` (API 19).
2. El filtro ve el modelo por `self._name` — `ir.module.module` es de
   `base`, `payment.provider` de `payment` (por eso la herencia dual en
   `base.py`).
3. El strip solo elimina el atributo `widget`; ningún campo desaparece.
4. `debranding_show_enterprise` es el único "interruptor" del módulo
   (decisión D-01/D-08).

## Documentos que cierra

- `Decisiones.md` → D-01, D-07.
- `TESTS_COVERAGE.md` → TestEnterpriseHidden, TestSettingsView.

## Pendientes post-release

- [ ] Revisar si el panel "Apps" del portal requiere el mismo filtro en
  navegador público (`/apps`).
- [ ] Evaluar si los "odoo-apps" del menú de usuario vuelven por otra vía
  en 19.0.x hotfix.