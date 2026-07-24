# from models.internship import Internship
# from models.internship_skill import InternshipSkill
# from database.database import db


# def seed_internships():

#     if Internship.query.first():
#         print("Internships already exist.")
#         return

#     internships = [

#         {
#             "company": "Google",
#             "title": "Frontend Developer Intern",
#             "description": "Work on modern web interfaces using HTML, CSS and JavaScript.",
#             "location": "Remote",
#             "internship_type": "Remote",
#             "apply_link": "apply_link": "https://careers.google.com/",",
#             "skills": [
#                 "HTML",
#                 "CSS",
#                 "JavaScript",
#                 "React"
#             ]
#         },

#         {
#             "company": "Microsoft",
#             "title": "Backend Developer Intern",
#             "description": "Develop backend APIs using Python and Flask.",
#             "location": "Bangalore",
#             "internship_type": "Hybrid",
#             "apply_link": "apply_link": "https://jobs.careers.microsoft.com/",,
#             "skills": [
#                 "Python",
#                 "Flask",
#                 "SQL",
#                 "Git"
#             ]
#         },

#         {
#             "company": "Amazon",
#             "title": "Full Stack Developer Intern",
#             "description": "Build full stack applications with Flask and JavaScript.",
#             "location": "Hyderabad",
#             "internship_type": "On-site",
#             "apply_link": "apply_link": "https://www.amazon.jobs/",
#             "skills": [
#                 "Python",
#                 "Flask",
#                 "JavaScript",
#                 "HTML",
#                 "CSS",
#                 "SQL"
#             ]
#         },

#         {
#             "company": "TCS",
#             "title": "Software Engineer Intern",
#             "description": "General software development and debugging.",
#             "location": "Mumbai",
#             "internship_type": "Hybrid",
#             "apply_link": "apply_link": "https://www.tcs.com/careers",
#             "skills": [
#                 "Python",
#                 "Java",
#                 "SQL",
#                 "Git"
#             ]
#         }

#     ]

#     for data in internships:

#         internship = Internship(
#             company=data["company"],
#             title=data["title"],
#             description=data["description"],
#             location=data["location"],
#             internship_type=data["internship_type"],
#             apply_link=data["apply_link"]
#         )

#         db.session.add(internship)
#         db.session.flush()      # Gets internship.id before commit

#         for skill in data["skills"]:

#             db.session.add(
#                 InternshipSkill(
#                     internship_id=internship.id,
#                     skill_name=skill
#                 )
#             )

#     db.session.commit()

#     print("Internships seeded successfully.")