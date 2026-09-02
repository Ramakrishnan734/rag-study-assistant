# Milestone 12 — UI Polish & Deployment Prep

## UI Changes
- Moved all styles from inline to App.css
- Dark background: #0f0f1a
- Card sections with border-radius and subtle borders
- Purple accent color: #a78bfa
- Gradient buttons with hover effects
- Styled file input, text input, answer box, source cards

## Deployment Notes
- Backend target: Render (free tier)
- Frontend target: Netlify (free tier)
- pymupdf==1.24.3 fails to build on Python 3.14 — needs pymupdf==1.27.1 + runtime.txt fix
- CORS updated in main.py to allow Netlify URL (placeholder for now)
