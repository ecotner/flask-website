def seed_db(app, db):
    with app.app_context():
        from application.models import User, Post, Tag, Comment

        """ Seeds the database with some sample data to play around with. """
        # app.app_context()
        # Drop and recreate tables
        db.drop_all()
        db.create_all()

        # Define some users
        admin = User(
            username="admin",
            password="super_secret_pass",
            email="hey.it.me@gmail.com",
            role="admin",
            ip_address="127.0.0.1",
        )
        user = User(
            username="anonymous",
            password="password",
            email="fkn.anime.tiddies@gmail.com",
            role="user",
            ip_address=None,
        )
        heckler = User(
            username="some_idiot",
            password="1234",
            email="xxx.cod-fan.420.xxx@aol.com",
            role="user",
        )
        db.session.add_all([admin, user, heckler])

        # Make some category tags
        physics = Tag(tag="physics", color="#00bcc9")
        ai = Tag(tag="AI", description="artificial intelligence", color="red")
        humor = Tag(tag="humor", color="#9dc900", description="haha")
        math = Tag(tag="math", color="#00bf29")
        cs = Tag(tag="comp_sci", color="#000dbf")
        serious = Tag(tag="serious", color="#bf7900")
        politics = Tag(tag="politics", color="#a300a3")
        db.session.add_all([physics, ai, humor, math, cs, serious, politics])

        # Make some posts and comments
        post1 = Post(
            title="AI is just a bunch of nested `if` statements",
            slug="ai-nested-if-statements",
            author=admin,
            text=(
                "Turns out that AI is just a bunch of nested if statements, who knew? "
                "Data scientists don't want you to find this out!"
            ),
            tags=[ai, humor],
        )
        post1_comments = [
            Comment(
                post=post1,
                author=heckler,
                text="This is a bunch of bullshit. AI is actually just a bunch of XOR gates!",
            ),
            Comment(
                post=post1,
                author=admin,
                text=(
                    "I'm sorry, my good fellow, but you have no idea what you're talking "
                    "about. I have a Phd, I'll have you know."
                ),
            ),
            Comment(post=post1, author=heckler, text="whatever, idiot."),
        ]
        db.session.add_all([post1] + post1_comments)

        post2 = Post(
            title="How to solve P=NP",
            slug="solving-p-np",
            author=user,
            text=(
                "Start with `P=NP`, then cancel `P` on both sides. Now you're left with "
                "`N=1`. That wasn't so hard."
            ),
            visible=True,
            tags=[cs, math],
        )
        post2_comments = [
            Comment(
                post=post2,
                author=heckler,
                text="This is patently wrong and you should feel bad.",
            ),
            Comment(
                post=post2,
                author=user,
                text="I'm sorry, I'm kind of new at algebra. I'm only in 3rd grade.",
            ),
            Comment(
                post=post2,
                author=heckler,
                text="are you fucking serious? get out of here kiddo",
            ),
            Comment(
                post=post2,
                author=admin,
                text="I'm sorry, that kind of language will not be tolerated!",
            ),
        ]
        db.session.add_all([post2] + post2_comments)

        post3 = Post(
            title="Dark matter: liberal conspiracy",
            author=heckler,
            slug="dm-liberal-consp",
            tags=[physics, serious, politics],
            text=(
                "Dark matter is supposedly this stuff that is everywhere, but you can't "
                "see it for some reason. Scientists are obviously just making this up. "
                "Just like the liberals are making up climate change - I believe the two "
                "are intimately linked, and the Deep State is spreading propaganda to try "
                "and turn us all into soy bois."
            ),
        )
        post3_comments = [
            Comment(
                post=post3, author=heckler, text="I dare anyone to challenge me on this"
            ),
            Comment(post=post3, author=user, text="Dude, you need help..."),
            Comment(
                post=post3,
                author=heckler,
                text="I'll fight you bro - give me a time and place",
            ),
        ]
        db.session.add_all([post3] + post3_comments)

        db.session.commit()
