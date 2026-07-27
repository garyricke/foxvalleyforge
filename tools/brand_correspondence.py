#!/usr/bin/env python3
"""Re-brand correspondence.html for Fox Valley Forge after a rebuild.

The shared skill script (~/.claude/skills/correspondence/build_correspondence.py)
regenerates correspondence.html from scratch with Olsson Roofing branding and no
password gate, so every rebuild wipes our customizations. Run this immediately
after it:

    python3 ~/.claude/skills/correspondence/build_correspondence.py
    python3 tools/brand_correspondence.py

Applies: Forge navy/crimson/gold palette, Oswald + Source Sans 3, Forge logo and
favicon, and the shared client-side 'fvf_admin' password gate used by the other
internal pages (status.html, meetings.html, forge-fest-cards.html).
"""
import re
import sys
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "correspondence.html"

LOGO = ("https://res.cloudinary.com/dsbllwpbh/image/upload/f_auto,q_auto/"
        "v1770763739/forge-logo-w-fox-valley-23jan2026_d1dlgi.png")
FAVICON = ("https://res.cloudinary.com/dsbllwpbh/image/upload/f_auto,q_auto/"
           "v1771377451/favicon-forge-1_r6l4ax.png")
# SHA-256 of the shared internal review password (same hash as the other gated pages)
GATE_HASH = "8e484aece8ea37afd67cd15d4f13fb2ef4ca78b2f5d5904400aa4bb1a2aad3a3"

GATE_CSS = """
    /* password gate */
    #pw-gate { position:fixed; inset:0; z-index:9999; background:linear-gradient(135deg,#000d22 0%,var(--navy) 60%,#1a0a1e 100%); display:flex; align-items:center; justify-content:center; }
    #pw-gate::before { content:''; position:absolute; inset:0; background-image:linear-gradient(rgba(197,160,89,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(197,160,89,.06) 1px,transparent 1px); background-size:40px 40px; pointer-events:none; }
    #pw-box { position:relative; background:rgba(255,255,255,.04); border:1px solid rgba(197,160,89,.25); border-radius:16px; padding:48px 40px; text-align:center; width:min(400px,90vw); box-shadow:0 24px 80px rgba(0,0,0,.5); }
    #pw-box img { height:52px; margin:0 auto 24px; display:block; }
    #pw-box h2 { font-family:'Oswald',Impact,sans-serif; font-size:1.9rem; color:#C5A059; letter-spacing:.06em; margin:0 0 8px; text-transform:uppercase; }
    #pw-box .sub { font-size:.85rem; color:rgba(236,244,249,.55); margin:0 0 28px; }
    #pw-input { width:100%; padding:12px 16px; background:rgba(0,0,0,.3); border:1px solid rgba(197,160,89,.3); border-radius:8px; color:#fff; font-size:.95rem; font-family:inherit; outline:none; transition:border-color .2s; }
    #pw-input:focus { border-color:#C5A059; }
    #pw-btn { margin-top:14px; width:100%; padding:12px; background:#C5A059; color:#001B44; border:0; border-radius:8px; font-family:'Oswald',Impact,sans-serif; font-size:1.1rem; letter-spacing:.1em; cursor:pointer; }
    #pw-btn:hover { background:#A6813C; }
    #pw-error { font-size:.8rem; color:#ff7a7a; margin:12px 0 0; min-height:1.2em; }
    .pw-shake { animation:pwShake .35s; }
    @keyframes pwShake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-8px)} 75%{transform:translateX(8px)} }
"""

