#!/usr/bin/env python3
"""
Sod.Company Page Generator
Generates city pages, pricing pages, and blog content
"""

import json
import os
from pathlib import Path

# Get paths
script_dir = Path(__file__).parent
base_dir = script_dir.parent
data_dir = base_dir / 'data'
www_dir = base_dir / 'www' / 'sod.company'

# Load data
with open(data_dir / 'cities.json') as f:
    cities_data = json.load(f)
    cities = cities_data['cities']

with open(data_dir / 'pricing.json') as f:
    pricing_data = json.load(f)

def get_nearby_cities(current_city, state, max_cities=6):
    """Get other cities in the same state for internal linking"""
    nearby = []
    for c in cities:
        if c['state'] == state and c['city'] != current_city:
            nearby.append(c)
        if len(nearby) >= max_cities:
            break
    return nearby


def calculate_price(grass_type, pallets):
    """Calculate total installed price for given grass type and pallet count"""
    engine = pricing_data['pricing_engine']

    sod_cost = engine['sod_cost_per_sqft'].get(grass_type, 0.45)
    labor_cost = engine['install_labor_per_sqft']
    delivery_base = engine['delivery']['base_fee']
    delivery_per_pallet = engine['delivery']['per_pallet']
    sqft_per_pallet = engine['sqft_per_pallet']

    # Apply multipliers
    sod_cost *= engine['master_controls']['sod_multiplier']
    labor_cost *= engine['master_controls']['labor_multiplier']
    delivery_base *= engine['master_controls']['delivery_multiplier']
    delivery_per_pallet *= engine['master_controls']['delivery_multiplier']

    total_sqft = pallets * sqft_per_pallet
    material = total_sqft * sod_cost
    labor = total_sqft * labor_cost
    delivery = delivery_base + (pallets * delivery_per_pallet)
    total = material + labor + delivery

    return {
        'sqft': total_sqft,
        'material': round(material, 2),
        'labor': round(labor, 2),
        'delivery': round(delivery, 2),
        'total': round(total, 2)
    }

def generate_pricing_table(grass_type, max_pallets=10):
    """Generate HTML pricing table for grass type"""
    rows = ""
    for pallets in range(1, max_pallets + 1):
        price = calculate_price(grass_type, pallets)
        rows += f"""
        <tr>
            <td>{pallets}</td>
            <td>{price['sqft']:,}</td>
            <td>${price['material']:,.2f}</td>
            <td>${price['labor']:,.2f}</td>
            <td>${price['delivery']:,.2f}</td>
            <td class="total"><strong>${price['total']:,.2f}</strong></td>
        </tr>"""

    return f"""
    <table class="pricing-table">
        <thead>
            <tr>
                <th>Pallets</th>
                <th>Sq Ft</th>
                <th>Material</th>
                <th>Labor</th>
                <th>Delivery</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """

def get_city_template(city_data):
    """Generate main city page HTML"""
    city = city_data['city']
    state = city_data['state']
    state_full = city_data['state_full']
    phone = city_data['phone']
    primary_grass = city_data['primary_grass']
    grasses = city_data['grasses']
    avg_price = city_data['avg_price']

    city_slug = city.lower().replace(' ', '-').replace('.', '')
    state_slug = state.lower()

    # Get nearby cities for internal linking
    nearby = get_nearby_cities(city, state)
    nearby_links = ''.join([
        f'<a href="/{c["state"].lower()}/{c["city"].lower().replace(" ", "-").replace(".", "")}/">{c["city"]}</a>'
        for c in nearby
    ])

    grass_options = ''.join([f'<option value="{g}">{g}</option>' for g in grasses])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sod Installation {city}, {state_full} | Professional {primary_grass} Sod | Sod.Company</title>
    <meta name="description" content="Professional sod installation in {city}, {state_full}. {primary_grass}, {', '.join(grasses[:2])} sod starting at {avg_price}/sqft installed. Free quotes, same-week service. Call {phone}">
    <meta name="keywords" content="sod installation {city}, {primary_grass} sod {city}, lawn installation {city}, sod prices {city} {state}">
    <link rel="canonical" href="https://sod.company/{state_slug}/{city_slug}/">

    <!-- Open Graph -->
    <meta property="og:title" content="Sod Installation {city}, {state_full} | Sod.Company">
    <meta property="og:description" content="Professional sod installation in {city}. {primary_grass} sod starting at {avg_price}/sqft installed. Free quotes, same-week service.">
    <meta property="og:url" content="https://sod.company/{state_slug}/{city_slug}/">
    <meta property="og:type" content="website">
    <meta property="og:image" content="https://sod.company/images/og-sod-installation.jpg">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Sod Installation {city} | Sod.Company">
    <meta name="twitter:description" content="{primary_grass} sod installation in {city} starting at {avg_price}/sqft.">

    <link rel="stylesheet" href="/css/main.css">

    <!-- Schema Markup -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Sod.Company - {city}",
        "description": "Professional sod installation in {city}, {state_full}",
        "telephone": "{phone}",
        "url": "https://sod.company/{state_slug}/{city_slug}/",
        "address": {{
            "@type": "PostalAddress",
            "addressLocality": "{city}",
            "addressRegion": "{state}",
            "addressCountry": "US"
        }},
        "priceRange": "$$",
        "areaServed": "{city}, {state_full}"
    }}
    </script>

    <!-- FAQ Schema -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {{
                "@type": "Question",
                "name": "How much does sod installation cost in {city}?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "Sod installation in {city} typically costs {avg_price} per square foot installed, including material, labor, and delivery. For a 5,000 sqft lawn, expect $4,250 - $5,500 total."
                }}
            }},
            {{
                "@type": "Question",
                "name": "What is the best grass for {city}?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "{primary_grass} is the most popular choice in {city} due to its excellent adaptation to local climate and soil conditions."
                }}
            }},
            {{
                "@type": "Question",
                "name": "How long does sod installation take?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "Most residential sod installations in {city} are completed in one day. A typical 5,000 sqft lawn takes 4-6 hours to install."
                }}
            }}
        ]
    }}
    </script>
