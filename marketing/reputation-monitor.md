# Reputation Monitoring & Issue Prevention System

## The Goal
Catch problems BEFORE they become bad reviews. One prevented bad review is worth 10 good ones.

---

## Issue Triggers That Lead to Bad Reviews

### Pre-Installation
| Trigger | Monitor | Alert Threshold |
|---------|---------|-----------------|
| Slow quote response | Time to first contact | > 2 hours |
| No follow-up | Lead not contacted | > 24 hours |
| Pricing confusion | Customer questions after quote | 2+ clarification requests |
| Scheduling delays | Days from booking to install | > 7 days |
| Poor communication | Missed calls/texts | 2+ unanswered |

### Installation Day
| Trigger | Monitor | Alert Threshold |
|---------|---------|-----------------|
| Crew late | Arrival vs scheduled time | > 30 min late |
| Crew no-show | No check-in by start time | 15 min past start |
| Sod quality | Crew inspection report | Any brown/dry pallets |
| Property damage | Crew incident report | Any damage |
| Customer complaint | Real-time feedback | Any negative |
| Job incomplete | End-of-day checklist | Missing items |

### Post-Installation
| Trigger | Monitor | Alert Threshold |
|---------|---------|-----------------|
| Sod not rooting | Day 7/14 check-in | Customer concern |
| Watering issues | Care guide questions | 3+ questions |
| Brown spots | Customer photo/report | Any report |
| Warranty claim | Support request | Any claim |
| No review request response | Email/SMS tracking | No response by Day 10 |
| Payment dispute | Billing system | Any dispute |

---

## Automated Monitoring System

### 1. Lead Response Monitor
```
CHECK every 30 minutes:
  - New leads with no response > 2 hours → ALERT owner
  - Leads with no follow-up > 24 hours → ESCALATE
  - Track: Average response time (goal: < 30 min)
```

### 2. Installation Day Tracker
```
MORNING of install:
  - Auto-text customer: "Crew arriving between X-Y today"
  - Crew check-in required via app/text

IF crew not checked in by start time:
  - Alert owner immediately
  - Auto-text customer: "Running slightly behind, ETA update coming"

END of day:
  - Crew submits completion photo + checklist
  - Auto-text customer: "How did today go? Reply 1-5"
  - If response < 4 → IMMEDIATE owner alert
```

### 3. Post-Install Health Check
```
DAY 3: Auto-text
  "How's your new lawn looking? Any concerns?"
  - Positive → Queue for review request
  - Concern → Alert owner, pause review request

DAY 7: Auto-text
  "Quick check-in - lawn rooting well?"
  - Positive → Send review request
  - Concern → Schedule callback, pause review request

DAY 14: Final check
  "Everything still looking good?"
  - Positive → Second review request if none given
  - Concern → Warranty evaluation
```

---

## Early Warning Indicators

### Conversation Sentiment Analysis
Monitor all customer communications for:
- Frustrated language ("still waiting", "no one called", "this is ridiculous")
- Confusion signals ("I don't understand", "that's not what I was told")
- Urgency ("need this fixed", "unacceptable", "want a refund")

**Action:** Flag for immediate owner review

### Pattern Detection
Track across all jobs:
- Same crew getting multiple complaints → Crew training/removal
- Same grass type having issues → Supplier problem
- Same city having issues → Local conditions/installer
- Same time period issues → Weather/seasonal factors

**Weekly Report:** Issue trends by category

---

## Issue Escalation Workflow

### Level 1: Minor Concern
- Customer asks question or expresses mild concern
- **Response:** Same-day callback, address issue
- **Goal:** Resolve in 24 hours

### Level 2: Moderate Issue
- Customer unhappy but not angry
- Sod has minor problems (small brown spot)
- **Response:** Owner calls within 2 hours
- **Action:** Offer partial remedy (free touch-up, discount)
- **Goal:** Resolve in 48 hours

