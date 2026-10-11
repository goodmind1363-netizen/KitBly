import re,os,json,shutil,html as H
import pathlib
ROOT=pathlib.Path(__file__).resolve().parent
S=open(ROOT/'src'/'toolbench.html',encoding='utf-8').read()
D="https://kitbly.com";LG=["en","fr","de"];NM={"en":"English","fr":"Français","de":"Deutsch"}
blk=re.search(r'const T=\{(.*?)\n\};',S,re.S).group(1)
T={m.group(1):dict(re.findall(r'(\w+):"((?:[^"\\]|\\.)*)"',m.group(2))) for m in re.finditer(r'^(en|fr|de):\{(.*)\},?$',blk,re.M)}
X={'en':dict(upl='Upload (Mbps)',unav='Unavailable on this network',done='Done'),'fr':dict(upl='Envoi (Mb/s)',unav='Indisponible sur ce réseau',done='Terminé'),'de':dict(upl='Upload (Mbit/s)',unav='In diesem Netzwerk nicht verfügbar',done='Fertig')}
X2={'en':dict(pdfh='PDF compressor',pdfin='Choose a PDF',lvl='Compression',lv1='Light',lv2='Medium',lv3='Strong',cmp='Compress',pnote='Pages are saved as images, so text can no longer be selected or searched.',pbig='The result is not smaller than the original, so keeping the original is the better choice.',perr='This PDF could not be processed.',page='Page',s6p='Shrink PDFs for email and forms, right in your browser.'),
'fr':dict(pdfh='Compresseur de PDF',pdfin='Choisir un PDF',lvl='Compression',lv1='Légère',lv2='Moyenne',lv3='Forte',cmp='Compresser',pnote='Les pages sont enregistrées en images : le texte ne peut plus être sélectionné ni recherché.',pbig='Le résultat n’est pas plus léger que l’original : gardez plutôt l’original.',perr='Ce PDF n’a pas pu être traité.',page='Page',s6p='Allégez vos PDF pour l’e-mail et les formulaires, directement dans votre navigateur.'),
'de':dict(pdfh='PDF-Verkleinerer',pdfin='PDF auswählen',lvl='Komprimierung',lv1='Leicht',lv2='Mittel',lv3='Stark',cmp='Komprimieren',pnote='Seiten werden als Bilder gespeichert, Text lässt sich danach nicht mehr markieren oder durchsuchen.',pbig='Das Ergebnis ist nicht kleiner als das Original, behalten Sie besser das Original.',perr='Dieses PDF konnte nicht verarbeitet werden.',page='Seite',s6p='Verkleinern Sie PDFs für E-Mail und Formulare direkt im Browser.')}
for l in LG:T[l].update(X[l]);T[l].update(X2[l])
COL={'loan':'#E5383B','percent':'#FF9F1C','words':'#1F8A4C','image':'#2447F5','speed':'#7B2CBF','pdf':'#D6336C'}
for l in LG: assert 'credit' in T[l] and 'a3p' in T[l] and 'err' in T[l],l
css=re.search(r'<style>(.*?)</style>',S,re.S).group(1).replace('"Bricolage Grotesque"','"Avenir Next"').replace('"Instrument Sans"','"Segoe UI"')
css+='''.s6{background:#D6336C;color:#fff}.s6 a{background:#fff;color:#8E1B45}
.pb{position:relative;height:16px;border-radius:99px;overflow:hidden;margin-top:16px;background:linear-gradient(90deg,#E5383B,#FF9F1C,#FFD60A,#2A9D55,#2447F5,#7B2CBF)}.pb i{position:absolute;right:0;top:0;bottom:0;width:100%;background:var(--line);transition:width .15s}
a.tool{display:block;text-decoration:none;color:inherit}a.tool:hover{border-color:var(--blue)}
.crumb{font-size:.88rem;color:var(--mut);margin:6px 0 14px}.crumb a{color:var(--mut)}.page{max-width:720px}
.page h1{font-size:clamp(1.8rem,5vw,2.6rem);margin-bottom:10px}.lead{color:var(--mut);margin:0 0 22px}.page p{margin:0 0 14px}
.faq{margin-top:34px}.faq h2{font-size:1.25rem;margin-bottom:10px}.faq h3{font-size:1.02rem;margin:14px 0 4px}.faq p{color:var(--mut)}
.note{margin-top:22px;padding:14px;border:1px dashed var(--line);border-radius:10px;color:var(--mut)}
header a.nl{color:var(--ink);font-weight:600;text-decoration:none}header div{display:flex;gap:14px;align-items:center}'''
css+='''html:root:root:root{--bg:#060A08;--ink:#E9F6EE;--mut:#93AE9C;--card:#0E1712;--line:#1D3025;--blue:#2EE57D;--lime:#2EE57D;--on-blue:#04130A;--on-lime:#04130A;color-scheme:dark}
body{background:radial-gradient(900px 420px at 12% -8%,rgba(46,229,125,.18),transparent 60%),radial-gradient(700px 380px at 105% 0,rgba(123,44,191,.14),transparent 60%),var(--bg);background-attachment:fixed}
.tool{transition:transform .2s,box-shadow .2s,border-color .2s}a.tool:hover{border-color:var(--blue);box-shadow:0 10px 30px rgba(46,229,125,.14)}
.btn{box-shadow:0 0 0 0 rgba(46,229,125,.5)}.btn:hover:not(:disabled){filter:brightness(1.1);box-shadow:0 6px 20px rgba(46,229,125,.3)}
h2.sec::after{content:"";display:block;width:46px;height:4px;border-radius:4px;background:var(--blue);margin-top:8px}
.logo b{box-shadow:0 0 18px rgba(46,229,125,.45)}.out strong{color:var(--blue)}
.lang{background:var(--card);color:var(--ink)}input[type=range]{accent-color:var(--blue)}
@media(prefers-reduced-motion:reduce){.tool,a.tool:hover{transition:none;transform:none}}
'''
SLUG={"home":("","",""),"loan":("loan-calculator","calculateur-de-pret","kreditrechner"),"percent":("percentage-calculator","calculateur-de-pourcentage","prozentrechner"),
"words":("word-counter","compteur-de-mots","wortzaehler"),"image":("image-converter","convertisseur-d-images","bildkonverter"),"speed":("connection-test","test-de-connexion","verbindungstest"),
"pdf":("pdf-compressor","compresseur-de-pdf","pdf-verkleinern"),"articles":("articles","articles","artikel"),"about":("about","a-propos","ueber-uns"),"privacy":("privacy","confidentialite","datenschutz"),"contact":("contact","contact","kontakt")}
def path(l,k):
    i=LG.index(l)
    if isinstance(k,tuple):return f"/{l}/{SLUG['articles'][i]}/{ART[k[1]][l]['slug']}/"
    s=SLUG[k][i]
    return f"/{l}/{s}/" if s else f"/{l}/"