</head>
<body>
    <header>
        <nav class="container">
            <div class="logo"><a href="/">Sod.Company</a></div>
            <div class="nav-links">
                <a href="/{state_slug}/{city_slug}/prices/">Pricing</a>
                <a href="/blog/">Blog</a>
                <a href="tel:{phone}" class="phone-link">{phone}</a>
            </div>
        </nav>
    </header>

    <section class="hero">
        <div class="container">
            <h1>Professional Sod Installation in {city}, {state_full}</h1>
            <p class="subtitle">Premium {primary_grass} sod starting at {avg_price}/sqft installed</p>
            <p class="cta-text">Free quotes • Same-week installation • 30-day warranty</p>
            <div class="hero-cta">
                <a href="tel:{phone}" class="btn btn-primary btn-large">Call {phone}</a>
                <a href="#quote" class="btn btn-secondary btn-large">Get Free Quote</a>
            </div>
        </div>
    </section>

    <section class="services">
        <div class="container">
            <h2>Sod Installation Services in {city}</h2>
            <div class="service-grid">
                <div class="service-card">
                    <h3>Residential Sod Installation</h3>
                    <p>Transform your {city} home with a beautiful new lawn. We handle everything from soil prep to final watering.</p>
                    <ul>
                        <li>Front and backyard installation</li>
                        <li>Soil preparation included</li>
                        <li>Same-week scheduling</li>
                    </ul>
                </div>
                <div class="service-card">
                    <h3>Commercial Sod Installation</h3>
                    <p>Professional sod installation for {city} businesses, HOAs, and property managers.</p>
                    <ul>
                        <li>Large area specialists</li>
                        <li>Volume discounts available</li>
                        <li>Flexible scheduling</li>
                    </ul>
                </div>
                <div class="service-card">
                    <h3>Sod Replacement & Repair</h3>
                    <p>Replace dead or damaged grass with fresh, healthy sod matched to your existing lawn.</p>
                    <ul>
                        <li>Patch repairs available</li>
                        <li>Full lawn renovation</li>
                        <li>Disease-resistant varieties</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <section class="grass-types">
        <div class="container">
            <h2>Grass Types Available in {city}</h2>
            <p>We install premium sod varieties suited to {city}'s climate:</p>
            <div class="grass-grid">
                {''.join([f'<div class="grass-card"><h3>{g}</h3><p>{"Shade-tolerant, lush appearance" if g == "St. Augustine" else "Drought-resistant, low maintenance" if g == "Zoysia" else "High traffic tolerance, full sun" if g == "Bermuda" else "Budget-friendly, minimal care" if g == "Bahia" else "Low maintenance, acidic soil" if g == "Centipede" else "Cool-season, stays green"}</p></div>' for g in grasses])}
            </div>
            <p class="recommendation"><strong>Recommended for {city}:</strong> {primary_grass} - Best suited for local climate and soil conditions.</p>
        </div>
    </section>

    <section class="pricing-preview">
        <div class="container">
            <h2>Sod Installation Pricing in {city}</h2>
            <p>Transparent pricing with no hidden fees. Price includes material, professional installation, and delivery.</p>
            <div class="price-highlight">
                <span class="price">{avg_price}</span>
                <span class="unit">per sqft installed</span>
            </div>
            <p>Average 5,000 sqft lawn: <strong>$4,250 - $5,500</strong> fully installed</p>
            <a href="/{state_slug}/{city_slug}/prices/" class="btn btn-primary">See Full Pricing Table</a>
        </div>
    </section>

    <section id="quote" class="quote-form">
        <div class="container">
            <h2>Get Your Free Quote</h2>
            <p>Fill out the form below for an instant estimate</p>
            <form id="leadForm" action="/contact-handler.php" method="POST">
                <input type="hidden" name="city" value="{city}">
                <input type="hidden" name="state" value="{state}">

                <div class="form-row">
                    <div class="form-group">
                        <label for="name">Name *</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="phone">Phone *</label>
                        <input type="tel" id="phone" name="phone" required>
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="email">Email *</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    <div class="form-group">
                        <label for="lawn_size">Lawn Size (sqft)</label>
                        <input type="number" id="lawn_size" name="lawn_size" placeholder="e.g., 5000">
                    </div>
                </div>

                <div class="form-group">
                    <label for="grass_type">Preferred Grass Type</label>
                    <select id="grass_type" name="grass_type">
                        <option value="">Not sure yet</option>
                        {grass_options}
                    </select>
                </div>

                <div class="form-group">
                    <label for="message">Additional Details</label>
                    <textarea id="message" name="message" rows="3" placeholder="Tell us about your project..."></textarea>
                </div>

                <button type="submit" class="btn btn-primary btn-large btn-full">Get My Free Quote</button>
            </form>
        </div>
    </section>

    <section class="why-us">
        <div class="container">
            <h2>Why Choose Sod.Company in {city}?</h2>
            <div class="benefits-grid">
                <div class="benefit">
                    <h3>Licensed & Insured</h3>
                    <p>Fully licensed contractors with liability insurance for your protection.</p>
                </div>
                <div class="benefit">
                    <h3>Same-Week Installation</h3>
                    <p>Fast scheduling - most jobs installed within 5-7 days of booking.</p>
                </div>
                <div class="benefit">
                    <h3>30-Day Warranty</h3>
                    <p>We stand behind our work with a satisfaction guarantee.</p>
                </div>
                <div class="benefit">
                    <h3>Transparent Pricing</h3>
                    <p>No hidden fees. Your quote is your final price.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="faq">
        <div class="container">
            <h2>Frequently Asked Questions - Sod Installation in {city}</h2>
            <div class="faq-list">
                <div class="faq-item">
                    <h3>How much does sod installation cost in {city}?</h3>
                    <p>Sod installation in {city} typically costs {avg_price} per square foot installed, including material, labor, and delivery. For a 5,000 sqft lawn, expect $4,250 - $5,500 total.</p>
                </div>
                <div class="faq-item">
                    <h3>What's the best grass for {city}?</h3>
                    <p>{primary_grass} is the most popular choice in {city} due to its excellent adaptation to local climate and soil conditions. Other good options include {', '.join(grasses[1:3]) if len(grasses) > 2 else grasses[-1] if len(grasses) > 1 else 'various warm-season grasses'}.</p>
                </div>
                <div class="faq-item">
                    <h3>How long does sod installation take?</h3>
                    <p>Most residential sod installations in {city} are completed in one day. A typical 5,000 sqft lawn takes 4-6 hours to install with our professional crew.</p>
                </div>
                <div class="faq-item">
                    <h3>When is the best time to install sod in {city}?</h3>
                    <p>In {city}, sod can be installed year-round. Spring and fall offer ideal conditions, but our {primary_grass} sod establishes well in any season with proper watering.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="nearby-cities">
        <div class="container">
            <h2>Sod Installation in Other {state_full} Cities</h2>
            <div class="city-links">
                {nearby_links}
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-col">
                    <h4>Sod.Company - {city}</h4>
                    <p>Professional sod installation serving {city}, {state_full} and surrounding areas.</p>
                    <p><a href="tel:{phone}">{phone}</a></p>
                </div>
                <div class="footer-col">
                    <h4>Services</h4>
                    <ul>
                        <li>Residential Sod Installation</li>
                        <li>Commercial Sod Installation</li>
                        <li>Sod Replacement</li>
                        <li>Lawn Renovation</li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Grass Types</h4>
                    <ul>
                        {''.join([f'<li>{g} Sod</li>' for g in grasses[:4]])}
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 Sod.Company. Professional sod installation in {city}, {state_full}.</p>
            </div>
        </div>
    </footer>

    <script src="/js/main.js"></script>
