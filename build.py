"""Build the static GraphViX website. Python standard library only."""
import json
from hashlib import sha1
from pathlib import Path
from html import escape as e
ROOT=Path(__file__).resolve().parent
D=json.loads((ROOT/'content.json').read_text())
CSS_VERSION=sha1((ROOT/'assets/site.css').read_bytes()).hexdigest()[:10]
JS_VERSION=sha1((ROOT/'assets/site.js').read_bytes()).hexdigest()[:10]
P=json.loads((ROOT/'publications.json').read_text())
IMAGES=json.loads((ROOT/'assets/image-manifest.json').read_text()) if (ROOT/'assets/image-manifest.json').exists() else {}
def image_src(path): return e(IMAGES.get(path,{}).get('src',path))
def image_size(path):
 info=IMAGES.get(path)
 return f' width="{info["width"]}" height="{info["height"]}"' if info else ''
def paper_id(p): return 'paper-'+sha1(p['title'].encode()).hexdigest()[:12]
NAV=[('index','Home'),('research','Research'),('publications','Publications'),('people','People'),('join','Join us')]
def header(page):
 links=''.join(f'<a href="{slug}.html" '+('aria-current="page" ' if slug==page else '')+f'>{label}</a>' for slug,label in NAV)
 return f'''<a class="skip" href="#main">Skip to content</a><header class="site-header wrap"><div class="header-identity"><div class="header-lab"><a class="brand" href="index.html" aria-label="GraphViX Lab home">GraphVi<span>X</span><small class="brand-lab">Lab</small></a><a class="header-university-text" href="https://www.ed.ac.uk/">University of Edinburgh</a></div><a class="header-university" href="https://www.ed.ac.uk/" aria-label="The University of Edinburgh"><img src="assets/university-of-edinburgh.png" alt="The University of Edinburgh" width="831" height="199"></a></div><button class="menu-toggle" aria-label="Open navigation" aria-expanded="false" aria-controls="nav">Menu <span>+</span></button><nav id="nav" aria-label="Main navigation">{links}</nav></header>'''
def footer():
 return '''<footer class="wrap"><div><a class="brand" href="index.html">GraphVi<span>X</span><small class="brand-lab">Lab</small></a><p>Graphics, Vision and X<br>University of Edinburgh</p></div><div class="footer-links"><a href="mailto:Changjian.li@ed.ac.uk">Get in touch ↗</a><a href="https://enigma-li.github.io/">Changjian Li ↗</a><a href="https://informatics.ed.ac.uk/">School of Informatics ↗</a></div><div class="footer-bottom"><span>Edinburgh, United Kingdom</span><span>Exploring what comes next.</span></div></footer>'''
def card(p,description=None):
 info=p['research']
 record='publications.html#'+paper_id(p)
 url=next((link['url'] for label in ('Project','Paper','arXiv Preprint') for link in p['links'] if link['label']==label),record)
 subtitle=description or (p['title'].split(':',1)[1].strip() if ':' in p['title'] else p['title'])
 links=''.join(f'<a href="{e(link["url"])}">{e(link["label"])} ↗</a>' for link in p['links'] if link['label'] in ('Paper','arXiv Preprint','Code','Code & data'))
 links+=f'<a href="{record}" aria-label="Publication details for {e(p["title"])}">Details →</a>'
 return f'''<article class="project-card" data-topic="{e(info['area'])}"><a class="project-image" href="{e(url)}" aria-label="{e(p['title'])}"><img src="{image_src(p['image'])}"{image_size(p['image'])} alt="{e(p['title'])} — research preview" loading="lazy" decoding="async"><span class="image-arrow" aria-hidden="true">↗</span></a><div class="card-meta"><span>{e(info['venue'])} · {p['year']}</span></div><h3><a href="{e(url)}">{e(info['name'])}</a></h3><p>{e(subtitle)}</p>{'<span class="award">'+e(p['award'])+'</span>' if p.get('award') else ''}<div class="pub-links">{links}</div></article>'''
