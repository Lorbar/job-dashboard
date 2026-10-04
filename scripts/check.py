#!/usr/bin/env python3
"""Daily link check. Stdlib only. Reads ROLES urls from index.html, writes status.json.
States: live | closed | unknown (JS-only pages can't be judged from raw HTML)."""
import re, json, urllib.request, urllib.error, datetime, os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html=open(os.path.join(root,"index.html"),encoding="utf8").read()
roles=re.findall(r'\{id:"([^"]+)",co:"[^"]*",title:"[^"]*".*?url:"([^"]+)"',html,re.S)
prev={}
try: prev=json.load(open(os.path.join(root,"status.json")))
except Exception: pass
added=prev.get("added",[])
for a in added: roles.append((a["id"],a["url"]))
DEAD=re.compile(r"no longer (available|accepting)|page not found|job (not found|has been (closed|filled))|position (has been|is no longer)|has expired|been filled|couldn.t find that|404",re.I)
def check(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (job-dashboard link checker)"})
    try:
        with urllib.request.urlopen(req,timeout=25) as r:
            body=r.read(400000).decode("utf8","ignore"); final=r.geturl()
    except urllib.error.HTTPError as e:
        return ("closed","HTTP %d"%e.code) if e.code in(404,410) else ("unknown","HTTP %d"%e.code)
    except Exception as e:
        return "unknown","fetch error"
    host=re.sub(r"^https?://([^/]+).*",r"\1",url)
    path=lambda u:re.sub(r"^https?://[^/]+","",u).split("?")[0].rstrip("/")
    if path(final)!=path(url) and "careers.cisco.com" in host: return "closed","redirected to home"
    text=re.sub(r"<(script|style)[^>]*>.*?</\1>","",body,flags=re.S); text=re.sub(r"<[^>]+>"," ",text)
    if DEAD.search(text[:6000]) and len(text)<20000: return "closed","page says unavailable"
    if "amazon.jobs" in host:
        return ("live","description present") if re.search(r"Basic Qualifications|Description",text) else ("closed","empty page")
    if len(re.sub(r"\s+","",text))>2500 and re.search(r"(Responsibilit|Qualifications|Requirements|About the (job|role))",text,re.I): return "live","job text present"
    return "unknown","JS-rendered or inconclusive"
now=datetime.datetime.utcnow().replace(microsecond=0).isoformat()
out={"checkedAt":now,"roles":{},"added":added,"log":[]}
for rid,url in roles:
    st,why=check(url); old=prev.get("roles",{}).get(rid,{}).get("state")
    out["roles"][rid]={"state":st,"checked":now,"note":why}
    if old and old!=st: out["log"].append(f"{rid}: {old} → {st} ({why})")
json.dump(out,open(os.path.join(root,"status.json"),"w"),indent=1)
print(json.dumps(out["log"] or ["no changes"]))
