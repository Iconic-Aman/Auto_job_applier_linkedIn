# 🤖 Auto Job Applier — LinkedIn (Full Repo Overview)

> **Purpose:** Read this file to fully understand the codebase without digging through individual files.  
> **Owner fork:** Aman Kumar Srivastava | **Original Author:** Sai Vignesh Golla (GitHub: GodsScion)  
> **License:** GNU AGPL v3

---

## 🧭 What This Repo Does — 30-Second Summary

This repo automates the entire LinkedIn job-application workflow using **Python + Selenium**, and also ships a **Chrome Extension** for autofilling external job-application forms on any website.

**Two distinct systems live here side-by-side:**

| System | Tech | What it does |
|---|---|---|
| **LinkedIn Bot** (`runAiBot.py`) | Python + Selenium | Opens Chrome, logs into LinkedIn, searches for Easy Apply jobs, filters/screens them, and auto-fills + submits applications |
| **Chrome Extension** (`extension/`) | JS (MV3) + Python FastAPI | Injects a content script on any page that detects form fields, sends them to a local AI backend, and fills them with answers derived from `resume_details.txt` |

---

## 📁 Root-Level Files

| File | Purpose |
|---|---|
| `runAiBot.py` | **Main brain** — 1267 lines, orchestrates the entire LinkedIn bot loop |
| `app.py` | Flask server exposing a small REST API + HTML UI to browse application history CSVs |
| `.env` | Secrets: `NVIDIA_API_KEY`, `NVIDIA_API_URL`, `LLM_MODEL`, `PASSWORD`, `RESUME_PDF_PATH` |
| `INSTRUCTIONS.ai` | Antigravity AI context hints |
| `README.md` | Original project README (setup, usage, FAQ) |

---

## 📁 Folder-by-Folder Breakdown

### `config/` — All User-Configurable Settings

This is the **only folder users need to edit** before running. Six Python files act as flat config:

| File | What it controls |
|---|---|
| `secrets.py` | LinkedIn credentials, AI provider (`openai`/`deepseek`/`gemini`), `llm_api_url`, `llm_api_key`, `llm_model`, `stream_output`, `use_AI`. Currently pointed at NVIDIA API (`qwen/qwen2.5-7b-instruct`). |
| `settings.py` | Global bot behavior: `run_in_background`, `stealth_mode`, `safe_mode`, `close_tabs`, `follow_companies`, `run_non_stop`, `smooth_scroll`, `keep_screen_awake`, `showAiErrorAlerts`, file/log paths, click gap |
| `search.py` | LinkedIn job-search preferences: `search_terms` (list), `search_location`, `switch_number` (apps per search term), `sort_by`, `date_posted`, `easy_apply_only=True`, experience level, job type, on-site filters, blacklist bad/good words, `current_experience` |
| `questions.py` | Auto-answers for Easy Apply forms: resume path, `years_of_experience`, `require_visa`, `website`, `linkedIn`, `cover_letter`, `linkedin_summary`, `desired_salary`, `current_ctc`, `notice_period`, `user_information_all` (full profile text fed to AI), `pause_before_submit`, `pause_at_failed_question` |
| `personals.py` | Personal details: `first_name`, `last_name`, `phone_number`, `current_city`, `country`, `state`, `ethnicity`, `gender`, `disability_status`, `veteran_status` |
| `resume.py` | (Small, path helper for resume generation — experimental) |

> ⚠️ **Never commit `secrets.py` or `.env` to a public repo.** Both contain API keys and LinkedIn passwords.

---

### `modules/` — Core Bot Logic

| File / Sub-folder | Purpose |
|---|---|
| `open_chrome.py` | Initializes a Chrome WebDriver session using Selenium or `undetected_chromedriver` (stealth mode). Finds the user's default Chrome profile, maximizes window, returns `(options, driver, actions, wait)` |
| `helpers.py` | Shared utilities: `print_lg` (print + write to log file), `buffer` (random sleep), `make_directories`, `find_default_profile_directory` (cross-platform), `calculate_date_posted`, `convert_to_lakhs`, `convert_to_json`, `truncate_for_csv`, `manual_login_retry` |
| `clickers_and_finders.py` | Selenium click/find helpers: `wait_span_click`, `multi_sel`, `boolean_button_click`, `scroll_to_view`, `text_input_by_ID`, `company_search_click`. Wraps Selenium with retry + buffer logic |
| `validator.py` | Validates the config before run — checks types, allowed values, paths |
| `javascript/unfollow_companies.js` | Standalone JS snippet to bulk-unfollow companies on LinkedIn (manual use in browser console) |
| `ai/` | AI provider connectors (see below) |
| `images/` | Screenshots and UI assets |
| `resumes/` | (Internal resume temp storage) |
| `__deprecated__/` | Old/unused code kept for reference |

