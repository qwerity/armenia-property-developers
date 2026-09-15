import rec
D = rec.Dev("22_shushipalace", "Lorida Group (Shushi Palace)", "https://www.shushi-palace.am/", ["+37498908908", "+37412208830", "+37441208830"], "info@shushi-palace.am",
            {"facebook": "https://www.facebook.com/ShushiPalaceResidentialComplex/", "instagram": "https://www.instagram.com/shushipalace/"})
S = "https://admin.shushi-palace.am/wp-content/uploads/2023/05/%D5%87%D5%B8%D6%82%D5%B7%D5%AB-"
D.add("https://www.shushi-palace.am/", "Shushi Palace", auto=False, district="Ajapnyak", address="Leningradyan St 50/102 (head office; complex in north-west Yerevan)", status="under construction", completion="2024",
      images=[S + x + ".webp" for x in ["9", "4", "2", "1-1", "3", "5", "6", "7", "8", "10"]] + ["https://admin.shushi-palace.am/wp-content/uploads/2021/08/50005B40-2047-4C02-B9C7-645AF5FAF7A7.jpeg"],
      description="Shushi Palace by Lorida Group (founder US-Armenian businessman Hrag Samuel Salibian): complex of eight seismic-resistant, energy-efficient high-rise buildings with ~1,100 apartments in north-west Yerevan with Ararat views; all apartments with open or French balconies, sound/thermal insulation. ~8,000 sq m car-free landscaped courtyard with playground, outdoor gym, 400 m bike/running track, sports field, fountains; two-level underground parking with lifts, CCTV, service and car-wash points; kindergarten, gym, supermarket, dental clinic, restaurant, pharmacy etc. 24/7 security. Income-tax refund eligible; apartments advertised as ready in 2024. Sales office Tamanyan 1A (Cascade).")
D.save("Nuxt SPA; no coordinates exposed")
