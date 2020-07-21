from .models import BlogEntry, Category


def get_blogs_by_category(category):
    # Get all related categories
    categories = []
    blogs = BlogEntry.objects.filter(category=category)

    categories.append(category)
    blogs = get_child_category_blogs(category.children, blogs)

    return blogs


def get_child_category_blogs(children, blogs):
    if len(children.all()) > 0:
        for child in children.all():
            blogs |= BlogEntry.objects.filter(category=child)
            blogs |= get_child_category_blogs(child.children, blogs)

            return blogs
    else:
        return blogs


def remove_restricted_blogs(blogs, user=None):
    return filter(
        lambda blog: (user is not None and blog.private and blog.author == user)
        or not blog.private,
        blogs
    )


def get_all_posts(entries, reblogs):
    pass