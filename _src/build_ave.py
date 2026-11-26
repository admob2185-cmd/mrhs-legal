# -*- coding: utf-8 -*-
# Generates ave/privacy.html, ave/delete-account.html, ave/terms.html (EN + SK)
import os, html
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ave')
DEV, EMAIL, APP, PKG = 'MR and HS Devs', 'prvyucetjedna@gmail.com', 'Ave', 'sk.ave.app'
CSS = """
:root{--c:#1F2F56;--c2:#121A2E;--a:#B8901F;--t:#1E2230;--m:#4A4F5E;--b:#E6DCC8;--bg:#F8F3E9}
*{box-sizing:border-box}body{margin:0;font:17px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--t);background:var(--bg)}
header{background:linear-gradient(135deg,var(--c),var(--c2));color:#fff;padding:28px 20px;border-bottom:3px solid #C9A227}
header .w,main{max-width:820px;margin:0 auto}header h1{margin:0;font:600 30px/1.2 Georgia,"Times New Roman",serif}header p{margin:4px 0 0;opacity:.9}
nav.lang{margin-top:14px;display:flex;gap:8px;flex-wrap:wrap}nav.lang a{color:#fff;border:1px solid rgba(255,255,255,.6);border-radius:999px;padding:4px 12px;text-decoration:none;font-size:14px}
main{padding:20px}section.doc{background:#FFFCF6;border:1px solid var(--b);border-radius:16px;padding:8px 24px 20px;margin:0 0 24px}
section.doc>h2{color:var(--c);margin:18px 0 0;font-family:Georgia,"Times New Roman",serif}.upd{color:var(--m);font-size:14px;margin:2px 0 8px}
h3{font-size:18px;margin:22px 0 4px}p,li{margin:6px 0}a{color:var(--a)}code{background:#EFE6D4;padding:1px 5px;border-radius:5px;font-size:14px}
footer{color:var(--m);font-size:14px;text-align:center;padding:10px 20px 40px}
@media (prefers-color-scheme:dark){:root{--t:#F2EDE3;--m:#C9C4BA;--b:#253052;--bg:#121A2E}section.doc{background:#1B2440}code{background:#253052}a{color:#E3C46A}section.doc>h2{color:#E3C46A}}
"""
def page(title, subtitle, sections, langs=('en','sk')):
    nav = ''.join(f'<a href="#{l}">{ {"en":"English","sk":"Slovenčina"}[l] }</a>' for l in langs)
    body = ''.join(sections[l] for l in langs)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} – {APP}</title><meta name="description" content="{html.escape(title)} – {APP} ({DEV})">
