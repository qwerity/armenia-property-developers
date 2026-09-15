import rec
from rec import imgs
D = rec.Dev("11_libertyone", "Capital Plus (Liberty One)", "https://www.libertyone.am/", ["+37494770221", "+37496060002"], "info@libertyone.am",
            {"facebook": "https://www.facebook.com/liberty1.yerevan", "instagram": "https://www.instagram.com/liberty1_yerevan/"})
u = "https://www.libertyone.am/"
D.add(u, "Liberty 1 (Azatutyun 1)", district="Arabkir", address="Azatutyan Ave 1/43, Nor Arabkir", status="under construction", floors="4-5",
      images=imgs(u, "media/", "mobile|gallery-.*-light"), videos=["https://www.youtube.com/watch?v=0IdBGSo5ouI"],
      description="Liberty 1: luxury complex of five buildings near Cascade in the Monument area. Every residence a corner unit with infinity terrace; heat-pump central cooling and radiant floor heating. Buildings 1-2: 4 floors with spa & fitness, game room and cigar lounge on ground floor, grand lobby, premium residences on floors 2-4; Buildings 3-4: cafe and day care, residences on floors 1-4 with north/west panoramas; Building 5: panoramic penthouse with private rooftop terrace. 24/7 concierge and security, underground parking with EV charging, landscaped courtyard.")
D.save()