</body>
</html>'''

def get_pricing_page_template(city_data):
    """Generate pricing page HTML"""
    city = city_data['city']
    state = city_data['state']
    state_full = city_data['state_full']
    phone = city_data['phone']
    primary_grass = city_data['primary_grass']
    grasses = city_data['grasses']

    city_slug = city.lower().replace(' ', '-').replace('.', '')
    state_slug = state.lower()

    # Generate pricing tables for each grass type
    pricing_sections = ""
    for grass in grasses:
        pricing_sections += f"""
        <div class="pricing-section">
            <h3>{grass} Sod Pricing - {city}</h3>
            {generate_pricing_table(grass, 10)}
        </div>
        """

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sod Prices {city} {state} | {primary_grass} Sod Installation Cost | Sod.Company</title>
    <meta name="description" content="Sod installation prices in {city}, {state_full}. {primary_grass} sod from $0.85/sqft installed. See our complete pricing table for 1-10 pallets. Call {phone}">
    <meta name="keywords" content="sod prices {city}, {primary_grass} sod cost, lawn installation prices {city} {state}">
    <link rel="canonical" href="https://sod.company/{state_slug}/{city_slug}/prices/">

    <!-- Open Graph -->
    <meta property="og:title" content="Sod Prices {city} {state} | Sod.Company">
    <meta property="og:description" content="Sod installation prices in {city}. {primary_grass} sod from $0.85/sqft installed. Complete pricing table.">
    <meta property="og:url" content="https://sod.company/{state_slug}/{city_slug}/prices/">
    <meta property="og:type" content="website">
    <meta property="og:image" content="https://sod.company/images/og-sod-installation.jpg">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Sod Prices {city} | Sod.Company">
    <meta name="twitter:description" content="{primary_grass} sod installation prices in {city}. See full pricing table.">

    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/pricing.css">
</head>
<body>
    <header>
        <nav class="container">
            <div class="logo"><a href="/">Sod.Company</a></div>
            <div class="nav-links">
                <a href="/{state_slug}/{city_slug}/">Back to {city}</a>
                <a href="tel:{phone}" class="phone-link">{phone}</a>
            </div>
        </nav>
    </header>

    <section class="hero hero-pricing">
        <div class="container">
            <h1>Sod Prices in {city}, {state_full}</h1>
            <p class="subtitle">Transparent pricing - Material, Labor & Delivery Included</p>
        </div>
    </section>

    <section class="pricing-content">
        <div class="container">
            <div class="pricing-intro">
                <p>All prices include <strong>premium sod</strong>, <strong>professional installation</strong>, and <strong>delivery</strong> within 50 miles of {city}. No hidden fees.</p>
                <p><strong>How to read this table:</strong> 1 pallet = 450 sqft of sod. Find your lawn size, see your total installed price.</p>
            </div>

            {pricing_sections}

            <div class="pricing-notes">
                <h3>What's Included</h3>
                <ul>
                    <li>✓ Premium sod from local farms</li>
                    <li>✓ Professional installation by licensed contractors</li>
                    <li>✓ Delivery within 50 miles</li>
                    <li>✓ Basic soil leveling</li>
                    <li>✓ Sod rolling for soil contact</li>
                    <li>✓ Initial watering</li>
                    <li>✓ 30-day installation warranty</li>
                </ul>

                <h3>Additional Services (Optional)</h3>
                <ul>
                    <li>Old grass removal: $0.15-$0.25/sqft</li>
                    <li>Soil amendment/topsoil: $50-$100 per cubic yard</li>
                    <li>Irrigation repair: Quote based on scope</li>
                    <li>Grading/leveling (extensive): $0.10-$0.20/sqft</li>
                </ul>
            </div>

            <div class="cta-box">
                <h3>Ready to Get Started?</h3>
                <p>Call for exact pricing or schedule your free on-site consultation.</p>
                <a href="tel:{phone}" class="btn btn-primary btn-large">Call {phone}</a>
                <a href="/{state_slug}/{city_slug}/#quote" class="btn btn-secondary btn-large">Get Free Quote</a>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2025 Sod.Company. Sod installation prices in {city}, {state_full}.</p>
        </div>
    </footer>
</body>
</html>'''