<style>{CSS}</style></head><body><header><div class="w"><h1>{APP}</h1><p>{html.escape(subtitle)} · {DEV}</p><nav class="lang">{nav}</nav></div></header>
<main>{body}</main><footer>{APP} (<code>{PKG}</code>) · {DEV} · <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="privacy.html">Privacy / Súkromie</a> · <a href="delete-account.html">Delete account / Vymazanie účtu</a> · <a href="terms.html">Terms / Podmienky</a></footer></body></html>
"""
def doc(lang, title, updated, secs, anchor_prefix=''):
    out = f'<section class="doc" id="{lang}" lang="{lang}"><h2>{title}</h2><p class="upd">{updated}</p>'
    for i, (aid, h, ps) in enumerate(secs):
        idattr = f' id="{aid}"' if aid else ''
        out += f'<h3{idattr}>{i+1}. {h}</h3>' + ''.join(p if p.startswith('<ul') else f'<p>{p}</p>' for p in ps)
    return out + '</section>'
UL = lambda items: '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'

PRIV_EN = [
 (None, 'Who we are', [f'{APP} (Android package <code>{PKG}</code>) is a Catholic prayer app developed and published by <b>{DEV}</b>, the controller under the EU General Data Protection Regulation (GDPR). Contact for all privacy questions: <a href="mailto:{EMAIL}">{EMAIL}</a>.']),
 (None, 'Summary', ['Most of the app works <b>without an account</b>. Your prayer history, streak, settings and challenge progress are stored only on your device. We do not show ads, we do not sell data and we never send the text of your prayer intentions to analytics or notifications.']),
 (None, 'Data stored only on your device', ['Prayer records (date, length), streak, settings (language, font size, reminders), challenge progress, downloaded audio and the date you first opened the app (used for the 7 free days of Premium). This data stays in the app\'s private storage and is deleted when you uninstall the app or use <i>Profile → Delete account and data</i>.']),
 (None, 'Data processed when you create an account (optional)', [UL([
   '<b>E-mail address and account ID</b> – sign-in (e-mail magic link or Google Sign-In) and prayer groups. Legal basis: contract (Art. 6(1)(b) GDPR).',
   '<b>Prayer groups</b> – group membership, prayer intentions you post, "I am praying for you" taps and reports of posts. Because this may reveal religious beliefs (special category data, Art. 9 GDPR), we ask for your <b>explicit consent</b> (Art. 9(2)(a)) when you create an account and when you join a group. Groups are private and visible only to their members.',
   '<b>Push notification token</b> – to notify you when someone prays for your intention. Legal basis: consent.'])]),
 (None, 'Analytics (optional, off by default)', ['If you turn on anonymous usage statistics, we record events such as "prayer completed" or "rosary completed" with a random identifier (PostHog, EU server). Analytics never contains your name, e-mail or the text of intentions. Legal basis: consent (Art. 6(1)(a)); you can switch it off at any time in the app.']),
 (None, 'Subscriptions', ['Payments are handled by <b>Google Play</b>; we never see your card details. We receive only the technical purchase ID and subscription status via <b>RevenueCat</b> to unlock Premium. Legal basis: contract.']),
 (None, 'Processors and where data is stored', [UL([
   '<b>Supabase</b> – database and sign-in, data centre in the EU (Frankfurt, Germany)',
   '<b>PostHog</b> – optional anonymous analytics, EU server',
   '<b>RevenueCat</b> and <b>Google Play</b> – subscription status',
   '<b>Firebase Cloud Messaging</b> (Google) – delivery of push notifications',
   '<b>Google Sign-In</b> – only if you choose it']),
   'Where a processor transfers data outside the EU, it relies on the EU Standard Contractual Clauses or the EU‑US Data Privacy Framework. We do not sell or share your data for advertising.']),
 (None, 'Retention', [UL(['Data on your device – until you uninstall the app or delete it in the app.', 'Account and server data – until you delete your account; deletion is immediate and irreversible.', 'Analytics events – at most 12 months.', 'Intentions are deleted together with the group or your account, or earlier by their author or the group admin.'])]),
 ('delete', 'Deleting your account and data', [f'In the app: <b>Profile → Privacy and data → Delete account and data</b> (without an account: <b>Delete all data</b>). This immediately deletes your account, group memberships, intentions, prayer taps and push tokens from our servers and clears the data on your device. Without an account, uninstalling the app deletes all data. You can also request deletion by e-mail to <a href="mailto:{EMAIL}">{EMAIL}</a> from the address of your account – see <a href="delete-account.html">delete-account.html</a>.']),
 (None, 'Your rights', ['You have the right of access, rectification, erasure, restriction, data portability, objection and to withdraw consent at any time. In the app you can export your data (JSON file), delete your account and switch analytics off. You may lodge a complaint with a supervisory authority, e.g. the Office for Personal Data Protection of the Slovak Republic (www.dataprotection.gov.sk).']),
 (None, 'Children', ['The app is intended for adults. Accounts and prayer groups are not intended for children under 16.']),
 (None, 'Security', ['All data is transmitted over encrypted connections (HTTPS/TLS). Server tables are protected by row-level security so that only members of a group can read its content.']),
 (None, 'Changes', ['We will inform you about material changes in the app and update the effective date above.']),
]
PRIV_SK = [
 (None, 'Kto sme', [f'{APP} (balík pre Android <code>{PKG}</code>) je katolícka modlitebná aplikácia, ktorú vyvíja a vydáva <b>{DEV}</b> – prevádzkovateľ podľa nariadenia EÚ o ochrane osobných údajov (GDPR). Kontakt pre všetky otázky súkromia: <a href="mailto:{EMAIL}">{EMAIL}</a>.']),
 (None, 'Zhrnutie', ['Väčšina aplikácie funguje <b>bez účtu</b>. História modlitieb, séria dní, nastavenia a priebeh výziev sú uložené iba v tvojom telefóne. Nezobrazujeme reklamy, údaje nepredávame a text tvojich úmyslov nikdy neposielame do analytiky ani do notifikácií.']),
 (None, 'Údaje uložené iba v telefóne', ['Záznamy o modlitbe (dátum, dĺžka), séria, nastavenia (jazyk, veľkosť písma, pripomienky), priebeh výziev, stiahnuté audio a dátum prvého otvorenia aplikácie (pre 7 dní Premium zadarmo). Tieto údaje zostávajú v súkromnom úložisku aplikácie a vymažú sa odinštalovaním aplikácie alebo cez <i>Profil → Súkromie a údaje → Vymazať všetky údaje</i>.']),
 (None, 'Údaje pri vytvorení účtu (dobrovoľné)', [UL([
   '<b>E-mailová adresa a ID účtu</b> – prihlásenie (odkaz e-mailom alebo Google) a modlitebné skupiny. Právny základ: zmluva (čl. 6 ods. 1 písm. b) GDPR).',
   '<b>Modlitebné skupiny</b> – členstvo, úmysly, ťuknutia „Modlím sa za teba“ a nahlásenia príspevkov. Keďže tieto údaje môžu odhaľovať náboženské presvedčenie (osobitná kategória, čl. 9 GDPR), pri vytvorení účtu a pri vstupe do skupiny žiadame tvoj <b>výslovný súhlas</b> (čl. 9 ods. 2 písm. a)). Skupiny sú súkromné a vidia ich iba ich členovia.',
   '<b>Token pre push notifikácie</b> – upozornenie, keď sa niekto modlí za tvoj úmysel. Právny základ: súhlas.'])]),
 (None, 'Analytika (dobrovoľná, predvolene vypnutá)', ['Ak zapneš anonymné štatistiky používania, zaznamenávame udalosti ako „modlitba dokončená“ s náhodným identifikátorom (PostHog, server v EÚ). Analytika nikdy neobsahuje meno, e-mail ani text úmyslov. Právny základ: súhlas (čl. 6 ods. 1 písm. a)); v aplikácii ju môžeš kedykoľvek vypnúť.']),
 (None, 'Predplatné', ['Platby spracúva <b>Google Play</b>, údaje o karte nikdy nevidíme. Cez <b>RevenueCat</b> dostávame iba technické ID nákupu a stav predplatného, aby sme odomkli Premium. Právny základ: zmluva.']),
 (None, 'Sprostredkovatelia a miesto uloženia', [UL([
   '<b>Supabase</b> – databáza a prihlásenie, dátové centrum v EÚ (Frankfurt, Nemecko)',
   '<b>PostHog</b> – dobrovoľná anonymná analytika, server v EÚ',
   '<b>RevenueCat</b> a <b>Google Play</b> – stav predplatného',
   '<b>Firebase Cloud Messaging</b> (Google) – doručenie push notifikácií',
   '<b>Prihlásenie cez Google</b> – iba ak ho zvolíš']),
   'Ak sprostredkovateľ prenáša údaje mimo EÚ, deje sa to na základe štandardných zmluvných doložiek EÚ alebo rámca EU‑US Data Privacy Framework. Údaje nepredávame ani nezdieľame na reklamu.']),
 (None, 'Ako dlho údaje uchovávame', [UL(['Údaje v telefóne – kým aplikáciu neodinštaluješ alebo ich v nej nevymažeš.', 'Účet a údaje na serveri – kým účet nevymažeš; vymazanie je okamžité a nevratné.', 'Analytické udalosti – najviac 12 mesiacov.', 'Úmysly sa vymažú spolu so skupinou alebo s tvojím účtom, prípadne skôr ich vymaže autor alebo správca skupiny.'])]),
 ('vymazanie', 'Vymazanie účtu a údajov', [f'V aplikácii: <b>Profil → Súkromie a údaje → Vymazať účet a údaje</b> (bez účtu: <b>Vymazať všetky údaje</b>). Okamžite sa vymaže tvoj účet, členstvá v skupinách, úmysly, ťuknutia a push tokeny z našich serverov a vyčistia sa údaje v telefóne. Bez účtu stačí aplikáciu odinštalovať. O vymazanie môžeš požiadať aj e-mailom na <a href="mailto:{EMAIL}">{EMAIL}</a> z adresy svojho účtu – pozri <a href="delete-account.html#sk">delete-account.html</a>.']),
 (None, 'Tvoje práva', ['Máš právo na prístup, opravu, vymazanie, obmedzenie spracúvania, prenosnosť, námietku a kedykoľvek odvolať súhlas. V aplikácii môžeš exportovať svoje údaje (súbor JSON), vymazať účet a vypnúť analytiku. Sťažnosť môžeš podať na Úrad na ochranu osobných údajov SR, Hraničná 12, 820 07 Bratislava, www.dataprotection.gov.sk.']),
 (None, 'Deti', ['Aplikácia je určená dospelým. Účty a modlitebné skupiny nie sú určené deťom mladším ako 16 rokov.']),
 (None, 'Bezpečnosť', ['Všetky údaje sa prenášajú šifrovane (HTTPS/TLS). Tabuľky na serveri chráni zabezpečenie na úrovni riadkov, takže obsah skupiny môžu čítať iba jej členovia.']),
 (None, 'Zmeny', ['O podstatných zmenách ťa budeme informovať v aplikácii a aktualizujeme dátum účinnosti.']),
]
DEL_EN = [
 (None, 'Delete in the app', [UL(['Open <b>Ave</b> and go to the <b>Profile</b> tab.', 'In <b>Privacy and data</b>, tap <b>Delete account and data</b> and confirm.', 'Your account and all related data are deleted immediately.'])]),
 (None, 'Delete by e-mail', [f'If you no longer have the app installed, send an e-mail to <a href="mailto:{EMAIL}?subject=Ave%20-%20delete%20account">{EMAIL}</a> with the subject <i>Ave – delete account</i> from the e-mail address you use to sign in. We will delete your account within 30 days (usually much sooner) and confirm by e-mail.']),
 (None, 'What is deleted', [UL(['Account (e-mail address, account ID, sign-in data)', 'Group memberships, prayer intentions you posted, "I am praying for you" taps and your reports', 'Push notification tokens', 'Analytics events linked to your random identifier']), 'Nothing is kept, except that Google Play keeps its own purchase records required by law; your subscription must be cancelled separately in Google Play → Payments & subscriptions. Groups you administer are deleted if you are their only admin.']),
 (None, 'Without an account', ['If you use Ave without an account, all your data is stored only on your device. Uninstalling the app or using <b>Profile → Privacy and data → Delete all data</b> deletes it.']),
]
DEL_SK = [
 (None, 'Vymazanie v aplikácii', [UL(['Otvor <b>Ave</b> a prejdi na kartu <b>Profil</b>.', 'V časti <b>Súkromie a údaje</b> ťukni na <b>Vymazať účet a údaje</b> a potvrď.', 'Účet a všetky súvisiace údaje sa okamžite vymažú.'])]),
 (None, 'Vymazanie e-mailom', [f'Ak už aplikáciu nemáš nainštalovanú, pošli e-mail na <a href="mailto:{EMAIL}?subject=Ave%20-%20vymazanie%20uctu">{EMAIL}</a> s predmetom <i>Ave – vymazanie účtu</i> z adresy, ktorou sa prihlasuješ. Účet vymažeme do 30 dní (zvyčajne oveľa skôr) a potvrdíme ti to e-mailom.']),
 (None, 'Čo sa vymaže', [UL(['Účet (e-mailová adresa, ID účtu, prihlasovacie údaje)', 'Členstvá v skupinách, tvoje úmysly, ťuknutia „Modlím sa za teba“ a tvoje nahlásenia', 'Tokeny pre push notifikácie', 'Analytické udalosti spojené s tvojím náhodným identifikátorom']), 'Nič neuchovávame; Google Play si však vedie vlastné záznamy o nákupoch, ktoré vyžaduje zákon. Predplatné treba zrušiť zvlášť v Google Play → Platby a predplatné. Skupiny, ktorých si jediný správca, sa vymažú.']),
 (None, 'Bez účtu', ['Ak používaš Ave bez účtu, všetky údaje sú iba v tvojom telefóne. Vymažeš ich odinštalovaním aplikácie alebo cez <b>Profil → Súkromie a údaje → Vymazať všetky údaje</b>.']),
]
TERMS_EN = [
 (None, 'The service', [f'{APP} provides prayers, audio, a guided Rosary, multi-day challenges and private prayer groups. By using the app you agree to these terms.']),
 (None, 'Premium subscription', ['New users get the Premium features free for the first 7 days, with no sign-up and no payment. After that, Premium is available as an auto-renewing monthly or yearly subscription purchased through Google Play. The price is shown in the app and in Google Play before purchase. The subscription renews automatically unless you cancel it at least 24 hours before the end of the current period in Google Play → Payments & subscriptions. Refunds follow Google Play\'s policies.']),
 (None, 'Prayer groups', ['Groups are private. Do not post content that is unlawful, hateful, harassing or that violates others\' privacy. Members can report posts and group admins can delete them. We may remove content or accounts that break these rules.']),
 (None, 'Content', ['Traditional prayers are in the public domain. Other texts and audio are provided for personal, non-commercial use. The app does not replace pastoral care, medical or psychological help.']),
 (None, 'Liability', ['The app is provided "as is". To the extent permitted by law, we are not liable for indirect damages or for interruptions of the service.']),
 (None, 'Contact', [f'<a href="mailto:{EMAIL}">{EMAIL}</a>. Privacy: <a href="privacy.html">privacy.html</a>.']),
]
TERMS_SK = [
 (None, 'Služba', [f'{APP} poskytuje modlitby, audio, sprevádzaný ruženec, viacdňové výzvy a súkromné modlitebné skupiny. Používaním aplikácie súhlasíš s týmito podmienkami.']),
 (None, 'Predplatné Premium', ['Noví používatelia majú funkcie Premium prvých 7 dní zadarmo, bez registrácie a bez platby. Potom je Premium dostupné ako automaticky obnovované mesačné alebo ročné predplatné cez Google Play. Cena sa zobrazí v aplikácii a v Google Play pred nákupom. Predplatné sa obnovuje automaticky, ak ho nezrušíš aspoň 24 hodín pred koncom obdobia v Google Play → Platby a predplatné. Vrátenie peňazí sa riadi pravidlami Google Play.']),
 (None, 'Modlitebné skupiny', ['Skupiny sú súkromné. Nezverejňuj obsah, ktorý je nezákonný, nenávistný, obťažujúci alebo porušuje súkromie iných. Členovia môžu príspevky nahlásiť a správcovia skupiny ich môžu vymazať. Obsah alebo účty porušujúce tieto pravidlá môžeme odstrániť.']),
 (None, 'Obsah', ['Tradičné modlitby sú voľné dielo. Ostatné texty a audio sú určené na osobné nekomerčné použitie. Aplikácia nenahrádza duchovné sprevádzanie ani lekársku či psychologickú pomoc.']),
 (None, 'Zodpovednosť', ['Aplikácia sa poskytuje „tak, ako je“. V rozsahu povolenom zákonom nezodpovedáme za nepriame škody ani za prerušenie služby.']),
 (None, 'Kontakt', [f'<a href="mailto:{EMAIL}">{EMAIL}</a>. Súkromie: <a href="privacy.html#sk">privacy.html</a>.']),
]
os.makedirs(OUT, exist_ok=True)
U_EN, U_SK = 'Effective date: 26 November 2026', 'Platné od: 26. novembra 2026'
open(f'{OUT}/privacy.html','w').write(page('Privacy Policy', 'Privacy Policy / Zásady ochrany súkromia', {
  'en': doc('en', f'Privacy Policy – {APP}', U_EN, PRIV_EN), 'sk': doc('sk', f'Zásady ochrany súkromia – {APP}', U_SK, PRIV_SK)}))
open(f'{OUT}/delete-account.html','w').write(page('Delete account and data', 'Delete account and data / Vymazanie účtu a údajov', {
  'en': doc('en', f'Delete your {APP} account and data', U_EN, DEL_EN), 'sk': doc('sk', f'Vymazanie účtu a údajov v aplikácii {APP}', U_SK, DEL_SK)}))
open(f'{OUT}/terms.html','w').write(page('Terms of Use', 'Terms of Use / Podmienky používania', {
  'en': doc('en', f'Terms of Use – {APP}', U_EN, TERMS_EN), 'sk': doc('sk', f'Podmienky používania – {APP}', U_SK, TERMS_SK)}))