def projects(items): return '<div class="project-grid">'+''.join(card(p) for p in items)+'</div>'
def page_title(kicker,title,desc): return f'<section class="page-title"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="lede">{desc}</p></section>'
def cta(): return '<section class="join-banner"><div><p class="eyebrow">Build what comes next</p><h2>Curious minds welcome.</h2></div><a class="button" href="join.html">Join the lab <span>↗</span></a></section>'
home=f'''<section class="opening" aria-labelledby="opening-title"><div class="opening-lead"><p class="eyebrow"><span class="status-dot"></span> University of Edinburgh · School of Informatics</p><h1 id="opening-title">GraphVi<span class="name-x">X</span> <span class="name-lab">Lab</span></h1><p class="opening-tagline">Graphics. Vision. <em>And beyond.</em></p><p class="opening-intro">{e(D['home']['intro'])}</p></div><div class="opening-work"><div class="opening-work-heading"><p class="eyebrow">Research in focus</p><div class="opening-work-tools"><a href="research.html">All research <span aria-hidden="true">↗</span></a><button id="demo-motion" type="button" aria-pressed="false">Pause motion <span aria-hidden="true">Ⅱ</span></button></div></div><div class="opening-directions opening-selected" aria-label="Explore our research directions">'''
for area in D['home']['featured']:
 project=next(p for p in D['projects'] if p['name']==area['project'])
 theme=next(t for t in D['research'] if t['id']==area['research_area'])
 if area.get('video'):
  media=f'<video muted loop playsinline preload="auto" aria-label="{e(project["name"])} research demonstration"><source src="assets/{e(area["video"])}" type="video/mp4"></video>'
 else:
  media=f'<img src="assets/{e(project["image"])}" alt="{e(project["name"])} research demonstration" decoding="async">'
 home+=f'''<a class="opening-direction" href="research.html#{e(theme['id'])}"><div class="opening-preview">{media}</div><div class="opening-direction-label"><h2>{e(theme['title'])}</h2><span aria-hidden="true">↗</span></div><p class="opening-caption">{e(area['caption'])}</p></a>'''
home+='</div></div></section>'
opening_footer='''<footer class="opening-footer wrap"><p>Led by <a href="https://enigma-li.github.io/">Changjian Li</a><span class="footer-separator"> · </span><a href="https://informatics.ed.ac.uk/">School of Informatics</a></p></footer>'''
research=page_title('What we explore','Creating across dimensions.','We connect geometry, learning and interaction to understand, create and animate the visual world.')
research+='<nav class="research-index" aria-label="Research themes">'+''.join(f'<a href="#{e(area["id"])}">{e(area["short_title"])} <span aria-hidden="true">↘</span></a>' for area in D['research'])+'</nav>'
for i,area in enumerate(D['research'],1):
 items=sorted([p for p in P if p['research']['area']==area['id'] and p['research'].get('show_on_research',True)],key=lambda p:p['year'],reverse=True)
 research+=''.join(f'<span id="{e(alias)}" aria-hidden="true"></span>' for alias in area.get('legacy_ids',[]))
 research+=f'<section id="{e(area["id"])}" class="research-area"><div class="area-heading"><span class="number">0{i}</span><h2>{e(area["title"])}</h2><div><p class="research-question">{e(area["question"])}</p><p>{e(area["description"])}</p></div></div>'
 selected=[]
 research+='<div class="project-grid" aria-label="Selected projects">'
 features={f['name']:f for f in area['featured']}
 for paper in items:
  feature=features.get(paper['research']['name'])
  if feature is None: continue
  selected.append(paper)
  markup=card(paper,feature['description'])
  research+=markup
 research+='</div>'
 if area.get('related'):
  label=e(area.get('related_title','Related work'))
  research+=f'<div class="design-works"><p class="design-works-label">{label}</p><div class="design-work-grid">'
  for feature in area['related']:
   p=next(p for p in items if p['research']['name']==feature['name'])
   selected.append(p)
   research+=f'<a class="design-work" href="publications.html#{paper_id(p)}"><div class="design-work-image"><img src="{image_src(p["image"])}"{image_size(p["image"])} alt="" loading="lazy" decoding="async"></div><div><p class="design-work-meta">{e(p["research"]["venue"])} · {p["year"]}</p><h3>{e(p["research"]["name"])} <span aria-hidden="true">↗</span></h3><p class="design-work-description">{e(feature["description"])}</p></div></a>'
  research+='</div></div>'
 remaining=[p for p in items if p not in selected]
 if remaining:
  research+=f'<details class="more-research"><summary>More work in this direction <span class="more-count">({len(remaining)})</span><span class="expand-mark" aria-hidden="true">+</span></summary><ul class="research-paper-list">'
  for p in remaining:
   research+=f'<li><span class="research-paper-year">{p["year"]}</span><a href="publications.html#{paper_id(p)}">{e(p["title"])}<span class="research-paper-venue">{e(p["research"]["venue"])}</span></a><span class="research-paper-arrow" aria-hidden="true">↗</span></li>'
  research+='</ul></details>'
 research+='</section>'
