import csv
import os
import re
from collections import Counter

# --- CONFIGURATION ---
TITLE = "Dutch Golden Age: Still Life Collection"
SUBTITLE = "12 Masterpieces from the Metropolitan Museum of Art"
AUTHOR = "Alexandra Pushkina"
CSV_FILE = "data.csv"


# --- ENCODING DETECTION ---
def detect_encoding(file_path):
    encodings = ['utf-8-sig', 'utf-8', 'cp1251', 'windows-1251', 'latin-1', 'cp866']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                f.read()
                return enc
        except UnicodeDecodeError:
            continue
    return 'utf-8'


# --- READ CSV ---
encoding = detect_encoding(CSV_FILE)
print(f"🔍 Detected encoding: {encoding}")

items = []
with open(CSV_FILE, 'r', encoding=encoding) as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row.get('Image') and row.get('Title'):
            items.append(row)

if not items:
    print("❌ No data found!")
    exit()

print(f"✅ Found {len(items)} items. Generating HTML...")

# --- COLLECT UNIQUE GENRES ---
genres = sorted(set(item.get('Genre', 'Uncategorized') for item in items if item.get('Genre')))
if not genres:
    genres = ['All']


# --- PARSE YEARS FOR TIMELINE (UPDATED) ---
def extract_year(date_str):
    """Extract a year from various date formats."""
    if not date_str:
        return None

    # First try to find a 4-digit number (e.g., "1659", "1628")
    match = re.search(r'\b(16\d{2}|17\d{2})\b', date_str)
    if match:
        return int(match.group(1))

    # Try to find a pattern like "1650s" or "1650s" with spaces
    match = re.search(r'(16\d{2}|17\d{2})\s*s', date_str)
    if match:
        return int(match.group(1))

    return None


years = []
for item in items:
    year = extract_year(item.get('Object Date', ''))
    if year:
        years.append(year)

