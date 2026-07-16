from models.resources import Resource
from database.database import db


def create_resource(skill_id, title, resource_type, url, description=None):
    resource = Resource(
        skill_id=skill_id,
        title=title,
        resource_type=resource_type,
        url=url,
        description=description,
    )

    db.session.add(resource)
    db.session.commit()

    return resource


def get_resource(resource_id):
    return Resource.query.get(resource_id)


def get_skill_resources(skill_id):
    return (
        Resource.query
        .filter_by(skill_id=skill_id)
        .order_by(Resource.created_at.desc())
        .all()
    )


def update_resource(resource, title, resource_type, url, description):
    resource.title = title
    resource.resource_type = resource_type
    resource.url = url
    resource.description = description

    db.session.commit()

    return resource


def delete_resource(resource):
    db.session.delete(resource)
    db.session.commit()