### Level 3: Major Problem
- Customer angry
- Significant sod failure (large dead areas)
- Property damage
- **Response:** Owner calls within 1 hour
- **Action:** Full replacement or refund offer
- **Goal:** Resolve same day, document everything

### Level 4: Crisis
- Customer threatens legal action or public complaint
- Social media post or review site complaint
- **Response:** Owner calls immediately
- **Action:** Whatever it takes to resolve
- **Goal:** Prevent public damage, document for legal

---

## Customer Satisfaction Checkpoints

### SMS Pulse Checks (Automated)

**Post-Quote (2 hours after):**
```
"Thanks for requesting a quote! Any questions about pricing
or next steps? Reply anytime - we're here to help."
```

**Pre-Installation (Day before):**
```
"Your sod installation is tomorrow! Crew arrives between
[TIME]. Any last questions? We're excited to transform
your lawn!"
```

**Post-Installation (Same evening):**
```
"Your new lawn is in! On a scale of 1-5, how was your
experience today? Reply with a number."

1-3 → Immediate alert, owner calls
4 → "Thanks! Anything we could improve?"
5 → "Awesome! We'd love a Google review: [LINK]"
```

**Day 3:**
```
"How's your new lawn looking? Watering going ok?
Reply with any questions!"
```

**Day 7:**
```
"One week check-in! How's everything rooting?
Any concerns before we close out your job?"
```

---

## Review Interception Strategy

### Before They Post Negative
1. **Catch unhappy customers via pulse checks**
2. **Call immediately when concern detected**
3. **Resolve issue completely**
4. **Only THEN ask for review**

### Script for Unhappy Customer Call
```
"Hi [NAME], this is [OWNER] from Sod.Company. I saw your
feedback and wanted to personally reach out. I'm sorry
you're not 100% happy - that's not acceptable to me.

Can you tell me what's going on so I can make this right?"

[LISTEN - don't interrupt]

"I completely understand. Here's what I'm going to do..."

[OFFER SOLUTION - be generous]

"Does that work for you? I want you to love your lawn."
```

---

## Monitoring Dashboard Metrics

### Daily Check
- [ ] New leads response time (all < 2 hours?)
- [ ] Today's installations - crews checked in?
- [ ] Yesterday's pulse check responses (any < 4?)
- [ ] Open issues count

### Weekly Review
- [ ] Average response time trend
- [ ] Customer satisfaction average (pulse checks)
- [ ] Issues by category (crew, sod quality, communication)
- [ ] Repeat issues (patterns emerging?)
- [ ] Review requests sent vs reviews received

### Monthly Analysis
- [ ] Net Promoter Score trend
- [ ] Issue resolution time trend
- [ ] Bad review prevention count (issues caught)
- [ ] Crew performance comparison
- [ ] Seasonal issue patterns

---

## Technology Stack Options

### Simple (Start Here)
- Google Forms for crew check-ins
- SMS automation via Twilio or SimpleTexting
- Google Sheets for tracking
- Manual review of alerts

### Intermediate
- CRM with automation (HubSpot, Jobber)
- Dedicated SMS platform (Podium, Birdeye)
- Automated sentiment detection

### Advanced
- Custom dashboard
- AI sentiment analysis on all communications
- Predictive issue detection
- Automated escalation workflows

---

## Quick Reference: When to Act

| Signal | Action | Timeframe |
|--------|--------|-----------|
| Lead no response | Call immediately | < 2 hours |
| Crew running late | Text customer + alert owner | Immediately |
| Pulse check < 4 | Owner calls customer | < 1 hour |
| Customer "concern" text | Callback scheduled | < 4 hours |
| Sod quality issue reported | Site visit + resolution | < 24 hours |
| Angry customer | Owner personal call | < 1 hour |
| Social media complaint | Owner response + call | < 30 min |

---

## The Bottom Line

**Every unhappy customer is a potential bad review.**

**Every bad review avoided = 20+ leads saved.**

Invest 10 minutes preventing an issue rather than 10 hours recovering from a bad review.
