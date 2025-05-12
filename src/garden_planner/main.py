from __future__ import annotations
import re
from garden_planner.crew import create_crew


# ---------- parsers ----------
PLANT_LINE = re.compile(r"^(.*?)[\s\t]+(\d+)$")
SIZE_RE = re.compile(r"(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)\s*ft", re.I)
DEPTH_RE = re.compile(r"depth\s+(\d+(?:\.\d+)?)\s*in", re.I)
LIGHT_RE = re.compile(
    r"(full sun|partial shade|partial sun|shade)", re.I
)


def parse_plants(raw: str) -> list[dict]:
    plants = []
    for line in filter(None, [l.strip() for l in raw.splitlines()]):
        m = PLANT_LINE.match(line)
        if m:
            name, qty = m.group(1), int(m.group(2))
        else:
            name, qty = line, 1
        plants.append({"name": name, "qty": qty})
    return plants


def parse_beds(raw: str) -> list[dict]:
    beds = []
    for line in filter(None, [l.strip() for l in raw.splitlines()]):
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 5:
            continue  # skip malformed
        bed_id = parts[0]
        size = SIZE_RE.search(line)
        depth = DEPTH_RE.search(line)
        light = LIGHT_RE.search(line)
        beds.append(
            {
                "id": bed_id,
                "width_ft": float(size.group(1)) if size else None,
                "length_ft": float(size.group(2)) if size else None,
                "depth_in": float(depth.group(1)) if depth else None,
                "light": light.group(1).lower() if light else None,
                "soil": parts[-1].lower(),
            }
        )
    return beds


# ---------- Crew runner ----------
def run_crew(plants_text: str, beds_text: str):
    plants = parse_plants(plants_text)
    beds = parse_beds(beds_text)

    crew = create_crew()

    # Pass data into the first task via crew.context
    crew.context = {
        "plants": plants,
        "beds": beds,
    }

    result = crew.kickoff()

    # TODO later: pull real filenames from result dict
    return "output/report.md", "output/garden_plan.png"


if __name__ == "__main__":
    # quick local smoke-test
    demo_plants = "Lavender 6\nTomato (Roma) 4"
    demo_beds = "Front-Left, 4x8 ft, depth 12 in, full sun, loamy"
    print(run_crew(demo_plants, demo_beds))
