import os, re, markdown, glob

SRC_DIR = "/tmp/arise-90day/jiawubang"

CSS = """
:root{--bg-primary:#070709;--bg-card:#111115;--bg-card-hover:#18181E;--bg-elevated:#1A1A22;--accent:#C8A45E;--accent-dim:#8A7040;--accent-glow:rgba(200,164,94,0.15);--text-primary:#E8E6E3;--text-secondary:#9A9898;--text-muted:#6B6969;--border:#1E1E24;--border-light:#2A2A32}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg-primary);color:var(--text-primary);font-family:'Noto Sans SC','Inter',sans-serif;line-height:1.8;min-height:100vh}
::selection{background:var(--accent);color:var(--bg-primary)}
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:var(--bg-primary)}
::-webkit-scrollbar-thumb{background:var(--border-light);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:var(--accent-dim)}
.hero{padding:80px 24px 60px;text-align:center;border-bottom:1px solid var(--border);position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);width:600px;height:600px;background:radial-gradient(circle,var(--accent-glow) 0%,transparent 70%);pointer-events:none;opacity:.4}
.hero-tag{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:2px;text-transform:uppercase;color:var(--accent);border:1px solid var(--accent-dim);padding:4px 16px;border-radius:20px;margin-bottom:24px}
.hero h1{font-family:'Noto Serif SC',serif;font-size:clamp(28px,5vw,48px);font-weight:900;background:linear-gradient(135deg,var(--text-primary) 0%,var(--accent) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:16px;position:relative}
.main{max-width:800px;margin:0 auto;padding:40px 24px 80px}
.section{margin-bottom:56px}
.section-header{display:flex;align-items:center;gap:12px;margin-bottom:32px;padding-bottom:16px;border-bottom:1px solid var(--border)}
.section-badge{width:4px;height:32px;background:linear-gradient(180deg,var(--accent),var(--accent-dim));border-radius:2px;flex-shrink:0}
.section-num{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--accent);letter-spacing:1px;margin-bottom:4px}
.section-title{font-family:'Noto Serif SC',serif;font-size:clamp(20px,3vw,28px);font-weight:700;color:var(--text-primary)}
.card{background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:28px;margin-bottom:20px;transition:all .25s ease}
.card:hover{border-color:var(--border-light);background:var(--bg-card-hover);transform:translateY(-1px)}
.card-title{font-family:'Noto Serif SC',serif;font-size:clamp(18px,2.5vw,24px);font-weight:700;color:var(--text-primary);margin-bottom:24px;padding-left:16px;border-left:3px solid var(--accent)}
.sub-title{font-family:'Noto Serif SC',serif;font-size:18px;font-weight:700;color:var(--text-primary);margin:28px 0 16px;padding-left:12px;border-left:3px solid var(--accent-dim)}
p{color:var(--text-secondary);margin-bottom:16px;font-size:15px;line-height:1.9}
strong{color:var(--text-primary);font-weight:600}
em{color:var(--accent);font-style:italic}
blockquote{background:var(--bg-elevated);border-left:3px solid var(--accent);border-radius:0 8px 8px 0;padding:20px 24px;margin:20px 0;font-size:14px;color:var(--text-secondary);line-height:1.8}
hr{border:none;height:1px;background:var(--border);margin:40px 0}
.formula{background:var(--bg-elevated);border:1px solid var(--border-light);border-radius:8px;padding:16px 24px;margin:16px 0;font-family:'JetBrains Mono',monospace;font-size:14px;color:var(--accent);text-align:center}
li{color:var(--text-secondary);font-size:15px;line-height:1.8;margin-bottom:8px;padding-left:8px;list-style:none}
li::before{content:'\\203A';color:var(--accent);font-weight:700;margin-right:8px}
ul,ol{margin-bottom:16px;padding-left:8px}
table{width:100%;border-collapse:collapse;margin:20px 0;font-size:14px}
th{background:var(--bg-elevated);color:var(--accent);font-weight:600;text-align:left;padding:12px 16px;border:1px solid var(--border-light)}
td{color:var(--text-secondary);padding:10px 16px;border:1px solid var(--border)}
tr:nth-child(even) td{background:rgba(26,26,34,0.5)}
.nav-bar{position:sticky;top:0;z-index:100;background:rgba(7,7,9,0.95);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:12px 24px;overflow-x:auto}
.nav-inner{max-width:800px;margin:0 auto;display:flex;gap:8px;flex-wrap:nowrap}
.nav-pill{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.5px;padding:6px 14px;border-radius:6px;border:1px solid var(--border);background:transparent;color:var(--text-muted);cursor:pointer;transition:all .2s;white-space:nowrap;text-decoration:none}
.nav-pill:hover,.nav-pill.active{border-color:var(--accent-dim);color:var(--accent);background:var(--accent-glow)}
@media(max-width:640px){.hero{padding:60px 16px 40px}.main{padding:24px 16px 60px}.card{padding:20px}blockquote{padding:16px 18px}}
"""

