import rec
from rec import imgs
D = rec.Dev("27_narmark", "NARMARK", "https://narmarkshin.am/", ["+37477201100"], "tadevosyan.ando@rambler.ru")
u = "https://narmarkshin.am/"
D.add(u, "NARMARK residential building near Davtashen", auto=False, district="Davtashen", address="adjacent to Davtashen district (exact address not given)", status="under construction",
      images=imgs(u, "uploads/2024/12/"),
      description="Residential building marketed on the Narmark construction company homepage (company founded 2020, director Andranik Tadevosyan, registered in Vardenis): luxury design, stained-glass (vitrage) windows, 10+ point seismic resistance, income-tax refund eligible, located immediately next to Davtashen district. Portfolio page is template placeholder; no name or exact address published.")
D.save("homepage mentions one building near Davtashen; portfolio is template placeholder")