TOOLS=["loan","percent","words","image","pdf","speed"];NAME={"loan":"s1h","percent":"s2h","words":"s3h","image":"imgh","speed":"spd","pdf":"pdfh"}
ART={};ART_LANG={l:[] for l in LG}
def parse_fm(txt):
    m=re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$',txt.replace('\r\n','\n'),re.S)
    if not m:return {},txt
    meta={};lines=m.group(1).split('\n');i=0
    while i<len(lines):
        ln=lines[i];i+=1
        if not ln.strip() or ln[0] in ' #-' or ':' not in ln:continue
        k,v=ln.split(':',1);k=k.strip();v=v.strip()
        if v in('>','>-','>+','|','|-','|+'):
            buf=[]
            while i<len(lines) and (lines[i].startswith(' ') or not lines[i].strip()):buf.append(lines[i].strip());i+=1
            v=(' ' if v[0]=='>' else '\n').join(x for x in buf if x)
        elif len(v)>1 and v[0]==v[-1] and v[0] in '"\'':
            q=v[0];v=v[1:-1];v=v.replace('\\"','"').replace('\\\\','\\') if q=='"' else v.replace("''","'")
        meta[k]=v
    return meta,m.group(2)
def inline(t):
    t=re.sub(r'`([^`]+)`',r'<code>\1</code>',t)
    t=re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)',r'<img src="\2" alt="\1" loading="lazy">',t)
    t=re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)',r'<a href="\2">\1</a>',t)
    t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
    t=re.sub(r'(?<![\w*])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![\w*])',r'<em>\1</em>',t)
    return t
def md(src):
    out=[];st={"p":[],"l":None,"c":None}
    def fp():
        if st["p"]:out.append('<p>'+inline(' '.join(st["p"]))+'</p>');st["p"]=[]
    def fl():
        if st["l"]:out.append(f'<{st["l"][0]}>'+''.join('<li>'+inline(x)+'</li>' for x in st["l"][1])+f'</{st["l"][0]}>');st["l"]=None
    for raw in src.replace('\r\n','\n').split('\n'):
        if raw.strip().startswith('```'):
            if st["c"] is None:fp();fl();st["c"]=[]
            else:out.append('<pre><code>'+H.escape('\n'.join(st["c"]))+'</code></pre>');st["c"]=None
            continue
        if st["c"] is not None:st["c"].append(raw);continue
        ln=H.escape(raw.rstrip(),quote=False)
        m=re.match(r'^(#{1,4})\s+(.*)$',ln)
        if m:
            fp();fl();n=max(2,len(m.group(1)));out.append(f'<h{n}>{inline(m.group(2))}</h{n}>');continue
        m=re.match(r'^\s*([-*+]|\d+[.)])\s+(.*)$',ln)
        if m:
            fp();kind='ol' if m.group(1)[0].isdigit() else 'ul'
            if st["l"] and st["l"][0]!=kind:fl()
            if not st["l"]:st["l"]=(kind,[])
            st["l"][1].append(m.group(2));continue
        if not ln.strip():fp();fl();continue
        if ln.startswith('&gt; '):fp();fl();out.append('<blockquote>'+inline(ln[5:])+'</blockquote>');continue
        if re.match(r'^(-{3,}|\*{3,})$',ln.strip()):fp();fl();out.append('<hr>');continue
        if st["l"] and not ln.startswith(' '):fl()
        st["p"].append(ln.strip())
    fp();fl()
    return ''.join(out)
