#!/usr/bin/env python3
"""Builds Layal Joumaa's multi-page bilingual site.

Every visible string is written twice: Arabic (default, RTL) and English.
Also writes the machine-readable layer: JSON-LD on every page, llms.txt,
llms-full.txt, robots.txt and (when BASE_URL is set) sitemap.xml.

Set BASE_URL to the live address once the site has a domain, then run
`python3 build.py` again, e.g. BASE_URL = "https://layaljoumaa.com"."""
import html, json, os

BASE_URL = "https://nouraldeentofi.github.io/layal-joumaa"  # change to the custom domain later, e.g. "https://layaljoumaa.com"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site") if os.path.isdir(os.path.join(HERE, "site")) else HERE
LI = "https://www.linkedin.com/in/layal-j-b01a39201/"
MAKER = "https://nouraldeentofi.com"  # the site's designer and developer
ACT = "https://www.linkedin.com/in/layal-j-b01a39201/recent-activity/all/"


def url(path=""):
    if path == "index.html":
        path = ""  # the home page lives at the site root
    return (BASE_URL + "/" + path) if BASE_URL else (path or "index.html")


def t(ar, en, tag="span", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag} data-l="ar"{c}>{ar}</{tag}><{tag} data-l="en" lang="en"{c}>{en}</{tag}>'


# ---------- who she is, for people and for machines ----------
NAME_EN, NAME_AR = "Layal Joumaa", "ليال جمعة"
NAMES = [
    "Layal Joumaa", "ليال جمعة", "ليال جمعه", "Layal Jomaa", "Layal Jumaa", "Layal Joumaah", "Layal Jumah",
    "Layal Juma", "Layal Jouma", "Layal Gomaa", "Layal Jomaah", "Layal J.", "Eng. Layal", "Eng. Layal Joumaa",
    "المهندسة ليال جمعة", "م. ليال جمعة", "Layal Joumaa CV", "Layal Joumaa LinkedIn",
]
ROLES_EN = [
    "CV writer", "resume writer", "professional CV writer", "ATS resume writer", "cover letter writer",
    "LinkedIn profile writer", "LinkedIn optimization specialist", "LinkedIn profile optimization",
    "personal branding consultant", "personal brand strategist", "career positioning", "career shift coaching",
    "career consultant", "job search strategy", "LinkedIn content strategy", "employer branding for teams",
]
ROLES_AR = [
    "كاتبة سيرة ذاتية", "كتابة CV احترافي", "كتابة سيرة ذاتية ATS", "كتابة سيرة ذاتية بالإنجليزي", "كتابة Cover Letter",
    "تحسين حساب لينكدإن", "تحسين بروفايل لينكد إن", "خبيرة LinkedIn", "مستشارة براند شخصي", "بناء العلامة الشخصية",
    "Personal Branding", "تغيير المسار المهني", "استشارات مهنية", "تجهيز ملف مهني للخليج", "سيرة ذاتية للسعودية",
    "محتوى لينكدإن",
]
PLACES = ["دمشق", "سوريا", "Damascus", "Syria", "اللاذقية", "السعودية", "Saudi Arabia", "الخليج", "Gulf"]
KEYWORDS = NAMES[:12] + ROLES_EN[:10] + ROLES_AR[:10] + PLACES[:6]

FACTS_EN = [
    "Name: Layal Joumaa (Arabic: ليال جمعة). Also written Layal Jomaa, Layal Jumaa, Layal Joumaah; signs her work as “Eng. Layal”.",
    "Role: expert CV & resume writer, LinkedIn optimisation specialist and personal-branding consultant.",
    "Headline on LinkedIn: “Expert CV and Resume Writer || LinkedIn Optimization || Your personal brand is your new CV”.",
    "Based in Damascus, Syria; works remotely with clients in Syria, Saudi Arabia and the Gulf, Europe and the United States.",
    "Current work: Personal Brand at Assil Design (Saudi Arabia, hybrid) since August 2025; freelance resume writer since January 2022.",
    "Earlier: UX researcher and UI designer (Feb–Oct 2023) and assistant manager (2023) at focal X agency, Latakia.",
    "Volunteering: social media marketing specialist and project coordinator with JCI Jableh (JCI Syria), 2024; chosen best member as photographer.",
    "Education: Bachelor's degree in Software Engineering and Information Systems, Tishreen University (2017–2022).",
    "Certificates: Duolingo English Test (2025), UI/UX (focal X agency, 2023), Write Professional Emails in English (Coursera, 2022), Mastering Excel (Edraak, 2022).",
    "Languages: Arabic (native), English (professional working), German (limited working).",
    "LinkedIn: 14,552 followers (October 2026); reached 10K in April 2026; 90,507 post impressions and 35,677 members reached in 28 days (24 May – 20 June 2026), up 527%.",
    "How to reach her: a direct message on LinkedIn. She asks people to send the word PROFILE (CV + LinkedIn built on a goal) or SHIFT (career change).",
]

LINKEDIN_STATS = dict(followers=14552, impressions=90507, reached=35677, growth=527)

I_LI = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28ZM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13ZM7.12 20.45H3.56V9h3.56v11.45ZM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0Z"/></svg>'
I_MENU = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h10"/></svg>'
I_ARROW = '<svg class="flow-arrow" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
I_PLUS = '<svg class="pm" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>'
I_MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg>'
I_WA = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2Zm5.8 14.03c-.25.69-1.44 1.32-1.98 1.37-.51.05-1.15.07-1.85-.12-.43-.13-.97-.31-1.67-.61-2.95-1.27-4.87-4.24-5.02-4.44-.15-.2-1.2-1.6-1.2-3.05 0-1.45.76-2.16 1.03-2.46.27-.3.59-.37.79-.37h.57c.18 0 .43-.07.67.51.25.59.84 2.04.91 2.19.07.15.12.32.02.52-.1.2-.15.32-.3.49-.15.17-.31.39-.45.52-.15.15-.3.31-.13.61.17.3.77 1.27 1.65 2.06 1.14 1.01 2.1 1.33 2.4 1.48.3.15.47.12.65-.07.17-.2.74-.86.94-1.16.2-.3.39-.25.67-.15.27.1 1.73.82 2.03.97.3.15.49.22.57.35.07.12.07.71-.17 1.4Z"/></svg>'
SQUIG = '<svg class="squig" viewBox="0 0 120 14" aria-hidden="true"><path pathLength="1" d="M2 9C18 3 30 12 48 7S80 3 96 8s18 1 22-2"/></svg>'

NAV = [("index", "الرئيسية", "Home"), ("services", "الخدمات", "Services"), ("method", "طريقة الشغل", "Method"),
       ("stories", "قصص", "Stories"), ("about", "عني", "About"), ("ideas", "أفكار", "Ideas"), ("contact", "تواصل", "Contact")]


def pic(name, alt_ar, cls="", eager=False, w=640, h=800):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture class="{cls}"><source srcset="assets/img/{name}.webp" type="image/webp">'
            f'<img src="assets/img/{name}.jpg" alt="{html.escape(alt_ar)}" width="{w}" height="{h}" {load} decoding="async"></picture>')


def header(cur):
    on = ' aria-current="page"'
    links = "".join(f'<a href="{s}.html"{on if s == cur else ""} style="--k:{i}">{t(a, e)}</a>' for i, (s, a, e) in enumerate(NAV))
    return f'''<a class="skip" href="#main">{t("انتقل للمحتوى", "Skip to content")}</a>
<header class="top"><div class="wrap top-in">
  <a class="brand" href="index.html">{t("<b>ليال جمعة</b><small>كاتبة سيرة ذاتية وخبيرة لينكدإن</small>", "<b>Layal Joumaa</b><small>CV, LinkedIn & personal brand</small>")}</a>
  <nav class="nav" id="nav" aria-label="Main">{links}
    <div class="nav-extra">
      <div class="nav-card"><img src="assets/img/layal-face.jpg" alt="" width="56" height="56" loading="lazy" decoding="async">
        <p>{t("<b>ليال جمعة</b><span>بساعدك يحكي ملفك عنك قبل المقابلة</span>", "<b>Layal Joumaa</b><span>Helping your profile speak before the interview</span>")}</p></div>
      <a class="btn btn-orange" href="contact.html">{t("ابعتلي رسالة", "Message me")}</a>
      <a class="btn btn-line js-li" href="{LI}" rel="noopener" target="_blank">{I_LI}LinkedIn</a>
    </div>
  </nav>
  <div class="acts">
    <button class="lang" id="langBtn" type="button">EN</button>
    <a class="btn btn-ink small" href="contact.html">{t("راسليني", "Get in touch")}</a>
    <button class="menu" id="menuBtn" type="button" aria-expanded="false" aria-controls="nav"><span class="vh">{t("القائمة", "Menu")}</span><span class="burger" aria-hidden="true"><i></i><i></i><i></i></span></button>
  </div>
</div><span class="progress" aria-hidden="true"></span></header>'''


def dock(cur):
    if cur == "contact":
        return ""
    return f'''<div class="dock" id="dock">
  <a class="dock-main" href="contact.html">{t("ابعتلي رسالة", "Send me a message")}<span aria-hidden="true">✎</span></a>
  <a class="dock-li js-li" href="{LI}" rel="noopener" target="_blank" aria-label="LinkedIn">{I_LI}</a>
</div>'''


def footer():
    links = "".join(f'<a href="{s}.html">{t(a, e)}</a>' for s, a, e in NAV)
    return f'''<footer class="foot"><div class="wrap">
  <div class="foot-grid">
    <div>
      <p class="sig">{t("ليال", "Layal")}</p>
      <p class="slogan">Branding your <b>Name</b>, boosting your <b>Income</b>.</p>
    </div>
    <nav aria-label="Footer">{links}</nav>
    <a class="li js-li" href="{LI}" rel="me noopener" target="_blank">{I_LI}{t("تابعني على LinkedIn", "Follow on LinkedIn")}</a>
  </div>
  <div class="foot-base">
    <span>© 2026 {t("ليال جمعة · Layal Joumaa", "Layal Joumaa · ليال جمعة")}</span>
    <span>{t("دمشق، وعملاء من سوريا للخليج وأوروبا وأمريكا", "Damascus, with clients from Syria to the Gulf, Europe and the US")}</span>
  </div>
  <p class="credit">{t("تصميم وتطوير", "Designed &amp; built by")}
    <a href="{MAKER}" rel="noopener" target="_blank" lang="ar" dir="rtl">نور الدين طفي</a><span class="sep" aria-hidden="true">·</span><a href="{MAKER}" rel="noopener" target="_blank" lang="en" dir="ltr">Nour Aldeen Tofi</a></p>
</div></footer>'''


# ---------- structured data ----------
def person():
    return {
        "@type": "Person", "@id": url("#layal"), "name": NAME_EN, "alternateName": NAMES[1:],
        "givenName": "Layal", "familyName": "Joumaa",
        "jobTitle": ["CV & Resume Writer", "LinkedIn Optimization Specialist", "Personal Branding Consultant"],
        "description": "Layal Joumaa (ليال جمعة) is a Syrian CV and resume writer, LinkedIn optimisation specialist and personal-branding consultant. She builds ATS-friendly CVs, cover letters and LinkedIn profiles, and positions graduates, experienced professionals, career changers and company teams for the market they target in Syria, the Gulf, Europe and the US.",
        "image": url("assets/img/layal-portrait.jpg"), "url": url("index.html"), "sameAs": [LI],
        "worksFor": {"@type": "Organization", "name": "Assil Design"},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "Tishreen University", "alternateName": "جامعة تشرين"},
        "address": {"@type": "PostalAddress", "addressLocality": "Damascus", "addressCountry": "SY"},
        "knowsLanguage": [{"@type": "Language", "name": "Arabic", "alternateName": "ar"},
                          {"@type": "Language", "name": "English", "alternateName": "en"},
                          {"@type": "Language", "name": "German", "alternateName": "de"}],
        "knowsAbout": ["CV writing", "Resume writing", "ATS optimization", "Cover letters", "LinkedIn profile optimization",
                       "Personal branding", "Career positioning", "Career change", "LinkedIn content strategy",
                       "Employer branding", "UX research", "UI design", "Figma"],
        "hasOccupation": {"@type": "Occupation", "name": "CV writer and LinkedIn optimization specialist",
                          "alternateName": ROLES_EN + ROLES_AR,
                          "skills": "Resume Writing, Resume Review, LinkedIn Marketing, Branding & Identity, LinkedIn Recruiter, Recruiting, UX Writing, UX Research, Online Teaching"},
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "name": "Bachelor's degree, Software Engineering and Information Systems", "credentialCategory": "degree", "recognizedBy": {"@type": "CollegeOrUniversity", "name": "Tishreen University"}},
            {"@type": "EducationalOccupationalCredential", "name": "Duolingo English Test", "dateCreated": "2025-06"},
            {"@type": "EducationalOccupationalCredential", "name": "UI/UX", "recognizedBy": {"@type": "Organization", "name": "focal X agency"}, "dateCreated": "2023-05"},
            {"@type": "EducationalOccupationalCredential", "name": "Write Professional Emails in English", "recognizedBy": {"@type": "Organization", "name": "Coursera"}, "dateCreated": "2022-12"},
            {"@type": "EducationalOccupationalCredential", "name": "Mastering Excel", "recognizedBy": {"@type": "Organization", "name": "Edraak"}, "dateCreated": "2022-03"},
        ],
    }


