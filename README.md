# 🖼️ Dutch Golden Age: Still Life Explorer

**Live Demo:** [https://pushkinaalexandra.github.io/dutch-still-life-catalog/](https://pushkinaalexandra.github.io/dutch-still-life-catalog/)

An interactive digital catalog of 12 Dutch Golden Age still life paintings from the Metropolitan Museum of Art. This project was developed as a portfolio piece to demonstrate skills in data processing, front-end development, and digital curation.

## ✨ Features
- **Genre Filtering:** Filter paintings by genre (Vanitas, Pronkstilleven, Flower Still Life, Sottobosco, Hunting/Gamepiece, Banketje).
- **Search:** Real-time search by artist name or painting title.
- **Modal View:** Click on any painting to open a detailed modal window.
- **Zoom & Drag:** Zoom in (up to 4x) and drag the image to explore fine details and textures.
- **Filter-Aware Navigation:** The arrows in the modal window cycle only through the currently filtered paintings.

## 🛠️ Technologies Used
- **Python:** Data processing and HTML generation from CSV.
- **HTML5 & CSS3:** Responsive layout and styling.
- **JavaScript:** Interactive features (filtering, search, modal, zoom, drag).
- **GitHub Pages:** Hosting.

## 📊 Data Source
- **Metropolitan Museum of Art Open Access API:** Image links and metadata sourced from the Met's public collection.

## 📂 Project Structure
- `generator.py`: Python script that reads `data.csv` and generates `index.html`.
- `data.csv`: Contains all metadata for the 12 paintings (Title, Artist, Date, Image URL, Description, Genre).
- `index.html`: The final, self-contained webpage ready for deployment.

## 🚀 How to Run Locally
1. Clone the repository.
2. Ensure `data.csv` is in the same directory.
3. Run `python generator.py`.
4. Open `index.html` in your browser.

## 📝 Author
**Alexandra Pushkina** 
