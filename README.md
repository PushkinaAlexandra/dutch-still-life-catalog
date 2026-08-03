# 🖼️ Dutch Golden Age: Still Life Explorer

**Live Demo:** [https://pushkinaalexandra.github.io/dutch-still-life-catalog/](https://pushkinaalexandra.github.io/dutch-still-life-catalog/)

An interactive digital catalog of 12 Dutch Golden Age still life paintings from the Metropolitan Museum of Art.

## ✨ Features
- **Genre Filtering** — filter paintings by genre (Vanitas, Pronkstilleven, Flower Still Life, etc.)
- **Timeline** — click on any decade to filter paintings from that period
- **Dynamic Tag Cloud** — symbols appear based on current filters; click to filter by symbol
- **Search** — by artist name or painting title
- **Modal View** — click on any painting for a detailed view
- **Zoom & Drag** — zoom in (up to 4×) and drag to explore fine details
- **Interactive Hotspots** — discover hidden symbols: click "💡 Show Symbols" to see golden dots; hover to learn their meaning (e.g., "Skull: a memento mori...")

## 🛠️ Technologies Used
- **Python** — data processing and HTML generation from CSV
- **HTML5 & CSS3** — responsive layout and styling
- **JavaScript** — filtering, timeline, dynamic tag cloud, modal, zoom, drag, hotspots
- **GitHub Pages** — hosting

## 📊 Data Source
- **Metropolitan Museum of Art Open Access API** — image links and metadata sourced from the Met's public collection.

## 📂 Project Structure
- `generator.py` — Python script that reads `data.csv` and generates `index.html`
- `data.csv` — contains all metadata (Title, Artist, Date, Image URL, Description, Genre, Tags, Hotspots)
- `index.html` — the final, self-contained webpage ready for deployment

## 🚀 How to Run Locally
1. Clone the repository
2. Run `python generator.py`
3. Open `index.html` in your browser
