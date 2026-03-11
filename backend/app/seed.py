"""Seed data for demo. Called on startup if collections are empty."""
from datetime import datetime, timezone, timedelta
from bson import ObjectId
from . import database as db

# Fixed IDs so relationships are stable across re-seeds
TEAM_IDS = {
    "lakers":   ObjectId("650000000000000000000001"),
    "warriors": ObjectId("650000000000000000000002"),
    "bucks":    ObjectId("650000000000000000000003"),
    "chiefs":   ObjectId("650000000000000000000004"),
    "bills":    ObjectId("650000000000000000000005"),
    "mancity":  ObjectId("650000000000000000000006"),
    "realmad":  ObjectId("650000000000000000000007"),
}

ATHLETE_IDS = {
    "lebron":   ObjectId("651000000000000000000001"),
    "curry":    ObjectId("651000000000000000000002"),
    "giannis":  ObjectId("651000000000000000000003"),
    "mahomes":  ObjectId("651000000000000000000004"),
    "allen":    ObjectId("651000000000000000000005"),
    "haaland":  ObjectId("651000000000000000000006"),
    "mbappe":   ObjectId("651000000000000000000007"),
    "ad":       ObjectId("651000000000000000000008"),
    "klay":     ObjectId("651000000000000000000009"),
    "dame":     ObjectId("651000000000000000000010"),
}

now = datetime.now(timezone.utc)


def avatar(name: str, bg: str = "1e3a5f") -> str:
    encoded = name.replace(" ", "+")
    return f"https://ui-avatars.com/api/?name={encoded}&background={bg}&color=fff&size=200&bold=true"


TEAMS = [
    {
        "_id": TEAM_IDS["lakers"],
        "name": "Los Angeles Lakers",
        "sport": "basketball",
        "league": "NBA",
        "city": "Los Angeles",
        "logo_url": avatar("LA", "552583"),
        "roster": [
            {"athlete_id": str(ATHLETE_IDS["lebron"]), "name": "LeBron James", "position": "SF"},
            {"athlete_id": str(ATHLETE_IDS["ad"]),     "name": "Anthony Davis", "position": "C"},
        ],
    },
    {
        "_id": TEAM_IDS["warriors"],
        "name": "Golden State Warriors",
        "sport": "basketball",
        "league": "NBA",
        "city": "San Francisco",
        "logo_url": avatar("GS", "1D428A"),
        "roster": [
            {"athlete_id": str(ATHLETE_IDS["curry"]), "name": "Stephen Curry", "position": "PG"},
            {"athlete_id": str(ATHLETE_IDS["klay"]),  "name": "Klay Thompson", "position": "SG"},
        ],
    },
    {
        "_id": TEAM_IDS["bucks"],
        "name": "Milwaukee Bucks",
        "sport": "basketball",
        "league": "NBA",
        "city": "Milwaukee",
        "logo_url": avatar("MIL", "00471B"),
        "roster": [
            {"athlete_id": str(ATHLETE_IDS["giannis"]), "name": "Giannis Antetokounmpo", "position": "PF"},
            {"athlete_id": str(ATHLETE_IDS["dame"]),    "name": "Damian Lillard", "position": "PG"},
        ],
    },
    {
        "_id": TEAM_IDS["chiefs"],
        "name": "Kansas City Chiefs",
        "sport": "football",
        "league": "NFL",
        "city": "Kansas City",
        "logo_url": avatar("KC", "E31837"),
        "roster": [
            {"athlete_id": str(ATHLETE_IDS["mahomes"]), "name": "Patrick Mahomes", "position": "QB"},
        ],
    },
    {
        "_id": TEAM_IDS["bills"],
        "name": "Buffalo Bills",
        "sport": "football",
        "league": "NFL",
        "city": "Buffalo",
        "logo_url": avatar("BUF", "00338D"),
        "roster": [
            {"athlete_id": str(ATHLETE_IDS["allen"]), "name": "Josh Allen", "position": "QB"},
        ],
    },
    {
        "_id": TEAM_IDS["mancity"],
        "name": "Manchester City",
        "sport": "soccer",
        "league": "Premier League",
        "city": "Manchester",
        "logo_url": avatar("MC", "6CABDD"),
        "roster": [
            {"athlete_id": str(ATHLETE_IDS["haaland"]), "name": "Erling Haaland", "position": "ST"},
        ],
    },
    {
        "_id": TEAM_IDS["realmad"],
        "name": "Real Madrid",
        "sport": "soccer",
        "league": "La Liga",
        "city": "Madrid",
        "logo_url": avatar("RM", "FEBE10"),
        "roster": [
            {"athlete_id": str(ATHLETE_IDS["mbappe"]), "name": "Kylian Mbappé", "position": "LW"},
        ],
    },
]