def generate_city_pages():
    """Generate all city and pricing pages"""
    print(f"Generating pages for {len(cities)} cities...")

    for city_data in cities:
        city = city_data['city']
        state = city_data['state']
        city_slug = city.lower().replace(' ', '-').replace('.', '')
        state_slug = state.lower()

        # Create directories
        city_dir = www_dir / state_slug / city_slug
        prices_dir = city_dir / 'prices'
        city_dir.mkdir(parents=True, exist_ok=True)
        prices_dir.mkdir(parents=True, exist_ok=True)

        # Generate main city page
        city_html = get_city_template(city_data)
        with open(city_dir / 'index.html', 'w') as f:
            f.write(city_html)

        # Generate pricing page
        pricing_html = get_pricing_page_template(city_data)
        with open(prices_dir / 'index.html', 'w') as f:
            f.write(pricing_html)

        print(f"  ✓ {city}, {state}")

    print(f"\n✅ Generated {len(cities) * 2} pages ({len(cities)} cities + {len(cities)} pricing pages)")

def generate_homepage():
    """Generate main homepage"""
    states = {}
    for city in cities:
        state = city['state_full']
        if state not in states:
            states[state] = []
        states[state].append(city)

    state_links = ""
    for state_name, state_cities in sorted(states.items()):
        city_links = ", ".join([
            f'<a href="/{c["state"].lower()}/{c["city"].lower().replace(" ", "-").replace(".", "")}/">{c["city"]}</a>'
            for c in state_cities
        ])
        state_links += f'<div class="state-group"><h4>{state_name}</h4><p>{city_links}</p></div>'

    homepage = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sod Installation | Professional Sod Company | Sod.Company</title>
    <meta name="description" content="Professional sod installation nationwide. St. Augustine, Bermuda, Zoysia sod installed. Free quotes, same-week service. Find sod installers near you.">
    <link rel="stylesheet" href="/css/main.css">
