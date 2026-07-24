from database.database import db


class InternshipSkill(db.Model):

    __tablename__ = "internship_skills"

    id = db.Column(db.Integer, primary_key=True)

    internship_id = db.Column(
        db.Integer, db.ForeignKey("internships.id"), nullable=False
    )

    skill_name = db.Column(db.String(100), nullable=False)
