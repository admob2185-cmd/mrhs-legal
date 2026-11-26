# -*- coding: utf-8 -*-
import os, html
from content import PRIVACY, TERMS
import content_dice
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEV, EMAIL = 'MR and HS Devs', 'prvyucetjedna@gmail.com'
DATES = dict(date_en='26 November 2026', date_sk='26. novembra 2026', date_cs='26. listopadu 2026')
APPS = {
  'zdravosken': dict(app='ZdravoSken', pkg='sk.zdravosken.app', langs=['sk', 'cs', 'en'], color='#1E9E4A', color2='#0E7A3C'),
  'nutrova': dict(app='Nutrova', pkg='app.nutrova.scanner', langs=['en', 'sk'], color='#5B3FD6', color2='#25165F'),
  'dice-of-fate': dict(app='Dice of Fate', pkg='com.mrandhsdevs.diceoffate', langs=['en', 'sk'], terms_langs=['en'], color='#8A3FD6', color2='#2A1150',
                       privacy=content_dice.PRIVACY, terms=content_dice.TERMS),
}
LANG_NAMES = {'en': 'English', 'sk': 'Slovenčina', 'cs': 'Čeština'}
CSS = """
:root{--c:%(color)s;--c2:%(color2)s;--t:#1b2420;--m:#5c6862;--b:#e3e8e5;--bg:#f6f8f7}
*{box-sizing:border-box}body{margin:0;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--t);background:var(--bg)}
header{background:linear-gradient(135deg,var(--c),var(--c2));color:#fff;padding:28px 20px}
header .w,main{max-width:820px;margin:0 auto}header h1{margin:0;font-size:28px}header p{margin:4px 0 0;opacity:.9}
nav.lang{margin-top:14px;display:flex;gap:8px;flex-wrap:wrap}nav.lang a{color:#fff;border:1px solid rgba(255,255,255,.6);border-radius:999px;padding:4px 12px;text-decoration:none;font-size:14px}
main{padding:20px}section.doc{background:#fff;border:1px solid var(--b);border-radius:16px;padding:8px 24px 20px;margin:0 0 24px}
section.doc>h2{color:var(--c);margin:18px 0 0}.upd{color:var(--m);font-size:14px;margin:2px 0 8px}
h3{font-size:17px;margin:20px 0 4px}p{margin:6px 0}a{color:var(--c)}code{background:#eef2f0;padding:1px 5px;border-radius:5px;font-size:14px}
footer{color:var(--m);font-size:14px;text-align:center;padding:10px 20px 40px}
@media (prefers-color-scheme:dark){:root{--t:#e6ece9;--m:#a3b0aa;--b:#26302b;--bg:#0e1311}section.doc{background:#171e1a}code{background:#212a25}a,section.doc>h2{color:#7fd6a0}}
"""
def page(app_key, kind):
    a = APPS[app_key]; data = a.get(kind, PRIVACY if kind == 'privacy' else TERMS)
    if kind == 'terms' and a.get('terms_langs'): a = dict(a, langs=a['terms_langs'])
    fill = dict(app=a['app'], pkg=a['pkg'], dev=DEV, email=EMAIL, **DATES)
    f = lambda s: s.format(**fill)
    title0 = f(data[a['langs'][0]]['title'])
    other = 'terms' if kind == 'privacy' else 'privacy'
    nav = ''.join(f'<a href="#{l}">{LANG_NAMES[l]}</a>' for l in a['langs'])
    docs = []
    for l in a['langs']:
        d = data[l]
        secs = ''.join(f'<h3>{i+1}. {f(h)}</h3>' + ''.join(f'<p>{f(p)}</p>' for p in ps) for i, (h, ps) in enumerate(d['sections']))
        docs.append(f'<section class="doc" id="{l}" lang="{l}"><h2>{f(d["title"])} – {a["app"]}</h2><p class="upd">{f(d["updated"])}</p>{secs}</section>')
    other_label = {'privacy': 'Terms of Use / Podmienky používania', 'terms': 'Privacy Policy / Ochrana súkromia'}[kind]
    return f"""<!doctype html><html lang="{a['langs'][0]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title0)} – {a['app']}</title><meta name="description" content="{html.escape(title0)} – {a['app']} ({DEV})">
<style>{CSS % a}</style></head><body><header><div class="w"><h1>{a['app']}</h1><p>{html.escape(title0)} · {DEV}</p><nav class="lang">{nav}</nav></div></header>
<main>{''.join(docs)}</main><footer>{a['app']} · {DEV} · <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{other}.html">{other_label}</a> · <a href="../index.html">Index</a></footer></body></html>
"""
os.makedirs(OUT, exist_ok=True)
for k in APPS:
    os.makedirs(f'{OUT}/{k}', exist_ok=True)
    for kind in ('privacy', 'terms'):
        open(f'{OUT}/{k}/{kind}.html', 'w', encoding='utf-8').write(page(k, kind))
    open(f'{OUT}/{k}/index.html', 'w', encoding='utf-8').write(f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=privacy.html"><a href="privacy.html">Privacy Policy</a>')
items = ''.join(f'<li><b>{a["app"]}</b> (<code>{a["pkg"]}</code>): <a href="{k}/privacy.html">Privacy Policy</a> · <a href="{k}/terms.html">Terms of Use</a></li>' for k, a in APPS.items())
open(f'{OUT}/index.html', 'w', encoding='utf-8').write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{DEV} – legal</title>
<style>{CSS % APPS['zdravosken']}</style></head><body><header><div class="w"><h1>{DEV}</h1><p>Privacy policies and terms of our apps</p></div></header>
<main><section class="doc"><ul>{items}</ul><p>Contact: <a href="mailto:{EMAIL}">{EMAIL}</a></p></section></main></body></html>
""")
open(f'{OUT}/.nojekyll', 'w').write('')
open(f'{OUT}/README.md', 'w').write(f'# {DEV} – legal pages\n\nPrivacy policies and terms of use for ZdravoSken, Nutrova and Dice of Fate, published with GitHub Pages.\n\n- ZdravoSken: zdravosken/privacy.html, zdravosken/terms.html\n- Nutrova: nutrova/privacy.html, nutrova/terms.html\n- Dice of Fate: dice-of-fate/privacy.html, dice-of-fate/terms.html\n\nContact: {EMAIL}\n')
print('ok')
