# Voice Search Optimization Guide

## Voice Search Strategy for Sod.Company

Voice search queries are conversational and question-based. This guide ensures your pages rank for "Hey Google/Alexa/Siri" queries.

---

## Target Voice Queries by Intent

### Informational Queries

**"How much does sod cost?"**
- Target page: Pricing pages
- Featured snippet answer: "Sod installation typically costs $0.65 to $1.00 per square foot, including material, labor, and delivery. For a 5,000 sqft lawn, expect $3,250 to $5,000 total."

**"What's the best grass for [CITY]?"**
- Target page: City landing pages
- Featured snippet answer: "[PRIMARY_GRASS] is the most popular choice in [CITY] due to its excellent adaptation to local climate conditions."

**"How long does sod installation take?"**
- Target page: FAQ section
- Featured snippet answer: "Most residential sod installations take 4-6 hours. A typical 5,000 square foot lawn can be installed in a single day."

**"When is the best time to install sod?"**
- Target page: Blog/FAQ
- Featured snippet answer: "Sod can be installed year-round. Spring and fall offer ideal conditions, but summer and winter installations work well with proper watering."

**"How do I care for new sod?"**
- Target page: Blog/Care guide
- Featured snippet answer: "Water new sod twice daily for the first week, then gradually reduce to deep watering 2-3 times per week. Keep off the lawn for 2-3 weeks."

### Local Intent Queries

**"Sod installation near me"**
- Target page: City pages with schema
- Optimization: LocalBusiness schema, NAP consistency

**"Who installs sod in [CITY]?"**
- Target page: City landing pages
- Featured snippet answer: "Sod.Company provides professional sod installation in [CITY] and surrounding areas. Call [PHONE] for a free quote."

**"Sod companies in [CITY]"**
- Target page: City pages
- Optimization: Local keywords, reviews, citations

### Transactional Queries

**"How do I get a sod quote?"**
- Target page: Quote form
- Answer: "Visit Sod.Company, enter your city and lawn size, and receive an instant quote. No obligation, free estimate."

**"Can I get sod installed this week?"**
- Target page: City pages
- Answer: "Yes, Sod.Company offers same-week installation in most areas. Call [PHONE] to check availability."

---

## Schema Markup Implementation

### LocalBusiness Schema (All City Pages)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Sod.Company - [CITY]",
  "description": "Professional sod installation in [CITY], [STATE]",
  "url": "https://sod.company/[state]/[city]/",
  "telephone": "[PHONE]",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "[CITY]",
    "addressRegion": "[STATE]",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[LAT]",
    "longitude": "[LONG]"
  },
  "areaServed": {
    "@type": "City",
    "name": "[CITY]"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Sod Installation Services",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "Residential Sod Installation"
        }
      },
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "Commercial Sod Installation"
        }
      }
    ]
  }
}
```

### FAQ Schema (FAQ Sections)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How much does sod installation cost in [CITY]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sod installation in [CITY] typically costs [AVG_PRICE] per square foot installed, including material, labor, and delivery. For a 5,000 sqft lawn, expect $4,250 - $5,500 total."
      }
    },
    {
      "@type": "Question",
      "name": "What's the best grass for [CITY]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[PRIMARY_GRASS] is the most popular choice in [CITY] due to its excellent adaptation to local climate and soil conditions."
      }
    },
    {
      "@type": "Question",
      "name": "How long does sod installation take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Most residential sod installations in [CITY] are completed in one day. A typical 5,000 sqft lawn takes 4-6 hours to install with our professional crew."
      }
    }
  ]
}
```

### Service Schema (Pricing Pages)

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Sod Installation",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Sod.Company"
  },
  "areaServed": {
    "@type": "City",
    "name": "[CITY]"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Sod Types",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Product",
          "name": "St. Augustine Sod"
        },
        "price": "0.85",
        "priceCurrency": "USD",
        "unitText": "per square foot installed"
      }
    ]
  }
}
```

---

## Content Optimization for Voice

### Page Structure
1. **Use question headings (H2/H3)**
   - "How much does sod cost in [CITY]?"
   - "What's the best grass for [CITY]?"

2. **Answer immediately after heading**
   - First sentence = complete answer
   - Following sentences = additional detail

3. **Keep answers concise**
   - Featured snippets prefer 40-50 words
   - Be direct and factual

### Example Optimized Section

```html
<h2>How much does sod installation cost in Jacksonville?</h2>
<p>Sod installation in Jacksonville costs $0.85 per square foot on average,
including material, professional installation, and delivery. For a typical
5,000 sqft lawn, expect to pay between $4,250 and $5,500 total. St. Augustine
is the most popular grass choice in Jacksonville.</p>
```

---

## Voice Query Tracking

### Google Search Console
- Filter by query type: Questions
- Look for queries starting with: who, what, when, where, why, how

### Target Rankings
- Position 0 (Featured Snippet)
- Position 1-3 (Voice typically pulls from top 3)

### KPIs
- Featured snippet capture rate
- Voice query impressions
- Click-through from voice results

---

## Speakable Schema (Future Implementation)

When Google fully supports speakable:

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [
      ".voice-answer",
      ".key-info"
    ]
  }
}
```

---

## Local Voice Optimization Checklist

- [ ] Google Business Profile complete and verified
- [ ] NAP consistent across all citations
- [ ] LocalBusiness schema on all city pages
- [ ] FAQ schema on FAQ sections
- [ ] Reviews actively collected (aim for 50+ per location)
- [ ] Questions in H2/H3 headings
- [ ] Concise answers (40-50 words)
- [ ] Mobile page speed < 3s
- [ ] SSL certificate active