research+='<p class="research-scope research-archive">These themes bring together work by Changjian Li and collaborators, including research before the lab was established in Edinburgh. <a href="publications.html">Browse all publications →</a></p>'
research+='<section class="news-section"><div><p class="eyebrow">From the group</p><h2>Latest news</h2></div><div>'+''.join(f'<a class="news-row" href="{e(n["url"])}"><time datetime="{n["date"]}">{n["label"]}</time><span>{e(n["text"])}</span><span aria-hidden="true">↗</span></a>' for n in D['news'])+'</div></section>'+cta()
years=sorted({p['year'] for p in P if p['year']>=2020},reverse=True)
if any(p['year']<2020 for p in P): years.append('before-2020')
def year_label(year): return 'Before 2020' if year=='before-2020' else str(year)
pubs=page_title('Research output','Publications.','Work by Changjian Li and collaborators, spanning graphics, vision and interdisciplinary applications.')
options=''.join(f'<option value="{year}">{year_label(year)}</option>' for year in years)
pubs+=f'''<div class="publication-tools"><label class="year-select" for="publication-year">Year <select id="publication-year"><option value="all">All years</option>{options}</select></label><label class="search"><span class="sr-only">Search publications</span><input id="publication-search" type="search" placeholder="Search title, author, venue…"><span aria-hidden="true">⌕</span></label></div><div class="publication-status"><p id="result-count" class="result-count" aria-live="polite">{len(P)} publications</p><p class="author-legend">* Equal contribution · # Corresponding author</p></div><div class="publication-list">'''
for year in years:
 pubs+=f'<section class="publication-year-group" aria-labelledby="year-{year}"><h2 class="publication-year-heading" id="year-{year}">{year_label(year)}</h2>'
 for p in sorted([p for p in P if p['year']==year or (year=='before-2020' and p['year']<2020)],key=lambda p:p['year'],reverse=True):
  primary=next((l['url'] for l in p['links'] if l['label']=='Project'),next((l['url'] for l in p['links'] if l['label'] in ('Paper','arXiv Preprint')),None))
  image=f'<img src="{image_src(p["image"])}"{image_size(p["image"])} alt="{e(p["title"])} — research preview" loading="lazy" decoding="async">'
  image_html=f'<a href="{e(primary)}" class="publication-image">{image}</a>' if primary else f'<div class="publication-image">{image}</div>'
  title=f'<a href="{e(primary)}">{e(p["title"])}</a>' if primary else e(p['title'])
  authors=e(p['authors']).replace('Changjian Li','<strong>Changjian Li</strong>').replace('*','<sup>*</sup>').replace('#','<sup>#</sup>')
  links=''.join(f'<a href="{e(l["url"])}">{e(l["label"])} ↗</a>' for l in p['links'])
  award=f'<span class="award">{e(p["award"])}</span>' if p.get('award') else ''
  pubs+=f'''<article class="publication" id="{paper_id(p)}" data-year="{p['year']}">{image_html}<div><h3>{title}</h3><p class="authors">{authors}</p><p class="publication-venue">{e(p['venue'])}</p><div class="pub-links">{links}</div>{award}</div></article>'''
 pubs+='</section>'
pubs+='</div><p id="empty-results" hidden>No matching publications. Try another title, author, venue or year.</p>'
people=page_title('The lab','People behind the ideas.','We are a lab of researchers exploring graphics, vision and the space between them, based in Edinburgh.')
people+='<nav class="people-index" aria-label="People sections"><a href="#current-members">Current members</a><a href="#alumni">Alumni</a></nav><section class="people-grid" id="current-members" aria-label="Current members">'+''.join(f'''<article class="person"><a class="portrait" href="{e(p['url'])}" aria-label="{e(p['name'])} homepage"><img src="{image_src('assets/'+p['image'])}" alt="{e(p['name'])}" loading="lazy" decoding="async" width="104" height="120"></a><div class="person-info"><h2><a href="{e(p['url'])}">{e(p['name'])}<span aria-hidden="true"> ↗</span></a></h2><p>{e(p['role'])}</p></div></article>''' for p in D['people'])+'</section>'
people+='<section class="alumni-section" id="alumni" aria-labelledby="alumni-title"><div class="alumni-heading"><h2 id="alumni-title">Alumni</h2><p>Former members and students, and their next destinations.</p></div>'
for group in D['alumni']:
 people+=f'<section class="alumni-group"><h3>{e(group["title"])}</h3><ul class="alumni-list">'
 for member in group['members']:
  name=f'<a href="{e(member["url"])}">{e(member["name"])} <span aria-hidden="true">↗</span></a>' if member.get('url') else e(member['name'])
  role=f'<p class="alumni-role">{e(member["role"])}</p>' if member.get('role') else ''
  destination=f'<p class="alumni-destination"><span class="sr-only">Next destination: </span>{e(member["destination"])}</p>' if member.get('destination') else ''
  note=f'<p class="alumni-note">{e(member["note"])}</p>' if member.get('note') else ''
  people+=f'<li class="alumni-row"><div class="alumni-identity"><p class="alumni-name">{name}</p>{role}</div><p class="alumni-period">{e(member["period"])}</p><div class="alumni-next">{destination}{note}</div></li>'
 people+='</ul></section>'