GATE_HTML = f"""
<!-- PASSWORD GATE — shares 'fvf_admin' session key -->
<div id="pw-gate">
  <div id="pw-box">
    <img src="{LOGO}" alt="Fox Valley Forge SC" onerror="this.style.display='none'">
    <h2>Correspondence</h2>
    <p class="sub">This page is password protected.</p>
    <input id="pw-input" type="password" placeholder="Enter password" autocomplete="current-password">
    <button id="pw-btn">Enter</button>
    <p id="pw-error"></p>
  </div>
</div>
<script>
(function(){{
  var KEY='fvf_admin';
  var HASH='{GATE_HASH}';
  var gate=document.getElementById('pw-gate');
  if(sessionStorage.getItem(KEY)==='1'){{gate.style.display='none';return;}}
  document.body.style.overflow='hidden';
  function unlock(){{sessionStorage.setItem(KEY,'1');document.body.style.overflow='';gate.style.display='none';}}
  function fail(){{document.getElementById('pw-error').textContent='Incorrect password. Try again.';var b=document.getElementById('pw-box');b.classList.remove('pw-shake');void b.offsetWidth;b.classList.add('pw-shake');document.getElementById('pw-input').select();}}
  function attempt(){{crypto.subtle.digest('SHA-256',new TextEncoder().encode(document.getElementById('pw-input').value)).then(function(buf){{var hex=Array.prototype.map.call(new Uint8Array(buf),function(b){{return b.toString(16).padStart(2,'0');}}).join('');if(hex===HASH){{unlock();}}else{{fail();}}}});}}
  document.getElementById('pw-btn').addEventListener('click',attempt);
  document.getElementById('pw-input').addEventListener('keydown',function(e){{if(e.key==='Enter')attempt();}});
  document.getElementById('pw-input').focus();
}})();
</script>
"""


def main():
    if not PAGE.exists():
        sys.exit(f"{PAGE} not found — run the build script first.")

    s = PAGE.read_text(encoding="utf-8")

    if "fvf_admin" in s:
        sys.exit("correspondence.html already branded — rebuild it first, then re-run.")

    # head
    s = s.replace("<title>Correspondence — Olsson Roofing</title>",
                  "<title>Correspondence — Fox Valley Forge SC</title>")
    s = re.sub(r'<link rel="icon"[^>]*/>',
               f'<link rel="icon" href="{FAVICON}" />', s, count=1)
    s = s.replace("family=Montserrat:wght@700;800;900&family=Inter:wght@400;500;600",
                  "family=Oswald:wght@500;600;700&family=Source+Sans+3:wght@400;500;600")

    # type + palette
    s = s.replace("'Montserrat',sans-serif", "'Oswald',Impact,sans-serif")
    s = s.replace("font-family:'Inter',system-ui,sans-serif",
                  "font-family:'Source Sans 3',system-ui,sans-serif")
    s = s.replace(":root { --red:#E9322E; --red-soft:#F0706D; --ink:#f2f2f2; }",
                  ":root { --red:#A91335; --red-soft:#C5A059; --ink:#ECF4F9; --navy:#001B44; }")
    s = s.replace("background:linear-gradient(165deg,#1e1e1e 0%,#161616 45%,#0d0d0d 100%)",
                  "background:linear-gradient(135deg,#000d22 0%,#001B44 60%,#1a0a1e 100%)")
    s = s.replace("background:rgba(233,50,46,0.12)", "background:rgba(197,160,89,0.14)")
    s = s.replace("rgba(242,242,242,", "rgba(236,244,249,")
    s = s.replace(".copy:hover { background:#c92a26; }", ".copy:hover { background:#B92B4A; }")

    # header block
    s = re.sub(r'<a href="index\.html" title="Back to olssonroofing\.com">.*?</a>',
               f'<a href="index.html" title="Back to forgesoccerclub.com">'
               f'<img src="{LOGO}" alt="Fox Valley Forge SC" style="height:52px" '
               f'onerror="this.style.display=\'none\'" /></a>',
               s, count=1, flags=re.S)
    s = s.replace("Every response email sent to the Olsson team",
                  "Every response email sent to the Forge team")
    s = s.replace('<a class="backlink" href="admin.html">', '<a class="backlink" href="index.html">')
    s = s.replace("Back to admin</a>", "Back to the site</a>")

    # gate
    s = s.replace("  </style>", GATE_CSS + "  </style>", 1)
    s = s.replace("<body>\n", "<body>\n" + GATE_HTML, 1)

    PAGE.write_text(s, encoding="utf-8")
    print(f"Re-branded {PAGE.name} — Forge palette + fvf_admin gate applied.")


if __name__ == "__main__":
    main()
