# config.py — Groups, fixtures, heat profiles
# No hand-set ratings — team quality is derived entirely from market-implied match probabilities.

# ── Groups A-L ────────────────────────────────────────────────────────────────
GROUPS = {
    "A": ["Mexico", "South Africa", "South Korea", "Czech Republic"],
    "B": ["Canada", "Bosnia", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["USA", "Paraguay", "Australia", "Turkey"],
    "E": ["Germany", "Curacao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"],
}

# ── Venue heat score (0 = cool, 1 = brutal) ───────────────────────────────────
VENUE_HEAT = {
    "Miami":        0.95,
    "Houston":      0.90,
    "Atlanta":      0.20,   # Mercedes-Benz Stadium — retractable roof, AC confirmed CWC 2025
    "Dallas":       0.85,
    "Kansas City":  0.80,
    "Philadelphia": 0.90,   # CWC data: 96-98°F afternoon games, heat emergency declared
    "New Jersey":   0.83,   # CWC data: 85°F final, humid stadium bowl
    "Foxborough":   0.55,
    "Los Angeles":  0.60,
    "Seattle":      0.20,
    "Vancouver":    0.15,
    "Toronto":      0.35,
    "Santa Clara":  0.50,
    "Mexico City":  0.55,   # altitude moderates effective heat stress
    "Guadalajara":  0.70,
    "Monterrey":    0.80,
    "TBD":          0.50,   # placeholder
}

# ── Heat tolerance per team ───────────────────────────────────────────────────
# Positive = thrives in heat, negative = struggles
# Applied as multiplier: lam *= (1 + heat_tolerance * venue_heat * time_factor)
HEAT_TOLERANCE = {
    # South American — heat adapted
    "Brazil":        0.15,
    "Colombia":      0.12,
    "Ecuador":       0.12,
    "Uruguay":       0.10,
    "Argentina":     0.10,
    "Paraguay":      0.10,
    # African — heat adapted
    "Senegal":       0.15,
    "Morocco":       0.12,
    "Ivory Coast":   0.15,
    "Ghana":         0.12,
    "Egypt":         0.10,
    "Algeria":       0.10,
    "Tunisia":       0.10,
    "DR Congo":      0.12,
    "South Africa":  0.08,
    "Cape Verde":    0.10,   # Atlantic island — warm but ocean breezes, not mainland equatorial
    # Caribbean / Central America
    "Haiti":         0.15,
    "Panama":        0.12,
    "Curacao":       0.15,
    # Middle East / Central Asia
    "Saudi Arabia":  0.10,
    "Iran":          0.05,
    "Iraq":          0.08,
    "Jordan":        0.08,
    "Qatar":         0.08,
    "Uzbekistan":    0.03,
    # Host nations
    "USA":           0.15,
    "Mexico":        0.15,
    "Canada":       -0.05,
    # European sides with many players of West African / Caribbean heritage (heat-adaptation hypothesis)
    "France":        0.08,
    "Belgium":       0.06,
    "Netherlands":   0.05,
    # Mediterranean — mild heat tolerance
    "Spain":         0.03,
    "Portugal":      0.03,
    "Turkey":        0.03,
    "Croatia":      -0.03,
    # Northern European — struggles in heat
    "Norway":       -0.15,
    "Sweden":       -0.12,
    "Germany":      -0.10,
    "Austria":      -0.10,
    "Czech Republic":-0.08,
    "Scotland":     -0.12,
    "Switzerland":  -0.07,
    "England":      -0.08,
    "Bosnia":       -0.05,
    # Asia/Pacific
    "Japan":         0.08,   # brutal humid summers, J-League plays through heat
    "South Korea":   0.08,   # Korean summer monsoon season, K-League heat
    "Australia":     0.05,
    "New Zealand":  -0.03,
}

# ── Group stage fixtures ──────────────────────────────────────────────────────
# local_time: HH:MM local venue time
# Converted from UK BST (UTC+1) to local:
#   EDT (EDT=UTC-4): BST-5  | CDT (UTC-5): BST-6  | PDT (UTC-7): BST-8
FIXTURES = [
    # GROUP A
    {"group":"A","home":"Mexico",       "away":"South Africa",  "date":"2026-06-11","local_time":"14:00","venue":"Mexico City"},
    {"group":"A","home":"South Korea",  "away":"Czech Republic","date":"2026-06-11","local_time":"21:00","venue":"Guadalajara"},
    {"group":"A","home":"Czech Republic","away":"South Africa", "date":"2026-06-18","local_time":"11:00","venue":"Atlanta"},
    {"group":"A","home":"Mexico",       "away":"South Korea",   "date":"2026-06-18","local_time":"20:00","venue":"Guadalajara"},
    {"group":"A","home":"South Africa", "away":"South Korea",   "date":"2026-06-24","local_time":"20:00","venue":"Monterrey"},
    {"group":"A","home":"Czech Republic","away":"Mexico",       "date":"2026-06-24","local_time":"20:00","venue":"Mexico City"},
    # GROUP B
    {"group":"B","home":"Canada",       "away":"Bosnia",        "date":"2026-06-12","local_time":"15:00","venue":"Toronto"},
    {"group":"B","home":"Qatar",        "away":"Switzerland",   "date":"2026-06-13","local_time":"13:00","venue":"Santa Clara"},
    {"group":"B","home":"Switzerland",  "away":"Bosnia",        "date":"2026-06-18","local_time":"13:00","venue":"Los Angeles"},
    {"group":"B","home":"Canada",       "away":"Qatar",         "date":"2026-06-18","local_time":"16:00","venue":"Vancouver"},
    {"group":"B","home":"Switzerland",  "away":"Canada",        "date":"2026-06-24","local_time":"13:00","venue":"Vancouver"},
    {"group":"B","home":"Bosnia",       "away":"Qatar",         "date":"2026-06-24","local_time":"13:00","venue":"Seattle"},
    # GROUP C
    {"group":"C","home":"Brazil",       "away":"Morocco",       "date":"2026-06-13","local_time":"18:00","venue":"New Jersey"},
    {"group":"C","home":"Haiti",        "away":"Scotland",      "date":"2026-06-13","local_time":"21:00","venue":"Foxborough"},
    {"group":"C","home":"Brazil",       "away":"Haiti",         "date":"2026-06-19","local_time":"20:30","venue":"Philadelphia"},
    {"group":"C","home":"Scotland",     "away":"Morocco",       "date":"2026-06-19","local_time":"18:00","venue":"Foxborough"},
    {"group":"C","home":"Morocco",      "away":"Haiti",         "date":"2026-06-24","local_time":"18:00","venue":"Atlanta"},
    {"group":"C","home":"Scotland",     "away":"Brazil",        "date":"2026-06-24","local_time":"18:00","venue":"Miami"},
    # GROUP D
    {"group":"D","home":"USA",          "away":"Paraguay",      "date":"2026-06-12","local_time":"18:00","venue":"Los Angeles"},
    {"group":"D","home":"Australia",    "away":"Turkey",        "date":"2026-06-13","local_time":"21:00","venue":"Vancouver"},
    {"group":"D","home":"USA",          "away":"Australia",     "date":"2026-06-19","local_time":"12:00","venue":"Seattle"},
    {"group":"D","home":"Turkey",       "away":"Paraguay",      "date":"2026-06-19","local_time":"20:00","venue":"Santa Clara"},
    {"group":"D","home":"Turkey",       "away":"USA",           "date":"2026-06-25","local_time":"19:00","venue":"Los Angeles"},
    {"group":"D","home":"Paraguay",     "away":"Australia",     "date":"2026-06-25","local_time":"19:00","venue":"Santa Clara"},
    # GROUP E
    {"group":"E","home":"Germany",      "away":"Curacao",       "date":"2026-06-14","local_time":"12:00","venue":"Houston"},
    {"group":"E","home":"Ivory Coast",  "away":"Ecuador",       "date":"2026-06-14","local_time":"19:00","venue":"Philadelphia"},
    {"group":"E","home":"Germany",      "away":"Ivory Coast",   "date":"2026-06-20","local_time":"16:00","venue":"Toronto"},
    {"group":"E","home":"Ecuador",      "away":"Curacao",       "date":"2026-06-20","local_time":"19:00","venue":"Kansas City"},
    {"group":"E","home":"Curacao",      "away":"Ivory Coast",   "date":"2026-06-25","local_time":"16:00","venue":"Philadelphia"},
    {"group":"E","home":"Ecuador",      "away":"Germany",       "date":"2026-06-25","local_time":"16:00","venue":"New Jersey"},
    # GROUP F  (Netherlands vs Sweden fixture time/venue TBD — placeholder added)
    {"group":"F","home":"Netherlands",  "away":"Japan",         "date":"2026-06-14","local_time":"15:00","venue":"Dallas"},
    {"group":"F","home":"Sweden",       "away":"Tunisia",       "date":"2026-06-14","local_time":"21:00","venue":"Monterrey"},
    {"group":"F","home":"Netherlands",  "away":"Sweden",        "date":"2026-06-20","local_time":"15:00","venue":"TBD"},
    {"group":"F","home":"Tunisia",      "away":"Japan",         "date":"2026-06-20","local_time":"23:00","venue":"Monterrey"},
    {"group":"F","home":"Tunisia",      "away":"Netherlands",   "date":"2026-06-25","local_time":"18:00","venue":"Kansas City"},
    {"group":"F","home":"Japan",        "away":"Sweden",        "date":"2026-06-25","local_time":"18:00","venue":"Dallas"},
    # GROUP G
    {"group":"G","home":"Belgium",      "away":"Egypt",         "date":"2026-06-15","local_time":"12:00","venue":"Seattle"},
    {"group":"G","home":"Iran",         "away":"New Zealand",   "date":"2026-06-15","local_time":"18:00","venue":"Los Angeles"},
    {"group":"G","home":"Belgium",      "away":"Iran",          "date":"2026-06-21","local_time":"12:00","venue":"Los Angeles"},
    {"group":"G","home":"New Zealand",  "away":"Egypt",         "date":"2026-06-20","local_time":"18:00","venue":"Vancouver"},
    {"group":"G","home":"New Zealand",  "away":"Belgium",       "date":"2026-06-26","local_time":"20:00","venue":"Vancouver"},
    {"group":"G","home":"Egypt",        "away":"Iran",          "date":"2026-06-26","local_time":"20:00","venue":"Seattle"},
    # GROUP H
    {"group":"H","home":"Spain",        "away":"Cape Verde",    "date":"2026-06-15","local_time":"11:00","venue":"Atlanta"},
    {"group":"H","home":"Saudi Arabia", "away":"Uruguay",       "date":"2026-06-15","local_time":"18:00","venue":"Miami"},
    {"group":"H","home":"Spain",        "away":"Saudi Arabia",  "date":"2026-06-21","local_time":"11:00","venue":"Atlanta"},
    {"group":"H","home":"Uruguay",      "away":"Cape Verde",    "date":"2026-06-21","local_time":"18:00","venue":"Miami"},
    {"group":"H","home":"Cape Verde",   "away":"Saudi Arabia",  "date":"2026-06-26","local_time":"19:00","venue":"Houston"},
    {"group":"H","home":"Uruguay",      "away":"Spain",         "date":"2026-06-26","local_time":"19:00","venue":"Guadalajara"},
    # GROUP I
    {"group":"I","home":"France",       "away":"Senegal",       "date":"2026-06-16","local_time":"15:00","venue":"New Jersey"},
    {"group":"I","home":"Iraq",         "away":"Norway",        "date":"2026-06-16","local_time":"18:00","venue":"Foxborough"},
    {"group":"I","home":"France",       "away":"Iraq",          "date":"2026-06-22","local_time":"17:00","venue":"Philadelphia"},
    {"group":"I","home":"Norway",       "away":"Senegal",       "date":"2026-06-22","local_time":"20:00","venue":"Toronto"},
    {"group":"I","home":"Norway",       "away":"France",        "date":"2026-06-26","local_time":"15:00","venue":"Foxborough"},
    {"group":"I","home":"Senegal",      "away":"Iraq",          "date":"2026-06-26","local_time":"15:00","venue":"Toronto"},
    # GROUP J
    {"group":"J","home":"Argentina",    "away":"Algeria",       "date":"2026-06-16","local_time":"20:00","venue":"Kansas City"},
    {"group":"J","home":"Austria",      "away":"Jordan",        "date":"2026-06-16","local_time":"21:00","venue":"Santa Clara"},
    {"group":"J","home":"Argentina",    "away":"Austria",       "date":"2026-06-22","local_time":"12:00","venue":"Dallas"},
    {"group":"J","home":"Jordan",       "away":"Algeria",       "date":"2026-06-22","local_time":"20:00","venue":"Santa Clara"},
    {"group":"J","home":"Algeria",      "away":"Austria",       "date":"2026-06-27","local_time":"21:00","venue":"Kansas City"},
    {"group":"J","home":"Jordan",       "away":"Argentina",     "date":"2026-06-27","local_time":"21:00","venue":"Dallas"},
    # GROUP K
    {"group":"K","home":"Portugal",     "away":"DR Congo",      "date":"2026-06-17","local_time":"12:00","venue":"Houston"},
    {"group":"K","home":"Uzbekistan",   "away":"Colombia",      "date":"2026-06-17","local_time":"21:00","venue":"Mexico City"},
    {"group":"K","home":"Portugal",     "away":"Uzbekistan",    "date":"2026-06-23","local_time":"12:00","venue":"Houston"},
    {"group":"K","home":"Colombia",     "away":"DR Congo",      "date":"2026-06-23","local_time":"21:00","venue":"Guadalajara"},
    {"group":"K","home":"Colombia",     "away":"Portugal",      "date":"2026-06-27","local_time":"19:30","venue":"Miami"},
    {"group":"K","home":"DR Congo",     "away":"Uzbekistan",    "date":"2026-06-27","local_time":"19:30","venue":"Atlanta"},
    # GROUP L
    {"group":"L","home":"England",      "away":"Croatia",       "date":"2026-06-17","local_time":"15:00","venue":"Dallas"},
    {"group":"L","home":"Ghana",        "away":"Panama",        "date":"2026-06-17","local_time":"19:00","venue":"Toronto"},
    {"group":"L","home":"England",      "away":"Ghana",         "date":"2026-06-23","local_time":"16:00","venue":"Foxborough"},
    {"group":"L","home":"Panama",       "away":"Croatia",       "date":"2026-06-23","local_time":"19:00","venue":"Foxborough"},
    {"group":"L","home":"Panama",       "away":"England",       "date":"2026-06-27","local_time":"17:00","venue":"New Jersey"},
    {"group":"L","home":"Croatia",      "away":"Ghana",         "date":"2026-06-27","local_time":"17:00","venue":"Philadelphia"},
]