#### `modules/ai/` — AI Provider Connectors

| File | Provider | What it does |
|---|---|---|
| `openaiConnections.py` | OpenAI / any OpenAI-compatible API (Ollama, NVIDIA, LM Studio) | `ai_create_openai_client`, `ai_extract_skills` (extracts tech_stack, required_skills etc from JD), `ai_answer_question` (answers individual form fields) |
| `deepseekConnections.py` | DeepSeek API | Same interface — `deepseek_create_client`, `deepseek_extract_skills`, `deepseek_answer_question` |
| `geminiConnections.py` | Google Gemini API | Same interface — `gemini_create_client`, `gemini_extract_skills`, `gemini_answer_question` |
| `prompts.py` | Shared — `extract_skills_prompt` (5-category JSON schema), `ai_answer_prompt` (form-filling prompt with user context), `deepseek_extract_skills_prompt` (optimized variant) |

---

### `extension/` — Chrome Extension (Universal Form Filler)

A **Manifest V3** Chrome extension that works on **any URL** (not just LinkedIn).

```
extension/
├── manifest.json          # MV3 config: permissions, content scripts, popup
├── content.js             # Content script — injected on every page
├── background.js          # Service worker (minimal, routes messages)
├── popup.html             # Extension popup UI (toggle, backend URL input)
├── popup.js               # Popup logic (sends AUTO_APPLY message to content.js)
├── icons/                 # icon48.png, icon128.png
└── backend/
    ├── server.py           # FastAPI server (the AI brain for the extension)
    └── .env.example        # Template for NVIDIA_API_KEY, LLM_MODEL, RESUME_PDF_PATH
```

#### How the Extension Works — Data Flow

```
User clicks "Auto Fill" in popup
    ↓
popup.js → chrome.tabs.sendMessage(AUTO_APPLY, { backendUrl })
    ↓
content.js (injected on page)
    ├─ collectFields()     → scans all input/textarea/select/contenteditable elements
    ├─ getLabel(el)        → extracts label text (aria-label, <label for>, ancestor heading)
    └─ askBackend()        → POST /fill  { fields: [{label, type, options}] }
    ↓
extension/backend/server.py  (FastAPI, run via uvicorn)
    ├─ reads personal/resume_details.txt on startup
    ├─ calls NVIDIA AI (OpenAI-compatible) per field
    └─ returns { answers: [{label, value}] }
    ↓
content.js
    ├─ fillField()         → fills each matched element (handles React/Vue native setter)
    └─ handleFileUpload()  → GET /resume → uploads PDF to <input type="file">
```

**To run the extension backend:**
```bash
uvicorn extension.backend.server:app --reload
# runs at http://localhost:8000
```

---

### `personal/` — User Profile Data

| File | Purpose |
|---|---|
| `resume_details.txt` | Plain-text resume — loaded by the extension backend on startup and sent to AI for every form field answer. Edit this to update your profile for the extension. |

---

### `all excels/` — Application History (CSV)

| File | Purpose |
|---|---|
| `all_applied_applications_history.csv` | Every successfully submitted Easy Apply job: Job ID, Title, Company, HR Name, HR Link, Job Link, External Link, Date Applied |
| `all_failed_applications_history.csv` | Every failed/skipped job with reason, screenshot name, error details |

> These CSVs are read by `app.py` and rendered in a web UI at `http://localhost:5000`.

---

### `all resumes/` — Resume Storage

```
all resumes/
├── default/         # Put your default resume.pdf here → used in Easy Apply upload
└── temp/            # Temp folder for generated resumes (experimental feature)
```

---

### `logs/` — Runtime Logs

| Item | Purpose |
|---|---|
| `log.txt` | Full runtime log of every action, print_lg output. Grows per run. |
| `screenshots/` | Auto-captured screenshots when applications fail or encounter errors |

---

### `setup/` — Installation Scripts

| File | OS | What it does |
|---|---|---|
| `setup.sh` | Linux/macOS | Creates venv, installs pip deps |
| `windows-setup.bat` | Windows (CMD) | Same, batch version |
| `windows-setup.ps1` | Windows (PowerShell) | Same, PowerShell version |

---