ATHLETES = [
    {
        "_id": ATHLETE_IDS["lebron"],
        "name": "LeBron James",
        "sport": "basketball",
        "position": "Small Forward",
        "team_id": str(TEAM_IDS["lakers"]),
        "team_name": "Los Angeles Lakers",
        "nationality": "USA",
        "age": 40,
        "image_url": avatar("LeBron James", "552583"),
        "stats": {"ppg": 25.7, "rpg": 7.3, "apg": 8.1, "gp": 71},
    },
    {
        "_id": ATHLETE_IDS["curry"],
        "name": "Stephen Curry",
        "sport": "basketball",
        "position": "Point Guard",
        "team_id": str(TEAM_IDS["warriors"]),
        "team_name": "Golden State Warriors",
        "nationality": "USA",
        "age": 36,
        "image_url": avatar("Stephen Curry", "1D428A"),
        "stats": {"ppg": 26.4, "rpg": 4.5, "apg": 6.1, "gp": 74},
    },
    {
        "_id": ATHLETE_IDS["giannis"],
        "name": "Giannis Antetokounmpo",
        "sport": "basketball",
        "position": "Power Forward",
        "team_id": str(TEAM_IDS["bucks"]),
        "team_name": "Milwaukee Bucks",
        "nationality": "Greece",
        "age": 30,
        "image_url": avatar("Giannis A", "00471B"),
        "stats": {"ppg": 30.4, "rpg": 11.5, "apg": 6.5, "gp": 73},
    },
    {
        "_id": ATHLETE_IDS["ad"],
        "name": "Anthony Davis",
        "sport": "basketball",
        "position": "Center",
        "team_id": str(TEAM_IDS["lakers"]),
        "team_name": "Los Angeles Lakers",
        "nationality": "USA",
        "age": 31,
        "image_url": avatar("Anthony Davis", "552583"),
        "stats": {"ppg": 24.7, "rpg": 12.6, "apg": 3.5, "gp": 76},
    },
    {
        "_id": ATHLETE_IDS["klay"],
        "name": "Klay Thompson",
        "sport": "basketball",
        "position": "Shooting Guard",
        "team_id": str(TEAM_IDS["warriors"]),
        "team_name": "Golden State Warriors",
        "nationality": "USA",
        "age": 34,
        "image_url": avatar("Klay Thompson", "1D428A"),
        "stats": {"ppg": 17.9, "rpg": 3.3, "apg": 2.4, "gp": 69},
    },
    {
        "_id": ATHLETE_IDS["dame"],
        "name": "Damian Lillard",
        "sport": "basketball",
        "position": "Point Guard",
        "team_id": str(TEAM_IDS["bucks"]),
        "team_name": "Milwaukee Bucks",
        "nationality": "USA",
        "age": 34,
        "image_url": avatar("Damian Lillard", "00471B"),
        "stats": {"ppg": 24.3, "rpg": 4.4, "apg": 7.1, "gp": 73},
    },
    {
        "_id": ATHLETE_IDS["mahomes"],
        "name": "Patrick Mahomes",
        "sport": "football",
        "position": "Quarterback",
        "team_id": str(TEAM_IDS["chiefs"]),
        "team_name": "Kansas City Chiefs",
        "nationality": "USA",
        "age": 29,
        "image_url": avatar("Patrick Mahomes", "E31837"),
        "stats": {"pass_yds": 4183, "pass_td": 26, "int": 11, "qbr": 97.6},
    },
    {
        "_id": ATHLETE_IDS["allen"],
        "name": "Josh Allen",
        "sport": "football",
        "position": "Quarterback",
        "team_id": str(TEAM_IDS["bills"]),
        "team_name": "Buffalo Bills",
        "nationality": "USA",
        "age": 28,
        "image_url": avatar("Josh Allen", "00338D"),
        "stats": {"pass_yds": 3731, "pass_td": 28, "int": 6, "qbr": 101.4},
    },
    {
        "_id": ATHLETE_IDS["haaland"],
        "name": "Erling Haaland",
        "sport": "soccer",
        "position": "Striker",
        "team_id": str(TEAM_IDS["mancity"]),
        "team_name": "Manchester City",
        "nationality": "Norway",
        "age": 24,
        "image_url": avatar("Erling Haaland", "6CABDD"),
        "stats": {"goals": 27, "assists": 5, "matches": 31, "shots_pg": 3.8},
    },
    {
        "_id": ATHLETE_IDS["mbappe"],
        "name": "Kylian Mbappé",
        "sport": "soccer",
        "position": "Left Wing",
        "team_id": str(TEAM_IDS["realmad"]),
        "team_name": "Real Madrid",
        "nationality": "France",
        "age": 26,
        "image_url": avatar("Kylian Mbappe", "FEBE10"),
        "stats": {"goals": 31, "assists": 9, "matches": 34, "shots_pg": 4.1},
    },
]