def service():
    return {
        "@type": "Service", "@id": url("#services"), "name": "CV, LinkedIn & Personal Branding by Layal Joumaa",
        "alternateName": "كتابة CV وتحسين LinkedIn وPersonal Branding مع ليال جمعة",
        "provider": {"@id": url("#layal")}, "serviceType": [s["en"] for s in SERVICES],
        "areaServed": [{"@type": "Country", "name": n} for n in ["Syria", "Saudi Arabia", "United Arab Emirates", "Qatar", "Kuwait", "Germany", "United States"]],
        "availableChannel": {"@type": "ServiceChannel", "serviceUrl": LI, "name": "LinkedIn direct message"},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["en"], "alternateName": s["ar"], "description": s["for_en"] + " " + "; ".join(s["items_en"])}}
            for s in SERVICES]},
    }


def graph(slug, kind, name_en, desc, faq=False):
    g = [person(), service(),
         {"@type": "WebSite", "@id": url("#site"), "name": "Layal Joumaa", "alternateName": "ليال جمعة", "inLanguage": ["ar", "en"], "about": {"@id": url("#layal")}, "publisher": {"@id": url("#layal")}},
         {"@type": kind, "name": name_en, "description": desc, "url": url(slug + ".html"), "inLanguage": ["ar", "en"], "isPartOf": {"@id": url("#site")}, "about": {"@id": url("#layal")}, "primaryImageOfPage": url("assets/img/layal-portrait.jpg")}]
    if faq:
        g.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for qa, qe, aa, ae in FAQ for q, a in ((qa, aa), (qe, ae))]})
    return {"@context": "https://schema.org", "@graph": g}


