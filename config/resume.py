
from personals import *
import json

###################################################### RESUME DATA — Extracted from LaTeX Resume ######################################################
# Source: Aman Kumar Srivastava's LaTeX resume (last synced: 2026-04-30)
# This file is the canonical structured reference for the bot and AI form-filler.

# ──────────────────────────────────────────────────────────────
# CONTACT & IDENTITY
# ──────────────────────────────────────────────────────────────
full_name       = "Aman Kumar Srivastava"
email           = "aman.apk01@gmail.com"
phone           = "+91-7739704188"
portfolio       = "https://botzcoder.com"
linkedin_url    = "https://www.linkedin.com/in/iconic-aman"
github_url      = "https://github.com/Iconic-Aman"
location        = "Varanasi, U.P, India"

headline        = "Data Engineer | Pipeline Automation | Cloud Lakehouse Architecture"

# ──────────────────────────────────────────────────────────────
# EDUCATION
# ──────────────────────────────────────────────────────────────
education = [
    {
        "institution": "Indian Institute of Information Technology, Kottayam",
        "degree": "B.Tech, Computer Science & Engineering",
        "gpa": "7.48 / 10.0",
        "duration": "2020 – 2024",
    }
]

# ──────────────────────────────────────────────────────────────
# PROFESSIONAL EXPERIENCE
# ──────────────────────────────────────────────────────────────
experience = [
    {
        "title": "Data Engineer — Data Lake and Workflow Automation",
        "company": "HumanizeIQ.ai",
        "duration": "Nov 2025 – Present",
        "location": "Remote",
        "bullets": [
            "Built a data pipeline that moves data from Cloudflare D1 into Cloudflare R2 storage, and set up Trino with Apache Iceberg so the team can run SQL queries directly on stored data without moving it anywhere.",
            "Created 10+ automation workflows using n8n to handle data syncing, query triggering, and result delivery automatically — saving around 8 hours of manual work every week.",
            "Set up data quality checks and tracking across the entire pipeline from D1 to Metabase, so the team can trust the data they see in dashboards and find issues quickly.",
        ],
    },
    {
        "title": "AI Engineer Intern",
        "company": "HumanizeIQ.ai",
        "duration": "June 2025 – Oct 2025",
        "location": "Remote",
        "bullets": [
            "Architected 5+ Apache Superset dashboards serving 300+ active users, cutting reporting turnaround by 40% and improving load performance by 35% through optimized PostgreSQL schema design and FastAPI backends.",
            "Built and deployed production ML solutions using FastAPI and Scikit-learn, managing the full lifecycle from model training and evaluation to live deployment with scalable backend architectures.",
            "Drove adoption of dashboards across 3 business teams, reducing ad-hoc SQL requests by 60%; mentored 3 junior interns who independently owned reporting tracks.",
        ],
    },
]

# ──────────────────────────────────────────────────────────────
# KEY PROJECTS
# ──────────────────────────────────────────────────────────────
projects = [
    {
        "name": "PDF Summarization — Full-Stack AI Web App",
        "tech": ["FastAPI", "Next.js", "PostgreSQL", "Cloudflare R2", "LoRA", "Mistral-7B"],
        "link": "https://pdf.botzcoder.com",
        "bullets": [
            "Engineered PDF ingestion and per-user storage on Cloudflare R2 with async FastAPI workers handling concurrent summarization jobs and live SSE token streaming to the client.",
            "Built a full-stack application with Next.js frontend, FastAPI backend, and Neon PostgreSQL — deployed on Vercel and Render with Google OAuth and per-user job history.",
            "Applied LoRA-based parameter-efficient fine-tuning on Mistral-7B, cutting trainable parameters by 99% vs full fine-tuning; packaged the adapter as a microservice on Hugging Face Spaces.",
        ],
    },
    {
        "name": "AI Chatbot — Food Delivery Platform",
        "tech": ["Python", "FastAPI", "Dialogflow", "MySQL", "NLP"],
        "link": "https://github.com/Iconic-Aman/ChatBot-for-food-delivery",
        "bullets": [
            "Built a FastAPI and MySQL backend to handle multiple order sessions at once with proper transaction management, ensuring data stays consistent across concurrent requests.",
            "Integrated Dialogflow NLP to understand user intents like order tracking, item lookup, and complaints — making the chatbot work reliably on a food delivery platform.",
        ],
    },
]

# ──────────────────────────────────────────────────────────────
# TECHNICAL SKILLS
# ──────────────────────────────────────────────────────────────
skills = {
    "Data Engineering":       ["Apache Iceberg", "Trino", "Apache Hive", "ELT/ETL Pipelines", "Data Lake Architecture", "Cloudflare D1 & R2", "PostgreSQL", "MySQL", "Pandas", "NumPy"],
    "Workflow & Analytics":   ["n8n", "Apache Superset", "Metabase", "Data Quality Checks", "Self-Serve BI", "KPI Dashboards"],
    "Backend & DevOps":       ["FastAPI", "RESTful APIs", "Docker", "Docker Swarm", "GitHub Actions", "CI/CD Pipelines", "AWS", "GCP", "Cloudflare", "Linux"],
    "ML & AI":                ["PyTorch", "Scikit-learn", "Hugging Face Transformers", "LoRA Fine-Tuning", "Mistral-7B", "Dialogflow NLP", "Prompt Engineering"],
    "Frontend & Other":       ["Next.js", "HTML", "CSS", "Google OAuth", "SSE Streaming", "Vercel", "Render"],
    "Languages":              ["Python", "SQL", "JavaScript"],
}

# ──────────────────────────────────────────────────────────────
# CERTIFICATIONS
# ──────────────────────────────────────────────────────────────
certifications = [
    {"name": "Generative AI with Large Language Models", "issuer": "DeepLearning.AI / Coursera", "year": "2024"},
    {"name": "Prompt Engineering for AI Models",         "issuer": "LetsUpgrade",                "year": "2024"},
]

# ──────────────────────────────────────────────────────────────
# COMPENSATION & AVAILABILITY
# ──────────────────────────────────────────────────────────────
years_of_experience  = "1"
current_ctc_inr      = 300000       # ₹3,00,000
expected_ctc_inr     = 600000       # ₹6,00,000
notice_period_days   = 10