EVENTS = [
    # Completed
    {
        "sport": "basketball", "league": "NBA",
        "home_team": {"id": str(TEAM_IDS["lakers"]),   "name": "Los Angeles Lakers"},
        "away_team": {"id": str(TEAM_IDS["warriors"]), "name": "Golden State Warriors"},
        "start_time": now - timedelta(days=1),
        "status": "completed",
        "score": {"home": 118, "away": 109},
        "venue": "Crypto.com Arena",
    },
    {
        "sport": "basketball", "league": "NBA",
        "home_team": {"id": str(TEAM_IDS["bucks"]),    "name": "Milwaukee Bucks"},
        "away_team": {"id": str(TEAM_IDS["lakers"]),   "name": "Los Angeles Lakers"},
        "start_time": now - timedelta(days=2),
        "status": "completed",
        "score": {"home": 124, "away": 121},
        "venue": "Fiserv Forum",
    },
    {
        "sport": "football", "league": "NFL",
        "home_team": {"id": str(TEAM_IDS["chiefs"]), "name": "Kansas City Chiefs"},
        "away_team": {"id": str(TEAM_IDS["bills"]),  "name": "Buffalo Bills"},
        "start_time": now - timedelta(days=3),
        "status": "completed",
        "score": {"home": 27, "away": 24},
        "venue": "GEHA Field at Arrowhead Stadium",
    },
    {
        "sport": "soccer", "league": "Premier League",
        "home_team": {"id": str(TEAM_IDS["mancity"]), "name": "Manchester City"},
        "away_team": {"id": str(TEAM_IDS["realmad"]), "name": "Real Madrid"},
        "start_time": now - timedelta(days=4),
        "status": "completed",
        "score": {"home": 3, "away": 3},
        "venue": "Etihad Stadium",
    },
    {
        "sport": "basketball", "league": "NBA",
        "home_team": {"id": str(TEAM_IDS["warriors"]), "name": "Golden State Warriors"},
        "away_team": {"id": str(TEAM_IDS["bucks"]),    "name": "Milwaukee Bucks"},
        "start_time": now - timedelta(days=5),
        "status": "completed",
        "score": {"home": 112, "away": 105},
        "venue": "Chase Center",
    },
    # Live
    {
        "sport": "basketball", "league": "NBA",
        "home_team": {"id": str(TEAM_IDS["bucks"]),    "name": "Milwaukee Bucks"},
        "away_team": {"id": str(TEAM_IDS["warriors"]), "name": "Golden State Warriors"},
        "start_time": now - timedelta(hours=1),
        "status": "live",
        "score": {"home": 87, "away": 82},
        "venue": "Fiserv Forum",
    },
    {
        "sport": "soccer", "league": "La Liga",
        "home_team": {"id": str(TEAM_IDS["realmad"]),  "name": "Real Madrid"},
        "away_team": {"id": str(TEAM_IDS["mancity"]),  "name": "Manchester City"},
        "start_time": now - timedelta(minutes=45),
        "status": "live",
        "score": {"home": 1, "away": 0},
        "venue": "Santiago Bernabéu",
    },
    # Upcoming
    {
        "sport": "football", "league": "NFL",
        "home_team": {"id": str(TEAM_IDS["bills"]),  "name": "Buffalo Bills"},
        "away_team": {"id": str(TEAM_IDS["chiefs"]), "name": "Kansas City Chiefs"},
        "start_time": now + timedelta(days=3),
        "status": "upcoming",
        "score": None,
        "venue": "Highmark Stadium",
    },
    {
        "sport": "basketball", "league": "NBA",
        "home_team": {"id": str(TEAM_IDS["lakers"]),   "name": "Los Angeles Lakers"},
        "away_team": {"id": str(TEAM_IDS["bucks"]),    "name": "Milwaukee Bucks"},
        "start_time": now + timedelta(days=2),
        "status": "upcoming",
        "score": None,
        "venue": "Crypto.com Arena",
    },
    {
        "sport": "soccer", "league": "Premier League",
        "home_team": {"id": str(TEAM_IDS["realmad"]),  "name": "Real Madrid"},
        "away_team": {"id": str(TEAM_IDS["mancity"]),  "name": "Manchester City"},
        "start_time": now + timedelta(days=5),
        "status": "upcoming",
        "score": None,
        "venue": "Santiago Bernabéu",
    },
]


async def seed_if_empty() -> None:
    if await db.teams().count_documents({}) > 0:
        return

    await db.teams().insert_many(TEAMS)
    await db.athletes().insert_many(ATHLETES)
    await db.events().insert_many(EVENTS)
    print(f"Seeded {len(TEAMS)} teams, {len(ATHLETES)} athletes, {len(EVENTS)} events.")