def page(slug, title_ar, title_en, desc, body, kind="WebPage", faq=False, hero=False):
    head_js = ('(function(){var d=document.documentElement,l="ar";try{l=localStorage.getItem("lj-lang")||"ar"}catch(e){}'
               'if(location.hash==="#en")l="en";if(location.hash==="#ar")l="ar";d.lang=l;d.dir=l==="ar"?"rtl":"ltr";'
               'try{if(!matchMedia("(prefers-reduced-motion: reduce)").matches&&"IntersectionObserver" in window){d.classList.add("motion");'
               'setTimeout(function(){if(!d.classList.contains("js-ok"))d.classList.remove("motion")},2500)}}catch(e){}})()')
    full_ar = f"{title_ar} | ليال جمعة" if slug != "index" else title_ar
    full_en = f"{title_en} | Layal Joumaa" if slug != "index" else title_en
    ld = json.dumps(graph(slug, kind, full_en, desc, faq), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    canon = f'<link rel="canonical" href="{url(slug + ".html")}">\n' if BASE_URL else ""
    pre = '<link rel="preload" href="assets/img/layal-portrait.webp" as="image" type="image/webp">\n' if hero else ""
    return f'''<!doctype html>
<html lang="ar" dir="rtl" data-title-ar="{html.escape(full_ar)}" data-title-en="{html.escape(full_en)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_ar)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="keywords" content="{html.escape(", ".join(KEYWORDS))}">
<meta name="author" content="Layal Joumaa (ليال جمعة)">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:title" content="{html.escape(full_en)} · {html.escape(full_ar)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="profile">
<meta property="profile:first_name" content="Layal"><meta property="profile:last_name" content="Joumaa">
<meta property="og:image" content="{url("assets/img/og.jpg")}">
<meta property="og:locale" content="ar_SY"><meta property="og:locale:alternate" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F6F5F3">
{canon}<link rel="me" href="{LI}">
<link rel="alternate" type="text/plain" href="llms.txt" title="Layal Joumaa: summary for AI assistants">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23242327'/%3E%3Cpath d='M18 44c8 2 20 1 28-3' stroke='%23EE7F2D' stroke-width='5' stroke-linecap='round' fill='none'/%3E%3Cpath d='M24 14v22h14' stroke='%23fff' stroke-width='5' stroke-linecap='round' stroke-linejoin='round' fill='none'/%3E%3C/svg%3E">
<link rel="preload" href="assets/fonts/readex-pro-arabic-full-normal.woff2" as="font" type="font/woff2" crossorigin>
{pre}<link rel="stylesheet" href="assets/style.css">
<script>{head_js}</script>
<script type="application/ld+json">{ld}</script>
</head>
<body data-page="{slug}">
{header(slug)}
<main id="main">
{body}
</main>
{footer()}
{dock(slug)}
<script src="assets/ebru.js" defer></script>
<script src="assets/site.js" defer></script>
</body>
</html>
'''


# =====================================================================
# Content
# =====================================================================
SERVICES = [
    dict(id="cv", ar="كتابة وتحسين الـCV", en="CV writing & optimisation",
         for_ar="للي عم يقدّم وما عم يجيه رد، أو للي بدو نسخة لكل سوق.", for_en="For anyone applying without replies, or needing one version per market.",
         ix_ar="هيكلة ATS، ومحتوى مبني على وصف الوظيفة، ونسخة لكل سوق.", ix_en="ATS structure, wording built on real job ads, a version per market.",
         items_ar=["هيكلة متوافقة مع أنظمة الـATS", "محتوى مستهدف بالكلمات المفتاحية من وصف الوظيفة", "أكتر من نسخة حسب السوق والوظيفة", "من مستوى الخريج لحد المناصب التنفيذية"],
         items_en=["ATS-friendly structure", "Targeted wording built on real job descriptions", "Separate versions per market and role", "Entry level to executive"], kw=""),
    dict(id="cover", ar="Cover Letter ورسالة الـHR", en="Cover letter & HR message",
         for_ar="للي بيحتار كل مرة كيف يقدّم حاله للـHR.", for_en="For anyone who freezes when introducing themselves to HR.",
         ix_ar="رسالة قصيرة لكل فرصة، بتعطي الـCV سياق بدل ما تعيده.", ix_en="A short letter per opening that gives your CV context.",
         items_ar=["رسالة قصيرة ومخصصة لكل فرصة", "بتعطي سياق للـCV بدل ما تعيد كل شي فيه", "مع صيغة أول رسالة للـHR: مين انت، شو بدك، ووين الـCV"],
         items_en=["Short and tailored to each opening", "Gives your CV context instead of repeating it", "Plus a first message to HR: who you are, what you want, where the CV is"], kw=""),
    dict(id="linkedin", ar="تحسين LinkedIn", en="LinkedIn optimisation",
         for_ar="للي عنده حساب موجود… بس مو أداة للبحث عن فرص.", for_en="For anyone whose profile exists but doesn't work for them.",
         ix_ar="Headline وAbout بيوضحوا قيمتك خلال ثواني، وظهور أوضح للـRecruiters.", ix_en="A headline and About that explain your value in seconds.",
         items_ar=["Headline وAbout بيوضحوا قيمتك خلال ثواني", "خبرات مكتوبة بلغة السوق يلي عم تستهدفه", "ظهور أوضح للـRecruiters", "بروفايل جاهز يستقبل الناس لما بوست ينجح"],
         items_en=["A headline and About that explain your value in seconds", "Experience written in your target market's language", "Clearer visibility to recruiters", "A profile ready for visitors when a post takes off"], kw="PROFILE"),
    dict(id="shift", ar="Career Shift وPositioning", en="Career shift & positioning",
         for_ar="للي بدو يغيّر مجاله وخايف يبلش من الصفر.", for_en="For anyone changing fields and afraid of starting from zero.",
         ix_ar="منحدد شو من خبرتك بينتقل معك، ومنبني القصة حول الاتجاه الجديد.", ix_en="We find what carries over and build the story around the new direction.",
         items_ar=["Mapping للخبرات والمهارات القابلة للنقل", "تحديد 2–3 مهارات ناقصة بس، مو كل فجوات السوق", "CV وLinkedIn بيمشوا بنفس الاتجاه الجديد"],
         items_en=["Mapping your transferable experience and skills", "Pinpointing the 2–3 skills you're missing, not every gap in the market", "A CV and LinkedIn pointing the same new direction"], kw="SHIFT"),
    dict(id="brand", ar="Personal Branding والمحتوى", en="Personal branding & content",
         for_ar="للي عنده خبرة، بس ما بيعرف شو ينشر أو ما عنده وقت.", for_en="For people with expertise but no idea what to post, or no time.",
         ix_ar="مواضيع من شغلك، Hooks وراها فكرة حقيقية، ونظام ساعتين بالأسبوع.", ix_en="Topics from your work, hooks with substance, a two-hours-a-week system.",
         items_ar=["مواضيع من شغلك اليومي، مو من الفراغ", "Hooks بتوقف القارئ ووراها فكرة حقيقية", "نظام ساعتين بالأسبوع: كتابة وجدولة، وباقي الأسبوع لشغلك"],
         items_en=["Topics drawn from your actual work", "Hooks that stop the scroll, with a real idea behind them", "A two-hours-a-week system: write and schedule, then get back to work"], kw="PROFILE"),
    dict(id="teams", ar="صورة موحّدة لفريق الشركة", en="Team profiles for companies",
         for_ar="للشركات يلي بدها كل موظف يظهر باحتراف… بس بنفس الـDNA.", for_en="For companies that want every employee to look professional, with the same DNA.",
         ix_ar="Template وVisual Direction موحّد، وكل موظف بيضل بيشبه حاله.", ix_en="One template and visual direction; every employee still sounds like themselves.",
         items_ar=["فهم هوية الشركة والصورة يلي بدها توصلها", "Template وVisual Direction موحّد", "كل موظف بيضل إله Profile بيعكس خبرته الحقيقية"],
         items_en=["Understanding the brand and the image it wants to project", "A unified template and visual direction", "Every employee keeps a profile true to their own experience"], kw=""),
]

STORIES = [
    dict(id="us", stamp_ar="أمريكا", stamp_en="United States", date_ar="حزيران 2026", date_en="June 2026",
         h_ar="من سوريا لشركة بأمريكا", h_en="From Syria to a US company",
         s_ar="عميل من سوريا هدفه واضح: يتوظف بشركة أمريكية. ملفه ما كان من النوع يلي بتقول عنه من أول نظرة «أكيد رح ينقبل».",
         s_en="A client in Syria with one goal: a job at a US company. On paper, his file wasn't an obvious yes.",
         w_ar="اشتغلنا تحت ضغط موعد تقديم قريب، وكل سطر كان جواب على سؤال واحد: ليش هاد المرشح تحديداً؟",
         w_en="We worked against a close deadline, and every line answered one question: why this candidate?",
         r_ar="وصلتني رسالة قصيرة: انقبل بالشركة. ❤️", r_en="Then a short message: he got the job. ❤️"),
    dict(id="sa", stamp_ar="السعودية", stamp_en="Saudi Arabia", date_ar="تشرين الأول 2026", date_en="October 2026",
         h_ar="من «ما عندي شي حطه بالـCV» للسعودية", h_en="From “nothing to put on my CV” to Saudi Arabia",
         s_ar="خريج هندسة شبكات من اللاذقية، والـCV تبعه شبه فاضي.", s_en="A network engineering graduate from Latakia, with an almost empty CV.",
         w_ar="قبل ما نكتب شي، رجع اشتغل على حاله: كورسات، تطوع، وتدريب على مشاريع عملاء حقيقيين. بعدها بنينا الـCV بأكتر من نسخة للخليج وأوروبا، وLinkedIn واضح.",
         w_en="Before we wrote anything, he went back to building: courses, volunteering and an internship on real client projects. Then we built CV versions for the Gulf and Europe, and a clear LinkedIn.",
         r_ar="اليوم عم يشتغل بالسعودية، براتب ممتاز لخريج جديد.", r_en="Today he works in Saudi Arabia, on a strong salary for a new graduate."),
    dict(id="gulf", stamp_ar="الخليج", stamp_en="The Gulf", date_ar="أيلول 2026", date_en="September 2026",
         h_ar="مهندسة كانت تقدّم بدون نتيجة", h_en="An engineer applying with no results",
         s_ar="دارسة هندسة وعم تستهدف الخليج. عندها LinkedIn، بس كان حساب موجود، مو أداة.", s_en="An engineering graduate targeting the Gulf. She had LinkedIn, but as an account, not a tool.",
         w_ar="اشتغلنا على الـCV والـLinkedIn وطريقة تقديم خبرتها للسوق يلي مستهدفته.", w_en="We reworked her CV, her LinkedIn and how she framed her experience for that market.",
         r_ar="ردود أكتر ومقابلات، والأهم: صارت تعرف تبحث وتقدّم وتستخدم شبكتها لحالها.", r_en="More replies and interviews, and above all she now searches, applies and uses her network on her own."),
    dict(id="shift", stamp_ar="مجال جديد", stamp_en="New field", date_ar="أيلول 2026", date_en="September 2026",
         h_ar="Career Shift بدون ما يبلش من الصفر", h_en="A career shift without starting from zero",
         s_ar="عميل عنده خبرة بمجال مختلف، وعم يستهدف مسار مهني جديد.", s_en="A client with experience in another field, aiming for a new career path.",
         w_ar="بدل ما نخبي خبرته القديمة، حددنا الخبرات القابلة للنقل وأعدنا الـPositioning حول الاتجاه الجديد.", w_en="Instead of hiding his past, we identified what transfers and rebuilt the positioning around the new direction.",
         r_ar="Profile أوضح للوظائف المستهدفة، وفرص مقابلات مرتبطة فعلاً بالمسار الجديد.", r_en="A clearer profile for the roles he wanted, and interviews tied to the new path."),
    dict(id="offer", stamp_ar="عرض بيوم", stamp_en="Offer in a day", date_ar="حزيران 2026", date_en="June 2026",
         h_ar="عرض شغل بعد ما نشر الـCV الجديد", h_en="A job offer right after the new CV",
         s_ar="عميل جرّب ينشر الـCV الجديد «من باب الفضول».", s_en="A client posted his new CV “just out of curiosity”.",
         w_ar="تاني يوم تواصلت معه شركة مصنّفة International Digital Partner، وبعد الاتصال بعتوله نسخة من العقد.", w_en="The next day a company ranked as an International Digital Partner called him, then sent over a contract.",
         r_ar="عرض شغل جديد خلال يوم.", r_en="A new job offer within a day."),
    dict(id="team", stamp_ar="شركة سعودية", stamp_en="Saudi company", date_ar="أيلول 2026", date_en="September 2026",
         h_ar="فريق كامل بنفس الـDNA", h_en="A whole team with one DNA",
         s_ar="شركة سعودية بدها كل موظف يظهر باحتراف، بس بهوية وحدة.", s_en="A Saudi company wanted every employee to look professional, under one identity.",
         w_ar="فهمنا الـBrand أول، وبعدين بنينا Template وVisual Direction موحّد، مع Profile لكل موظف بيعكس خبرته الحقيقية.", w_en="We started with the brand, then built one template and visual direction, with each profile still true to its owner.",
         r_ar="صورة مهنية متسقة للشركة عبر موظفيها، وطريقة أوضح لكل موظف يعرض فيها خبرته.", r_en="A consistent professional image across the company, and a clearer way for each employee to present their work."),
]
STORY = {s["id"]: s for s in STORIES}

TOPICS = [("cv", "CV", "CV"), ("linkedin", "LinkedIn", "LinkedIn"), ("shift", "Career Shift", "Career shift"),
          ("content", "المحتوى", "Content"), ("market", "سوق العمل", "Job market"), ("journey", "رحلتي", "My journey")]
TOPIC = {k: (a, e) for k, a, e in TOPICS}

IDEAS = [
    ("2026-10-08", "8 تشرين الأول", "Oct 8", "cv", "«ما عندي شي حطه بالـCV غير اسمي ورقمي.»", "“I have nothing to put on my CV except my name and number.”",
     "قصة خريج بنى خبرته قبل أول وظيفة، واليوم عم يشتغل بالسعودية.", "A graduate who built experience before his first job, and now works in Saudi Arabia."),
    ("2026-10-07", "7 تشرين الأول", "Oct 7", "linkedin", "لو قابلت الشخص يلي ممكن يفتحلك باب فرصة… هل أنت جاهز؟", "If you met the person who could open a door for you, would you be ready?",
     "قبل أي Event، جهّز جوابك والـCV والـLinkedIn. هنن الانطباع يلي بيكمّل بعد ما تخلص الفعالية.", "Before any event, prepare your answer, CV and LinkedIn. They're the impression that lasts after it ends."),
    ("2026-10-06", "6 تشرين الأول", "Oct 6", "cv", "لا تخلي الـHR يسحب منك المعلومات سؤال سؤال.", "Don't make HR pull information out of you one question at a time.",
     "أول رسالة للـHR: بوزشن واضح، Cover Letter قصيرة، CV، ومعلومات التواصل.", "Your first message to HR: a clear position, a short cover letter, your CV and contact details."),
    ("2026-10-05", "5 تشرين الأول", "Oct 5", "market", "هل فعلاً سوق العمل بسوريا عم يتحسن؟", "Is Syria's job market really improving?",
     "سؤال مفتوح للموظفين والـHR وأصحاب الشركات عن الرواتب والمزايا والـFeedback، والفرق بين المحافظات.", "An open question to employees, HR and employers about pay, benefits, feedback and how cities differ."),
    ("2026-10-04", "4 تشرين الأول", "Oct 4", "journey", "لسا ما وصلت للمكان يلي بدي ياه… ويمكن هاد الشي يلي بحبه.", "I haven't reached where I want to be, and maybe that's what I love about it.",
     "من Software Engineering للـUI/UX للـPersonal Branding، والطريق لسا مكمّل.", "From software engineering to UI/UX to personal branding, and the road keeps going."),
    ("2026-10-03", "3 تشرين الأول", "Oct 3", "content", "اذا خايف حدا يختلف معك، لا تكتب رأيك أصلاً.", "If you're afraid someone will disagree, don't post your opinion at all.",
     "الجملة المستفزة بتوقف القارئ، بس الفكرة الحقيقية هي يلي بتخليه يكمّل.", "A provocative line stops the reader; a real idea is what keeps them reading."),
    ("2026-10-01", "1 تشرين الأول", "Oct 1", "linkedin", "بوست عندك ضرب؟ لا تعتبر المهمة خلصت هون.", "A post of yours took off? The job isn't done.",
     "مين وصله؟ ليش تفاعل؟ شو الخطوة الجاية؟ وخلي بروفايلك جاهز يستقبلهم.", "Who did it reach, why did they engage, what's next? And make sure your profile is ready to receive them."),
    ("2026-09-30", "30 أيلول", "Sep 30", "shift", "اذا قررت تعمل Career Shift… لا تبلش بتعديل الـCV.", "Changing careers? Don't start by editing your CV.",
     "خمس خطوات قبل ما تلمس الـCV، من تحديد الوظيفة لتوحيد الاتجاه بين الـCV والـLinkedIn.", "Five steps before you touch the CV, from choosing the role to aligning CV and LinkedIn."),
    ("2026-09-29", "29 أيلول", "Sep 29", "shift", "الـCareer Shift ما بيعني تبلش من الصفر.", "A career shift doesn't mean starting from zero.",
     "سنوات خبرتك وطريقة تفكيرك والمشاكل يلي تعلمت تحلها، كلها Career Capital.", "Your years, your thinking and the problems you've learned to solve are all career capital."),
    ("2026-09-28", "28 أيلول", "Sep 28", "content", "شو بدنا ننشر ع LinkedIn؟", "What should we post on LinkedIn?",
     "الأفكار حواليك: خبر، نقاش مع زميل، سؤال من عميل، أو ملاحظة صغيرة من يومك.", "Ideas are all around you: a news item, a chat with a colleague, a client's question, a small note from your day."),
    ("2026-09-26", "26 أيلول", "Sep 26", "cv", "مشروع تخرجك مو بس شي لازم تسلّمه للدكتور.", "Your graduation project isn't just something to hand in.",
     "ممكن يكون أول مشروع بتحطه قدام سوق العمل.", "It could be the first project you put in front of the job market."),
    ("2026-09-24", "24 أيلول", "Sep 24", "linkedin", "شركة سعودية طلبت مني شغلة مختلفة.", "A Saudi company asked me for something different.",
     "CV وLinkedIn لكل موظف، مختلفين بالمحتوى وموحّدين بهوية الشركة.", "A CV and LinkedIn for every employee, different in content, united by the company's identity."),
    ("2026-09-22", "22 أيلول", "Sep 22", "content", "ليال، كيف كل يوم بتنزلي بوست؟", "“Layal, how do you post every single day?”",
     "ساعتين بالأسبوع للمواضيع والكتابة والجدولة. الاستمرارية بدها نظام، مو وقت كل يوم.", "Two hours a week to pick topics, write and schedule. Consistency needs a system, not daily time."),
    ("2026-09-21", "21 أيلول", "Sep 21", "journey", "أحلى جزء بشغلي لما العميل يرجع ويقلي: هلأ فهمت ليش ما كنت عم أوصل.", "The best part of my work: when a client says “now I get why I wasn't getting anywhere.”",
     "قصة مهندسة صارت تستخدم LinkedIn كأداة بحث عن فرص، مو مكان بتحط فيه الـCV وبتستنى.", "An engineer who now uses LinkedIn to find opportunities, not as a place to park a CV and wait."),
    ("2026-08-17", "17 آب", "Aug 17", "journey", "أول شغل، أول عميل، وأول دولار… كلهن إجوا من LinkedIn.", "My first job, first client and first dollar all came from LinkedIn.",
     "ليش بآمن إن LinkedIn مو حساب، هو باب.", "Why I believe LinkedIn isn't an account, it's a door."),
    ("2026-06-20", "20 حزيران", "Jun 20", "cv", "الشركات ما عم توظف عدد سنوات خبرة… الشركات عم توظف قيمة.", "Companies don't hire years of experience. They hire value.",
     "كيف وصل CV عميل سوري لشركة بأمريكا.", "How a Syrian client's CV got him into a US company."),
]

FAQ = [
    ("مين ليال جمعة؟", "Who is Layal Joumaa?",
     "ليال جمعة (Layal Joumaa) كاتبة CV وخبيرة تحسين LinkedIn وPersonal Branding من سوريا. خريجة هندسة برمجيات ونظم معلومات من جامعة تشرين، اشتغلت بالـUI/UX وأبحاث المستخدمين، وبتكتب CVs من 2022، وحالياً بتشتغل Personal Brand مع Assil Design.",
     "Layal Joumaa (ليال جمعة) is a Syrian CV writer, LinkedIn optimisation specialist and personal-branding consultant. She studied Software Engineering and Information Systems at Tishreen University, worked in UI/UX and user research, has written CVs since 2022 and now works on personal branding with Assil Design."),
    ("شو الخدمات يلي بتقدمها؟", "What services does she offer?",
     "كتابة وتحسين الـCV بهيكلة ATS ونسخة لكل سوق، Cover Letter ورسالة أولى للـHR، تحسين LinkedIn، Career Shift وPositioning لمين عم يغيّر مجاله، Personal Branding والمحتوى، وصورة مهنية موحّدة لفرق الشركات.",
     "ATS-friendly CV writing with a version per market, cover letters and first messages to HR, LinkedIn optimisation, career-shift positioning, personal branding and content, and unified professional profiles for company teams."),
    ("لمين بتشتغل، ووين؟", "Who does she work with, and where?",
     "خريجين جدد، أصحاب خبرة، ناس عم يغيّروا مجالهم، وشركات. مقيمة بدمشق وبتشتغل عن بعد مع عملاء بسوريا والسعودية والخليج وأوروبا وأمريكا، بقطاعات IT والهندسة والـBusiness والرعاية الصحية وغيرها.",
     "New graduates, experienced professionals, career changers and companies. She is based in Damascus and works remotely with clients in Syria, Saudi Arabia and the Gulf, Europe and the US, across IT, engineering, business, healthcare and more."),
    ("كيف بتواصل معها؟", "How do I contact her?",
     "برسالة على LinkedIn. ابعتلها كلمة PROFILE إذا بدك CV وLinkedIn مبنيين على هدفك، أو SHIFT إذا عم تغيّر مجالك، وقلّها مين انت وشو الوظيفة يلي عم تستهدفها.",
     "Send her a direct message on LinkedIn. Write PROFILE for a CV and LinkedIn built on your goal, or SHIFT if you're changing fields, and say who you are and which role you're targeting."),
    ("كيف بينكتب اسمها؟", "How is her name spelled?",
     "بالعربي ليال جمعة، وبالإنجليزي Layal Joumaa. ممكن تلاقيه كمان Layal Jomaa أو Layal Jumaa أو Layal Joumaah، وبتوقّع شغلها باسم Eng. Layal.",
     "In Arabic ليال جمعة, in English Layal Joumaa. You may also see Layal Jomaa, Layal Jumaa or Layal Joumaah, and she signs her work “Eng. Layal”."),
    ("شو بيميّز طريقتها؟", "What makes her approach different?",
     "ما بتبلش بكتابة CV. بتبلش بفهم المسار والسوق، بعدين الـPositioning، وبعدها بتبني الـCV والـLinkedIn ليحكوا نفس القصة. وهدفها إنك تعرف تكمّل لحالك بعدها.",
     "She doesn't start with the CV. She starts with your path and target market, then positioning, then builds the CV and LinkedIn to tell the same story, so you can carry on well on your own afterwards."),
]

SHEET_CASES = [
    {"ar": {"old": "«ما عندي شي حطه بالـCV غير اسمي ورقمي.»", "new": "مهندس شبكات | 3 مشاريع عملية | تدريب على مشاريع عملاء حقيقيين",
            "n1": "شو تعلّمت؟ شو طبّقت؟", "n2": "نسخة للخليج، ونسخة لأوروبا", "cap": "من قصة حقيقية: خريج من اللاذقية، اليوم عم يشتغل بالسعودية.", "more": "القصة", "href": "stories.html#sa"},
     "en": {"old": "“I have nothing to put on my CV except my name and number.”", "new": "Network Engineer | 3 hands-on projects | Internship on live client work",
            "n1": "What did you learn? What did you apply?", "n2": "One version for the Gulf, one for Europe", "cap": "A real story: a graduate from Latakia, now working in Saudi Arabia.", "more": "Read it", "href": "stories.html#sa"}},
    {"ar": {"old": "CV بيحكي عن الشخص يلي كنت عليه", "new": "CV بيوضّح الشخص يلي عم تتجه لتصير عليه",
            "n1": "شو من خبرتك بينتقل معك؟", "n2": "Career Capital ✓", "cap": "Career Shift بدون ما تبلش من الصفر.", "more": "القصة", "href": "stories.html#shift"},
     "en": {"old": "A CV about the person you used to be", "new": "A CV that shows the person you're becoming",
            "n1": "What carries over?", "n2": "Career capital ✓", "cap": "A career shift without starting from zero.", "more": "Read it", "href": "stories.html#shift"}},
    {"ar": {"old": "LinkedIn؟ عندي حساب… بس ما بستخدمه", "new": "LinkedIn أداة: بحث، تقديم، وشبكة بتشتغل معي",
            "n1": "بروفايل جاهز يستقبل الناس", "n2": "ردود ومقابلات أكتر", "cap": "مهندسة كانت تقدّم للخليج بدون نتيجة.", "more": "القصة", "href": "stories.html#gulf"},
     "en": {"old": "LinkedIn? I have an account… I just don't use it", "new": "LinkedIn as a tool: search, apply, and a network that works for me",
            "n1": "A profile ready for visitors", "n2": "More replies, more interviews", "cap": "An engineer applying to the Gulf with no results.", "more": "Read it", "href": "stories.html#gulf"}},
]


ICONS = {
    "cv": '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4"/><path d="M10 9h2M10 12.5h5M10 16h5"/>',
    "cover": '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="m3.5 7 8.5 6.5L20.5 7"/>',
    "linkedin": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2.2"/><path d="M5.8 16.5c.6-1.8 1.8-2.8 3.2-2.8s2.6 1 3.2 2.8M14.5 9h4M14.5 12.5h4"/>',
    "shift": '<path d="M4 8h13M14 4.5 17.5 8 14 11.5M20 16H7M10 12.5 6.5 16 10 19.5"/>',
    "brand": '<path d="M4 10v4a1 1 0 0 0 1 1h2l5 4V5L7 9H5a1 1 0 0 0-1 1z"/><path d="M16 9.5a3.5 3.5 0 0 1 0 5M18.5 7a7 7 0 0 1 0 10"/>',
    "teams": '<circle cx="12" cy="8" r="3"/><circle cx="5.5" cy="10" r="2.2"/><circle cx="18.5" cy="10" r="2.2"/><path d="M6.5 19c.7-2.8 2.8-4.3 5.5-4.3s4.8 1.5 5.5 4.3M2.5 17.5c.4-1.6 1.5-2.6 3-2.8M21.5 17.5c-.4-1.6-1.5-2.6-3-2.8"/>',
}
PITCH = {
    "cv": dict(hook_ar="بتقدّم وما حدا عم يرد؟", hook_en="Applying and hearing nothing back?",
               promise_ar="CV بيعدّي أنظمة الـATS وبيوصل لعين الـHR، وبنسخة لكل سوق عم تستهدفه.",
               promise_en="A CV that gets past ATS and in front of HR, with a version for every market you target.",
               proof_ar="عميل من سوريا انقبل بشركة بأمريكا", proof_en="A client from Syria hired by a US company", href="stories.html#us", cta="cv"),
    "cover": dict(hook_ar="بتحتار شو تكتب للـHR؟", hook_en="Never sure what to write to HR?",
                  promise_ar="رسالة قصيرة بتعرّف عنك من أول سطر، وبتخلي الـHR يطلب المقابلة بدل ما يسألك سؤال سؤال.",
                  promise_en="A short message that introduces you from line one, so HR asks for the interview instead of asking questions one by one.",
                  proof_ar="ليش «في شواغر عندكم؟» ما بتجيب رد", proof_en="Why “any openings?” gets no reply", href="ideas.html", cta="cover"),
    "linkedin": dict(hook_ar="عندك LinkedIn… بس ما عم يجيب فرص؟", hook_en="On LinkedIn… but no opportunities?",
                     promise_ar="بروفايل بيفهّم الزائر خلال ثواني مين انت وشو بتقدّم، وبيخلي الـRecruiters يلاقوك.",
                     promise_en="A profile that tells visitors who you are in seconds, and gets recruiters to find you.",
                     proof_ar="مهندسة صارت تجيها مقابلات بالخليج", proof_en="An engineer now getting interviews in the Gulf", href="stories.html#gulf", cta="li"),
    "shift": dict(hook_ar="بدك تغيّر مجالك وخايف تبلش من الصفر؟", hook_en="Changing fields and afraid of starting from zero?",
                  promise_ar="منحوّل خبرتك القديمة لـCareer Capital، ومنبني قصة بتوصلك للمجال الجديد.",
                  promise_en="We turn your past into career capital and build a story that gets you into the new field.",
                  proof_ar="مقابلات مرتبطة فعلاً بالمسار الجديد", proof_en="Interviews tied to the new path", href="stories.html#shift", cta="shift"),
    "brand": dict(hook_ar="عندك خبرة… بس ما حدا بيعرف فيك؟", hook_en="Great at what you do, but nobody knows?",
                  promise_ar="محتوى من شغلك الحقيقي ونظام ساعتين بالأسبوع، لتصير الاسم يلي بيخطر عبالهم.",
                  promise_en="Content from your real work and a two-hours-a-week system, so you become the name they think of.",
                  proof_ar="من حسابي: 90,507 ظهور بـ28 يوم", proof_en="My own account: 90,507 impressions in 28 days", href="index.html#proof", cta="brand"),
    "teams": dict(hook_ar="بدك كل فريقك يبيّن بنفس المستوى؟", hook_en="Want your whole team to look equally strong?",
                  promise_ar="صورة مهنية موحّدة لكل موظفينك، وكل واحد فيهم بيضل بيشبه حاله.",
                  promise_en="One professional look across your team, with everyone still sounding like themselves.",
                  proof_ar="شركة سعودية صار فريقها بنفس الـDNA", proof_en="A Saudi company's team, one DNA", href="stories.html#team", cta="team"),
}


def icon(k, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[k]}</svg>'


def pitch_cards():
    cards = ""
    order = ["cv", "linkedin", "cover", "shift", "brand", "teams"]
    by = {x["id"]: x for x in SERVICES}
    for i, sv in enumerate(by[k] for k in order):
        P = PITCH[sv["id"]]
        big = sv["id"] in ("cv", "linkedin")
        gets = ""
        if big:
            gets = '<ul class="gets">' + "".join(f"<li>{t(a, e)}</li>" for a, e in list(zip(sv["items_ar"], sv["items_en"]))[:3]) + "</ul>"
        cls = "pc" + (" big" if big else "") + (" dark" if sv["id"] == "cv" else "")
        cards += f'''<article class="{cls}" data-tilt style="--k:{i}">
  <div class="pc-top"><span class="pc-ic">{icon(sv['id'])}</span><span class="pc-name">{t(sv['ar'], sv['en'])}</span></div>
  <h3 class="pc-hook">{t(P['hook_ar'], P['hook_en'])}</h3>
  <p class="pc-promise">{t(P['promise_ar'], P['promise_en'])}</p>
  {gets}
  <div class="pc-foot">
    <a class="pc-cta" href="contact.html?svc={P['cta']}">{t("بدي هالخدمة", "I want this")}<span class="arr" aria-hidden="true">←</span></a>
    <a class="pc-proof" href="{P['href']}">{t(P['proof_ar'], P['proof_en'])}</a>
  </div>
</article>'''
    return cards


def idea_card(i):
    d, dar, den, tp, har, hen, sar, sen = i
    return (f'<a class="idea" href="ideas.html"><time datetime="{d}">{t(dar, den)}</time>'
            f'<q>{t(har, hen)}</q><p>{t(sar, sen)}</p></a>')


def story_card(s, big=False, glass=True):
    return f'''<article class="story{' big' if big else ''}{' glass' if glass else ''}" id="{s['id']}" data-tilt>
  <span class="stamp">{t(s['stamp_ar'], s['stamp_en'])}</span>
  <h3>{t(s['h_ar'], s['h_en'])}</h3>
  <dl class="beats">
    <div><dt>{t("البداية", "Start")}</dt><dd>{t(s['s_ar'], s['s_en'])}</dd></div>
    <div><dt>{t("الشغل", "The work")}</dt><dd>{t(s['w_ar'], s['w_en'])}</dd></div>
    <div class="res"><dt>{t("النتيجة", "Result")}</dt><dd>{t(s['r_ar'], s['r_en'])}</dd></div>
  </dl>
  <div class="story-foot"><span>{t(s['date_ar'], s['date_en'])}</span>
    <a class="link" href="{ACT}" rel="noopener" target="_blank">{t("اقرأها على LinkedIn", "Read it on LinkedIn")}</a></div>
</article>'''


def sec_head(h_ar, h_en, p_ar=None, p_en=None):
    p = f'<p class="lede">{t(p_ar, p_en)}</p>' if p_ar else ""
    return f'<div class="sec-head"><h2 class="h2">{t(h_ar, h_en)}</h2>{SQUIG}{p}</div>'


def phead(h_ar, h_en, lede_ar, lede_en, note_ar, note_en, art=""):
    return f'''<section class="phead"><div class="wrap phead-grid">
  <div>
    <h1 class="display">{t(h_ar, h_en)}</h1>
    <p class="lede">{t(lede_ar, lede_en)}</p>
  </div>
  {art or f'<span class="note" aria-hidden="true">{t(note_ar, note_en)}</span>'}
</div></section>'''


def growth_svg():
    # shape traced from her LinkedIn analytics screenshot (cumulative impressions, 24 May – 20 Jun 2026)
    pts = [(0, 0), (25, .2), (40, .5), (52, 1), (58, 3), (62, 11), (66, 17), (72, 21), (78, 24), (84, 30), (89, 38), (93, 47), (96, 62), (98.5, 80), (100, 100)]
    W, H = 300, 110
    xy = [(x / 100 * W, H - y / 100 * H) for x, y in pts]
    line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in xy)
    area = line + f" L{W} {H} L0 {H} Z"
    return f'''<svg class="growth" viewBox="0 -14 {W} {H + 34}" role="img" aria-label="{html.escape("Cumulative LinkedIn impressions rising from near zero to 90,507 between 24 May and 20 June 2026")}">
  <defs><linearGradient id="gArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EE7F2D" stop-opacity=".35"/><stop offset="1" stop-color="#EE7F2D" stop-opacity="0"/></linearGradient></defs>
  <line class="axis" x1="0" y1="{H}" x2="{W}" y2="{H}"/>
  <path class="area" d="{area}"/><path class="line" pathLength="1" d="{line}"/>
  <text x="0" y="{H + 16}">24 May</text><text x="{W}" y="{H + 16}" text-anchor="end">20 Jun</text>
</svg>'''


