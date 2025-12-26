# Deploy to HostGator + Cloudflare

## Quick Start (2-3 hours)

### Step 1: Cloudflare Setup (15 min)

1. **Sign up**: https://cloudflare.com (free)
2. **Add site**: sod.company
3. **Copy nameservers** (e.g., `chloe.ns.cloudflare.com`)
4. **Update at your registrar**: Replace existing nameservers
5. **Configure**:
   - SSL/TLS → Full mode
   - Always Use HTTPS → On

### Step 2: HostGator Setup (15 min)

1. **Login to cPanel**: https://your-server.hostgator.com:2083
2. **Addon Domains** → Add `sod.company`
3. **FTP Accounts** → Create account for uploads

### Step 3: Upload Files (30 min)

Using FileZilla (free: https://filezilla-project.org):

```
Host: ftp.sod.company (or your IP)
Username: your-ftp-user
Password: your-ftp-password
Port: 21
```

**Upload** contents of `www/sod.company/` to `/public_html/sod.company/`

### Step 4: DNS in Cloudflare (10 min)

Add these records:

| Type | Name | Value | Proxy |
|------|------|-------|-------|
| A | @ | YOUR_HOSTGATOR_IP | Proxied |
| CNAME | www | sod.company | Proxied |

Find HostGator IP in cPanel or ping your server.

### Step 5: Create .htaccess (5 min)

In `/public_html/sod.company/` create `.htaccess`:

```apache
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

RewriteCond %{HTTP_HOST} ^www\.(.*)$ [NC]
RewriteRule ^(.*)$ https://%1/$1 [R=301,L]

DirectoryIndex index.html index.php
Options -Indexes

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript
</IfModule>
```

### Step 6: Test Site (10 min)

- ✅ https://sod.company (homepage)
- ✅ https://sod.company/fl/jacksonville/ (city page)
- ✅ https://sod.company/fl/jacksonville/prices/ (pricing)
- ✅ Form submission works
- ✅ Mobile responsive

### Step 7: Update Email (5 min)

Edit `contact-handler.php`:
- Change `leads@sod.company` to YOUR email

### Step 8: Add Google Analytics (10 min)

1. Get GA4 ID from analytics.google.com
2. Add to all pages in `<head>`:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Step 9: Submit to Google (10 min)

1. https://search.google.com/search-console
2. Add property: sod.company
3. Verify via DNS (TXT record in Cloudflare)
4. Submit sitemap: https://sod.company/sitemap.xml

---

## What You Have

- 40 cities with pricing pages (80 total pages)
- Homepage with all city links
- AI Chatbot (auto-engages visitors)
- Contact form with email notification
- Sitemap for SEO
- Mobile responsive design

---

## Quick Checklist

- [ ] Cloudflare nameservers updated
- [ ] DNS propagated (check: https://dnschecker.org)
- [ ] Files uploaded to HostGator
- [ ] .htaccess created
- [ ] Site loads with HTTPS
- [ ] Forms working
- [ ] Email receiving leads
- [ ] Google Analytics added
- [ ] Search Console submitted

---

## Expected Results

**Week 1**: Site live, first leads
**Month 1**: 3-5 leads/day ($270-$450/day)
**Month 3**: 10+ leads/day ($900+/day)

Total monthly revenue potential: **$10,000-$30,000**

---

## File Structure

```
www/sod.company/
├── index.html          (homepage)
├── sitemap.xml         (for Google)
├── contact-handler.php (form handler)
├── css/
│   ├── main.css
│   └── pricing.css
├── js/
│   ├── main.js
│   └── chatbot.js
├── fl/                 (Florida cities)
│   ├── jacksonville/
│   │   ├── index.html
│   │   └── prices/index.html
│   ├── tampa/
│   ├── orlando/
│   └── ...
├── tx/                 (Texas cities)
├── az/                 (Arizona cities)
└── ...
```

---

## Need Help?

1. **DNS not working**: Wait 24 hours, check https://dnschecker.org
2. **SSL error**: Set Cloudflare to "Full" (not Flexible)
3. **Forms not sending**: Check email in contact-handler.php
4. **Pages 404**: Check .htaccess and file permissions (755/644)

---

**You're ready to go live! 🚀**
