# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sod.Company is a lead generation website for sod installation services. It uses a Python static site generator to create city-specific landing pages with dynamic pricing across 555 cities in 24 states.

## Architecture

```
sod-company-deploy/
├── data/                    # Source data for page generation
│   ├── cities.json          # 555 city definitions (phone, grasses, pricing)
│   └── pricing.json         # Pricing engine with master multipliers
├── scripts/
│   └── generate_pages.py    # Main generator - creates all HTML + sitemap
├── www/sod.company/         # Generated static site (deploy this)
│   ├── {state}/{city}/      # City landing pages
│   ├── blog/                # SEO blog articles (6 posts)
│   ├── css/, js/, images/   # Static assets
│   └── sitemap.xml          # 1,118 URLs
├── docs/                    # GitHub Pages mirror of www/sod.company
├── tools/
│   └── sms-review-system/   # Twilio SMS for review requests
└── marketing/               # Email, video, social, citation assets
```

## Commands

**Regenerate all pages:**
```bash
python3 scripts/generate_pages.py
```

**Update GitHub Pages after regenerating:**
```bash
rm -rf docs && cp -r www/sod.company docs
```

**SMS Review System:**
```bash
cd tools/sms-review-system
./venv/bin/python review_sms.py add "John Smith" "+15551234567" "Houston"
./venv/bin/python review_sms.py send      # Process scheduled messages
./venv/bin/python review_sms.py list      # Show all customers
./venv/bin/python review_sms.py reply "+15551234567" 5  # Record satisfaction score
```

**Generate citation files:**
```bash
python3 marketing/citations/citation-generator.py
```

## Page Generation Flow

1. `generate_pages.py` reads `data/cities.json` and `data/pricing.json`
2. For each city, generates:
   - `/{state}/{city}/index.html` - Main landing page with lead form
   - `/{state}/{city}/prices/index.html` - Pricing table page
3. Generates homepage with state/city directory
4. Generates `sitemap.xml` with all URLs including blog posts

## Pricing Engine

Modify `data/pricing.json` master multipliers to adjust all prices site-wide:

```json
"master_controls": {
  "sod_multiplier": 1.0,
  "labor_multiplier": 1.0,
  "delivery_multiplier": 1.0
}
```

Then run `python3 scripts/generate_pages.py` to regenerate.

## Adding New Cities

1. Add entry to `data/cities.json`:
   ```json
   {
     "city": "Austin",
     "state": "TX",
     "state_full": "Texas",
     "phone": "(512) 555-0100",
     "zip": "78701",
     "grasses": ["Bermuda", "St. Augustine", "Zoysia"],
     "primary_grass": "Bermuda",
     "avg_price": "$0.85"
   }
   ```
2. Run `python3 scripts/generate_pages.py`
3. Update docs folder for GitHub Pages

## SEO Features

Each generated page includes:
- LocalBusiness schema markup (JSON-LD)
- FAQ schema markup for rich snippets
- Open Graph + Twitter Card meta tags
- Canonical URLs
- "Nearby Cities" internal linking section
- Preload/preconnect hints for performance

## SMS Review System (Pulse-First Flow)

Located in `tools/sms-review-system/`. Asks customer satisfaction (1-5) before requesting reviews:
- Score 4-5: Sends Google review link
- Score 1-3: Alerts for immediate follow-up, no review request

Requires Twilio credentials in `tools/sms-review-system/config.py`.

## Deployment

**GitHub Pages:** Enable in repo Settings → Pages → Source: `/docs` folder

**Production:** See `DEPLOY_HOSTGATOR.md` for HostGator + Cloudflare setup. Update email in `www/sod.company/contact-handler.php`.