if years:
    min_year = min(years)
    max_year = max(years)
    min_decade = (min_year // 10) * 10
    max_decade = (max_year // 10) * 10
    decades = list(range(min_decade, max_decade + 1, 10))
else:
    decades = []

# --- COLLECT TAGS ---
tag_counter = Counter()
for item in items:
    tags = item.get('Tags', '')
    if tags:
        for tag in tags.split(','):
            tag = tag.strip()
            if tag:
                tag_counter[tag] += 1

sorted_tags = sorted(tag_counter.items(), key=lambda x: x[1], reverse=True)
max_tag_count = max(tag_counter.values()) if tag_counter else 1

# --- BUILD DATA FOR JAVASCRIPT ---
js_items = []
for item in items:
    title = item.get('Title', 'Untitled').replace("'", "\\'").replace('"', '\\"')
    artist = item.get('Artist', 'Unknown').replace("'", "\\'").replace('"', '\\"')
    year = item.get('Object Date', '').replace("'", "\\'").replace('"', '\\"')
    desc = item.get('Description', '').replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
    image = item.get('Image', '').replace("'", "\\'").replace('"', '\\"')
    genre = item.get('Genre', 'Uncategorized').replace("'", "\\'").replace('"', '\\"')
    tags = item.get('Tags', '').replace("'", "\\'").replace('"', '\\"')
    js_items.append(
        f"{{title:'{title}',artist:'{artist}',year:'{year}',desc:'{desc}',image:'{image}',genre:'{genre}',tags:'{tags}'}}")

js_data = '[' + ','.join(js_items) + ']'

# --- GENERATE HTML ---
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #f9f7f4; margin: 0; padding: 20px; color: #2c2c2c; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ font-weight: 300; font-size: 2.5rem; text-align: center; border-bottom: 2px solid #d4c9b8; padding-bottom: 10px; }}
        .subtitle {{ text-align: center; font-size: 1.1rem; color: #6b5f4f; margin-top: -10px; margin-bottom: 30px; }}

        .timeline-section {{ background: white; border-radius: 8px; padding: 20px 30px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
        .timeline-title {{ font-size: 0.9rem; font-weight: 600; color: #6b5f4f; margin-bottom: 15px; letter-spacing: 1px; text-transform: uppercase; }}
        .timeline {{ display: flex; justify-content: space-between; align-items: center; position: relative; padding: 10px 0; }}
        .timeline::before {{ content: ''; position: absolute; top: 50%; left: 0; right: 0; height: 2px; background: #d4c9b8; transform: translateY(-50%); }}
        .timeline-decade {{ display: flex; flex-direction: column; align-items: center; cursor: pointer; padding: 5px 0; position: relative; z-index: 1; transition: all 0.3s ease; }}
        .timeline-decade .year {{ font-size: 0.8rem; color: #8c7d6b; background: white; padding: 0 6px; transition: all 0.3s ease; }}
        .timeline-decade .dot {{ width: 12px; height: 12px; border-radius: 50%; background: #d4c9b8; border: 2px solid white; box-shadow: 0 1px 4px rgba(0,0,0,0.1); transition: all 0.3s ease; margin-top: 4px; }}
        .timeline-decade .count {{ font-size: 0.6rem; color: #b0a392; margin-top: 2px; transition: all 0.3s ease; }}
        .timeline-decade:hover .year {{ color: #2c2c2c; font-weight: 600; }}
        .timeline-decade:hover .dot {{ background: #6b5f4f; transform: scale(1.3); }}
        .timeline-decade.active .dot {{ background: #6b5f4f; transform: scale(1.3); }}
        .timeline-decade.active .year {{ color: #2c2c2c; font-weight: 600; }}
        .timeline-decade.has-items .dot {{ background: #6b5f4f; }}

        .tag-cloud-section {{ background: white; border-radius: 8px; padding: 20px 30px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
        .tag-cloud-title {{ font-size: 0.9rem; font-weight: 600; color: #6b5f4f; margin-bottom: 15px; letter-spacing: 1px; text-transform: uppercase; }}
        .tag-cloud {{ display: flex; flex-wrap: wrap; gap: 8px 12px; justify-content: center; }}
        .tag {{ cursor: pointer; padding: 4px 14px; border-radius: 20px; background: #f0ede8; color: #4a3f33; font-size: 0.85rem; transition: all 0.3s ease; border: 1px solid transparent; }}
        .tag:hover {{ background: #d4c9b8; transform: scale(1.05); }}
        .tag.active {{ background: #6b5f4f; color: white; border-color: #6b5f4f; }}

        .filter-bar {{ text-align: center; margin-bottom: 25px; display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; }}
        .filter-btn {{ padding: 8px 20px; border: 1px solid #d4c9b8; background: white; border-radius: 30px; cursor: pointer; font-size: 0.9rem; transition: all 0.2s ease; color: #2c2c2c; }}
        .filter-btn:hover {{ background: #eae5dd; }}
        .filter-btn.active {{ background: #6b5f4f; color: white; border-color: #6b5f4f; }}
        .search-bar {{ text-align: center; margin-bottom: 25px; }}
        .search-bar input {{ padding: 10px 20px; width: 60%; max-width: 400px; border: 1px solid #ccc; border-radius: 30px; font-size: 1rem; outline: none; }}
        .search-bar input:focus {{ border-color: #6b5f4f; }}
        .gallery {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; }}
        .card {{ background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-radius: 8px; overflow: hidden; transition: transform 0.2s ease; display: block; cursor: pointer; }}
        .card:hover {{ transform: translateY(-5px); }}
        .card img {{ width: 100%; height: 220px; object-fit: cover; background: #eae5dd; }}
        .card-content {{ padding: 15px; }}
        .card-title {{ font-size: 1rem; font-weight: 600; margin: 0 0 5px 0; }}
        .card-artist {{ font-size: 0.9rem; color: #4a3f33; margin: 0 0 5px 0; font-style: italic; }}
        .card-year {{ font-size: 0.8rem; color: #7e6f5c; margin: 0 0 8px 0; }}
        .card-desc {{ font-size: 0.85rem; line-height: 1.4; color: #3d352b; margin: 0; }}
        .card-genre {{ display: inline-block; margin-top: 8px; font-size: 0.75rem; background: #eae5dd; padding: 2px 12px; border-radius: 20px; color: #4a3f33; }}
        .card-tags {{ display: flex; flex-wrap: wrap; gap: 4px; margin-top: 6px; }}
        .card-tag {{ font-size: 0.6rem; background: #f5f0ea; padding: 1px 8px; border-radius: 12px; color: #6b5f4f; }}
        .footer {{ text-align: center; margin-top: 40px; font-size: 0.8rem; color: #8c7d6b; border-top: 1px solid #ddd; padding-top: 20px; }}

        .modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.92); }}
        .modal.open {{ display: flex; align-items: center; justify-content: center; }}
        .modal-content {{ max-width: 90%; max-height: 90%; display: flex; flex-direction: column; align-items: center; position: relative; }}
        .modal-image-container {{ width: 100%; max-height: 80vh; overflow: hidden; display: flex; align-items: center; justify-content: center; position: relative; cursor: grab; background: transparent; }}
        .modal-image-container:active {{ cursor: grabbing; }}
        .modal-image-container img {{ max-width: 100%; max-height: 80vh; object-fit: contain; user-select: none; -webkit-user-drag: none; }}
        .modal-close {{ position: absolute; top: 20px; right: 30px; color: white; font-size: 2.5rem; font-weight: 300; cursor: pointer; transition: 0.3s; z-index: 10; background: none; border: none; }}
        .modal-close:hover {{ color: #d4c9b8; transform: scale(1.1); }}
        .modal-nav {{ position: absolute; top: 50%; transform: translateY(-50%); color: white; font-size: 3rem; cursor: pointer; background: rgba(0,0,0,0.3); padding: 10px 16px; border-radius: 50%; transition: 0.3s; z-index: 10; border: none; user-select: none; }}
        .modal-nav:hover {{ background: rgba(255,255,255,0.2); }}
        .modal-prev {{ left: 20px; }}
        .modal-next {{ right: 20px; }}
        .modal-info {{ color: white; text-align: center; padding: 15px 20px; max-width: 80%; background: rgba(0,0,0,0.6); border-radius: 8px; margin-top: 15px; }}
        .modal-info h2 {{ margin: 0 0 5px 0; font-weight: 400; font-size: 1.4rem; }}
        .modal-info p {{ margin: 3px 0; font-size: 0.95rem; color: #d4c9b8; }}
        .modal-info .modal-desc {{ font-size: 0.85rem; color: #bbb; margin-top: 8px; max-width: 600px; }}
        .modal-zoom-controls {{ position: absolute; bottom: 100px; right: 30px; display: flex; flex-direction: column; gap: 10px; z-index: 10; }}
        .modal-zoom-controls button {{ background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3); border-radius: 50%; width: 40px; height: 40px; font-size: 1.2rem; cursor: pointer; transition: 0.3s; }}
        .modal-zoom-controls button:hover {{ background: rgba(255,255,255,0.3); }}
        .modal-counter {{ position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); color: rgba(255,255,255,0.5); font-size: 0.9rem; z-index: 10; }}
    </style>
</head>
<body>
<div class="container">
    <h1>{TITLE}</h1>
    <p class="subtitle">{SUBTITLE} · curated by {AUTHOR}</p>
"""

# --- TIMELINE ---
if decades:
    html_content += """
    <div class="timeline-section">
        <div class="timeline-title">📅 Timeline · click to filter by decade</div>
        <div class="timeline" id="timeline">
    """
    for decade in decades:
        # Check if any item falls in this decade (using the updated extract_year)
        has_items = any(extract_year(item.get('Object Date', '')) and decade <= extract_year(
            item.get('Object Date', '')) < decade + 10 for item in items)
        active_class = 'has-items' if has_items else ''
        count = sum(1 for item in items if extract_year(item.get('Object Date', '')) and decade <= extract_year(
            item.get('Object Date', '')) < decade + 10)
        html_content += f"""
            <div class="timeline-decade {active_class}" data-decade="{decade}">
                <span class="year">{decade}s</span>
                <span class="dot"></span>
                <span class="count">{count}</span>
            </div>
        """
    html_content += """
        </div>
    </div>
    """

# --- TAG CLOUD ---
if tag_counter:
    html_content += """
    <div class="tag-cloud-section">
        <div class="tag-cloud-title">🏷️ Tag Cloud · click to filter by symbol</div>
        <div class="tag-cloud" id="tagCloud">
    """
    for tag, count in sorted_tags:
        size = 0.7 + (count / max_tag_count) * 0.7
        html_content += f"""
            <span class="tag" data-tag="{tag}" style="font-size:{size}rem;">{tag} ({count})</span>
        """
    html_content += """
        </div>
    </div>
    """

html_content += """
    <div class="filter-bar">
        <button class="filter-btn active" data-genre="all">All</button>
"""

for genre in genres:
    html_content += f'        <button class="filter-btn" data-genre="{genre}">{genre}</button>\n'

html_content += """
    </div>
    <div class="search-bar">
        <input type="text" id="searchInput" placeholder="🔍 Search by artist or title..." onkeyup="filterGallery()">
    </div>
    <div class="gallery" id="gallery">
"""

# --- CARDS ---
for idx, item in enumerate(items):
    title = item.get('Title', 'Untitled')
    artist = item.get('Artist', 'Unknown')
    year = item.get('Object Date', '')
    desc = item.get('Description', '')
    img = item.get('Image', '')
    genre = item.get('Genre', 'Uncategorized')
    tags = item.get('Tags', '')

    tag_spans = ''
    if tags:
        for tag in tags.split(','):
            tag = tag.strip()
            if tag:
                tag_spans += f'<span class="card-tag">{tag}</span>'

    html_content += f"""
        <div class="card" data-index="{idx}" data-genre="{genre}" data-search="{title.lower()} {artist.lower()}" data-year="{extract_year(year) or ''}" data-tags="{tags.lower()}">
            <img src="{img}" alt="{title}" loading="lazy" onerror="this.src='https://via.placeholder.com/280x220/f0ede8/6b5f4f?text=No+Image'">
            <div class="card-content">
                <p class="card-title">{title}</p>
                <p class="card-artist">{artist}</p>
                <p class="card-year">{year}</p>
                <p class="card-desc">{desc}</p>
                <span class="card-genre">{genre}</span>
                <div class="card-tags">{tag_spans}</div>
            </div>
        </div>
    """

html_content += """
    </div>
    <div class="footer">Data source: Metropolitan Museum of Art · Open Access</div>
</div>

<!-- ===== MODAL ===== -->
<div id="modal" class="modal">
    <button class="modal-close" id="modalClose">&times;</button>
    <button class="modal-nav modal-prev" id="modalPrev">&#10094;</button>
    <button class="modal-nav modal-next" id="modalNext">&#10095;</button>
    <div class="modal-content">
        <div class="modal-image-container" id="modalImageContainer">
            <img id="modalImage" src="" alt="">
        </div>
        <div class="modal-info" id="modalInfo">
            <h2 id="modalTitle"></h2>
            <p id="modalArtist"></p>
            <p id="modalYear"></p>
            <p class="modal-desc" id="modalDesc"></p>
        </div>
    </div>
    <div class="modal-zoom-controls">
        <button id="zoomIn">+</button>
        <button id="zoomOut">-</button>
        <button id="zoomReset">&#9851;</button>
    </div>
    <div class="modal-counter" id="modalCounter"></div>
</div>

<script>
    const allItems = """ + js_data + """;

    // --- STATE ---
    let currentFilteredItems = [];
    let currentIndex = 0;
    let scale = 1;
    let translateX = 0, translateY = 0;
    let isDragging = false;
    let startX = 0, startY = 0;
    let dragStartX = 0, dragStartY = 0;
    let activeDecade = null;
    let activeTag = null;
    let activeGenre = 'all';

    let imgNaturalW = 0, imgNaturalH = 0;
    let containerW = 0, containerH = 0;
    let imgDisplayW = 0, imgDisplayH = 0;

    const modal = document.getElementById('modal');
    const modalImg = document.getElementById('modalImage');
    const modalContainer = document.getElementById('modalImageContainer');
    const modalTitle = document.getElementById('modalTitle');
    const modalArtist = document.getElementById('modalArtist');
    const modalYear = document.getElementById('modalYear');
    const modalDesc = document.getElementById('modalDesc');
    const modalCounter = document.getElementById('modalCounter');

    // --- UPDATE DIMENSIONS ---
    function updateDimensions() {
        const containerRect = modalContainer.getBoundingClientRect();
        containerW = containerRect.width;
        containerH = containerRect.height;
        imgNaturalW = modalImg.naturalWidth || 1;
        imgNaturalH = modalImg.naturalHeight || 1;
        const ratioX = containerW / imgNaturalW;
        const ratioY = containerH / imgNaturalH;
        const fitRatio = Math.min(ratioX, ratioY);
        imgDisplayW = imgNaturalW * fitRatio;
        imgDisplayH = imgNaturalH * fitRatio;
    }

    // --- CLAMP POSITION ---
    function clampPosition() {
        if (scale <= 1) {
            translateX = 0;
            translateY = 0;
            return;
        }
        const zoomedW = imgDisplayW * scale;
        const zoomedH = imgDisplayH * scale;
        const maxX = Math.max(0, (zoomedW - containerW) / 2);
        const maxY = Math.max(0, (zoomedH - containerH) / 2);
        translateX = Math.min(Math.max(translateX, -maxX), maxX);
        translateY = Math.min(Math.max(translateY, -maxY), maxY);
    }

    // --- UPDATE TRANSFORM ---
    function updateTransform() {
        modalImg.style.transform = 'translate(' + translateX + 'px, ' + translateY + 'px) scale(' + scale + ')';
    }

    // --- APPLY ZOOM ---
    function applyZoom(newScale) {
        scale = Math.min(Math.max(newScale, 0.5), 4);
        updateDimensions();
        clampPosition();
        updateTransform();
    }

    // --- MODAL ---
    function getVisibleItems() {
        const cards = document.querySelectorAll('.card');
        const visible = [];
        cards.forEach(card => {
            if (card.style.display !== 'none') {
                visible.push(parseInt(card.dataset.index));
            }
        });
        return visible;
    }

    function openModal(index) {
        const visible = getVisibleItems();
        if (visible.length === 0) return;
        currentFilteredItems = visible;
        const pos = visible.indexOf(index);
        if (pos === -1) return;
        currentIndex = pos;
        showItem();
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';
    }

    function showItem() {
        const item = allItems[currentFilteredItems[currentIndex]];
        modalImg.src = item.image;
        modalTitle.textContent = item.title;
        modalArtist.textContent = item.artist;
        modalYear.textContent = item.year;
        modalDesc.textContent = item.desc || '';
        modalCounter.textContent = (currentIndex + 1) + ' / ' + currentFilteredItems.length;
        scale = 1;
        translateX = 0;
        translateY = 0;
        modalImg.onload = function() {
            updateDimensions();
            clampPosition();
            updateTransform();
        };
        setTimeout(function() {
            updateDimensions();
            clampPosition();
            updateTransform();
        }, 100);
    }

    function closeModal() {
        modal.classList.remove('open');
        document.body.style.overflow = '';
    }

    function changeImage(direction) {
        if (currentFilteredItems.length === 0) return;
        currentIndex = (currentIndex + direction + currentFilteredItems.length) % currentFilteredItems.length;
        showItem();
    }

    function resetZoom() { applyZoom(1); }
    function zoomIn() { applyZoom(scale + 0.2); }
    function zoomOut() { applyZoom(scale - 0.2); }

    // --- DRAG ---
    modalContainer.addEventListener('mousedown', function(e) {
        if (scale <= 1) return;
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        dragStartX = translateX;
        dragStartY = translateY;
        modalContainer.style.cursor = 'grabbing';
        e.preventDefault();
    });

    document.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        translateX = dragStartX + dx;
        translateY = dragStartY + dy;
        clampPosition();
        updateTransform();
    });

    document.addEventListener('mouseup', function() {
        if (isDragging) {
            isDragging = false;
            modalContainer.style.cursor = 'grab';
        }
    });

    // --- TOUCH ---
    let touchStartX = 0, touchStartY = 0;
    let touchDragStartX = 0, touchDragStartY = 0;

    modalContainer.addEventListener('touchstart', function(e) {
        if (scale <= 1) return;
        const touch = e.touches[0];
        touchStartX = touch.clientX;
        touchStartY = touch.clientY;
        touchDragStartX = translateX;
        touchDragStartY = translateY;
    }, { passive: true });

    modalContainer.addEventListener('touchmove', function(e) {
        if (scale <= 1) return;
        const touch = e.touches[0];
        const dx = touch.clientX - touchStartX;
        const dy = touch.clientY - touchStartY;
        translateX = touchDragStartX + dx;
        translateY = touchDragStartY + dy;
        clampPosition();
        updateTransform();
    }, { passive: true });

    // --- EVENTS ---
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', function() {
            openModal(parseInt(this.dataset.index));
        });
    });

    document.getElementById('modalClose').addEventListener('click', closeModal);
    document.getElementById('modalPrev').addEventListener('click', function(e) {
        e.stopPropagation();
        changeImage(-1);
    });
    document.getElementById('modalNext').addEventListener('click', function(e) {
        e.stopPropagation();
        changeImage(1);
    });
    document.getElementById('zoomIn').addEventListener('click', function(e) {
        e.stopPropagation();
        zoomIn();
    });
    document.getElementById('zoomOut').addEventListener('click', function(e) {
        e.stopPropagation();
        zoomOut();
    });
    document.getElementById('zoomReset').addEventListener('click', function(e) {
        e.stopPropagation();
        resetZoom();
    });

    modal.addEventListener('click', function(e) {
        if (e.target === modal) closeModal();
    });

    document.addEventListener('keydown', function(e) {
        if (!modal.classList.contains('open')) return;
        if (e.key === 'Escape') closeModal();
        if (e.key === 'ArrowLeft') changeImage(-1);
        if (e.key === 'ArrowRight') changeImage(1);
    });

    // --- TIMELINE ---
    const decadeElements = document.querySelectorAll('.timeline-decade');
    decadeElements.forEach(el => {
        el.addEventListener('click', function() {
            const decade = parseInt(this.dataset.decade);
            if (activeDecade === decade) {
                activeDecade = null;
                this.classList.remove('active');
            } else {
                decadeElements.forEach(d => d.classList.remove('active'));
                activeDecade = decade;
                this.classList.add('active');
            }
            applyAllFilters();
        });
    });

    // --- TAG CLOUD ---
    const tagElements = document.querySelectorAll('.tag');
    tagElements.forEach(el => {
        el.addEventListener('click', function() {
            const tag = this.dataset.tag;
            if (activeTag === tag) {
                activeTag = null;
                this.classList.remove('active');
            } else {
                tagElements.forEach(t => t.classList.remove('active'));
                activeTag = tag;
                this.classList.add('active');
            }
            applyAllFilters();
        });
    });

    // --- GENRE FILTER ---
    const filterButtons = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.card');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            activeGenre = this.dataset.genre;
            applyAllFilters();
            if (modal.classList.contains('open')) closeModal();
        });
    });

    // --- SEARCH ---
    document.getElementById('searchInput').addEventListener('keyup', function() {
        applyAllFilters();
        if (modal.classList.contains('open')) closeModal();
    });

// --- UPDATE TAG CLOUD BASED ON VISIBLE CARDS ---
function updateTagCloud() {
    const visibleCards = document.querySelectorAll('.card[style*="display: block"]');
    const tagCounts = {};
    
    visibleCards.forEach(card => {
        const tags = card.dataset.tags || '';
        if (tags) {
            tags.split(',').forEach(tag => {
                tag = tag.trim();
                if (tag) {
                    tagCounts[tag] = (tagCounts[tag] || 0) + 1;
                }
            });
        }
    });
    
    const tagCloud = document.getElementById('tagCloud');
    if (!tagCloud) return;
    
    // Clear current cloud
    tagCloud.innerHTML = '';
    
    // Get max count for sizing
    const maxCount = Math.max(...Object.values(tagCounts), 1);
    
    // Sort tags alphabetically
    const sortedTags = Object.keys(tagCounts).sort();
    
    if (sortedTags.length === 0) {
        tagCloud.innerHTML = '<span style="color: #b0a392; font-size: 0.9rem;">No tags match current filters</span>';
        return;
    }
    
    sortedTags.forEach(tag => {
        const count = tagCounts[tag];
        const size = 0.7 + (count / maxCount) * 0.7;
        const span = document.createElement('span');
        span.className = 'tag';
        span.dataset.tag = tag;
        span.style.fontSize = size + 'rem';
        span.textContent = tag + ' (' + count + ')';
        
        // Add click handler for filtering by tag
        span.addEventListener('click', function() {
            const tag = this.dataset.tag;
            if (activeTag === tag) {
                activeTag = null;
                this.classList.remove('active');
            } else {
                document.querySelectorAll('.tag').forEach(t => t.classList.remove('active'));
                activeTag = tag;
                this.classList.add('active');
            }
            applyAllFilters();
        });
        
        // Preserve active state if this tag is currently active
        if (activeTag === tag) {
            span.classList.add('active');
        }
        
        tagCloud.appendChild(span);
    });
}

    // --- MASTER FILTER FUNCTION ---
    function applyAllFilters() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    cards.forEach(card => {
        const cardGenre = card.dataset.genre;
        const cardSearch = card.dataset.search;
        const cardYear = parseInt(card.dataset.year) || null;
        const cardTags = card.dataset.tags || '';

        // Genre filter
        const matchesGenre = activeGenre === 'all' || cardGenre === activeGenre;

        // Search filter
        const matchesSearch = cardSearch.includes(search);

        // Decade filter
        let matchesDecade = true;
        if (activeDecade !== null) {
            if (cardYear === null) {
                matchesDecade = false;
            } else {
                matchesDecade = cardYear >= activeDecade && cardYear < activeDecade + 10;
            }
        }

        // Tag filter
        let matchesTag = true;
        if (activeTag !== null) {
            matchesTag = cardTags.includes(activeTag.toLowerCase());
        }

        const visible = matchesGenre && matchesSearch && matchesDecade && matchesTag;
        card.style.display = visible ? 'block' : 'none';
    });

    // --- UPDATE TAG CLOUD AFTER FILTERING ---
    updateTagCloud();
}

    // --- WINDOW RESIZE ---
    window.addEventListener('resize', function() {
        if (modal.classList.contains('open')) {
            updateDimensions();
            clampPosition();
            updateTransform();
        }
    });

    // Initialize
    applyAllFilters();
</script>
</body>
</html>
"""

# --- SAVE HTML ---
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Done! Open index.html in your browser.")