# BEGIN src/garden_planner/main.py
from __future__ import annotations
import re
from pathlib import Path
from .crew import create_crew

# ---------- parsers ----------
PLANT_LINE = re.compile(r"^(.*?)[\s\t]+(\d+)$")
SIZE_RE = re.compile(r"(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)\s*ft", re.I)
DEPTH_RE = re.compile(r"depth\s+(\d+(?:\.\d+)?)\s*in", re.I)
LIGHT_RE = re.compile(r"(full sun|partial shade|partial sun|shade)", re.I)


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
            continue
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


# ---------- helper to draw a simple diagram ----------
from PIL import Image, ImageDraw, ImageFont

def draw_diagram(plants: list[dict], beds: list[dict]) -> Path:
    """Render a naive top-down diagram: one rectangle per bed."""
    SCALE = 50  # pixels per foot
    PAD = 40    # margin around each bed

    # pick a basic font that exists in the Streamlit image
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 14)
    except IOError:
        font = ImageFont.load_default()

    # compute canvas size (beds stacked vertically)
    canvas_w = max(int(b["width_ft"] * SCALE) for b in beds) + PAD * 2
    canvas_h = sum(int(b["length_ft"] * SCALE) + PAD for b in beds) + PAD

    img = Image.new("RGBA", (canvas_w, canvas_h), "white")
    draw = ImageDraw.Draw(img)

    y_cursor = PAD
    for bed in beds:
        w = int(bed["width_ft"] * SCALE)
        h = int(bed["length_ft"] * SCALE)
        x0, y0 = PAD, y_cursor
        x1, y1 = x0 + w, y0 + h

        # bed rectangle
        draw.rectangle([x0, y0, x1, y1], outline="black", width=2, fill="#ecf0f1")

        # bed label
        draw.text((x0 + 6, y0 + 6), bed["id"], font=font, fill="black")

        # simple plant list (all plants for now)
        plant_lines = [f"{p['name']} × {p['qty']}" for p in plants]
        text = "\n".join(plant_lines)
        draw.text((x0 + 6, y0 + 24), text, font=font, fill="green")

        y_cursor += h + PAD  # move down for next bed

    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True, exist_ok=True)
    png_path = out_dir / "garden_plan.png"
    img.save(png_path)
    return png_path



# ---------- Crew runner ----------
def run_crew(plants_text: str, beds_text: str):
    plants = parse_plants(plants_text)
    beds = parse_beds(beds_text)

    crew = create_crew()
    _ = crew.kickoff({"plants": plants, "beds": beds})   # context delivered here



    # Write a basic markdown report
    report_path = write_markdown(plants, beds)

    # Diagram not implemented yet – create an empty placeholder
    diagram_path = draw_diagram(plants, beds)
    

    return str(report_path), str(diagram_path)


if __name__ == "__main__":
    demo_plants = "Lavender 6\nTomato (Roma) 4"
    demo_beds = "Front-Left, 4x8 ft, depth 12 in, full sun, loamy"
    print(run_crew(demo_plants, demo_beds))
# END src/garden_planner/main.py
