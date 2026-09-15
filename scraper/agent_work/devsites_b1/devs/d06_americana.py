import rec, re, f
D = rec.Dev("06_americana", "Armat Realty / SaGa-Shin (Americana Armenia)", "https://www.americanaarmenia.com/", ["+37493913191", "+37477918891", "+37493280110"], "khachatur@americanaarmenia.com")
u = "https://www.americanaarmenia.com/"
im = []
for x in f.meta(u, f.get(u))["images"]:
    if "a4f9f9_" in x or "9bd95e_" in x:
        k = re.search(r"media/([^/]+)", x).group(1)
        full = "https://static.wixstatic.com/media/" + k
        if full not in im: im.append(full)
D.add(u, "Americana Armenia gated community", district="Ajapnyak", address="off Ashtarak highway, Yerevan", status="completed", completion="2022", floors="",
      images=im, description="Americana Armenia: gated green suburban community right off the Ashtarak highway, under 10 km from Republic Square. Planned 19 private homes and five apartment buildings with duplex apartments (site plan lists Americana 1-24), security system, artistic lighting, shops, restaurants, green parks, playgrounds and kindergarten, homeowners association. Builder SaGa-Shin LLC (director Khachatur Galstyan), architect Eivien Group, developer Tigran Sahakyan (NY), broker ARMAT LLC (agent Galust Avagyan, Shinararneri 28/2). Target completion 2021-22; all listed properties currently marked Sold.")
D.save("single community site; all units marked sold; 'Amelia Residence' not found on site")