def map_svg():
    data = json.load(open(os.path.join(HERE, "mapdots.json")))
    land = "".join(f"M{x} {y}h0" for x, y in data["dots"])
    P = data["places"]
    sx, sy = P["sy"]
    dests = [("sa", P["sa"], "السعودية", "Saudi Arabia", "sa team", 0.2),
             ("gulf", P["gulf"], "الخليج", "The Gulf", "gulf", 0.5),
             ("us", P["us"], "أمريكا", "United States", "us", 0.8)]
    arcs, pins = "", ""
    for key, (x, y), ar, en, ids, d in dests:
        mx, my = (sx + x) / 2, min(sy, y) - abs(x - sx) * (0.35 if key == "us" else 0.6) - 20
        path = f"M{sx} {sy} Q{mx:.0f} {my:.0f} {x} {y}"
        arcs += (f'<path id="arc-{key}" class="arc" data-to="{key}" pathLength="1" style="--d:{d}s" d="{path}"/>'
                 f'<circle class="plane" r="4"><animateMotion dur="{3.2 + d * 2:.1f}s" begin="{d + 1.6:.1f}s" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1" calcMode="linear"><mpath href="#arc-{key}"/></animateMotion></circle>')
        lx = x + (14 if key != "gulf" else 16)
        anchor = "start"
        ly = y + (28 if key == "sa" else -12)
        if key == "us":
            ly = y - 14
        pins += (f'<g class="dest" data-key="{key}" data-to="{ids}" tabindex="0" role="link" aria-label="{html.escape(en)}">'
                 f'<circle class="halo" cx="{x}" cy="{y}" r="9"/><circle class="dot" cx="{x}" cy="{y}" r="7"/>'
                 f'<text x="{lx}" y="{ly}" text-anchor="{anchor}">{t(ar, en, "tspan")}</text></g>')
    # on phones the map zooms into the Middle East; the US arc then leaves the frame, so label where it exits
    ux, uy = P["us"]; umx, umy = (sx + ux) / 2, min(sy, uy) - abs(ux - sx) * 0.35 - 20
    def qa(tt):
        return ((1 - tt) ** 2 * sx + 2 * (1 - tt) * tt * umx + tt * tt * ux, (1 - tt) ** 2 * sy + 2 * (1 - tt) * tt * umy + tt * tt * uy)
    tt = min((k / 400 for k in range(401)), key=lambda v: abs(qa(v)[0] - 612))
    ex, ey = qa(tt)
    edge = (f'<g class="us-edge" aria-hidden="true"><text x="{ex + 4:.0f}" y="{ey + 26:.0f}" text-anchor="start">'
            f'{t("أمريكا ←", "← United States", "tspan")}</text></g>')
    origin = (f'<g class="origin"><circle class="dot" cx="{sx}" cy="{sy}" r="7"/>'
              f'<text x="{sx - 12}" y="{sy - 14}" text-anchor="end">{t("سوريا", "Syria", "tspan")}</text></g>')
    return f'''<figure class="map"><svg viewBox="-20 -70 1270 420" role="group" aria-label="{html.escape("Map: stories from Syria to Saudi Arabia, the Gulf and the United States")}">
  <path class="land" d="{land}"/>{arcs}{origin}{pins}{edge}
</svg><figcaption class="map-hint">{t("مرّر أو اكبس على أي وجهة لتشوف قصتها.", "Hover or tap a destination to see its story.")}</figcaption></figure>'''