for l in LG:
    d=ROOT/'content'/l
    if not d.is_dir():continue
    for f in sorted(d.glob('*.md')):
        meta,body=parse_fm(f.read_text(encoding='utf-8'))
        if meta.get('draft','').lower()=='true' or not meta.get('title'):continue
        aid=meta.get('id') or f.stem;w=len(re.findall(r'\S+',body))
        ART.setdefault(aid,{})[l]=dict(slug=f.stem,title=meta['title'],desc=meta.get('description',''),cat=meta.get('category','money'),tool=meta.get('tool',''),date=(meta.get('date','') or '')[:10],body=md(body),min=max(1,-(-w//220)))
        ART_LANG[l].append(aid)
def arts(l):return sorted(ART_LANG[l],key=lambda a:(ART[a][l]['date'],a),reverse=True)
CATS=["money","text","images","internet"];CATCOL={"money":"#E5383B","text":"#1F8A4C","images":"#2447F5","internet":"#7B2CBF"}
CATN={"en":{"money":"Money & calculators","text":"Text & writing","images":"Images & PDF","internet":"Internet & speed"},"fr":{"money":"Argent et calculs","text":"Texte et rédaction","images":"Images et PDF","internet":"Internet et débit"},"de":{"money":"Geld & Rechner","text":"Text & Schreiben","images":"Bilder & PDF","internet":"Internet & Tempo"}}
def langs_for(k):
    if isinstance(k,tuple):return [x for x in LG if x in ART[k[1]]]
    if k=="articles":return [x for x in LG if ART_LANG[x]]
    return LG
def opt_path(x,k):
    if isinstance(k,tuple) and x not in ART[k[1]]:return path(x,"articles") if ART_LANG[x] else path(x,"home")
    if k=="articles" and not ART_LANG[x]:return path(x,"home")
    return path(x,k)
css+='''.prose h2{font-size:1.35rem;margin:28px 0 10px}.prose h3{font-size:1.1rem;margin:20px 0 6px}.prose p,.prose li{line-height:1.7}.prose ul,.prose ol{padding-left:22px;margin:0 0 14px}.prose li{margin:4px 0}.prose a{color:var(--blue)}.prose img{max-width:100%;height:auto;border-radius:10px}.prose blockquote{margin:14px 0;padding:8px 14px;border-left:4px solid var(--blue);color:var(--mut)}.prose code{background:var(--card);padding:1px 5px;border-radius:5px}.prose pre{overflow-x:auto;background:var(--card);padding:12px;border-radius:10px}.meta{color:var(--mut);font-size:.9rem;margin:0 0 8px}.tag{display:inline-block;font-size:.75rem;font-weight:600;letter-spacing:.02em;padding:2px 9px;border-radius:99px;border:1px solid var(--line);color:var(--mut);margin-bottom:8px}.cta{margin:26px 0 6px}
'''
N={"en":dict(home="Home",arts="Articles",rel="Related article",reltool="Related tool",draft="The full article text will be published here.",tag="Free online calculators and tools that run in your browser."),
"fr":dict(home="Accueil",arts="Articles",rel="Article associé",reltool="Outil associé",draft="Le texte complet de l’article sera publié ici.",tag="Des calculateurs et outils en ligne gratuits, directement dans votre navigateur."),
"de":dict(home="Startseite",arts="Artikel",rel="Passender Artikel",reltool="Passendes Tool",draft="Der vollständige Artikeltext wird hier veröffentlicht.",tag="Kostenlose Online-Rechner und Tools direkt in Ihrem Browser.")}
TT={"pdf":[("Make PDF files smaller to send by email or upload to a form. Choose a compression level, and the file is processed on your device.","Will the text still be searchable?","No. This tool saves each page as a compressed image, so text can no longer be selected or searched. It works best for scans and image-heavy PDFs."),
("Réduisez le poids de vos PDF pour les envoyer par e-mail ou les déposer dans un formulaire. Choisissez un niveau de compression ; le fichier est traité sur votre appareil.","Le texte reste-t-il recherchable ?","Non. Cet outil enregistre chaque page sous forme d’image compressée, le texte ne peut donc plus être sélectionné ni recherché. Il convient surtout aux scans et aux PDF riches en images."),
("Verkleinern Sie PDF-Dateien für den E-Mail-Versand oder Formular-Uploads. Wählen Sie eine Komprimierungsstufe; die Datei wird auf Ihrem Gerät verarbeitet.","Bleibt der Text durchsuchbar?","Nein. Das Tool speichert jede Seite als komprimiertes Bild, daher lässt sich Text nicht mehr markieren oder durchsuchen. Am besten eignet es sich für Scans und bildlastige PDFs.")],
"loan":[("Estimate your monthly payment and total interest for a fixed-rate loan. Enter the amount, the yearly interest rate and the term.","How is the monthly payment calculated?","It uses the standard annuity formula: each payment covers the interest for the month plus part of the principal, so the payment stays the same. Fees and insurance are not included."),
("Estimez votre mensualité et le total des intérêts d’un prêt à taux fixe. Saisissez le montant, le taux annuel et la durée.","Comment la mensualité est-elle calculée ?","Le calcul utilise la formule d’annuité classique : chaque échéance couvre les intérêts du mois et une part du capital, donc la mensualité reste constante. Les frais et l’assurance ne sont pas inclus."),
("Berechnen Sie Rate und Gesamtzinsen für einen Kredit mit festem Zins. Geben Sie Betrag, Jahreszins und Laufzeit ein.","Wie wird die monatliche Rate berechnet?","Die Berechnung nutzt die übliche Annuitätenformel: Jede Rate deckt die Monatszinsen und einen Teil der Tilgung, sodass sie gleich bleibt. Gebühren und Versicherungen sind nicht enthalten.")],
"percent":[("Find a percentage of any number, such as a discount, a tip or a tax amount.","How do I calculate a percentage of a number?","Multiply the number by the percentage and divide by 100. For example, 15% of 240 is 240 × 15 ÷ 100 = 36."),
("Calculez le pourcentage d’un nombre : remise, pourboire ou montant de taxe.","Comment calculer un pourcentage d’un nombre ?","Multipliez le nombre par le pourcentage puis divisez par 100. Par exemple, 15 % de 240 font 240 × 15 ÷ 100 = 36."),
("Berechnen Sie den Prozentwert einer Zahl, etwa für Rabatt, Trinkgeld oder Steuer.","Wie berechne ich einen Prozentwert?","Multiplizieren Sie die Zahl mit dem Prozentsatz und teilen Sie durch 100. Beispiel: 15 % von 240 sind 240 × 15 ÷ 100 = 36.")],
"words":[("Count words and characters and estimate reading time while you type or paste text.","How is reading time estimated?","We assume an average adult reads about 220 words per minute and round up to the next full minute."),
("Comptez les mots et les caractères et estimez le temps de lecture pendant que vous écrivez ou collez un texte.","Comment le temps de lecture est-il estimé ?","Nous partons d’une lecture moyenne d’environ 220 mots par minute et arrondissons à la minute supérieure."),
("Zählen Sie Wörter und Zeichen und schätzen Sie die Lesezeit, während Sie Text eingeben oder einfügen.","Wie wird die Lesezeit geschätzt?","Wir gehen von etwa 220 Wörtern pro Minute aus und runden auf die nächste volle Minute auf.")],
"image":[("Convert images between JPG, PNG and WebP directly in your browser and compare the file size before and after.","Are my images uploaded anywhere?","No. The conversion happens on your device, so your image never leaves your browser."),
("Convertissez vos images entre JPG, PNG et WebP directement dans le navigateur et comparez la taille avant et après.","Mes images sont-elles envoyées quelque part ?","Non. La conversion se fait sur votre appareil, votre image ne quitte jamais votre navigateur."),
("Konvertieren Sie Bilder zwischen JPG, PNG und WebP direkt im Browser und vergleichen Sie die Dateigröße davor und danach.","Werden meine Bilder hochgeladen?","Nein. Die Umwandlung erfolgt auf Ihrem Gerät, Ihr Bild verlässt Ihren Browser nie.")],
"speed":[("Measure your download speed and latency with one click.","Why does my result change between tests?","Speed varies with Wi-Fi signal, other devices on your network and server load. Run the test a few times and compare."),
("Mesurez votre débit descendant et votre latence en un clic.","Pourquoi le résultat varie-t-il d’un test à l’autre ?","Le débit dépend du signal Wi-Fi, des autres appareils du réseau et de la charge du serveur. Lancez le test plusieurs fois et comparez."),
("Messen Sie Download-Tempo und Latenz mit einem Klick.","Warum ändert sich das Ergebnis zwischen Tests?","Das Tempo hängt von WLAN-Signal, anderen Geräten im Netzwerk und der Serverauslastung ab. Testen Sie mehrmals und vergleichen Sie.")]}
LEG={"en":{"about":["Kitbly offers free online tools that run in your browser. We build them to be fast, clear and private.","Questions or ideas for new tools? Write to contact@kitbly.com."],
"privacy":["Most Kitbly tools run entirely in your browser. The numbers, text and images you use are not sent to our servers.","We plan to show ads through Google AdSense. Google and its partners may use cookies to personalize ads. Where the law requires it, we ask for your consent first, and you can change your choice at any time.","For questions about your data, write to contact@kitbly.com."],
"contact":["For questions, feedback or tool ideas, write to contact@kitbly.com."]},
"fr":{"about":["Kitbly propose des outils en ligne gratuits qui fonctionnent dans votre navigateur. Nous les concevons rapides, clairs et respectueux de votre vie privée.","Une question ou une idée d’outil ? Écrivez à contact@kitbly.com."],
"privacy":["La plupart des outils Kitbly fonctionnent entièrement dans votre navigateur. Les nombres, textes et images que vous utilisez ne sont pas envoyés à nos serveurs.","Nous prévoyons d’afficher des publicités via Google AdSense. Google et ses partenaires peuvent utiliser des cookies pour personnaliser les annonces. Lorsque la loi l’exige, nous demandons d’abord votre consentement, et vous pouvez modifier votre choix à tout moment.","Pour toute question sur vos données, écrivez à contact@kitbly.com."],
"contact":["Pour toute question, remarque ou idée d’outil, écrivez à contact@kitbly.com."]},
"de":{"about":["Kitbly bietet kostenlose Online-Tools, die in Ihrem Browser laufen. Wir entwickeln sie schnell, übersichtlich und datensparsam.","Fragen oder Ideen für neue Tools? Schreiben Sie an contact@kitbly.com."],
"privacy":["Die meisten Kitbly-Tools laufen vollständig in Ihrem Browser. Zahlen, Texte und Bilder, die Sie verwenden, werden nicht an unsere Server gesendet.","Wir planen, Werbung über Google AdSense anzuzeigen. Google und seine Partner können Cookies verwenden, um Anzeigen zu personalisieren. Wo das Gesetz es verlangt, holen wir zuerst Ihre Einwilligung ein, und Sie können Ihre Wahl jederzeit ändern.","Bei Fragen zu Ihren Daten schreiben Sie an contact@kitbly.com."],
"contact":["Bei Fragen, Feedback oder Tool-Ideen schreiben Sie an contact@kitbly.com."]}}
JS_LOAN='function calc(){const a=+$("la").value||0,r=(+$("lr").value||0)/1200,n=Math.max(1,(+$("ly").value||1)*12),m=r?a*r/(1-Math.pow(1+r,-n)):a/n,c={maximumFractionDigits:2,minimumFractionDigits:2};$("lm").textContent=nf(m,c);$("li").textContent=nf(m*n-a,c)}["la","lr","ly"].forEach(i=>$(i).addEventListener("input",calc));calc();'
JS_PCT='function calc(){$("pr").textContent=nf((+$("pa").value||0)*(+$("pb").value||0)/100,{maximumFractionDigits:4})}["pa","pb"].forEach(i=>$(i).addEventListener("input",calc));calc();'
JS_WORDS=r'function calc(){const v=$("wt").value,t=v.trim(),w=t?t.split(/\s+/).length:0;$("ww").textContent=nf(w);$("wc").textContent=nf(v.length);$("wr").textContent=nf(Math.max(w?1:0,Math.ceil(w/220)))}$("wt").addEventListener("input",calc);calc();'
JS_IMG=r'''let blobUrl;$("imgGo").onclick=()=>{const f=$("imgF").files[0];if(!f)return;const fm=$("imgFmt").value,q=+$("imgQ").value/100,im=new Image();
im.onload=()=>{const c=document.createElement("canvas");c.width=im.width;c.height=im.height;const x=c.getContext("2d");if(fm==="image/jpeg"){x.fillStyle="#fff";x.fillRect(0,0,c.width,c.height)}x.drawImage(im,0,0);
c.toBlob(b=>{if(blobUrl)URL.revokeObjectURL(blobUrl);blobUrl=URL.createObjectURL(b);const a=$("imgDl");a.href=blobUrl;a.download=f.name.replace(/\.[^.]+$/,"")+"."+fm.split("/")[1].replace("jpeg","jpg");a.hidden=false;$("imgSz").textContent=(f.size/1024).toFixed(0)+" KB → "+(b.size/1024).toFixed(0)+" KB"},fm,q);URL.revokeObjectURL(im.src)};im.src=URL.createObjectURL(f)};'''
JS_PDF=r'''let pdUrl;$("pdGo").onclick=async()=>{const f=$("pdF").files[0];if(!f)return;const cfg={light:[2,.85],medium:[1.5,.7],strong:[1,.55]}[$("pdL").value],bar=$("pdBar"),ph=$("pdPh"),set=p=>{bar.style.width=(100-p)+"%"},kb=n=>nf(n/1024,{maximumFractionDigits:0})+" KB";
$("pdGo").disabled=true;$("pdErr").textContent="";$("pdDl").hidden=true;set(0);
try{const [pj,pl]=await Promise.all([import("/assets/pdfjs.js"),import("/assets/pdflib.js")]);pj.GlobalWorkerOptions.workerSrc="/assets/pdfjs-worker.js";
const doc=await pj.getDocument({data:await f.arrayBuffer()}).promise,out=await pl.PDFDocument.create();
for(let i=1;i<=doc.numPages;i++){ph.textContent=MSG.page+" "+i+"/"+doc.numPages;const pg=await doc.getPage(i),v1=pg.getViewport({scale:1});let sc=cfg[0];const mx=Math.max(v1.width,v1.height)*sc;if(mx>3000)sc*=3000/mx;
const vp=pg.getViewport({scale:sc}),cv=document.createElement("canvas");cv.width=Math.ceil(vp.width);cv.height=Math.ceil(vp.height);const cx=cv.getContext("2d");cx.fillStyle="#fff";cx.fillRect(0,0,cv.width,cv.height);
await pg.render({canvasContext:cx,viewport:vp}).promise;const bl=await new Promise(r=>cv.toBlob(r,"image/jpeg",cfg[1]));const im=await out.embedJpg(await bl.arrayBuffer());
out.addPage([v1.width,v1.height]).drawImage(im,{x:0,y:0,width:v1.width,height:v1.height});cv.width=cv.height=0;pg.cleanup();set(100*i/doc.numPages)}
const bytes=await out.save({useObjectStreams:true}),blob=new Blob([bytes],{type:"application/pdf"});$("pdSz").textContent=kb(f.size)+" → "+kb(blob.size);ph.textContent="";
if(blob.size>=f.size){$("pdErr").textContent=MSG.big}else{if(pdUrl)URL.revokeObjectURL(pdUrl);pdUrl=URL.createObjectURL(blob);const a=$("pdDl");a.href=pdUrl;a.download=f.name.replace(/\.pdf$/i,"")+"-compressed.pdf";a.hidden=false}
}catch(e){$("pdErr").textContent=MSG.err+" ("+(e&&e.message?e.message:e)+")";ph.textContent=""}$("pdGo").disabled=false};'''
JS_SPEED='''const up=(set,live,n1)=>new Promise((res,rej)=>{const n=4*1024*1024,x=new XMLHttpRequest(),b=new Blob([new Uint8Array(n)],{type:"text/plain"});let t0=0;x.open("POST","https://speed.cloudflare.com/__up");x.timeout=15000;
x.upload.onloadstart=()=>t0=performance.now();
x.upload.onprogress=e=>{const s=(performance.now()-t0)/1000;if(s>0){live.textContent=n1(e.loaded*8/1e6/s);set(60+40*e.loaded/n)}};
x.upload.onload=()=>res(n*8/1e6/((performance.now()-t0)/1000));x.onerror=x.ontimeout=()=>rej();x.send(b)});
$("spGo").onclick=async()=>{const n1=v=>nf(v,{maximumFractionDigits:1}),u=Date.now(),bar=$("spBar"),ph=$("spPh"),live=$("spL"),set=p=>{bar.style.width=(100-p)+"%"};
$("spGo").disabled=true;$("spErr").textContent="";["spP","spD","spU"].forEach(i=>$(i).textContent="–");live.textContent="–";set(0);
try{ph.textContent=PH[0];let t=performance.now();const p=await fetch("/assets/probe.txt?"+u,{cache:"no-store"});if(!p.ok)throw new Error("probe HTTP "+p.status);await p.text();const lat=performance.now()-t;$("spP").textContent=n1(lat);live.textContent=n1(lat);set(10);
ph.textContent=PH[1];t=performance.now();const r=await fetch("/assets/sample.dat?"+u,{cache:"no-store"});if(!r.ok)throw new Error("sample HTTP "+r.status);const tot=+r.headers.get("content-length")||8388608,rd=r.body.getReader();let got=0;
for(;;){const c=await rd.read();if(c.done)break;got+=c.value.length;live.textContent=n1(got*8/1e6/((performance.now()-t)/1000));set(10+50*got/tot)}
const dl=got*8/1e6/((performance.now()-t)/1000);$("spD").textContent=n1(dl);live.textContent=n1(dl);set(60);
ph.textContent=PH[2];try{const ul=await up(set,live,n1);$("spU").textContent=n1(ul);live.textContent=n1(ul)}catch(e){$("spU").textContent=NA}
set(100);ph.textContent=DONE}catch(e){$("spErr").textContent=ERR+" ("+(e&&e.message?e.message:e)+")"}$("spGo").disabled=false};'''
def tool(k,t):
    if k=="pdf":return (f'<section class="tool"><label for="pdF">{t["pdfin"]}</label><input id="pdF" type="file" accept="application/pdf,.pdf"><label for="pdL">{t["lvl"]}</label><select id="pdL" class="in"><option value="light">{t["lv1"]}</option><option value="medium" selected>{t["lv2"]}</option><option value="strong">{t["lv3"]}</option></select><button class="btn" id="pdGo">{t["cmp"]}</button><a class="btn" id="pdDl" hidden>{t["dl"]}</a><div class="pb" aria-hidden="true"><i id="pdBar"></i></div><div id="pdPh" style="margin-top:10px;color:var(--mut);font-size:.9rem" aria-live="polite">&nbsp;</div><p style="color:var(--mut);font-size:.9rem;margin:10px 0 0">{t["pnote"]}</p><p id="pdErr" style="color:var(--mut);font-size:.9rem;margin:8px 0 0"></p><div class="out"><div><span>{t["sz"]}</span><strong id="pdSz">–</strong></div></div></section>','const MSG='+json.dumps({"big":t["pbig"],"err":t["perr"],"page":t["page"]},ensure_ascii=False)+';'+JS_PDF)
    if k=="loan":return (f'<section class="tool"><label for="la">{t["amt"]}</label><input id="la" type="number" inputmode="decimal" value="20000" min="0"><label for="lr">{t["rate"]}</label><input id="lr" type="number" inputmode="decimal" value="5.5" min="0" step="0.1"><label for="ly">{t["term"]}</label><input id="ly" type="number" inputmode="decimal" value="5" min="1"><div class="out"><div><span>{t["mon"]}</span><strong id="lm"></strong></div><div><span>{t["int"]}</span><strong id="li"></strong></div></div></section>',JS_LOAN)
    if k=="percent":return (f'<section class="tool"><label for="pa">{t["what"]}</label><div class="row"><input id="pa" type="number" inputmode="decimal" value="15"><span>{t["of"]}</span></div><label for="pb">&nbsp;</label><input id="pb" type="number" inputmode="decimal" value="240"><div class="out"><div><span>{t["res"]}</span><strong id="pr"></strong></div></div></section>',JS_PCT)
    if k=="words":return (f'<section class="tool"><label for="wt">{t["ph"]}</label><textarea id="wt"></textarea><div class="out"><div><span>{t["w"]}</span><strong id="ww">0</strong></div><div><span>{t["c"]}</span><strong id="wc">0</strong></div><div><span>{t["rt"]}</span><strong id="wr">0</strong></div></div></section>',JS_WORDS)
    if k=="image":return (f'<section class="tool"><label for="imgF">{t["imgin"]}</label><input id="imgF" type="file" accept="image/*"><label for="imgFmt">{t["fmt"]}</label><select id="imgFmt" class="in"><option value="image/jpeg">JPG</option><option value="image/png">PNG</option><option value="image/webp">WebP</option></select><label for="imgQ">{t["qual"]}</label><input id="imgQ" type="range" min="40" max="100" value="85"><button class="btn" id="imgGo">{t["conv"]}</button><a class="btn" id="imgDl" hidden>{t["dl"]}</a><div class="out"><div><span>{t["sz"]}</span><strong id="imgSz">–</strong></div></div></section>',JS_IMG)
    return (f'<section class="tool"><button class="btn" id="spGo">{t["go"]}</button><div class="pb" aria-hidden="true"><i id="spBar"></i></div><div id="spPh" style="margin-top:10px;color:var(--mut);font-size:.9rem" aria-live="polite">&nbsp;</div><div id="spL" style="font:800 2.6rem/1.1 system-ui,sans-serif;margin:4px 0">–</div><p id="spErr" style="color:var(--mut);font-size:.9rem;margin:0"></p><div class="out"><div><span>{t["dlm"]}</span><strong id="spD">–</strong></div><div><span>{t["upl"]}</span><strong id="spU">–</strong></div><div><span>{t["png"]}</span><strong id="spP">–</strong></div></div></section>','const ERR='+json.dumps(t["err"],ensure_ascii=False)+',NA='+json.dumps(t["unav"],ensure_ascii=False)+',DONE='+json.dumps(t["done"],ensure_ascii=False)+',PH='+json.dumps([t["png"],t["dlm"],t["upl"]],ensure_ascii=False)+';'+JS_SPEED)
ICON="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22%3E%3Ctext y=%22.9em%22 font-size=%2290%22%3E🧰%3C/text%3E%3C/svg%3E"
def layout(l,k,title,desc,main,js="",ld=""):
    t=T[l];e=lambda s:H.escape(s,quote=True)
    ls=langs_for(k);alts="".join(f'<link rel="alternate" hreflang="{x}" href="{D}{path(x,k)}">' for x in ls)+f'<link rel="alternate" hreflang="x-default" href="{D}{path("en" if "en" in ls else ls[0],k)}">'
    opts="".join(f'<option value="{opt_path(x,k)}"{" selected" if x==l else ""}>{NM[x]}</option>' for x in LG)
    nlk=f'<a class="nl" href="{path(l,"articles")}">{N[l]["arts"]}</a>' if ART_LANG[l] else ""
    foot=f'<footer><span>{t["priv"]}</span><span>{t["credit"]}</span><nav><a href="{path(l,"about")}">{t["about"]}</a><a href="{path(l,"privacy")}">{t["pp"]}</a><a href="{path(l,"contact")}">{t["contact"]}</a></nav></footer>'
    return (f'<!DOCTYPE html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{D}{path(l,k)}">{alts}<link rel="icon" href="{ICON}">{ld}<style>{css}</style></head>'
    f'<body><div class="wrap"><header><a class="logo" href="{path(l,"home")}" style="text-decoration:none;color:inherit"><b>Kit</b>bly</a><div>{nlk}<select class="lang" aria-label="Language" onchange="nav(this.value)">{opts}</select></div></header>{main}{foot}</div>'
    f'<script>function nav(u){{location.href=u}}const $=i=>document.getElementById(i),LOC="{t["loc"]}",nf=(v,o)=>new Intl.NumberFormat(LOC,o).format(v);{js}</script></body></html>')
def crumb(l,*parts):return f'<nav class="crumb" aria-label="Breadcrumb"><a href="{path(l,"home")}">{N[l]["home"]}</a>'+"".join(" / "+p for p in parts)+'</nav>'
N["en"].update(mins="min read",more="More articles",relp="Related articles")
N["fr"].update(mins="min de lecture",more="Autres articles",relp="Articles associés")
N["de"].update(mins="Min. Lesezeit",more="Weitere Artikel",relp="Passende Artikel")
def card(l,a):
    x=ART[a][l];c=x['cat']
    return f'<a class="tool" style="border-top:4px solid {CATCOL.get(c,"#2EE57D")}" href="{path(l,("a",a))}"><span class="tag">{H.escape(CATN[l].get(c,c))}</span><h3>{H.escape(x["title"])}</h3><p style="color:var(--mut);margin:0 0 12px">{H.escape(x["desc"])}</p><span style="font-weight:600;color:var(--blue)">{T[l]["read"]} – {x["min"]} {N[l]["mins"]}</span></a>'
def acards(l,items):return "".join(card(l,a) for a in items)
SLIDES=[("s1",'<div class="bars" aria-hidden="true"><i style="height:70px"></i><i style="height:120px"></i><i style="height:170px"></i><i style="height:210px"></i></div>',"s1h","s1p","loan"),
("s2",'<div class="art" aria-hidden="true">%</div>',"s2h","s2p","percent"),("s3",'<div class="art" aria-hidden="true">Aa</div>',"s3h","s3p","words"),
("s4",'<div class="art" aria-hidden="true" style="font-size:8rem;bottom:-10px">JPG</div>',"imgh","s4p","image"),("s5",'<div class="art" aria-hidden="true">↓</div>',"spd","s5p","speed"),("s6",'<div class="art" aria-hidden="true" style="font-size:9rem">PDF</div>',"pdfh","s6p","pdf")]
SLJS=S.rsplit("/* slider */",1)[1].split("go(0);restart();")[0]+"go(0);restart();"
SLJS=SLJS.replace("N=5,","N=6,")
pages={}
for l in LG:
    t=T[l];n=N[l];i=LG.index(l)
    sl="".join(f'<div class="slide {c}">{a}<h2>{t[h]}</h2><p>{t[p]}</p><a href="{path(l,k)}">{t["open"]}</a></div>' for c,a,h,p,k in SLIDES)
    slider=f'<div class="rb"></div><section class="slider" aria-roledescription="carousel" aria-label="Kitbly"><div class="track" id="track">{sl}</div><div class="nav"><div class="dots" id="dots"></div><div class="arrows"><button id="prev" aria-label="Previous">&#8592;</button><button id="next" aria-label="Next">&#8594;</button></div></div></section>'
    tc="".join(f'<a class="tool" style="border-top:4px solid {COL[k]}" href="{path(l,k)}"><h3>{t[NAME[k]]}</h3><p style="color:var(--mut);margin:0">{TT[k][i][0]}</p></a>' for k in TOOLS)
    ab=f'<h2 class="sec" style="margin-top:44px">{t["art"]}</h2><div class="grid">{acards(l,arts(l)[:6])}</div><p style="margin-top:18px"><a class="nl" style="color:var(--blue);font-weight:600;text-decoration:none" href="{path(l,"articles")}">{n["more"]} →</a></p>' if ART_LANG[l] else ""
    main=f'<h1 style="font-size:1.05rem;margin:14px 0;color:var(--mut);font-weight:600">{n["tag"]}</h1>{slider}<h2 class="sec">{t["all"]}</h2><div class="grid">{tc}</div>{ab}'
    pages[path(l,"home")]=layout(l,"home","Kitbly – "+t["all"],n["tag"],main,SLJS)
    for k in TOOLS:
        intro,q,a=TT[k][i];th,js=tool(k,t);name=t[NAME[k]];th=th.replace('<section class="tool"','<section class="tool" style="border-top:4px solid '+COL[k]+'"',1)
        ra=[a for a in arts(l) if ART[a][l]['tool']==k][:3];rel=f'<h2 class="sec" style="font-size:1.3rem;margin-top:34px">{n["relp"]}</h2><div class="grid">{acards(l,ra)}</div>' if ra else ""
        ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}]},ensure_ascii=False)+'</script>'
        main=f'<div class="page">{crumb(l,name)}<h1>{name}</h1><p class="lead">{intro}</p>{th}<section class="faq"><h2>FAQ</h2><h3>{q}</h3><p>{a}</p></section></div>{rel}'
        pages[path(l,k)]=layout(l,k,f"{name} – Kitbly",intro,main,js,ld)
    if ART_LANG[l]:
        order=CATS+sorted({ART[a][l]['cat'] for a in ART_LANG[l]}-set(CATS));secs=""
        for c in order:
            it=[a for a in arts(l) if ART[a][l]['cat']==c]
            if it:secs+=f'<h2 class="sec" style="margin-top:34px">{H.escape(CATN[l].get(c,c))}</h2><div class="grid">{acards(l,it)}</div>'
        pages[path(l,"articles")]=layout(l,"articles",f'{n["arts"]} – Kitbly',n["tag"],f'<div class="page" style="max-width:none">{crumb(l,n["arts"])}<h1>{n["arts"]}</h1>{secs}</div>')
        for a in ART_LANG[l]:
            x=ART[a][l];tk=x['tool'];tl=''
            if tk in NAME:tl=f'<div class="cta"><a class="btn" href="{path(l,tk)}">{t[NAME[tk]]} →</a></div>'
            rl=[b for b in arts(l) if b!=a and ART[b][l]['cat']==x['cat']][:3]
            rb=f'<h2 class="sec" style="font-size:1.3rem;margin-top:36px">{n["more"]}</h2><div class="grid">{acards(l,rl)}</div>' if rl else ''
            ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Article","headline":x['title'],"description":x['desc'],"datePublished":x['date'],"inLanguage":l,"author":{"@type":"Organization","name":"Kitbly"},"publisher":{"@type":"Organization","name":"Kitbly"}},ensure_ascii=False)+'</script>'
            cn=H.escape(CATN[l].get(x['cat'],x['cat']))
            main=f'<article class="page">{crumb(l,"<a href=\""+path(l,"articles")+"\">"+n["arts"]+"</a>",H.escape(x["title"]))}<p class="meta"><span class="tag">{cn}</span> {x["date"]} – {x["min"]} {n["mins"]}</p><h1>{H.escape(x["title"])}</h1><p class="lead">{H.escape(x["desc"])}</p><div class="prose">{x["body"]}</div>{tl}</article>{rb}'
            pages[path(l,("a",a))]=layout(l,("a",a),f'{x["title"]} – Kitbly',x['desc'],main,"",ld)
    for k in("about","privacy","contact"):
        nm=t[{"about":"about","privacy":"pp","contact":"contact"}[k]]
        main=f'<div class="page">{crumb(l,nm)}<h1>{nm}</h1>'+"".join(f"<p>{x}</p>" for x in LEG[l][k])+'</div>'
        pages[path(l,k)]=layout(l,k,f"{nm} – Kitbly",LEG[l][k][0],main)
