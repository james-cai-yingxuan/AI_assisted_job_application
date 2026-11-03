# AI-Assisted Job Application — V2

This is an incremental upgrade of the original V1 HTML prototype, not a redesign. `index.html` retains the original page layout, styling, file picker, score card, suggestions card, cover-letter card and copy feature.

## Files
- `index.html` — original V1 layout with asynchronous API submission and dynamic results.
- `server.py` — small Flask backend, PDF/DOCX/TXT text extraction, OpenAI request and JSON response.
- `requirements.txt` — Python dependencies.
- `.env.example` — environment variable names; do not enter a real key into tracked files.
- `.gitignore` — excludes local secrets and Python virtual environments.
- `test_server.py` — offline backend tests with mock AI responses.

## Setup (Windows PowerShell)

1. Install Python 3.10 or newer.
2. In PowerShell, change to this extracted folder.
3. Create a virtual environment and install dependencies:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

4. Configure the API key **in PowerShell**, not in HTML or JavaScript:

   ```powershell
   $env:OPENAI_API_KEY = 'YOUR_ACTUAL_KEY_ON_YOUR_COMPUTER_ONLY'
   # Optional: $env:OPENAI_MODEL = 'gpt-4.1-mini'
   ```

   If you prefer persistent local configuration, use your operating system's user environment variables and restart PowerShell. Never share, commit or screenshot the key.

5. Start the backend:

   ```powershell
   python server.py
   ```

6. Open **http://127.0.0.1:5000** in your browser. Do **not** double-click `index.html`: the API requests require the backend server.

## Test the API connection before analysis

In a **second** PowerShell window while the server is running:

```powershell
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:5000/api/test-connection
```

Expected: `connected: true` and a short reply such as `CONNECTION_OK`. This is a **real billable API request**; it only runs when you issue the command. If it fails, check your API key, billing, network connection and access to the selected model. Do not paste the key into bug reports.

Then upload a **text-based** PDF/DOCX/TXT resume, paste the role description and click **Analyse My Fit**. The new results will appear in the same three V1 result cards.

## Other platforms

On macOS/Linux use `python3 -m venv .venv`, `source .venv/bin/activate`, `pip install -r requirements.txt`, `export OPENAI_API_KEY='...'`, then `python server.py`.

## Security and prototype limitations

- The key is read by the Python server from `OPENAI_API_KEY`; it never appears in client code or API responses.
- Resumes and job descriptions are transmitted to the **local** backend, which sends extracted text to OpenAI for analysis. Only use personal data you are comfortable sending to this service.
- Files are processed in memory, not intentionally saved to disk; the server is bound to `127.0.0.1` and is **not production-ready**. Do not deploy publicly without authentication, rate limiting, CSRF protection, privacy controls and HTTPS.
- Max request size is 5 MB. Scanned/image-only PDFs (no extractable text) are not supported.
- The AI-generated score is an illustrative judgement, not an ATS score, hiring probability or verified candidate assessment. Always fact-check the generated cover letter.
- API usage may incur charges. Never commit credentials.

## Tests

```powershell
pip install pytest
pytest -q
```

These offline tests mock the AI connection and **do not call OpenAI**. A real connection test is only possible on your machine with your API key.
