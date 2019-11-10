from application.models import User, Post, Tag, Comment


def seed_db(app, db):
    """ Seeds the database with some sample data to play around with. """
    app.app_context()

    # Define some users
    admin = User(
        username="ecotner",
        password="super_secret_pass",
        email="2.71828cotner@gmail.com",
        role="admin",
        ip_address="127.0.0.1",
    )
    db.session.add(admin)

    user = User(
        username="anonymous",
        password="password",
        email="fkn.anime.tiddies@gmail.com",
        role="user",
        ip_address=None,
    )
    db.session.add(user)

    # Make some posts and their associated tags
    tag1 = Tag(tag="physics", color="#232323")
    tag2 = Tag(tag="AI", description="artificial intelligence", color="red")
    tag3 = Tag(tag="humor", description="haha")
    db.session.add_all([tag1, tag2, tag3])

    post1 = Post(
        title="AI is just a bunch of nested `if` statements",
        slug="ai-nested-if-statements",
        author=admin,
        text=(
            "Turns out that AI is just a bunch of nested if statements, who knew? "
            "Data scientists don't want you to find this out!"
        ),
        tags=[tag2, tag3],
    )
    db.session.add(post1)
    post2 = Post(
        title="How to solve P=NP",
        slug="solving-p-np",
        author=user,
        text=(
            "Start with `P=NP`, then cancel `P` on both sides. Now you're left with "
            "`N=1`. That wasn't so hard."
        ),
        visible=True,
        tags=[tag1, tag2],
    )
    db.session.add(post2)
    # post3 = Post(title="Dark matter: liberal conspiracy")
    # post4 = Post(title="One weird trick to win Nobel Prize - laureates are furious")

    db.session.commit()
