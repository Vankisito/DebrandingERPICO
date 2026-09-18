# Manual de Pruebas y Testing — `erpico_debranding`

Procedimientos reproducibles para validar el debranding sin ambigüedad.
Cada prueba referencia la superficie S# y el criterio de aceptación.

**Entorno de referencia:** `odoo_debrand_test` (Docker), base `debrand_test`,
`/mnt/extra-addons` montando `Custom_addons`.

---

## 1. Rápido: suite automatizada

```bash
docker exec -i odoo_debrand_test odoo -d debrand_test \
  -u erpico_debranding,erpico_debranding_sale,erpico_debranding_pos \
  --test-enable --test-tags=erpico_debranding \
  --http-port=8090 --no-http --stop-after-init
```

- **Expectativa:** 20/20 PASS.
- **Ojo sintaxis de tags:** usar el tag plano (`erpico_debranding`), NO
  `/erpico_debranding`: la barra añade filtro de módulo y excluye los tests
  de `_sale`/`_pos`.
- **Ojo puerto:** si el server principal del container ya corre en 8069,
  pasar SIEMPRE `--http-port=8090 --no-http` (con `--no-http` solo, el bind a
  8069 del proceso conviviente aborta el run).
- Rodríguez de errores: revisar `tests/` de los 3 módulos + `log`; nunca
  asumas que un cambio cosmético no rompe un assert.

## 2. HTTP (QA manual)

### 2.1 Login

```bash
curl -L -s -o login.html -w "%{http_code} %{size_download}\n" \
  http://localhost:8069/web/login
grep -c "Powered by <b>ERPICO</b>" login.html   # >= 1
grep -c "odoo.com" login.html                     # 0
grep -c "web/database/manager" login.html         # 0
```

**Aceptación:** 200, ≈5783 bytes, footer ERPICO, sin links de DB.

### 2.2 404

```bash
curl -L -s -o nf.html -w "%{http_code}\n" http://localhost:8069/no-existe
grep -c "ERPICO" nf.html  # >= 1
grep -c "odoo.com" nf.html # 0
```

### 2.3 Rutas de BD

```bash
for r in /web/database/manager /web/database/selector; do
  curl -s -o /dev/null -w "$r %{http_code}\n" "http://localhost:8069$r"
done
# POST (R-001, desde 19.0.1.2.0)
for r in create duplicate drop backup restore change_password; do
  curl -s -o /dev/null -w "POST /web/database/$r %{http_code}\n" \
    -X POST -d "master_pwd=x" "http://localhost:8069/web/database/$r"
done
```

**Aceptación:** todos 403 (GET y POST).
**Fuera de alcance:** JSON-RPC `/web/database/list` (compat móvil).

### 2.4 Assets

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  "http://localhost:8069/erpico_debranding/static/src/img/erpico-isotipo.png"
```

**Aceptación:** 200.

## 3. Shell de Odoo (renders)

```bash
docker exec -i odoo_debrand_test odoo shell -d debrand_test \
  --db_host=db --db_user=odoo --db_password=odoo --no-http <<'EOF'
# Renders de emails legados
from odoo.addons.erpico_debranding.patches.legacy_emails import (
    LEGACY_EMAIL_XMLIDS)
for x in LEGACY_EMAIL_XMLIDS:
    tpl = env.ref(x)
    html = str(tpl._render_field('body_html', {}) or '')
    checks = ('ERPICO' in html, 'odoo.com' in html, 'Odoo Tour' in html)
    print(x, checks)
# Idempotencia
from odoo.addons.erpico_debranding.patches.legacy_emails import (
    patch_legacy_emails)
print('patched:', patch_legacy_emails(env))
# Bot
bots = env['res.partner'].search(
    [('name', '=', 'OdooBot'), ('active', 'in', (True, False))])
print('OdooBot count:', len(bots))
EOF
```

**Aceptación:** todos `(True, False, False)`, `patched: []`, count 0.
**Ojo BUG-003:** si EScribes algo, `env.cr.commit()`.

## 4. Renders QWeb dinámicos

```bash
# brand promotion
env['ir.ui.view']._render('web.brand_promotion_message')
# mail layout
env['ir.ui.view']._render('mail.mail_notification_layout')
# recibo POS
env['ir.ui.view']._render(
    'point_of_sale.OrderReceipt', values={'order': order})
```

**Aceptación:** ERPICO in / odoo.com out.

## 5. Checklist humano de aceptación en UI

1. Login: no ver "Odoo" en ninguna parte (título, fuente, footer, tab).
2. Apps: la App "Odoo" corporate NO aparece; "Settings" sí.
3. Ajustes → tarjeta About dice ERPICO; ningún campo "Upgrade".
4. Menú de usuario: sin "Support" ni "Odoo Account".
5. Página pública de una cotización (portal): sin botón "Connect with your
   software!".
6. Recibo POS: footer "Powered by ERPICO".
7. `/web/database/manager` por URL directa → 403.

---

*Repetir la suite completa antes de cada release. Resultados →
`TESTS_COVERAGE.md`.*