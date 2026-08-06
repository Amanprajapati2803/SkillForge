from database.database import db
from models.community_post import CommunityPost
from models.community_like import CommunityLike
from models.community_comment import CommunityComment


def create_post(
    user_id,
    title,
    content,
    category,
    image_url=None,
    attachment_url=None,
):
    """Create a new community post."""

    post = CommunityPost(
        user_id=user_id,
        title=title,
        content=content,
        category=category,
        image_url=image_url,
        attachment_url=attachment_url,
    )

    db.session.add(post)
    db.session.commit()

    return post


def get_all_posts():
    """Return all community posts ordered by newest first."""

    return CommunityPost.query.order_by(CommunityPost.created_at.desc()).all()


# def get_post_by_id(post_id):
#     post = CommunityPost.query.get(post_id)

#     if not post:
#         return None

#     post.views += 1
#     db.session.commit()

#     return post


def get_post_details(post_id, user_id):
    post = CommunityPost.query.get(post_id)


    if not post:
        return None
    
    post.views += 1
    db.session.commit()
    
    like_count = CommunityLike.query.filter_by(post_id=post.id).count()

    comment_count = CommunityComment.query.filter_by(post_id=post.id).count()

    liked = (
        CommunityLike.query.filter_by(post_id=post.id, user_id=user_id).first() is not None
    )

    comments = (
        CommunityComment.query.filter_by(post_id=post.id)
        .order_by(CommunityComment.created_at.asc())
        .all()
    )

    return {
        "post": post,
        "comments": comments,
        "like_count": like_count,
        "comment_count": comment_count,
        "liked": liked,
    }


def toggle_like(post_id, user_id):
    """Like or unlike a community post."""

    like = CommunityLike.query.filter_by(post_id=post_id, user_id=user_id).first()

    if like:
        db.session.delete(like)
        liked = False
    else:
        like = CommunityLike(post_id=post_id, user_id=user_id)
        db.session.add(like)
        liked = True

    db.session.commit()

    like_count = CommunityLike.query.filter_by(post_id=post_id).count()

    return {"liked": liked, "like_count": like_count}


def add_comment(post_id, user_id, content):
    """Add a comment to a community post."""

    comment = CommunityComment(
        post_id=post_id, user_id=user_id, content=content.strip()
    )

    db.session.add(comment)
    db.session.commit()

    return comment


def delete_comment(comment_id, user_id):
    """Delete a user's own comment."""

    comment = CommunityComment.query.get(comment_id)

    if not comment:
        return False

    if comment.user_id != user_id:
        return False

    db.session.delete(comment)
    db.session.commit()

    return True
