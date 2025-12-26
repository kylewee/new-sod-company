# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sod.Company is a lead generation website for sod installation services. It uses a static site generator to create city-specific landing pages with dynamic pricing.

## Architecture

**Data-Driven Page Generation:**
- `data/cities.json` - City definitions (40 cities across 13 states) with phone, grass types, pricing
- `data/pricing.json` - Pricing engine with master multipliers for global price adjustments
- `scripts/generate_pages.py` - Generates all HTML pages from data files

**Output Structure:**
- `www/sod.company/` - Generated static site (deploy this folder)
- Each city gets `/{state}/{city}/index.html` and `/{state}/{city}/prices/index.html`

**Key Files:**
- `contact-handler.php` - PHP form handler for lead capture (saves to `/leads/` directory, sends email)
- `js/chatbot.js` - AI chatbot that auto-engages visitors after 8 seconds, guides through quote flow
- `js/main.js` - Form validation, smooth scrolling, analytics tracking

## Commands

**Regenerate all pages after data changes:**
```bash
python3 scripts/generate_pages.py
```

**Deploy to HostGator:**
Upload contents of `www/sod.company/` to server's `public_html/sod.company/`

## Pricing Engine

The pricing engine in `data/pricing.json` uses master multipliers to adjust all prices globally:

```json
"master_controls": {
  "sod_multiplier": 1.0,    // Multiply all sod costs
  "labor_multiplier": 1.0,   // Multiply all labor costs
  "delivery_multiplier": 1.0 // Multiply all delivery fees
}
```

Change these values and regenerate pages to update pricing site-wide.

## Adding New Cities

1. Add city entry to `data/cities.json`
2. Run `python3 scripts/generate_pages.py`
3. Verify pages at `www/sod.company/{state}/{city}/`

## Form Handler Configuration

Update email address in `www/sod.company/contact-handler.php`:
```php
$to = 'leads@sod.company'; // CHANGE THIS to your email
```

## Deployment

See `DEPLOY_HOSTGATOR.md` for HostGator + Cloudflare setup instructions.