# =====================================================================
# Pages
# =====================================================================
def home():
    c0 = SHEET_CASES[0]
    cases_attr = html.escape(json.dumps(SHEET_CASES, ensure_ascii=False))
    sheet = f'''<figure class="sheet" id="sheet" data-tilt data-cases="{cases_attr}" aria-label="{html.escape("CV before and after")}">
  <span class="note sh-note n1" id="shN1" aria-hidden="true">{t(c0["ar"]["n1"], c0["en"]["n1"])}</span>
  <div class="sh-name" aria-hidden="true"><span class="sh-dot"></span><span class="bars"><span class="bar w60"></span><span class="bar w40"></span></span></div>
  <p class="sh-label">{t("قبل", "Before")}</p>
  <p class="old"><del><span class="x" id="shOld">{t(c0["ar"]["old"], c0["en"]["old"])}</span></del></p>
  <p class="sh-label">{t("بعد", "After")}</p>
  <p class="new" id="shNew" aria-live="off">{t(c0["ar"]["new"], c0["en"]["new"])}</p>
  <div class="sh-lines" aria-hidden="true"><span class="bar w90"></span><span class="bar w80"></span><span class="bar w70"></span></div>
  <span class="note sh-note n2" id="shN2" aria-hidden="true">{t(c0["ar"]["n2"], c0["en"]["n2"])}</span>
</figure>'''
    dots = "".join(f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" aria-label="{i + 1}">{i + 1}</button>' for i in range(len(SHEET_CASES)))
    system = [("Content يجذب", "Content attracts", "بوست بيوقف الشخص الصح عند اسمك.", "A post that stops the right person at your name."),
              ("Profile يعرّف فيك", "Profile introduces", "خلال ثواني لازم يفهم مين انت وشو بتقدم.", "Within seconds they get who you are and what you offer."),
              ("Positioning يوضح قيمتك", "Positioning clarifies", "ليش انت تحديداً، مو حدا غيرك.", "Why you specifically, and not someone else."),
              ("الخدمة بتحوّل الاهتمام لتعاون", "The offer converts", "خطوة واضحة: رسالة، مقابلة، أو عقد.", "A clear next step: a message, an interview, a contract.")]
    sys_html = "".join(f'<li><span class="sys-n">{i + 1}</span><span class="sys-t">{t(a, e)}</span><span class="sys-d">{t(da, de)}</span>{I_ARROW}</li>'
                       for i, (a, e, da, de) in enumerate(system))
    faq = "".join(f'<details><summary>{t(qa, qe)}{I_PLUS}</summary><p>{t(aa, ae)}</p></details>' for qa, qe, aa, ae in FAQ)
    checks = [("who", "واضح مين انت", "It says who you are"), ("value", "في تخصص أو قيمة بتقدّمها", "It names a specialty or the value you bring"),
              ("direction", "مو بس «عم دوّر على شغل»", "It's more than “looking for a job”"), ("proof", "في دليل: أداة، شهادة، أو رقم", "There's proof: a tool, certificate or number"),
              ("length", "طول مناسب (50 لـ 220 حرف)", "A useful length (50–220 characters)")]
    ck = "".join(f'<li data-k="{k}">{t(a, e)}</li>' for k, a, e in checks)
    st = LINKEDIN_STATS
    body = f'''
<section class="hero"><div class="wrap">
 <div class="hero-grid">
  <div>
    <h1 class="display">{t("ملفك المهني لازم يحكي عنك قبل المقابلة.", "Your profile should speak for you before the interview.")}</h1>
    <p class="lede">{t("أنا ليال جمعة. بكتب الـCV، وببني LinkedIn، وبشتغل على الـPositioning، لحتى خبرتك الحقيقية توصل للشخص الصح بالطريقة الصح.",
                      "I'm Layal Joumaa. I write CVs, rebuild LinkedIn profiles and work on positioning, so your real experience reaches the right person in the right way.")}</p>
    <div class="cta-row">
      <a class="btn btn-ink js-li" href="{LI}" rel="noopener" target="_blank">{I_LI}{t("راسليني على LinkedIn", "Message me on LinkedIn")}</a>
      <a class="btn btn-line" href="services.html">{t("شو بقدّم", "What I offer")}</a>
    </div>
    <p class="reach">{t("أكتر من <strong>14,500</strong> شخص بيتابعوا شغلي على LinkedIn، وعملائي اليوم بسوريا والخليج وأوروبا وأمريكا.",
                       "More than <strong>14,500</strong> people follow my work on LinkedIn, and my clients now work across Syria, the Gulf, Europe and the US.")}</p>
  </div>
  <div class="hero-art">
    <div class="arch-wrap" data-depth="0.6"><figure class="arch">{pic("layal-portrait", "ليال جمعة، كاتبة CV وخبيرة LinkedIn", eager=True)}</figure></div>
    <div class="chips">
    <span class="chip-f c1" data-depth="1.6">🤍 <b data-count="{st['followers']}">{st['followers']:,}</b> {t("متابع", "followers")}</span>
    <span class="chip-f c2" data-depth="2.2"><b dir="ltr">+{st['growth']}%</b> {t("ظهور بشهر", "reach in a month")}</span>
    <span class="chip-f c3" data-depth="1.2">✔ {t("متوافق مع ATS", "ATS-friendly")}</span>
    </div>
    {sheet}
  </div>
 </div>
 <div class="hero-foot">
   <p class="sh-cap" id="shCap">{t(c0["ar"]["cap"] + ' <a class="link" href="stories.html#sa">' + c0["ar"]["more"] + '</a>', c0["en"]["cap"] + ' <a class="link" href="stories.html#sa">' + c0["en"]["more"] + '</a>')}</p>
   <div class="sh-dots" role="group" aria-label="{html.escape("Before and after examples")}">{dots}</div>
 </div>
</div></section>


<section class="paper"><div class="wrap">
  {sec_head("شو الشي يلي واقف بطريقك؟", "What's standing in your way?", "اختار المشكلة يلي بتشبهك، وأنا بتكفّل بالباقي. كل خدمة بتبلش من هدفك، وبتخلص بملف بيحكي عنك قبل المقابلة.", "Pick the problem that sounds like you and I'll take it from there. Every service starts with your goal and ends with a profile that speaks before the interview.")}
  <div class="pitch" data-snap>{pitch_cards()}</div>
  <p class="more"><a class="link" href="services.html">{t("شوف تفاصيل كل خدمة", "See every service in detail")}</a></p>
</div></section>

<section class="ink"><div class="wrap">
  {sec_head("LinkedIn منظومة كاملة، مو حساب", "LinkedIn is a system, not an account", "ممكن بوست واحد يجيبلك آلاف الزيارات. إذا الشخص دخل على بروفايلك وما فهم خلال ثواني مين انت، ضاعت الفرصة.", "One post can bring thousands of visits. If someone lands on your profile and can't tell who you are within seconds, the chance is gone.")}
  <ol class="system">{sys_html}</ol>
  <div class="proof" id="proof">
    <div class="pf"><b data-count="{st['impressions']}">{st['impressions']:,}</b><span>{t("ظهور لبوستاتي خلال 28 يوم", "post impressions in 28 days")}</span></div>
    <div class="pf"><b data-count="{st['reached']}">{st['reached']:,}</b><span>{t("شخص وصلهم المحتوى", "members reached")}</span></div>
    <div class="pf"><b dir="ltr">+<span data-count="{st['growth']}">{st['growth']}</span>%</b><span>{t("عن الـ28 يوم يلي قبلها", "vs. the previous 28 days")}</span></div>
    {growth_svg()}
    <p class="src">{t("من إحصائيات حسابي على LinkedIn، 24 أيار – 20 حزيران 2026. المنحنى مرسوم تقريبياً من اللقطة.", "From my LinkedIn analytics, 24 May – 20 June 2026. The curve is traced approximately from the screenshot.")}</p>
  </div>
  <p class="first-line">{t("أول شغل، أول عميل، وأول دولار… كلهن إجوا من LinkedIn. لهيك بشتغل عليه كباب، مو كحساب.", "My first job, first client and first dollar all came from LinkedIn. That's why I treat it as a door, not an account.")}</p>
  <p class="more"><a class="link" href="method.html">{t("كيف منشتغل سوا خطوة بخطوة", "How we work together, step by step")}</a></p>
</div></section>

<section class="lab"><div class="wrap lab-grid">
  <div>
    {sec_head("عندك 7 ثواني… شو بيفهم الزائر من الـHeadline تبعك؟", "You get 7 seconds. What does a visitor learn from your headline?")}
    <p class="lede">{t("اكتب الـHeadline يلي على LinkedIn، وشوف فوراً شو ناقصه.", "Type your LinkedIn headline and see right away what it's missing.")}</p>
    <label class="vh" for="hl">{t("الـHeadline تبعك", "Your headline")}</label>
    <textarea id="hl" maxlength="220" rows="3" dir="auto" data-ph-ar="مثلاً: Fresh graduate looking for opportunities" data-ph-en="e.g. Fresh graduate looking for opportunities"></textarea>
    <div class="lab-meta"><span id="hlCount">0/220</span><button type="button" class="link" id="hlTry">{t("جرّب مثال", "Try an example")}</button></div>
    <p class="privacy">{t("الفحص بصير بمتصفحك وما بينبعت لأي مكان.", "The check runs in your browser; nothing is sent anywhere.")}</p>
  </div>
  <div class="lab-out" aria-live="polite">
    <div class="score"><svg viewBox="0 0 100 100" aria-hidden="true"><circle class="bg" cx="50" cy="50" r="42"/><circle class="fg" id="hlRing" cx="50" cy="50" r="42" pathLength="1"/></svg>
      <b><span id="hlScore">0</span><small>/100</small></b></div>
    <ul class="checks">{ck}</ul>
    <p class="verdict" id="hlVerdict">{t("اكتب الـHeadline تبعك وشوف شو بيفهم الزائر.", "Type your headline and see what a visitor understands.")}</p>
    <a class="btn btn-ink" href="contact.html">{t("بدي Headline بيحكي عني", "I want a headline that speaks for me")}</a>
  </div>
</div></section>

<section><div class="wrap">
  {sec_head("ورا كل CV في إنسان عنده حلم", "Behind every CV is a person with a dream")}
  <div class="stories" data-snap>{story_card(STORY["us"])}{story_card(STORY["gulf"])}</div>
  <p class="more"><a class="link" href="stories.html">{t("كل القصص", "All stories")}</a></p>
</div></section>

<section class="paper"><div class="wrap journey">
  <div class="frame"><div class="portrait" data-tilt>{pic("layal-workshop", "ليال جمعة جنب لابتوب عليه عرض عن الخبرة العملية والإنجازات", w=474, h=593)}</div></div>
  <div>
    {sec_head("ما وصلت لهون بطريق واحد", "I didn't get here by one road")}
    <div class="trail road-trail" data-trail><span class="trail-line" aria-hidden="true"><span class="trail-fill"></span><span class="trail-head"></span></span>
    <ol class="road">
      <li><span class="pin"></span><div>{t("<b>Software Engineer</b><span>بكالوريوس هندسة البرمجيات ونظم المعلومات، جامعة تشرين</span>", "<b>Software engineer</b><span>B.Sc. Software Engineering & Information Systems, Tishreen University</span>")}</div></li>
      <li><span class="pin"></span><div>{t("<b>UI/UX وأبحاث المستخدمين</b><span>focal X agency، وفيها تعلّمت كيف بيقرأ الناس الشاشة</span>", "<b>UI/UX and user research</b><span>focal X agency, where I learned how people read a screen</span>")}</div></li>
      <li><span class="pin"></span><div>{t("<b>Personal Branding</b><span>من 2022 بكتب CVs، واليوم مع Assil Design</span>", "<b>Personal branding</b><span>Writing CVs since 2022, now with Assil Design</span>")}</div></li>
    </ol></div>
    <a class="link" href="about.html">{t("قصتي كاملة", "My full story")}</a>
  </div>
</div></section>

<section><div class="wrap">
  {sec_head("آخر أفكاري على LinkedIn", "Latest from my LinkedIn")}
  <div class="ideas" data-snap>{"".join(idea_card(i) for i in IDEAS[:3])}</div>
  <p class="more"><a class="link" href="ideas.html">{t("كل الأفكار", "All ideas")}</a></p>
</div></section>

<section class="paper"><div class="wrap">
  {sec_head("أسئلة بتنسأل كتير", "Questions people ask")}
  <div class="faq">{faq}</div>
</div></section>

'''
    return page("index", "ليال جمعة | كاتبة CV وخبيرة LinkedIn وPersonal Branding", "Layal Joumaa | CV Writer, LinkedIn & Personal Branding",
                "Layal Joumaa (ليال جمعة): Syrian CV & resume writer, LinkedIn optimisation specialist and personal-branding consultant for graduates, professionals, career changers and teams in Syria, the Gulf, Europe and the US.",
                body, kind="ProfilePage", faq=True, hero=True)


def services():
    idx = "".join(f'<a href="#{sv["id"]}">{icon(sv["id"])}<span>{t(sv["ar"], sv["en"])}</span></a>' for sv in SERVICES)
    rows = ""
    for i, sv in enumerate(SERVICES):
        P = PITCH[sv["id"]]
        gets = "".join(f'<li style="--k:{j}">{t(a, e)}</li>' for j, (a, e) in enumerate(zip(sv["items_ar"], sv["items_en"])))
        rows += f'''<article class="sv{' glassy' if i % 2 == 0 else ''}" id="{sv['id']}">
  <div class="sv-main">
    <div class="pc-top"><span class="pc-ic">{icon(sv['id'])}</span><span class="pc-name">{t(sv['ar'], sv['en'])}</span></div>
    <h2 class="sv-hook">{t(P['hook_ar'], P['hook_en'])}</h2>
    <p class="sv-promise">{t(P['promise_ar'], P['promise_en'])}</p>
    <p class="sv-for">{t(sv['for_ar'], sv['for_en'])}</p>
    <a class="btn btn-ink" href="contact.html?svc={P['cta']}">{t("بدي هالخدمة", "I want this")}</a>
  </div>
  <div class="sv-side">
    <p class="sv-sub">{t("شو بتاخد", "What you get")}</p>
    <ul class="sv-gets">{gets}</ul>
    <a class="sv-proof" href="{P['href']}"><span class="sv-proof-k">{t("من الشغل الحقيقي", "From real work")}</span><span>{t(P['proof_ar'], P['proof_en'])}</span></a>
  </div>
</article>'''
    tag = lambda xs: "".join(f"<li>{t(a, e)}</li>" for a, e in xs)
    inds = [("IT", "IT"), ("الهندسة", "Engineering"), ("Business", "Business"), ("الرعاية الصحية", "Healthcare"), ("وغيرها", "and more")]
    mkts = [("سوريا", "Syria"), ("الخليج", "The Gulf"), ("أوروبا", "Europe"), ("أمريكا", "United States")]
    lvls = [("خريجين جدد", "New graduates"), ("أصحاب خبرة", "Experienced professionals"), ("مناصب تنفيذية", "Executives"), ("فرق الشركات", "Company teams")]
    body = phead("كل خدمة بتبلش من سؤال واحد: شو الفرصة يلي بدك ياها؟", "Every service starts with one question: which opportunity are you after?",
                 "أول شي منحدد وين رايح، وبعدين بنبني كل قطعة لتحكي نفس القصة: الـCV، الـLinkedIn، والمحتوى يلي بتنشره.",
                 "First we decide where you're heading, then every piece is built to tell the same story: your CV, your LinkedIn and what you post.",
                 "مو تجميل… توضيح", "Not polish. Clarity.") + f'''
<section style="padding-top:0"><div class="wrap sv-layout">
  <nav class="sv-index" aria-label="Services">{idx}</nav>
  <div class="sv-list">{rows}</div>
</div></section>

<section class="paper"><div class="wrap">
  {sec_head("لمين بشتغل", "Who I work with")}
  <div class="who" data-snap>
    <div><h3>{t("قطاعات", "Industries")}</h3><ul class="tags">{tag(inds)}</ul></div>
    <div><h3>{t("أسواق", "Markets")}</h3><ul class="tags">{tag(mkts)}</ul></div>
    <div><h3>{t("مستويات", "Career stages")}</h3><ul class="tags">{tag(lvls)}</ul></div>
  </div>
</div></section>

<section class="ink"><div class="wrap cta-band">
  <div>
    <h2 class="h2">{t("مو متأكد شو بيناسبك؟", "Not sure which one fits?")}</h2>
    <p class="lede">{t("جاوب على 3 أسئلة بكبسات، وبتطلعلك رسالة جاهزة تبعتها لليال.", "Answer three quick taps and get a ready message to send to Layal.")}</p>
  </div>
  <a class="btn btn-orange" href="contact.html">{t("يلا نبلش", "Let's start")}</a>
</div></section>
'''
    return page("services", "الخدمات", "Services",
                "Services by Layal Joumaa: ATS CV writing, cover letters, LinkedIn optimisation, career-shift positioning, personal branding and team profiles.", body, kind="WebPage")


def method():
    proc = [("منفهم المسار", "We map the path", "شو الوظيفة يلي عم تستهدفها، وبأي سوق؟", "Which role, in which market?"),
            ("منحدد الـPositioning", "We set the positioning", "شو من خبرتك بيخدم هالهدف، وكيف منحكيه.", "Which parts of your experience serve the goal, and how to say them."),
            ("منبني الـCV", "We build the CV", "وبأكتر من نسخة إذا عم تقدّم لأكتر من سوق.", "In more than one version if you're applying to more than one market."),
            ("منبني LinkedIn بنفس الاتجاه", "We align LinkedIn", "Headline وAbout وخبرات بيحكوا نفس القصة.", "Headline, About and experience telling the same story."),
            ("بتكمّل لحالك أقوى", "You carry on stronger", "بتعرف كيف تبحث، وين تقدّم، وكيف تستخدم شبكتك.", "You know how to search, where to apply and how to use your network.")]
    steps = "".join(f"<li>{t(f'<b>{a}</b><span>{da}</span>', f'<b>{e}</b><span>{de}</span>')}</li>" for a, e, da, de in proc)
    shift = [("حدّد الوظيفة الجديدة قبل الـCV", "Choose the new role before the CV",
              "لا تقول «بدي اترك مجالي». حدّد بالضبط شو الوظائف يلي عم تستهدفها. كل ما كان الاتجاه أوضح، صار أسهل تعرف شو بتحتفظ فيه من خبرتك.",
              "Don't just say “I want out.” Name the exact roles you're targeting. The clearer the direction, the easier it is to know what to keep."),
             ("اعمل Mapping لخبرتك الحالية", "Map your current experience",
              "شو منها مطلوب بالمجال الجديد؟ شو قابل للنقل؟ وشو ما عاد يخدمك؟ أحياناً بتكتشف انك أقرب مما كنت مفكّر.",
              "What's in demand in the new field? What transfers? What no longer serves you? You're often closer than you think."),
             ("سدّ فجوة المهارات، مو كل الفجوات", "Close your skills gap, not every gap",
              "حدّد 2–3 مهارات أساسية ناقصتك، واشتغل عليها عبر Courses أو Projects أو Freelance.",
              "Find the 2–3 core skills you're missing and build them through courses, projects or freelance work."),
             ("غيّر طريقة تقديم خبرتك", "Reframe how you present your experience",
              "نفس الخبرة ممكن تنكتب بطريقة تبعدك عن الوظيفة الجديدة، أو بطريقة توضّح ليش إلها قيمة فيها.",
              "The same experience can be written to push you away from the new role, or to show why it matters there."),
             ("خلي الـCV والـLinkedIn يمشوا بنفس الاتجاه", "Point your CV and LinkedIn the same way",
              "إذا الـCV بيحكي عن مجال جديد والـLinkedIn لسا بالمجال القديم، عم تعطي السوق صورتين مختلفتين عنك.",
              "If your CV says new field and your LinkedIn still says old field, the market sees two different people.")]
    det = "".join(
        f'<details><summary><span class="n">{i + 1}</span>{t(a, e)}{I_PLUS}</summary><p>{t(da, de)}</p>'
        f'<label class="tick"><input type="checkbox">{t("خلّصت هالخطوة", "I've done this step")}</label></details>'
        for i, (a, e, da, de) in enumerate(shift))
    body = phead("شغلي مو إني جمّل خبرتك أو كبّرها.", "My job isn't to polish or inflate your experience.",
                 "شغلي إني اكتشف القيمة الموجودة فعلاً، وأعرف كيف وصّلها للشخص الصح بالطريقة الصح.",
                 "It's to find the value that's really there, and get it to the right person in the right way.",
                 "لو أنا المسؤول عن التوظيف، ليش لازم اختار هاد المرشح؟", "If I were hiring, why this candidate?") + f'''
<section class="paper"><div class="wrap">
  {sec_head("كيف منشتغل سوا", "How we work together", "ما ببلش بكتابة CV جديد مباشرة. ببلش بفهم المسار، وبعدين الـPositioning، وبعدها الملفات.", "I never start by writing a new CV. I start with the path, then the positioning, then the documents.")}
  <ol class="steps">{steps}</ol>
</div></section>

<section><div class="wrap">
  {sec_head("إذا قررت تعمل Career Shift… لا تبلش بتعديل الـCV", "Changing fields? Don't start by editing your CV", "خمس خطوات بشتغل عليها مع كل حدا عم يغيّر مساره. علّم يلي خلّصته وشوف وين صرت.", "Five steps I work through with everyone changing careers. Tick what you've done and see where you stand.")}
  <div class="shift-prog"><span id="shiftN">0/5</span><div class="shift-track"><div id="shiftBar"></div></div></div>
  <div class="shift" id="shiftList">{det}</div>
  <div class="shift-done" id="shiftDone" hidden><p>{t("خلّصت الخمسة 🤍 هلأ وقت الـCV والـLinkedIn.", "All five done 🤍 Now it's time for the CV and LinkedIn.")}</p>
    <a class="btn btn-orange" href="contact.html">{t("جهّز رسالتك إلي", "Draft your message to me")}</a></div>
</div></section>

<section class="ink"><div class="wrap">
  <p class="pull">{t("الـCareer Shift ما بيبلش لما تغيّر المسمى الوظيفي… بيبلش لما تعرف كيف تنقل قيمتك من مكان لمكان.",
                     "A career shift doesn't start with a new job title. It starts when you know how to carry your value from one place to the next.")}</p>
  <p class="pull-by">{t("هدفي مو انك تستلم ملف حلو وتكمّل بنفس الطريقة القديمة. هدفي انك تعرف تقدّم حالك أقوى حتى لما تكمّل لحالك.",
                        "The goal isn't a nice file and back to the old habits. It's that you present yourself better, even on your own.")}</p>
  <p style="margin-top:28px;margin-bottom:0"><a class="btn btn-orange" href="contact.html">{t("جهّز أول رسالة", "Draft your first message")}</a></p>
</div></section>
'''
    return page("method", "طريقة الشغل", "Method",
                "How Layal Joumaa works: path, positioning, CV, LinkedIn, and leaving you able to carry on alone. Plus an interactive five-step career-shift checklist.", body)


def stories():
    order = ["sa", "us", "gulf", "shift", "offer", "team"]
    cards = "".join(story_card(STORY[k], big=(k in ("sa", "team")), glass=(k != "team")) for k in order)
    body = phead("ورا كل CV في إنسان عنده حلم.", "Behind every CV is a person with a dream.",
                 "قصص حكيتها على LinkedIn، بدون أسماء. كل وحدة بلشت من مكان مختلف ووصلت لمكان جديد.",
                 "Stories I've shared on LinkedIn, without names. Each began somewhere different and ended somewhere new.",
                 "ما في شعور أحلى من إنك تكون جزء من الرحلة", "Nothing beats being part of the journey") + f'''
<section style="padding-top:0"><div class="wrap">
  {map_svg()}
  <h2 class="vh">{t("القصص", "Stories")}</h2>
  <div class="stories">{cards}</div>
</div></section>
'''
    return page("stories", "قصص", "Stories",
                "Client stories from Layal Joumaa's LinkedIn: from Syria to the US, Saudi Arabia and the Gulf, career shifts and company teams.", body, kind="CollectionPage")


def about():
    tl = [
        ("2025 – اليوم", "2025 – now", "Personal Brand", "Personal brand", "Assil Design · السعودية (Hybrid)", "Assil Design · Saudi Arabia (hybrid)",
         "بساعد المحترفين يحوّلوا خبرتهم لبراند مهني واضح بيجذب الفرص الصح: CV متوافق مع الـATS، LinkedIn أوضح، وPositioning حسب القطاع والسوق.",
         "Helping professionals turn experience into a clear personal brand that attracts the right opportunities: ATS-ready CVs, sharper LinkedIn, positioning by industry and market.", True),
        ("حزيران 2026", "June 2026", "90,507 ظهور بـ28 يوم", "90,507 impressions in 28 days", "LinkedIn", "LinkedIn",
         "وصل المحتوى لـ35,677 شخص، بزيادة 527% عن الشهر يلي قبله.", "Content reached 35,677 members, up 527% on the month before.", False),
        ("نيسان 2026", "April 2026", "10K متابع", "10K followers", "LinkedIn", "LinkedIn",
         "وصلت لعشرة آلاف متابع، واليوم صاروا أكتر من 14,500.", "Reached ten thousand followers; today it's over 14,500.", False),
        ("2024", "2024", "تطوع مع JCI جبلة", "Volunteering, JCI Jableh", "JCI Syria", "JCI Syria",
         "Social Media Marketing وبعدين Project Coordinator لبرامج تدريب ومعارض وفعاليات. وانختارت أفضل عضو كمصوّرة من بداية الغرفة.",
         "Social media marketing, then project coordinator for trainings, exhibitions and events. Chosen best member as photographer since the chamber began.", False),
        ("2023", "2023", "Assistant Manager", "Assistant manager", "focal X agency · اللاذقية", "focal X agency · Latakia",
         "إدارة فرق التدريب، تنظيم المهام بـTrello وKanban، ومتابعة الـKPIs وتحويلها لتقارير قابلة للتنفيذ.",
         "Led training teams, ran tasks in Trello and Kanban, and turned KPIs into actionable reports.", False),
        ("2023", "2023", "UX Researcher وUI Designer", "UX researcher & UI designer", "focal X agency", "focal X agency",
         "أبحاث ومقابلات مع المستخدمين، Personas وUser Journeys وWireframes، وتصميم واجهات بـFigma. من هون تعلّمت كيف بيقرأ الناس قبل ما يقرروا.",
         "User research and interviews, personas, journeys and wireframes, interfaces in Figma. Where I learned how people read before they decide.", False),
        ("2022 – اليوم", "2022 – now", "Resume Writer مستقلة", "Freelance resume writer", "عن بعد", "Remote",
         "CVs وCover Letters مخصصة من مستوى الخريج للتنفيذي، لقطاعات IT والهندسة والـBusiness والرعاية الصحية.",
         "Tailored CVs and cover letters, entry level to executive, across IT, engineering, business and healthcare.", True),
        ("2017–2022", "2017–2022", "بكالوريوس هندسة البرمجيات ونظم المعلومات", "B.Sc. Software Engineering & Information Systems", "جامعة تشرين", "Tishreen University",
         "تخرّجت Software Engineer، وجرّبت الشغل بمجالي قبل ما يفتحلي الـUI/UX باب الـBranding.",
         "Graduated as a software engineer and worked in the field before UI/UX led me to branding.", False),
    ]
    tl_html = "".join(
        f'<li class="{"now" if now else ""}"><span class="yr">{t(ya, ye)}</span><div class="body"><h3>{t(ha, he)}</h3>'
        f'<p class="org">{t(oa, oe)}</p><p>{t(pa, pe)}</p></div></li>'
        for ya, ye, ha, he, oa, oe, pa, pe, now in tl)
    certs = [("Duolingo English Test", "Duolingo", "2025"), ("UI/UX", "focal X agency", "2023"),
             ("Write Professional Emails in English", "Coursera", "2022"), ("Mastering Excel", "Edraak إدراك", "2022")]
    skills = [("Branding وLinkedIn", "Branding & LinkedIn", ["LinkedIn Marketing", "Branding & Identity", "LinkedIn Recruiter"]),
              ("كتابة الملفات", "Writing", ["Resume Writing", "Resume Review", "UX Writing"]),
              ("التصميم والبحث", "Design & research", ["UX Research", "Mobile UX", "Design Research", "Figma"]),
              ("العمل مع الناس", "Working with people", ["Recruiting", "Leadership", "Communication", "Online Teaching"])]
    # LinkedIn's own five-step proficiency scale
    langs = [("العربية", "Arabic", "اللغة الأم", "Native", 5), ("الإنجليزية", "English", "مستوى عمل احترافي", "Professional working", 3),
             ("الألمانية", "German", "مستوى عمل محدود", "Limited working", 2)]
    seal = '<svg viewBox="0 0 48 48" aria-hidden="true"><path class="ring" d="M24 2l4.2 3.6 5.5-.7 2.4 5 5.1 2.2-.5 5.5L44 22l-3.3 4.4.5 5.5-5.1 2.2-2.4 5-5.5-.7L24 42l-4.2-3.6-5.5.7-2.4-5-5.1-2.2.5-5.5L4 22l3.3-4.4-.5-5.5 5.1-2.2 2.4-5 5.5.7z"/><path class="tick" pathLength="1" d="M16 23l6 6 11-12"/></svg>'
    cert_html = "".join(f'<li style="--k:{i}"><span class="seal">{seal}</span><span class="ct"><b lang="en">{n}</b><small>{o} · {y}</small></span></li>' for i, (n, o, y) in enumerate(certs))
    k = 0
    skill_html = ""
    for a, e, items in skills:
        chips = ""
        for it in items:
            chips += f'<li lang="en" style="--k:{k}">{it}</li>'; k += 1
        skill_html += f'<div class="sg"><p class="sg-t">{t(a, e)}</p><ul class="chipset">{chips}</ul></div>'
    lang_html = "".join(
        f'<li><span class="ln">{t(a, e)}</span><span class="meter" style="--lv:{lv}" role="img" aria-label="{lv}/5">' + "".join(f'<i style="--k:{j}"></i>' for j in range(5)) +
        f'</span><small>{t(la, le)}</small></li>' for a, e, la, le, lv in langs)
    body = f'''
<section class="phead"><div class="wrap about-top">
  <div>
    <h1 class="display">{t("لسا ما وصلت للمكان يلي بدي ياه. وهاد يلي بحبه برحلتي.", "I haven't arrived yet, and that's what I love about the journey.")}</h1>
    <p class="lede">{t("تخرّجت Software Engineer، جرّبت الشغل بمجالي، دخلت عالم الـUI/UX، وبعدين اكتشفت قدّيش بحب الـPersonal Branding. مرّت أوقات وقفت فيها وتعبت وشكّيت بحالي، بس دايماً كنت ارجع اتطلّع لقدّام.",
                       "I graduated as a software engineer, worked in the field, moved into UI/UX, then found how much I love personal branding. There were times I stopped, got tired and doubted myself, but I always came back to looking ahead.")}</p>
    <p class="note">{t("بدي يضل عندي شي جديد اتعلّمه", "I always want something new to learn")}</p>
  </div>
  <div class="frame"><div class="portrait" data-tilt>{pic("layal-portrait", "ليال جمعة", eager=True)}</div></div>
</div></section>

<section class="paper"><div class="wrap">
  {sec_head("الطريق لهون", "The road so far")}
  <div class="trail tl-trail" data-trail><span class="trail-line" aria-hidden="true"><span class="trail-fill"></span><span class="trail-head"></span></span>
  <ol class="tl">{tl_html}</ol></div>
</div></section>

<section><div class="wrap">
  <div class="facts" data-snap>
    <div class="fact certs"><h3>{t("شهادات", "Certificates")}</h3><ul>{cert_html}</ul></div>
    <div class="fact skills"><h3>{t("مهارات", "Skills")}</h3>{skill_html}</div>
    <div class="fact langs"><h3>{t("لغات", "Languages")}</h3><ul>{lang_html}</ul>
      <p class="fol"><b data-count="14552">14,552</b><span>{t("متابع على LinkedIn، وبنشر تقريباً كل يوم", "LinkedIn followers, with a post almost every day")}</span></p></div>
  </div>
</div></section>
'''
    return page("about", "عني", "About",
                "About Layal Joumaa (ليال جمعة): software engineering graduate from Tishreen University, UI/UX and UX research at focal X, JCI volunteer, CV writer since 2022, personal brand at Assil Design.", body, kind="AboutPage")


def ideas():
    chips = f'<button class="chip" type="button" data-f="all" aria-pressed="true">{t("الكل", "All")}</button>' + "".join(
        f'<button class="chip" type="button" data-f="{k}" aria-pressed="false">{t(a, e)}</button>' for k, a, e in TOPICS)
    posts = ""
    for d, dar, den, tp, har, hen, sar, sen in IDEAS:
        ta, te = TOPIC[tp]
        extra = (f' <a class="link" href="method.html">{t("الخطوات الخمسة", "The five steps")}</a>' if d == "2026-09-30" else "")
        posts += f'''<article class="post" data-t="{tp}">
  <div class="post-meta"><time datetime="{d}">{t(dar + " 2026", den + ", 2026")}</time><span class="tp">{t(ta, te)}</span></div>
  <q>{t(har, hen)}</q>
  <p>{t(sar, sen)}</p>
  <p><a class="link" href="{ACT}" rel="noopener" target="_blank">{t("البوست على LinkedIn", "The post on LinkedIn")}</a>{extra}</p>
</article>'''
    body = phead("أفكار بكتبها تقريباً كل يوم على LinkedIn", "Ideas I write on LinkedIn almost every day",
                 "ما بخصص كل يوم وقت للنشر. ساعتين بالأسبوع بختار فيهم المواضيع وبكتب وبجدول، وباقي الأسبوع لعملائي.",
                 "I don't set aside time every day to post. Two hours a week to pick topics, write and schedule; the rest of the week is for clients.",
                 "الاستمرارية بدها نظام", "Consistency needs a system") + f'''
<section style="padding-top:0"><div class="wrap">
  <div class="ideas-tools"><div class="filters" role="group" aria-label="Topics">{chips}</div>
    <button class="btn btn-line small" type="button" id="surprise">✦ {t("فاجئني بفكرة", "Surprise me")}</button></div>
  <p class="vh" id="feedCount" role="status" aria-live="polite"></p>
  <div class="feed">{posts}</div>
  <p class="more"><a class="btn btn-line js-li" href="{ACT}" rel="noopener" target="_blank">{I_LI}{t("كل البوستات على LinkedIn", "All posts on LinkedIn")}</a></p>
</div></section>
'''
    return page("ideas", "أفكار", "Ideas",
                "Layal Joumaa's LinkedIn ideas on CVs, LinkedIn, career shifts, content and the Syrian job market.", body, kind="CollectionPage")


import re as _re

# Hand-drawn style icons for the contact tiles: 32px grid, ink line work,
# a soft blush fill (class f) and one orange accent (class a / filled dot d).
TILE_ICONS = {
    # step 1: where are you now
    "grad": '<path class="f" d="M4 13 16 7l12 6-12 6z"/><path d="M4 13 16 7l12 6-12 6z"/>'
            '<path d="M9 15.6v5.2c0 1.6 3.1 3.2 7 3.2s7-1.6 7-3.2v-5.2"/><path class="a" d="M28 13v6"/><circle class="d" cx="28" cy="21" r="1.6"/>',
    "exp": '<rect class="f" x="4" y="10" width="24" height="16" rx="3"/><rect x="4" y="10" width="24" height="16" rx="3"/>'
           '<path d="M12 10V8a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M4 16.5c7.5 3 16.5 3 24 0"/><path class="a" d="M14.5 18h3"/>',
    "shift": '<path class="f" d="M7 6h15l3.5 3.5L22 13H7z"/><path d="M16 3v26"/><path d="M7 6h15l3.5 3.5L22 13H7z"/>'
             '<path class="a" d="M25 16H11l-3.5 3.5L11 23h14z"/><path d="M12 29h8"/>',
    "team": '<rect class="f" x="7" y="5" width="13" height="22" rx="1.5"/><path d="M7 27V6.5A1.5 1.5 0 0 1 8.5 5h10A1.5 1.5 0 0 1 20 6.5V27"/>'
            '<path d="M20 13h4.5a1.5 1.5 0 0 1 1.5 1.5V27"/><path d="M4 27h24"/><path d="M11 10h1.5M15 10h1.5M11 14h1.5M15 14h1.5M11 18h1.5M15 18h1.5"/>'
            '<path class="a" d="M12.5 27v-4h3v4"/><path d="M22.5 18h1M22.5 22h1"/>',
    # step 2: what should we work on
    "both": '<path d="M12 7V5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2h-7"/><circle class="a" cx="20" cy="9" r="2.2"/>'
            '<path class="a" d="M16.8 16c.6-1.8 1.8-2.7 3.2-2.7s2.6.9 3.2 2.7"/><path class="f" d="M4 10h9l4 4v15H4z"/><path d="M4 10h9l4 4v15H4z"/>'
            '<path d="M13 10v4h4"/><path d="M7.5 19h6M7.5 22.5h6M7.5 26h3.5"/>',
    "cv": '<path class="f" d="M8 4h10l6 6v18H8z"/><path d="M8 4h10l6 6v18H8z"/><path d="M18 4v6h6"/><path d="M12 14.5h8M12 18.5h8"/>'
          '<path class="a" d="M12 23.5l2.2 2.2 4.3-4.3"/>',
    "li": '<rect class="f" x="4" y="6" width="24" height="20" rx="3"/><rect x="4" y="6" width="24" height="20" rx="3"/>'
          '<circle cx="11.5" cy="13.5" r="3"/><path d="M7 22c.8-2.4 2.5-3.6 4.5-3.6s3.7 1.2 4.5 3.6"/><path d="M19 12.5h5M19 16.5h5"/><path class="a" d="M19 20.5h3"/>',
    "cover": '<path class="a" d="M9 13V5.5A1.5 1.5 0 0 1 10.5 4h11A1.5 1.5 0 0 1 23 5.5V13"/><path class="a" d="M13 8.5h6"/>'
             '<rect class="f" x="4" y="11" width="24" height="16" rx="3"/><rect x="4" y="11" width="24" height="16" rx="3"/><path d="m5 12.5 11 7.5 11-7.5"/>',
    "shift2": '<circle class="f" cx="16" cy="16" r="12"/><circle cx="16" cy="16" r="12"/><path d="M16 4v2.5M16 25.5V28M4 16h2.5M25.5 16H28"/>'
              '<path class="a" d="m20.5 11.5-2.8 6.2-6.2 2.8 2.8-6.2z"/><circle class="d" cx="16" cy="16" r="1.2"/>',
    "brand": '<path class="f" d="M5 13v6h4l9 6V7l-9 6z"/><path d="M5 13v6h4l9 6V7l-9 6z"/><path d="M9 19l1.6 6.5h3.2L12.6 21"/>'
             '<path class="a" d="M22 12.5a5 5 0 0 1 0 7M25.5 9.5a9.5 9.5 0 0 1 0 13"/>',
    "people": '<circle class="f" cx="16" cy="11" r="4.5"/><circle cx="16" cy="11" r="4.5"/><path d="M8.5 27c.8-4.2 3.7-6.6 7.5-6.6s6.7 2.4 7.5 6.6"/>'
              '<circle class="a" cx="6.5" cy="13.5" r="2.6"/><circle class="a" cx="25.5" cy="13.5" r="2.6"/>'
              '<path class="a" d="M2.5 24c.5-2.7 2-4.1 4.4-4.4M29.5 24c-.5-2.7-2-4.1-4.4-4.4"/>',
    # step 3: where are you heading
    "gulf": '<path class="f" d="M3 27c4-3.6 9-5.2 13-5.2s9 1.6 13 5.2z"/><path d="M3 27h26"/><path d="M15.5 23c.7-4.5.5-9-1-13"/>'
            '<path d="M14.5 10c-3-2.6-7-2.4-9.5.5M14.5 10c-.5-3.6-3.5-5.6-7-5M14.5 10c2.5-3 6.5-3.5 9.5-1.5M14.5 10c3 .3 5.6 2.6 6.5 5.6"/>'
            '<circle class="d" cx="25.5" cy="5" r="2"/>',
    "sy": '<path class="f" d="M7 13.5 16 6l9 7.5V27H7z"/><path d="M4 15.5 16 5.5l12 10"/><path d="M7 13v14h18V13"/>'
          '<path class="a" d="M16 23.6s-3.6-2.2-3.6-4.7a1.9 1.9 0 0 1 3.6-1 1.9 1.9 0 0 1 3.6 1c0 2.5-3.6 4.7-3.6 4.7z"/>',
    "eu": '<path class="f" d="M4 11 16 5l12 6z"/><path d="M4 11 16 5l12 6z"/><path d="M5 14h22M5 23h22M3.5 26.5h25"/>'
          '<path d="M8 14v9M13 14v9M19 14v9M24 14v9"/><circle class="d" cx="16" cy="8.8" r="1.3"/>',
    "us": '<rect class="f" x="13" y="6" width="7" height="21"/><path d="M3 27h26"/><path d="M5 27V14h6v13M13 27V6h7v21M22 27V11h5v16"/>'
          '<path d="M15.5 10h2M15.5 14h2M15.5 18h2M7.5 18h1M7.5 22h1M24 15h1M24 19h1"/><path class="a" d="M16.5 6V2.5"/>',
    "open": '<path class="f" d="M4 8l7-3 10 3 7-3v19l-7 3-10-3-7 3z"/><path d="M4 8l7-3 10 3 7-3v19l-7 3-10-3-7 3z"/><path d="M11 5v19M21 8v19"/>'
            '<path class="a" d="M6.5 20.5c2-3 4.5-1 6.5-3s2.5-4.5 5-5 3.5 1 5-1"/>',
}


def tile_icon(key):
    body = TILE_ICONS[key]
    # every line (not the soft fills or dots) gets pathLength=1 so it can be drawn on
    body = _re.sub(r'<(path|rect|circle)(?![^>]*class="(?:f|d)")', r'<\1 pathLength="1"', body)
    return f'<svg viewBox="0 0 32 32" aria-hidden="true">{body}</svg>'


def contact():
    def tiles(name, opts):
        out = ""
        for v, em, a, e, ha, he in opts:
            hint = f'<small>{t(ha, he)}</small>' if ha else ""
            out += (f'<label class="tile"><input type="radio" name="{name}" value="{v}"><span class="ti" aria-hidden="true">{tile_icon(em)}</span>'
                    f'<span class="tx"><b>{t(a, e)}</b>{hint}</span><span class="ok" aria-hidden="true">✓</span></label>')
        return out
    stage = [("grad", "grad", "تخرّجت حديثاً", "Just graduated", "بدي أول فرصة حقيقية", "I want my first real job"),
             ("exp", "exp", "عندي خبرة", "I have experience", "بدي ملف يعكسها صح", "I want it to show properly"),
             ("shift", "shift", "عم غيّر مجالي", "Changing fields", "بدون ما خسر يلي بنيته", "Without losing what I built"),
             ("team", "team", "بمثّل شركة", "I represent a company", "بدنا صورة موحّدة لفريقنا", "We want one look for our team")]
    svc = [("both", "both", "CV + LinkedIn", "CV + LinkedIn", "الملف المهني كامل", "The full profile"),
           ("cv", "cv", "CV", "CV", "", ""),
           ("li", "li", "LinkedIn", "LinkedIn", "", ""),
           ("cover", "cover", "Cover Letter", "Cover letter", "", ""),
           ("shift", "shift2", "Career Shift", "Career shift", "", ""),
           ("brand", "brand", "المحتوى والبراند", "Content & brand", "", ""),
           ("team", "people", "فريق الشركة", "Company team", "", "")]
    mkt = [("gulf", "gulf", "الخليج", "The Gulf", "", ""), ("sy", "sy", "سوريا", "Syria", "", ""),
           ("eu", "eu", "أوروبا", "Europe", "", ""), ("us", "us", "أمريكا", "United States", "", ""),
           ("open", "open", "لسا مو محدد", "Not decided yet", "", "")]
    steps = [("وين انت", "You"), ("شو بدك", "Service"), ("لوين", "Market"), ("رسالتك", "Message")]
    step_html = "".join(f'<li><span class="n">{i + 1}</span><span class="l">{t(a, e)}</span></li>' for i, (a, e) in enumerate(steps))
    picks = "".join(f'<button type="button" class="pick" data-for="{n}" data-step="{i}" hidden><span class="pk"></span><span class="ed" aria-hidden="true">✎</span></button>'
                    for i, n in enumerate(["stage", "svc", "market"]))
    body = f'''
<section class="phead slim"><div class="wrap">
  <h1 class="display">{t("خلّي أول رسالة تحكي كل شي.", "Make your first message say it all.")}</h1>
  <p class="lede">{t("3 كبسات وبتطلعلك رسالة جاهزة: مين انت، شو بدك، ولوين رايح. بعدها انسخها وابعتها لليال على LinkedIn.", "Three taps and your message is ready: who you are, what you want and where you're heading. Then copy it and send it to Layal on LinkedIn.")}</p>
</div></section>

<section style="padding-top:0"><div class="wrap contact">
  <div class="wiz" id="wiz">
    <div class="wiz-head">
      <ol class="wiz-steps">{step_html}</ol>
      <div class="wiz-bar" aria-hidden="true"><span></span></div>
    </div>
    <div class="wiz-stage">
      <fieldset class="wiz-pane" data-name="stage">
        <legend class="wiz-q">{t("وين انت هلأ؟", "Where are you right now?")}</legend>
        <p class="wiz-hint">{t("اختار وحدة، ومنكمّل لحالنا", "Pick one and we'll move on")}</p>
        <div class="tiles big">{tiles("stage", stage)}</div>
      </fieldset>
      <fieldset class="wiz-pane" data-name="svc">
        <legend class="wiz-q">{t("شو بدك نشتغل عليه؟", "What should we work on?")}</legend>
        <div class="tiles compact">{tiles("svc", svc)}</div>
      </fieldset>
      <fieldset class="wiz-pane" data-name="market">
        <legend class="wiz-q">{t("لوين رايح؟", "Where are you heading?")}</legend>
        <div class="tiles compact">{tiles("market", mkt)}</div>
      </fieldset>
      <div class="wiz-pane final" role="group" aria-label="Message">
        <div class="picks">{picks}</div>
        <div class="fields">
          <label><span>{t("اسمك", "Your name")}</span><input id="fName" type="text" autocomplete="name" data-ph-ar="اختياري" data-ph-en="Optional"></label>
          <label><span>{t("مجالك", "Your field")}</span><input id="fRole" type="text" autocomplete="organization-title" data-ph-ar="مثلاً: مهندس شبكات" data-ph-en="e.g. network engineer"></label>
        </div>
        <div class="bubble"><div class="out" id="msgOut" aria-live="polite"></div></div>
        <div class="out-acts">
          <button class="btn btn-orange" type="button" id="copyMsg">{t("انسخ الرسالة", "Copy message")}</button>
          <a class="btn btn-ink js-li" href="{LI}" rel="noopener" target="_blank">{I_LI}{t("افتح LinkedIn", "Open LinkedIn")}</a>
        </div>
        <p class="status" id="msgStatus" role="status" aria-live="polite"></p>
      </div>
    </div>
    <div class="wiz-nav">
      <button class="wiz-btn" type="button" id="wizBack">{t("رجوع", "Back")}</button>
      <button class="wiz-btn next" type="button" id="wizNext">{t("التالي", "Next")}</button>
    </div>
  </div>

  <div class="direct">
    <div class="point-wrap frame"><figure class="photo flip">{pic("layal-pointing", "ليال جمعة عم تأشّر على نموذج الرسالة")}</figure>
      <span class="note" aria-hidden="true">{t("من هون 👉 أسرع", "Right here 👉 fastest")}</span></div>
    <h2 class="h3">{t("أو مباشرة", "Or directly")}</h2>
    <a class="row js-li" href="{LI}" rel="noopener" target="_blank"><span class="ic">{I_LI}</span><span><b>LinkedIn</b><small>{t("أسرع طريقة توصلني", "The fastest way to reach me")}</small></span></a>
    <a class="row" id="rowEmail" href="#" hidden><span class="ic">{I_MAIL}</span><span><b>{t("البريد", "Email")}</b><small></small></span></a>
    <a class="row" id="rowWa" href="#" hidden rel="noopener" target="_blank"><span class="ic">{I_WA}</span><span><b>WhatsApp</b><small></small></span></a>
  </div>
</div></section>
'''
    return page("contact", "تواصل", "Contact",
                "Contact Layal Joumaa (ليال جمعة): three taps to a ready first message, then send it on LinkedIn.", body, kind="ContactPage")


# =====================================================================
# Machine-readable layer
# =====================================================================
def llms_txt():
    pages = [("index.html", "Home", "Overview: who she is, services, LinkedIn method and results, headline checker, client stories, FAQ."),
             ("services.html", "Services", "Six services with who each is for and what is included."),
             ("method.html", "Method", "How she works (path, positioning, CV, LinkedIn, independence) and a five-step career-shift checklist."),
             ("stories.html", "Stories", "Six anonymised client stories from her LinkedIn posts, with a map of destinations."),
             ("about.html", "About", "Career timeline, education, certificates, skills, languages and LinkedIn milestones."),
             ("ideas.html", "Ideas", "Summaries of her recent LinkedIn posts by topic."),
             ("contact.html", "Contact", "How to contact her on LinkedIn, with a first-message builder.")]
    out = ["# Layal Joumaa (ليال جمعة)", "",
           "> Layal Joumaa is a Syrian CV & resume writer, LinkedIn optimisation specialist and personal-branding consultant. "
           "She helps new graduates, experienced professionals, career changers and company teams present their real experience "
           "clearly to the market they target in Syria, Saudi Arabia and the Gulf, Europe and the US. Contact: LinkedIn direct message.", "",
           "## Key facts", ""] + [f"- {f}" for f in FACTS_EN] + ["",
           "## Name spellings", "", "- " + "; ".join(NAMES), "",
           "## What people search for when they need her", "", "- English: " + "; ".join(ROLES_EN), "- العربية: " + "؛ ".join(ROLES_AR), "",
           "## Services", ""] + [f"- **{s['en']}** ({s['ar']}): {s['for_en']} Includes: {'; '.join(s['items_en'])}." for s in SERVICES] + ["",
           "## How she works", "",
           "- Starts with the path and target market, then positioning, then builds the CV and LinkedIn so both tell the same story.",
           "- Sees LinkedIn as one system: content attracts, the profile introduces, positioning clarifies value, and the offer turns interest into work.",
           "- Her stated aim: “my job isn't to polish or inflate experience; it's to find the value that is really there and get it to the right person.”", "",
           "## Pages", ""] + [f"- [{n}]({url(p)}): {d}" for p, n, d in pages] + ["",
           "## Optional", "", f"- [Full text of the site]({url('llms-full.txt')})", f"- [LinkedIn profile]({LI})", ""]
    return "\n".join(out)


def llms_full():
    L = [llms_txt(), "", "---", "", "# Full content", "", "## FAQ", ""]
    for qa, qe, aa, ae in FAQ:
        L += [f"### {qe}", ae, "", f"### {qa}", aa, ""]
    L += ["## Client stories (anonymised, from her LinkedIn posts)", ""]
    for s in STORIES:
        L += [f"### {s['h_en']} ({s['stamp_en']}, {s['date_en']})", f"- Start: {s['s_en']}", f"- The work: {s['w_en']}", f"- Result: {s['r_en']}",
              f"### {s['h_ar']} ({s['stamp_ar']})", f"- البداية: {s['s_ar']}", f"- الشغل: {s['w_ar']}", f"- النتيجة: {s['r_ar']}", ""]
    L += ["## Recent LinkedIn ideas", ""]
    for d, dar, den, tp, har, hen, sar, sen in IDEAS:
        L += [f"- {d} [{TOPIC[tp][1]}] {hen} {sen}", f"  - {har} {sar}"]
    L += ["", "## Services in Arabic", ""] + [f"- **{s['ar']}**: {s['for_ar']} {'؛ '.join(s['items_ar'])}" for s in SERVICES] + [""]
    return "\n".join(L)


def robots():
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "anthropic-ai", "PerplexityBot",
            "Perplexity-User", "Google-Extended", "Applebot-Extended", "CCBot", "Meta-ExternalAgent", "DuckAssistBot", "Bingbot", "Googlebot"]
    s = "# Everyone is welcome, including AI assistants and search engines.\nUser-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
    if BASE_URL:
        s += f"Sitemap: {BASE_URL}/sitemap.xml\n"
    return s


def sitemap():
    items = "".join(f"<url><loc>{url(p + '.html')}</loc><lastmod>2026-10-11</lastmod></url>" for p, _, _ in NAV)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>\n'


if __name__ == "__main__":
    pages = {"index": home, "services": services, "method": method, "stories": stories, "about": about, "ideas": ideas, "contact": contact}
    for slug, fn in pages.items():
        with open(os.path.join(OUT, slug + ".html"), "w", encoding="utf-8") as f:
            f.write(fn())
    files = {"llms.txt": llms_txt(), "llms-full.txt": llms_full(), "robots.txt": robots()}
    if BASE_URL:
        files["sitemap.xml"] = sitemap()
    for n, c in files.items():
        with open(os.path.join(OUT, n), "w", encoding="utf-8") as f:
            f.write(c)
    print("built", len(pages), "pages +", ", ".join(files))