O=str(ROOT/"dist");shutil.rmtree(O,ignore_errors=True)
for p,h in pages.items():
    d=O+p;os.makedirs(d,exist_ok=True);open(d+"index.html","w",encoding="utf-8").write(h)
sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
def url(k,ls):
    return "".join(f'<url><loc>{D}{path(l,k)}</loc>'+"".join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{D}{path(x,k)}"/>' for x in ls)+'</url>' for l in ls)
for k in SLUG:
    ls=langs_for(k)
    if ls:sm+=url(k,ls)
for a in ART:sm+=url(("a",a),langs_for(("a",a)))
open(O+"/sitemap.xml","w",encoding="utf-8").write(sm+'</urlset>')
open(O+"/robots.txt","w").write(f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {D}/sitemap.xml\n")
os.makedirs(O+"/assets",exist_ok=True);open(O+"/assets/probe.txt","w").write("ok");open(O+"/assets/sample.dat","wb").write(os.urandom(8*1024*1024))
[shutil.copy(ROOT/"static"/"t"/a,O+"/assets/"+b) for a,b in {"pdf.min.mjs":"pdfjs.js","pdf.worker.min.mjs":"pdfjs-worker.js","pdf-lib.esm.min.js":"pdflib.js"}.items()]
if (ROOT/"static"/"media").is_dir():shutil.copytree(ROOT/"static"/"media",O+"/media")
open(O+"/ads.txt","w").write("# Add the line from your AdSense account here after approval\n")
open(O+"/_headers","w").write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n/assets/*\n  Cache-Control: no-store\n")
open(O+"/index.html","w",encoding="utf-8").write('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Kitbly</title><link rel="alternate" hreflang="x-default" href="'+D+'/en/"><script>var l=(navigator.language||"en").slice(0,2);location.replace("/"+(l=="fr"||l=="de"?l:"en")+"/")</script></head><body><p><a href="/en/">English</a> · <a href="/fr/">Français</a> · <a href="/de/">Deutsch</a></p></body></html>')
open(O+"/404.html","w",encoding="utf-8").write('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>404 – Kitbly</title></head><body style="font-family:system-ui;padding:24px;background:#060A08;color:#E9F6EE"><style>a{color:#2EE57D}</style><h1>404</h1><p><a href="/en/">English</a> · <a href="/fr/">Français</a> · <a href="/de/">Deutsch</a></p></body></html>')
os.makedirs(O+"/admin",exist_ok=True)
open(O+"/admin/index.html","w",encoding="utf-8").write('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>Admin – Kitbly</title><meta http-equiv="refresh" content="3;url=https://app.pagescms.org/"></head><body style="font-family:system-ui;padding:24px;background:#060A08;color:#E9F6EE"><style>a{color:#2EE57D}</style><h1>Kitbly admin</h1><p>Opening the content editor. If nothing happens, <a href="https://app.pagescms.org/">open Pages CMS</a> and choose the KitBly repository.</p></body></html>')
# checks
bad=[];fa=re.compile(r'[\u0600-\u06FF]')
for p,h in pages.items():
    if fa.search(h):bad.append("persian:"+p)
    for u in re.findall(r'href="(/[^"#]*)"',h):
        if u not in pages and u not in("/",) and not u.startswith(("/media/","/assets/")):bad.append(f"broken:{p}->{u}")
print(len(pages),"pages;","problems:",bad or "none")
FIX='<script>nav=function(u){parent.postMessage({go:u},"*")};document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a");if(!a)return;var h=a.getAttribute("href");if(h&&h.charAt(0)==="/"){e.preventDefault();parent.postMessage({go:h},"*")}})</script>'
P=json.dumps({p:h.replace("</body>",FIX+"</body>") for p,h in pages.items()},ensure_ascii=False).replace("</","<\\/")
V='<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>Kitbly site viewer</title><style>:root{color-scheme:light dark;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);box-sizing:border-box}html,body{height:100%;margin:0;font:15px system-ui,sans-serif}body{display:flex;flex-direction:column}.bar{display:flex;gap:8px;align-items:center;padding:8px 10px;border-bottom:1px solid #8884}select{flex:1;min-width:0;font:inherit;padding:6px}iframe{flex:1;border:0;width:100%}</style></head><body><div class="bar"><b>Site</b><select id="s" aria-label="Page"></select></div><iframe id="f" title="Page preview"></iframe><script>const P='+P+';const f=document.getElementById("f"),s=document.getElementById("s");Object.keys(P).sort().forEach(k=>{const o=document.createElement("option");o.value=k;o.textContent=k;s.appendChild(o)});function show(k){if(!P[k])return;s.value=k;f.srcdoc=P[k]}s.onchange=()=>show(s.value);addEventListener("message",e=>{const g=e.data&&e.data.go;if(g)show(g.split("#")[0])});show("/en/");</script></body></html>'
if os.environ.get("VIEWER_OUT"):open(os.environ["VIEWER_OUT"],"w",encoding="utf-8").write(V)
