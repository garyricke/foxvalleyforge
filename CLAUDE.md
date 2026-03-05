# Fox Valley Forge — Claude Session Notes

## Project Overview
Single-page website (`index.html`) for Fox Valley Forge SC, a youth soccer club. All styles and JS are inline in `index.html`. Images hosted on Cloudinary (`res.cloudinary.com/dsbllwpbh`).

## Key Files
- `index.html` — main website (currently ~1891 lines)
- `fox-valley-forge-brand-guide.html` — brand guide (root level, NOT in /assets)
- `pitch-deck.html` — sponsor pitch deck (slide-based, fullscreen, mobile-responsive as of Mar 5)
- `generated_imgs/` — locally generated images (most now replaced with Cloudinary URLs)

## Git & Deployment
- Repo: `git@github.com:garyricke/foxvalleyforge.git` (SSH configured, pushes auto-deploy to Netlify)
- Git global user: Gary Ricke / gary.ricke@orbisdesign.com
- Working directory: `/Users/garyricke/Documents/foxvalley forge`

## Brand Colors
- Navy: `#001B44` (primary)
- Crimson: `#A91335`
- Gold: `#C5A059`
- Home jersey: Navy with Gold trim

## Where We Left Off (Mar 5, 2026)

### Brand Guide (`fox-valley-forge-brand-guide.html`)
- Added 3 official logos with updated Cloudinary URLs (see Logo System section)
  - With Fox Valley: `v1772573826/forge-logo-w-fox-valley-23jan2026_ojhvif.png`
  - No Fox Valley (compact): `v1772573827/forge-logo-no-fox-valley-23jan2026_olh5tk.png`
  - Rec/Kids: `v1772573826/forge-logo-rec-23jan2026_bifcvt.png`
- ZIP download (public): `v1772575623/forge-logos-23jan2026_p8wkmz.zip`
- Download link in both TOC and Logo System section

### index.html Footer — Connect column additions
- Brand Guide → `fox-valley-forge-brand-guide.html`
- Pitch Deck → `pitch-deck.html`
- Pitch Deck Hi Res → Google Drive
- Pitch Deck Med Res → Cloudinary PDF (`v1772636268/...medres_cav5ci.pdf`)

### pitch-deck.html
- Full mobile CSS added (`@media max-width: 767px`)
- Slides scroll vertically, grids collapse, padding reduced, touch-friendly nav

---

## Previous Notes (Feb 27 – Mar 2, 2026)

### Events Section
- Default view shows **only "Girls in Sports Day"**
- All other events hidden via `[data-hidden-event]` CSS attribute
- To reveal all events: append `?show=hiddenevents` to URL
- JS toggle is at the top of the `<script>` block, uses `display: 'grid'` (not `''`) to override CSS

### Event Cards (hidden by default)
- St. Patrick's Day Parade — March 14
- March ID Sessions (was "Open Gyms")
- April ID Sessions (was "Open Gyms")
- Team Selections & Tryouts — May 18–21
- 3v3 Live Tournament — June 27
- USA Cup — July 10–18

### Cloudinary Image URLs (event cards)
- St. Patrick's Day Parade: `v1772211945/st-patricks-day-parade_ftgx7y.jpg`
- ID Sessions (March & April): `v1772211945/open-gyms_jtvx1c.jpg`
- Team Tryouts: `v1772211945/team-tryouts_v47xti.jpg`
- 3v3 Tournament: `v1772211945/3v3-tournament_oc6m62.jpg`
- USA Cup: `v1772211945/usa-cup_exkhct.jpg`

### Programs
- Forge Community: U6–U12
- Forge Ignite: U6–U12
- Forge Performance: U11–U19
- **Forge College Prep: labeled as "Add-On Package"** (not a standalone program tier)

### Other Changes Made
- All CTAs changed from "Register Now" → "Request Information"
- Registration form submit: "SECURE MY SPOT" → "REQUEST INFORMATION"
- `openRegisterWithProgram(program)` function pre-selects program in modal dropdown
- Footer nav events link: "Girls in Sports Day — Mar 22" → "Upcoming Events"
- St. Patrick's Day Parade image regenerated with Forge navy/gold jerseys and correct sign text
