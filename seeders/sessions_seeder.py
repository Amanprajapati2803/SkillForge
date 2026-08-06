from database.database import db
from models.session import Session
from datetime import datetime, timedelta


def seed_sessions():

    now = datetime.now()

    sessions = [

        # ==========================
        # LIVE SESSIONS
        # ==========================

        {
            "title": "Python Fundamentals Workshop",
            "description": "Master Python basics through interactive live coding.",
            "category": "Workshop",
            "host": "SkillForge Team",
            "start_datetime": now - timedelta(minutes=20),
            "end_datetime": now + timedelta(minutes=40),
            "meeting_link": "https://meet.google.com/python-live",
            "recording_link": None,
            "thumbnail": "python_workshop.jpg"
        },

        {
            "title": "Git & GitHub Live Bootcamp",
            "description": "Learn branching, commits and collaboration in GitHub.",
            "category": "Workshop",
            "host": "Aarav Sharma",
            "start_datetime": now - timedelta(minutes=10),
            "end_datetime": now + timedelta(minutes=80),
            "meeting_link": "https://meet.google.com/git-live",
            "recording_link": None,
            "thumbnail": "git_bootcamp.jpg"
        },

        # ==========================
        # UPCOMING
        # ==========================

        {
            "title": "Flask API Masterclass",
            "description": "Build REST APIs using Flask and SQLAlchemy.",
            "category": "Workshop",
            "host": "SkillForge Team",
            "start_datetime": now + timedelta(days=1),
            "end_datetime": now + timedelta(days=1, hours=2),
            "meeting_link": "https://meet.google.com/flask-api",
            "recording_link": None,
            "thumbnail": "flask.jpg"
        },

        {
            "title": "Introduction to Artificial Intelligence",
            "description": "Explore the fundamentals of AI and machine learning.",
            "category": "Webinar",
            "host": "Dr. Meera Joshi",
            "start_datetime": now + timedelta(days=2),
            "end_datetime": now + timedelta(days=2, hours=2),
            "meeting_link": "https://meet.google.com/ai-session",
            "recording_link": None,
            "thumbnail": "ai.jpg"
        },

        {
            "title": "Docker Essentials",
            "description": "Containerize your applications with Docker.",
            "category": "Workshop",
            "host": "Rahul Verma",
            "start_datetime": now + timedelta(days=3),
            "end_datetime": now + timedelta(days=3, hours=2),
            "meeting_link": "https://meet.google.com/docker",
            "recording_link": None,
            "thumbnail": "docker.jpg"
        },

        {
            "title": "Career Guidance & Resume Review",
            "description": "Improve your resume and prepare for internships.",
            "category": "Career Session",
            "host": "SkillForge Mentors",
            "start_datetime": now + timedelta(days=5),
            "end_datetime": now + timedelta(days=5, hours=2),
            "meeting_link": "https://meet.google.com/resume",
            "recording_link": None,
            "thumbnail": "resume.jpg"
        },

        {
            "title": "Java Interview Preparation",
            "description": "Practice Java interview questions and coding problems.",
            "category": "Interview Prep",
            "host": "Ananya Patel",
            "start_datetime": now + timedelta(days=7),
            "end_datetime": now + timedelta(days=7, hours=2),
            "meeting_link": "https://meet.google.com/java",
            "recording_link": None,
            "thumbnail": "java.jpg"
        },

        # ==========================
        # RECORDED
        # ==========================

        {
            "title": "Python Object-Oriented Programming",
            "description": "Understand classes, objects and inheritance.",
            "category": "Workshop",
            "host": "SkillForge Team",
            "start_datetime": now - timedelta(days=7),
            "end_datetime": now - timedelta(days=7, hours=-2),
            "meeting_link": None,
            "recording_link": "https://www.youtube.com/watch?v=Ej_02ICOIgs",
            "thumbnail": "oop.jpg"
        },

        {
            "title": "SQL Joins Explained",
            "description": "Master INNER, LEFT, RIGHT and FULL joins.",
            "category": "Workshop",
            "host": "Neha Kapoor",
            "start_datetime": now - timedelta(days=10),
            "end_datetime": now - timedelta(days=10, hours=-2),
            "meeting_link": None,
            "recording_link": "https://www.youtube.com/watch?v=9yeOJ0ZMUYw",
            "thumbnail": "sql.jpg"
        },

        {
            "title": "Git Crash Course",
            "description": "Everything you need to start using Git efficiently.",
            "category": "Workshop",
            "host": "SkillForge Team",
            "start_datetime": now - timedelta(days=14),
            "end_datetime": now - timedelta(days=14, hours=-2),
            "meeting_link": None,
            "recording_link": "https://www.youtube.com/watch?v=RGOj5yH7evk",
            "thumbnail": "git.jpg"
        }

    ]

    for session in sessions:

        exists = Session.query.filter_by(
            title=session["title"]
        ).first()

        if exists:
            continue

        db.session.add(
            Session(
                title=session["title"],
                description=session["description"],
                category=session["category"],
                host=session["host"],
                start_datetime=session["start_datetime"],
                end_datetime=session["end_datetime"],
                meeting_link=session["meeting_link"],
                recording_link=session["recording_link"],
                thumbnail=session["thumbnail"]
            )
        )

    db.session.commit()

    #print("✅ Sessions seeded successfully!")