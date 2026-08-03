# Dutch Golden Age: Still Life Explorer

**Live Demo:** https://pushkinaalexandra.github.io/dutch-still-life-catalog/

An interactive digital catalog of 12 Dutch Golden Age still life paintings from the Metropolitan Museum of Art.

## Features
- **Timeline** — filter paintings by decade (1600–1720)
- **Dynamic Tag Cloud** — click on any symbol to filter; updates based on active filters
- **Genre Filtering** — by Vanitas, Pronkstilleven, Flower Still Life, etc.
- **Search** — by artist name or painting title
- **Modal View** — click on any painting for a detailed view
- **Zoom & Drag** — zoom in (up to 4×) and drag to explore fine details

## Technologies
- Python (data processing, HTML generation)
- HTML5 / CSS3 (responsive layout, animations)
- JavaScript (filtering, timeline, tag cloud, modal, zoom, drag)

## Project Structure
- `generator.py` — reads `data.csv` and generates `index.html`
- `data.csv` — contains all painting metadata (Title, Artist, Date, Image URL, Description, Genre, Tags)
- `index.html` — the final self-contained webpage

## Data Source
Metropolitan Museum of Art Open Access API

## How to Run Locally
1. Clone the repository
2. Run `python generator.py`
3. Open `index.html` in your browser
