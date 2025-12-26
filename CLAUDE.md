# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sod.Company is a lead generation website for sod installation services. It uses a static site generator to create city-specific landing pages with dynamic pricing across 370 cities in 18 states.

## Architecture

**Data-Driven Page Generation:**
- `data/cities.json` - City definitions (370 cities) with phone, grass types, zip, pricing
- `data/pricing.json` - Pricing engine with master multipliers for global price adjustments
- `scripts/generate_pages.py` - Generates all HTML pages, homepage, and sitemap from data files

**Output Structure:**
- `www/sod.company/` - Generated static site (741 HTML pages) - deploy this folder
- Each city gets `/{state}/{city}/index.html` and `/{state}/{city}/prices/index.html`
- Homepage at `index.html`, sitemap at `sitemap.xml`

**Frontend:**
- `js/chatbot.js` - AI chatbot (auto-engages after 8s, captures leads via quote flow)
- `js/main.js` - Form validation, smooth scrolling, analytics tracking
- `css/main.css` - Primary styles, `css/pricing.css` - Pricing table styles

**Backend:**
- `contact-handler.php` - PHP form handler (saves to `/leads/`, sends email notification)

**Marketing Assets:**
- `marketing/email-campaigns/` - 6-email drip sequence
- `marketing/video-scripts/` - 6 video scripts (hero, explainer, testimonial, FAQ, social, local)
- `marketing/social-media/` - 3-week content calendar with monthly themes
- `marketing/citations/` - Citation generator (CSV/JSON output for 370 cities)
- `marketing/voice-search-optimization.md` - Schema markup and voice query optimization
- `marketing/review-management.md` - Review collection templates and response scripts

## Commands

**Regenerate all pages:**
```bash
python3 scripts/generate_pages.py
```

**Generate citation files:**
```bash
python3 marketing/citations/citation-generator.py
```

## Pricing Engine

The pricing engine in `data/pricing.json` uses master multipliers:

```json
"master_controls": {
  "sod_multiplier": 1.0,
  "labor_multiplier": 1.0,
  "delivery_multiplier": 1.0
}
```

Change values and run `python3 scripts/generate_pages.py` to update all pricing site-wide.

## Adding New Cities

1. Add entry to `data/cities.json` with: city, state, state_full, phone, zip, grasses, primary_grass, avg_price
2. Run `python3 scripts/generate_pages.py`
3. Run `python3 marketing/citations/citation-generator.py` to update citations

## Configuration

**Form Handler Email** - Update in `www/sod.company/contact-handler.php`:
```php
$to = 'leads@sod.company'; // CHANGE THIS
```

**Deployment** - See `DEPLOY_HOSTGATOR.md` for HostGator + Cloudflare setup.
