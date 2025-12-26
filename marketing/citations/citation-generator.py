#!/usr/bin/env python3
"""
Local Citation Generator for Sod.Company
Generates consistent NAP (Name, Address, Phone) data for local directory submissions
"""

import json
from pathlib import Path

# Load cities data
script_dir = Path(__file__).parent
base_dir = script_dir.parent.parent
data_dir = base_dir / 'data'

with open(data_dir / 'cities.json') as f:
    cities_data = json.load(f)
    cities = cities_data['cities']

# Business info template
BUSINESS_INFO = {
    "business_name": "Sod.Company",
    "tagline": "Professional Sod Installation",
    "website": "https://sod.company",
    "email": "info@sod.company",
    "hours": "Mon-Fri: 7:00 AM - 6:00 PM, Sat: 8:00 AM - 4:00 PM, Sun: Closed",
    "year_established": "2024",
    "employees": "10-50",
    "categories": [
        "Landscaping",
        "Lawn Care",
        "Sod Installation",
        "Lawn Installation",
        "Landscaping Service",
        "Lawn Service"
    ],
    "payment_methods": [
        "Cash",
        "Check",
        "Credit Card",
        "Debit Card",
        "Financing Available"
    ],
    "services": [
        "Residential Sod Installation",
        "Commercial Sod Installation",
        "Sod Replacement",
        "Lawn Renovation",
        "Soil Preparation",
        "Sod Delivery"
    ],
    "description_short": "Professional sod installation with premium farm-fresh sod, expert installation, and 30-day warranty.",
    "description_long": "Sod.Company provides professional sod installation services for residential and commercial properties. We source premium, farm-fresh sod and install it the same day for a beautiful, instant lawn. Our services include soil preparation, professional installation, delivery, and a 30-day installation warranty. We serve customers across multiple states with transparent pricing and no hidden fees."
}

# Top citation sources
CITATION_SOURCES = [
    {"name": "Google Business Profile", "url": "https://business.google.com", "priority": 1},
    {"name": "Yelp", "url": "https://biz.yelp.com", "priority": 1},
    {"name": "Facebook", "url": "https://facebook.com/business", "priority": 1},
    {"name": "Apple Maps", "url": "https://mapsconnect.apple.com", "priority": 1},
    {"name": "Bing Places", "url": "https://bingplaces.com", "priority": 1},
    {"name": "Yellow Pages", "url": "https://yellowpages.com", "priority": 2},
    {"name": "Angi (Angie's List)", "url": "https://angi.com", "priority": 2},
    {"name": "HomeAdvisor", "url": "https://homeadvisor.com", "priority": 2},
    {"name": "Thumbtack", "url": "https://thumbtack.com", "priority": 2},
    {"name": "BBB", "url": "https://bbb.org", "priority": 2},
    {"name": "Nextdoor", "url": "https://business.nextdoor.com", "priority": 2},
    {"name": "Manta", "url": "https://manta.com", "priority": 3},
    {"name": "Foursquare", "url": "https://business.foursquare.com", "priority": 3},
    {"name": "MapQuest", "url": "https://mapquest.com", "priority": 3},
    {"name": "Superpages", "url": "https://superpages.com", "priority": 3},
    {"name": "Hotfrog", "url": "https://hotfrog.com", "priority": 3},
    {"name": "Brownbook", "url": "https://brownbook.net", "priority": 3},
    {"name": "Cylex", "url": "https://cylex.us.com", "priority": 3},
    {"name": "EZlocal", "url": "https://ezlocal.com", "priority": 3},
    {"name": "Local.com", "url": "https://local.com", "priority": 3},
    {"name": "MerchantCircle", "url": "https://merchantcircle.com", "priority": 3},
    {"name": "ShowMeLocal", "url": "https://showmelocal.com", "priority": 3},
    {"name": "CitySquares", "url": "https://citysquares.com", "priority": 3},
    {"name": "eLocal", "url": "https://elocal.com", "priority": 3},
    {"name": "Insider Pages", "url": "https://insiderpages.com", "priority": 3}
]