people+='<p class="alumni-source">Dates and destinations from <a href="https://enigma-li.github.io/">Changjian Li’s alumni list ↗</a>.</p></section>'+cta()
join=page_title('Join GraphViX','Make your next<br>discovery here.','Interested in graphics, vision, geometry or creative tools? We would love to hear about your research interests.')
join+='''<section class="join-layout"><div><div class="opportunity"><span class="number">01</span><div><h2>Doctoral research</h2><p>Explore a PhD at the intersection of computer graphics and computer vision. Contact Changjian with your CV and a short introduction to your interests.</p><a class="text-link" href="https://informatics.ed.ac.uk/study-with-us/our-degrees/postgraduate-research-programmes-and-centres-doctoral-training/postgraduate-research-and-cdts/postgraduate-research-funding-opportunities">Informatics PhD funding information ↗</a></div></div><div class="opportunity"><span class="number">02</span><div><h2>Research & visiting students</h2><p>We welcome enquiries about MSc by Research, visiting research and internships. Tell us about your background, the questions you want to explore and your proposed dates.</p></div></div></div><aside class="contact-panel"><p class="eyebrow">Start a conversation</p><h2>Say hello.</h2><a class="email" href="mailto:Changjian.li@ed.ac.uk">Changjian.li@ed.ac.uk ↗</a><p>Include your CV and a brief description of your research interests.</p><hr><p class="eyebrow">Find us</p><address>Informatics Forum<br>10 Crichton Street<br>Edinburgh, EH8 9AB<br>United Kingdom</address><a class="text-link" href="https://enigma-li.github.io/">PI homepage & current opportunities ↗</a></aside></section>'''
SITE='https://graphvix-lab.github.io'
DESCRIPTIONS={
 'index':'GraphViX Lab at the University of Edinburgh, School of Informatics. We develop intuitive ways to understand, create and animate the 3D world.',
 'research':'Explore GraphViX Lab research in interactive CAD, sketch-based shape modeling, controllable animation, and 3D reconstruction and understanding.',
 'publications':'Publications by Changjian Li and collaborators in computer graphics, computer vision and geometric modeling.',
 'people':'Meet GraphViX Lab at the University of Edinburgh: Changjian Li, current researchers and alumni.',
 'join':'Explore research opportunities with GraphViX Lab in the School of Informatics at the University of Edinburgh.',
 '404':'This page could not be found. Explore GraphViX Lab at the University of Edinburgh.'
}
not_found=page_title('404 · Page not found','A different direction.','The page you are looking for may have moved or the address may be incorrect.')+'<p><a class="button" href="index.html">Back to home <span>↗</span></a></p>'
pages=[('index','Graphics, Vision and X',home),('research','Research',research),('publications','Publications',pubs),('people','People',people),('join','Join us',join),('404','Page not found',not_found)]
for slug,title,body in pages:
 page_class='opening-page' if slug=='index' else ('research-page' if slug=='research' else '')
 page_footer=opening_footer if slug=='index' else footer()
 page_title_text=e(title+' — GraphViX Lab')
 description=e(DESCRIPTIONS[slug])
 canonical=SITE+('/' if slug=='index' else '/'+slug+'.html')
 extra='<base href="/"><meta name="robots" content="noindex">' if slug=='404' else f'<link rel="canonical" href="{canonical}">'
 html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{extra}<meta name="description" content="{description}"><meta name="theme-color" content="#f8f9f5"><title>{page_title_text}</title><meta property="og:type" content="website"><meta property="og:site_name" content="GraphViX Lab"><meta property="og:title" content="{page_title_text}"><meta property="og:description" content="{description}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}/assets/social-card.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="GraphViX Lab — Graphics. Vision. And beyond. — University of Edinburgh"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css?v={CSS_VERSION}"><script src="assets/site.js?v={JS_VERSION}" defer></script></head><body class="{page_class}">{header(slug)}<main id="main" class="wrap">{body}</main>{page_footer}</body></html>'''
 (ROOT/(slug+'.html')).write_text(html)
urls=''.join('<url><loc>'+SITE+('/' if slug=='index' else '/'+slug+'.html')+'</loc></url>' for slug,_,_ in pages if slug!='404')
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls+'</urlset>\n')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+SITE+'/sitemap.xml\n')
print('Built 6 pages, sitemap.xml and robots.txt.')
