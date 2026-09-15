import socket, re, json
from concurrent.futures import ThreadPoolExecutor
from fetch import fetch
G = {"Shin-Stroy House": ["wellstone.am", "shinstroyhouse.am", "wellstoneresidence.am"],
     "Grandshin": ["e1residence.am", "grandshin.am", "e1.am"], "Yeryak Capital": ["araratpark.am", "yeryakcapital.am"],
     "Pavilion Group": ["doubletowers.am", "paviliongroup.am"], "Armat Realty": ["americanaarmenia.com", "armatrealty.am"],
     "SILUET INVEST": ["siluetresidence.am", "siluet.am"], "New Age LLC": ["ayas.am", "ayasresidence.am", "newage.am"],
     "GM Development": ["parkviewresidence.am", "gmdevelopment.am", "parkview.am"], "Just Developer": ["cult.am", "cultresidence.am", "justdeveloper.am"],
     "Posterum": ["davinchiclubhouse.am", "davinchi.am", "posterum.am"], "Royal Hills": ["cascadeclub.am", "royalhills.am"],
     "Amikson Sapphire": ["boscowelltown.am", "sapphire.am", "welltown.am"], "Buldozer Group": ["heavenheights.am", "buldozergroup.am"],
     "AP TOWER": ["panoramahills.am", "aptower.am"], "As Concern": ["zeytunplaza.am"], "Snart Construction Company": ["rivera.am", "riveraresidence.am"],
     "Malkhasyanshin": ["smartplaza.am"], "Eliteshin Group": ["lvovyantower.am"], "Nova Building": ["novabuilding.am"],
     "Rich Garden": ["richgarden.am"], "NAIRI HOUSE": ["nairihouse.am"], "Domum": ["domum.am", "domumresidence.am"],
     "Man Invest Group": ["drsum.am", "maninvestgroup.am"], "Mitstart": ["zovbuilding.am", "mitstart.am"],
     "Midis Construction": ["midispark.am", "midis.am", "midisconstruction.am"], "Renaissance Premium Home": ["renaissancepremium.am"],
     "Mountain Plaza": ["mountainplaza.am"], "Aurea Group": ["aurea.am", "aureagroup.am"], "Armani - Erebuni": ["armani-erebuni.am", "armanierebuni.am"],
     "Norq": ["norqresidence.am", "norq.am"], "Kievian Residence": ["kievyanresidence.am", "kievianresidence.am"],
     "Life House": ["lifehouse.am"], "Siluet": [], "EcoPanel Group": ["ecopanel.am", "ecopanelgroup.am"], "Itarco Construction": ["itarco.am"],
     "Aygedzor Construction Company": ["aygedzor.am"], "Nork Residential Complex": [], "Northern Gates": ["northerngates.am"],
     "Green Hills": ["greenhills.am"], "Mashtots Residence": ["mashtotsresidence.am"], "Slavonic Residence": ["slavonicresidence.am"],
     "NOR HATCHN HILLS": ["norhachnhills.am"], "Avan Residence": ["avanresidence.am"], "Olymp Construction": ["olympus.am", "olympusdavtashen.am"],
     "Advanced Development": ["garunavan.am"], "New Era": ["newera.am", "neweraresidence.am"], "Tsaghkadzor Plaza": ["tsaghkadzorplaza.am"],
     "Mush Towers": ["mushtowers.am"], "Altera Home": ["alterahome.am"], "Mia Town": ["miatown.am"], "Novel Residential Complex": ["novelresidence.am", "novel.am"],
     "Park Royal Tsaghkadzor": ["parkroyal.am"], "Faith Built": ["faithbuilt.com"], "Venni Group": ["venni.am", "vennigroup.com"],
     "V&B Construction": ["vbc.am", "vandb.am"], "Hay Develop": ["haydevelop.am", "hayview.am"], "Metsn Erik": ["metsnerik.am", "ar23.am"],
     "Tesq": ["tesq.am", "monolith.am"], "Nest House": ["nesthouse.am"], "Platinum Homes": ["platinumhomes.am"], "Quadra Construction": ["quadra.am"],
     "Rem Group": ["remtower.am", "remgroup.am"], "Dream House": ["dreamhouse.am"], "Gevmik": ["gevmik.am"], "Kechark": ["kechark.am"],
     "Soho Construction": ["soho.am"], "Jet Set Construct": ["jetset.am"], "Liashin": ["liashin.am"], "Edno Group": ["ednogroup.am"]}


def check(item):
    name, doms = item
    hits = []
    for d in doms:
        try:
            socket.gethostbyname(d)
        except Exception:
            continue
        st, fu, t = fetch("https://" + d)
        if not st.startswith("2"):
            st, fu, t = fetch("http://" + d)
        tm = re.search(r"(?is)<title[^>]*>(.*?)</title>", t)
        hits.append((d, st, fu, len(t), tm.group(1).strip()[:80] if tm else ""))
    return name, hits


with ThreadPoolExecutor(10) as ex:
    for name, hits in ex.map(check, G.items()):
        if hits:
            print(name, hits)