# Map filenames to display info
file_info = {}
md_files = sorted(glob.glob(os.path.join(SRC_DIR, "M*.md")), key=lambda x: int(re.search(r'M(\d+)', os.path.basename(x)).group(1)))

for f in md_files:
    num = int(re.search(r'M(\d+)', os.path.basename(f)).group(1))
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    # Extract first line as title
    first_line = content.strip().split('\n')[0].lstrip('#').strip()
    file_info[num] = {'file': f, 'title': first_line}

def extract_sections(md_text):
    """Extract ## level headings for nav bar"""
    sections = []
    for m in re.finditer(r'^## (.+)$', md_text, re.MULTILINE):
        title = m.group(1).strip()
        anchor = 'sec-' + re.sub(r'[^\w\u4e00-\u9fff]', '', title.replace(' ', '-'))
        sections.append((title, anchor))
    return sections

def md_to_structured_html(md_text):
    """Convert markdown to structured HTML with sections and cards"""
    # Split by ## headings
    parts = re.split(r'^(## .+)$', md_text, flags=re.MULTILINE)
    
    # First part is the title and intro
    intro = parts[0].strip()
    # Remove the # title line
    intro = re.sub(r'^# .+\n', '', intro).strip()
    # Convert intro markdown
    intro_html = markdown.markdown(intro, extensions=['tables', 'fenced_code'])
    
    sections_html = []
    sec_num = 0
    i = 1
    while i < len(parts):
        heading = parts[i]  # "## Section Title"
        body = parts[i+1] if i+1 < len(parts) else ""
        sec_num += 1
        
        title = heading.lstrip('#').strip()
        anchor = 'sec-' + re.sub(r'[^\w\u4e00-\u9fff]', '', title.replace(' ', '-'))
        
        # Split body by ### sub-headings
        sub_parts = re.split(r'^(### .+)$', body.strip(), flags=re.MULTILINE)
        
        # First sub_part may be intro text before any ###
        sub_html = ""
        j = 0
        if sub_parts and not sub_parts[0].startswith('### '):
            sub_html += markdown.markdown(sub_parts[0], extensions=['tables', 'fenced_code'])
            j = 1
        else:
            j = 0
        
        while j < len(sub_parts):
            sub_heading = sub_parts[j]
            sub_body = sub_parts[j+1] if j+1 < len(sub_parts) else ""
            sub_title = sub_heading.lstrip('#').strip()
            sub_html += f'<h4 class="sub-title">{sub_title}</h4>\n'
            sub_html += markdown.markdown(sub_body, extensions=['tables', 'fenced_code'])
            j += 2
        
        section_block = f'''<div class="section" id="{anchor}">
<div class="section-header"><div class="section-badge"></div><div><div class="section-num">SECTION {sec_num:02d}</div><h2 class="section-title">{title}</h2></div></div>
<div class="card">{sub_html}</div>
</div>'''
        sections_html.append(section_block)
        i += 2
    
    return intro_html, sections_html

for num, info in file_info.items():
    with open(info['file'], 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # Extract full title from first # line
    full_title = info['title']
    # Short title for hero
    short_title = full_title
    if ' ' in full_title:
        # Remove "M1 " prefix if present
        short_title = re.sub(r'^M\d+\s*', '', full_title)
    
    sections = extract_sections(md_text)
    intro_html, sections_html = md_to_structured_html(md_text)
    
    # Build nav
    nav_pills = ''.join(f'<a class="nav-pill" href="#{anchor}">{title}</a>' for title, anchor in sections)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>M{num} · {short_title} — 加五磅 · 三天营养课</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700;900&family=Noto+Sans+SC:wght@300;400;500;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="hero">
<div class="hero-tag">MODULE {num:02d}</div>
<h1>{short_title}</h1>
<p style="color:var(--text-secondary);font-size:16px;max-width:600px;margin:0 auto">加五磅 · 三天营养课</p>
</div>
<div class="nav-bar"><div class="nav-inner">{nav_pills}</div></div>
<div class="main">
{intro_html}
{''.join(sections_html)}
<div style="text-align:center;margin-top:60px;padding-top:40px;border-top:1px solid var(--border)">
<p style="color:var(--text-muted);font-size:13px">3HFIT · Arise · 加五磅 · 三天营养课</p>
</div>
</div>
</body>
</html>"""
    
    out_path = os.path.join(SRC_DIR, f"M{num}.html")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated M{num}.html - {short_title}")

print(f"\nDone! Generated {len(file_info)} HTML files.")
