# 🖼️ Dutch Golden Age: Still Life Explorer

**Live Demo:** [https://pushkinaalexandra.github.io/dutch-still-life-catalog/](https://pushkinaalexandra.github.io/dutch-still-life-catalog/)

An interactive digital catalog of 12 Dutch Golden Age still life paintings from the Metropolitan Museum of Art. This project was developed as a portfolio piece to demonstrate skills in data processing, front-end development, and digital curation.

---

## ✨ Features

- **Genre Filtering** — filter paintings by genre (Vanitas, Pronkstilleven, Flower Still Life, etc.)
- **Timeline** — click on any decade to filter paintings from that period
- **Dynamic Tag Cloud** — symbols appear based on current filters; click to filter by symbol
- **Search** — by artist name or painting title
- **Modal View** — click on any painting for a detailed view
- **Zoom & Drag** — zoom in (up to 4×) and drag to explore fine details
- **Interactive Hotspots** — discover hidden symbols: click "💡 Show Symbols" to see golden dots; hover to learn their meaning (e.g., "Skull: a memento mori...")
- **Keyboard Navigation** — use `←`/`→` to navigate, `+`/`-` or mouse wheel to zoom
- **Reset Filters** — one-click reset of all active filters
- **Highlight Mode** — when a tag is selected, matching cards glow with a golden shadow

---

## 🛠️ Technologies Used

- **Python** — data processing and HTML generation from CSV
- **HTML5 & CSS3** — responsive layout and styling
- **JavaScript** — filtering, timeline, dynamic tag cloud, modal, zoom, drag, hotspots
- **GitHub Pages** — hosting

---

## 📊 Data Source

- **Metropolitan Museum of Art Open Access API** — image links and metadata sourced from the Met's public collection.

---

## 📂 Project Structure
dutch-still-life-catalog/
├── generator.py # Python script that reads data.csv and generates index.html
├── data.csv # Painting metadata (Title, Artist, Date, Image URL, Description, Genre, Tags, Hotspots)
├── index.html # The final, self-contained webpage
└── README.md # Project documentation

---

## 🚀 How to Run Locally

1. Clone the repository
2. Run `python generator.py`
3. Open `index.html` in your browser

---

## 📝 Author

**Alexandra Pushkina**

---

## 🏷️ Tags

`Digital Humanities` `GLAM` `Art History` `Python` `JavaScript` `Interactive Gallery` `Museum Technology` `Metropolitan Museum of Art` `Data Visualization`