### `templates/` — Flask HTML Templates

| File | Purpose |
|---|---|
| `index.html` | Web dashboard served by `app.py` at `/` — displays applied jobs history, supports edit of "Date Applied" |

---

### `.github/` — GitHub Actions / Issue Templates

Contains CI configs and issue/PR templates for the open-source repo.

---

## 🔄 LinkedIn Bot — Full Execution Flow (`runAiBot.py`)

```
1. Load all config (config/*)
2. Open Chrome via modules/open_chrome.py
3. Navigate to LinkedIn, login (username/password or manual)
4. For each search_term in search_terms:
   a. Build LinkedIn jobs search URL
   b. Apply filters (date, salary, easy_apply_only, experience level, etc.)
   c. Paginate through job listings
   d. For each job card:
      ├─ Extract job_id, title, company, work_location
      ├─ Skip if: already applied | blacklisted company | bad_words in JD | experience > current_experience
      ├─ Check about_company_bad_words
      ├─ Click "Easy Apply" button
      ├─ answer_questions() loop across all form pages:
      │   ├─ Upload resume PDF
      │   ├─ Match each field (select / radio / text / textarea / checkbox)
      │   ├─ Use hardcoded answers from config/questions.py first
      │   └─ Fall back to AI (openai/deepseek/gemini) if no rule matches
      ├─ pause_before_submit → optional human review dialog
      ├─ Submit application
      └─ Write result to all_applied or all_failed CSV
   e. After switch_number applications, move to next search term
5. Optionally run_non_stop or exit
```

---

## 🔑 Key Design Decisions

| Decision | Rationale |
|---|---|
| Config as Python files | Easy for non-developers to edit; no YAML/JSON parsing |
| AI is optional (`use_AI=False`) | Rule-based fallbacks handle 80% of common questions without API calls |
| Stealth mode | `undetected_chromedriver` bypasses LinkedIn anti-bot detection |
| Extension uses its own backend | Completely decoupled from the Selenium bot; works on any job site |
| Resume as plain text | `personal/resume_details.txt` is LLM-friendly; avoids PDF parsing |
| CSV over database | Portable, zero-dependency history tracking |

---

## 🚀 Quick Start (Minimal)

```bash
# 1. Install dependencies
pip install -r requirements.txt   # or run setup/windows-setup.ps1

# 2. Configure
# Edit config/secrets.py  → add LinkedIn credentials + AI API key
# Edit config/search.py   → set search_terms, search_location
# Edit config/questions.py → set your salary, experience, cover letter
# Edit config/personals.py → set name, phone, city

# 3. Add resume
# Place resume PDF at: all resumes/default/resume.pdf

# 4. Run the bot
python runAiBot.py

# 5. (Optional) View history
python app.py        # → http://localhost:5000

# 6. (Optional) Extension backend
uvicorn extension.backend.server:app --reload
# Then load extension/ folder in Chrome → chrome://extensions (Developer Mode)
```

---

## 🗂️ Import Map (Who imports what)

```
runAiBot.py
├── config/personals.py, questions.py, search.py, secrets.py, settings.py
├── modules/open_chrome.py   (→ config/settings.py, config/questions.py)
├── modules/helpers.py       (→ config/settings.py)
├── modules/clickers_and_finders.py (→ config/settings.py, modules/helpers.py)
├── modules/validator.py
└── modules/ai/
    ├── openaiConnections.py  (→ modules/ai/prompts.py, config/secrets.py)
    ├── deepseekConnections.py
    └── geminiConnections.py

extension/backend/server.py
├── personal/resume_details.txt  (read at startup)
├── .env                          (NVIDIA_API_KEY, LLM_MODEL, RESUME_PDF_PATH)
└── all resumes/<RESUME_PDF_PATH> (served via /resume endpoint)

app.py
└── all excels/all_applied_applications_history.csv
```

---

## ⚙️ Environment Variables (`.env`)

```env
PASSWORD=<linkedin_password>
NVIDIA_API_KEY=<your_nvidia_nim_api_key>
NVIDIA_API_URL=https://integrate.api.nvidia.com/v1
LLM_MODEL=meta/llama-3.1-8b-instruct
RESUME_PDF_PATH=all resumes/default/resume.pdf
```

> `config/secrets.py` reads these via `python-dotenv`.  
> `extension/backend/server.py` also reads the same `.env` from repo root.

---

*Last updated: 2026-04-30 | Conversation: 70d1153a-c892-4421-9638-19f6ad72b579*
