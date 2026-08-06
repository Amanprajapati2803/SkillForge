#from models.internship import Internship
#from models.internship_skill import InternshipSkill
#from database.database import db


#def seed_internships():
 #   if Internship.query.first():
  #      print("Internships already exist.")
   #     return

    #internships = [
     #   {
      #      "company": "Google",
       #     "title": "Frontend Developer Intern",
        #    "description": "Work on modern web interfaces using HTML, CSS and JavaScript. Build reusable components and optimize performance for millions of users.",
         #   "location": "Remote",
#            "internship_type": "Remote",
 #           "apply_link": "https://careers.google.com/",
  #          "skills": ["HTML", "CSS", "JavaScript", "React"]
   #     },
    #    {
     #       "company": "Microsoft",
      #      "title": "Backend Developer Intern",
       #     "description": "Develop backend APIs using Python and Flask. Work on scalable microservices and cloud infrastructure.",
#            "location": "Bangalore",
 #           "internship_type": "Hybrid",
  #          "apply_link": "https://jobs.careers.microsoft.com/",
   #         "skills": ["Python", "Flask", "SQL", "Git"]
    #    },
     #   {
      #      "company": "Amazon",
       #     "title": "Full Stack Developer Intern",
        #    "description": "Build full stack applications with Flask and JavaScript. Own features end-to-end from database to UI.",
         #   "location": "Hyderabad",
          #  "internship_type": "On-site",
           # "apply_link": "https://www.amazon.jobs/",
            #"skills": ["Python", "Flask", "JavaScript", "HTML", "CSS", "SQL"]
#        },
 #       {
  #          "company": "TCS",
   #         "title": "Software Engineer Intern",
    #        "description": "General software development and debugging. Work with enterprise clients on legacy modernization.",
     #       "location": "Mumbai",
      #      "internship_type": "Hybrid",
       #     "apply_link": "https://www.tcs.com/careers",
        #    "skills": ["Python", "Java", "SQL", "Git"]
#        },
 #       {
  #          "company": "Meta",
   #         "title": "React Native Intern",
    #        "description": "Build cross-platform mobile experiences. Optimize rendering performance and animation smoothness.",
     #       "location": "London",
      #      "internship_type": "On-site",
       #     "apply_link": "https://www.metacareers.com/",
        #    "skills": ["JavaScript", "React", "React Native", "CSS"]
#        },
#       {
 #           "company": "Netflix",
  #          "title": "UI Engineering Intern",
   #         "description": "Craft pixel-perfect interfaces for the streaming platform. Focus on accessibility and design systems.",
    #        "location": "Remote",
     #       "internship_type": "Remote",
      #      "apply_link": "https://jobs.netflix.com/",
       #     "skills": ["HTML", "CSS", "JavaScript", "TypeScript"]
#        },
 #       {
  #          "company": "Stripe",
   #         "title": "API Developer Intern",
    #        "description": "Design and implement developer-facing APIs. Write SDKs and documentation for global payments infrastructure.",
     #       "location": "Singapore",
      #      "internship_type": "Hybrid",
       #     "apply_link": "https://stripe.com/jobs",
#            "skills": ["Python", "REST APIs", "SQL", "Git"]
 #       },
  #      {
   #         "company": "OpenAI",
    #        "title": "ML Engineering Intern",
     #       "description": "Train and fine-tune large language models. Build evaluation pipelines and data processing systems.",
      #      "location": "San Francisco",
       #     "internship_type": "On-site",
        #    "apply_link": "https://openai.com/careers",
         #   "skills": ["Python", "PyTorch", "SQL", "Machine Learning"]
#        }
 #   ]
#
 #   for data in internships:
  #         company=data["company"],
   #         title=data["title"],
    #        description=data["description"],
        #       location=data["location"],
 #               internship_type=data["internship_type"],
  #          apply_link=data["apply_link"]
   #     )
    #    db.session.add(internship)
     #   db.session.flush()  # Gets internship.id before commit
#
 #       for skill in data["skills"]:
  #          db.session.add(InternshipSkill(
   #             internship_id=internship.id,
    #            skill_name=skill
     #       ))

#    db.session.commit()
 #   print(f"Seeded {len(internships)} internships successfully.")