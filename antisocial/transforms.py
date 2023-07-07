import markdown

from .models import Post


def render_post_body(post: Post):
    return markdown.markdown(post.body)


def render_post_preview(post: Post):
    # TODO: Extract only the first block-level element
    html_body = markdown.markdown(post.body)
    return {
        "title": post.title,
        "body": html_body,
        "timestamp": post.save_time,
        "tags": post.tags,
        "id": post.id,
    }

