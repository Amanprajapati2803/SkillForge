from database.database import db
from models.resources import Resource
from models.skill import Skill


def seed_resources():

    resources = [

        # =========================
        # Python
        # =========================

        {
            "skill": "Python",
            "title": "Python Full Course - Bro Code",
            "resource_type": "youtube",
            "difficulty": "Beginner",
            "url": "https://www.youtube.com/watch?v=XKHEtdqhLK8",
            "description": "Complete Python course for beginners."
        },

        {
            "skill": "Python",
            "title": "CS50's Introduction to Programming with Python",
            "resource_type": "course",
            "difficulty": "Beginner",
            "url": "https://cs50.harvard.edu/python/",
            "description": "Harvard's free Python course."
        },

        {
            "skill": "Python",
            "title": "Official Python Documentation",
            "resource_type": "website",
            "difficulty": "Advanced",
            "url": "https://docs.python.org/3/",
            "description": "Official Python documentation."
        },

        {
            "skill": "Python",
            "title": "Real Python",
            "resource_type": "website",
            "difficulty": "Intermediate",
            "url": "https://realpython.com/",
            "description": "High-quality Python tutorials and articles."
        },

        {
            "skill": "Python",
            "title": "Automate the Boring Stuff with Python",
            "resource_type": "book",
            "difficulty": "Beginner",
            "url": "https://automatetheboringstuff.com/",
            "description": "One of the best beginner Python books."
        },

        # =========================
        # JavaScript
        # =========================

        {
            "skill": "Java script",
            "title": "JavaScript Crash Course - Traversy Media",
            "resource_type": "youtube",
            "difficulty": "Beginner",
            "url": "https://www.youtube.com/watch?v=hdI2bqOjy3c",
            "description": "Complete JavaScript crash course."
        },

        {
            "skill": "Java script",
            "title": "Namaste JavaScript",
            "resource_type": "youtube",
            "difficulty": "Intermediate",
            "url": "https://www.youtube.com/playlist?list=PLlasXeu85E9cQ32gLCvAvr9vNaUccPVNP",
            "description": "Deep dive into JavaScript concepts."
        },

        {
            "skill": "Java script",
            "title": "MDN JavaScript Guide",
            "resource_type": "website",
            "difficulty": "Advanced",
            "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
            "description": "Official JavaScript documentation."
        },

        {
            "skill": "Java script",
            "title": "JavaScript.info",
            "resource_type": "website",
            "difficulty": "Intermediate",
            "url": "https://javascript.info/",
            "description": "Modern JavaScript tutorial."
        },

        {
            "skill": "Java script",
            "title": "Eloquent JavaScript",
            "resource_type": "book",
            "difficulty": "Intermediate",
            "url": "https://eloquentjavascript.net/",
            "description": "Free online JavaScript book."
        },

    ]

    for resource in resources:

        skill = Skill.query.filter_by(
            name=resource["skill"]
        ).first()

        if not skill:
            print(f"⚠ Skill '{resource['skill']}' not found.")
            continue

        exists = Resource.query.filter_by(
            title=resource["title"],
            skill_id=skill.id
        ).first()

        if exists:
            continue

        db.session.add(
            Resource(
                skill_id=skill.id,
                title=resource["title"],
                resource_type=resource["resource_type"],
                difficulty=resource["difficulty"],
                url=resource["url"],
                description=resource["description"]
            )
        )

    db.session.commit()

    print("✅ Resources seeded successfully!")