</head>
<body>
    <header>
        <nav class="container">
            <div class="logo"><a href="/">Sod.Company</a></div>
            <div class="nav-links">
                <a href="/blog/">Blog</a>
                <a href="#locations">Locations</a>
            </div>
        </nav>
    </header>

    <section class="hero hero-home">
        <div class="container">
            <h1>Professional Sod Installation</h1>
            <p class="subtitle">Transform your lawn in just one day</p>
            <p>Premium sod • Professional installation • 30-day warranty</p>
            <a href="#locations" class="btn btn-primary btn-large">Find Your City</a>
        </div>
    </section>

    <section class="features">
        <div class="container">
            <h2>Why Choose Sod.Company?</h2>
            <div class="feature-grid">
                <div class="feature">
                    <h3>Instant Lawn</h3>
                    <p>No waiting months for grass to grow. Beautiful lawn installed in hours.</p>
                </div>
                <div class="feature">
                    <h3>Premium Sod</h3>
                    <p>Fresh sod from local farms, installed within 24 hours of harvest.</p>
                </div>
                <div class="feature">
                    <h3>Expert Installation</h3>
                    <p>Licensed, insured contractors with years of experience.</p>
                </div>
                <div class="feature">
                    <h3>Transparent Pricing</h3>
                    <p>Upfront quotes with no hidden fees. Material, labor & delivery included.</p>
                </div>
            </div>
        </div>
    </section>

    <section id="locations" class="locations">
        <div class="container">
            <h2>Service Locations</h2>
            <p>Select your city for local pricing and scheduling:</p>
            <div class="state-grid">
                {state_links}
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2025 Sod.Company. Professional sod installation nationwide.</p>
        </div>
    </footer>
</body>
</html>'''

    with open(www_dir / 'index.html', 'w') as f:
        f.write(homepage)

    print("✅ Generated homepage")

def generate_sitemap():
    """Generate XML sitemap"""
    urls = ['https://sod.company/']

    for city_data in cities:
        city_slug = city_data['city'].lower().replace(' ', '-').replace('.', '')
        state_slug = city_data['state'].lower()
        urls.append(f"https://sod.company/{state_slug}/{city_slug}/")
        urls.append(f"https://sod.company/{state_slug}/{city_slug}/prices/")

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        sitemap += f'  <url><loc>{url}</loc></url>\n'

    sitemap += '</urlset>'

    with open(www_dir / 'sitemap.xml', 'w') as f:
        f.write(sitemap)

    print(f"✅ Generated sitemap with {len(urls)} URLs")

if __name__ == '__main__':
    print("=" * 50)
    print("Sod.Company Page Generator")
    print("=" * 50)

    # Generate all content
    generate_homepage()
    generate_city_pages()
    generate_sitemap()

    print("\n" + "=" * 50)
    print("COMPLETE!")
    print("=" * 50)