def generate_city_citation(city_data):
    """Generate citation data for a specific city"""
    city = city_data['city']
    state = city_data['state']
    state_full = city_data['state_full']
    phone = city_data['phone']
    zip_code = city_data.get('zip', '')

    city_slug = city.lower().replace(' ', '-').replace('.', '')
    state_slug = state.lower()

    citation = {
        "business_name": f"Sod.Company - {city}",
        "phone": phone,
        "website": f"https://sod.company/{state_slug}/{city_slug}/",
        "city": city,
        "state": state,
        "state_full": state_full,
        "zip": zip_code,
        "country": "United States",
        "categories": BUSINESS_INFO["categories"],
        "description": f"Professional sod installation in {city}, {state_full}. Premium farm-fresh sod, expert installation, and 30-day warranty. Free quotes available.",
        "hours": BUSINESS_INFO["hours"],
        "services": BUSINESS_INFO["services"],
        "payment_methods": BUSINESS_INFO["payment_methods"]
    }

    return citation


def generate_all_citations():
    """Generate citations for all cities"""
    citations = []

    for city_data in cities:
        citation = generate_city_citation(city_data)
        citations.append(citation)

    return citations


def export_citations_csv(citations, filename="citations.csv"):
    """Export citations to CSV format"""
    import csv

    output_path = script_dir / filename

    fieldnames = [
        "business_name", "phone", "website", "city", "state",
        "state_full", "zip", "country", "categories", "description",
        "hours", "services", "payment_methods"
    ]

    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for citation in citations:
            # Convert lists to strings for CSV
            row = citation.copy()
            row['categories'] = ', '.join(row['categories'])
            row['services'] = ', '.join(row['services'])
            row['payment_methods'] = ', '.join(row['payment_methods'])
            writer.writerow(row)

    print(f"Exported {len(citations)} citations to {output_path}")


def export_citations_json(citations, filename="citations.json"):
    """Export citations to JSON format"""
    output_path = script_dir / filename

    with open(output_path, 'w') as f:
        json.dump(citations, f, indent=2)

    print(f"Exported {len(citations)} citations to {output_path}")


def generate_submission_checklist():
    """Generate a checklist for citation submissions"""
    checklist = []

    checklist.append("# Citation Submission Checklist\n")
    checklist.append("Track your progress submitting to local directories.\n\n")

    for priority in [1, 2, 3]:
        priority_name = {1: "Priority 1 (Essential)", 2: "Priority 2 (Important)", 3: "Priority 3 (Supplemental)"}
        checklist.append(f"## {priority_name[priority]}\n\n")

        sources = [s for s in CITATION_SOURCES if s['priority'] == priority]
        for source in sources:
            checklist.append(f"- [ ] {source['name']} - {source['url']}\n")

        checklist.append("\n")

    checklist.append("## Submission Notes\n\n")
    checklist.append("- Ensure NAP (Name, Address, Phone) is EXACTLY consistent across all listings\n")
    checklist.append("- Use the same business name format everywhere\n")
    checklist.append("- Use the exact same phone number format\n")
    checklist.append("- Use the same website URL format (include or exclude www consistently)\n")
    checklist.append("- Upload the same logo/photos to all platforms\n")
    checklist.append("- Select the same categories where possible\n")
    checklist.append("- Keep hours of operation consistent\n")

    output_path = script_dir / "submission-checklist.md"
    with open(output_path, 'w') as f:
        f.writelines(checklist)

    print(f"Generated submission checklist at {output_path}")


def main():
    print("=" * 50)
    print("Sod.Company Citation Generator")
    print("=" * 50)

    # Generate all citations
    citations = generate_all_citations()
    print(f"\nGenerated {len(citations)} city citations")

    # Export to different formats
    export_citations_csv(citations)
    export_citations_json(citations)

    # Generate submission checklist
    generate_submission_checklist()

    print("\n" + "=" * 50)
    print("COMPLETE!")
    print("=" * 50)
    print("\nFiles generated:")
    print("  - citations.csv (for spreadsheet import)")
    print("  - citations.json (for programmatic use)")
    print("  - submission-checklist.md (tracking)")


if __name__ == '__main__':
    main()
