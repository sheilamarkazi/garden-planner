"""Streamlit front-end for the Garden-Planner app."""

from pathlib import Path
import streamlit as st

# Import the helper that runs your CrewAI pipeline
# (make sure src/garden_planner/main.py defines run_crew)
from src.garden_planner.main import run_crew


# ---------- Page settings ----------
st.set_page_config(page_title="Garden-Planner", page_icon="🪴", layout="wide")
st.title("🪴 Garden-Planner — turn your plant haul into a smart layout")

st.markdown(
    """
Paste the plants you bought **and** your planting-bed details, then click  
**Plan my garden**.  
The app returns a printable Markdown report and a diagram of where each plant goes.
"""
)

# ---------- Input helpers ----------
with st.expander("▶️ Input format examples", expanded=False):
    st.markdown(
        """
**Plants** – one line per item, quantity last  
```text
Lavender 6
Tomato (Roma) 4
Marigold 12
```

**Beds** – one line per bed, comma-separated fields  
```text
Front-Left, 4x8 ft, depth 12 in, full sun, loamy
Back-Corner, 6x4 ft, depth 9 in, partial shade, clay over septic
```
"""
    )

plants_text = st.text_area(
    "Plant list",
    placeholder="Lavender 6\\nTomato (Roma) 4\\nMarigold 12",
    height=150,
)

beds_text = st.text_area(
    "Bed specifications",
    placeholder="Front-Left, 4x8 ft, depth 12 in, full sun, loamy",
    height=150,
)

# ---------- Run button ----------
if st.button("Plan my garden", type="primary"):
    if not plants_text.strip() or not beds_text.strip():
        st.warning(
            "Please provide both a plant list and at least one bed description."
        )
        st.stop()

    with st.spinner("Planting gnomes are thinking…"):
        # run_crew should return (report_path, diagram_path)
        report_path, diagram_path = run_crew(plants_text, beds_text)

    st.success("Garden plan ready!")

    # ---------- Display outputs ----------
    st.subheader("📄 Planting report")
    st.download_button(
        label="Download report.md",
        data=Path(report_path).read_bytes(),
        file_name="garden_report.md",
        mime="text/markdown",
    )
    st.markdown(Path(report_path).read_text())

    st.subheader("🖼️ Garden diagram")
    st.image(str(diagram_path))
