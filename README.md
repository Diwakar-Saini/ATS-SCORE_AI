# ATS Score Checker

Production-ready first version of a browser ATS checker with:
- Local fallback scoring and text extraction (TXT/DOCX/PDF)
- Optional remote OCR integration for PDFs (configurable, no hard-coded secrets)
- ATS report with score, matched/missing keywords, formatting/section checks, and actionable fixes

## Run locally

No build step is required.

```bash
cd /home/runner/work/ATS-SCORE_AI/ATS-SCORE_AI
python3 -m http.server 8080
```

Open:

`http://localhost:8080/sarvam_AI/ATS%20Score%20Checker.html`

> Using a local HTTP server is recommended so browser file parsing and CDN dependencies behave consistently.

## Usage flow

1. Upload CV (`.pdf`, `.docx`, `.txt`, `.md`)
2. Click **Analyze uploaded CV**
3. Add **Target role** / **Target company**
4. Paste job description (optional but recommended for keyword matching)
5. Review score, category breakdown, keywords, and suggested fixes

The **Load sample** and **Clear both** buttons are preserved.

## Remote OCR configuration (optional)

In the app’s **Remote OCR (optional)** section:
- Enable **remote OCR for PDF files**
- Set:
  - **OCR API base URL** (example: `http://localhost:4000`)
  - **OCR endpoint path** (example: `/api/ocr/extract-text`)

Configuration is stored in browser localStorage (URL/path only).

### Request contract expected by frontend

- Method: `POST`
- Content-Type: `multipart/form-data`
- File field name: `file`

### Response contract supported by frontend

The adapter accepts common response shapes:
- Plain text response body
- JSON with text in fields such as:
  - `text`, `content`, `extractedText`, `extracted_text`
  - nested under `data`, `result`, `ocr`, `document`
  - arrays under `pages`, `items`, `results`

If remote OCR fails or returns empty text, the app falls back to local browser PDF extraction automatically.

## Security and privacy notes

- Do **not** put private API keys in frontend code.
- Prefer calling your own backend/proxy endpoint that injects secrets server-side.
- If remote OCR is enabled, PDF files are sent to your configured endpoint.
- If disabled or unavailable, processing remains in browser.
- Resume contents are not intentionally logged by this app.

## CORS / proxy guidance

If browser requests fail due to CORS:
- Enable CORS on your OCR backend for your app origin, or
- Route through a same-origin backend proxy.

Avoid exposing vendor OCR keys directly to browser clients.
