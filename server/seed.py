from faker import Faker

try:
    from .app import app
    from .models import Note, User, db
except ImportError:
    from app import app
    from models import Note, User, db


fake = Faker()


def run_seed():
    with app.app_context():
        Note.query.delete()
        User.query.delete()

        demo_users = []
        for username in ("alexdev", "samfocus", "tayplanner"):
            user = User(username=username)
            user.password = "password123"
            demo_users.append(user)

        db.session.add_all(demo_users)
        db.session.commit()

        notes = []
        categories = ["work", "study", "personal", "ideas"]

        for user in demo_users:
            for _ in range(5):
                notes.append(
                    Note(
                        title=fake.sentence(nb_words=4).rstrip("."),
                        content=fake.paragraph(nb_sentences=3),
                        category=fake.random_element(categories),
                        user_id=user.id,
                    )
                )

        db.session.add_all(notes)
        db.session.commit()
        print("Database seeded with demo users and notes.")


if __name__ == "__main__":
    run_seed()
