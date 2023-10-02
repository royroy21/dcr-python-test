from db import DBO


migrations = [
    """ALTER TABLE country ADD COLUMN topLevelDomain TEXT;""",
    """ALTER TABLE country ADD COLUMN capital TEXT;""",
]


class DatabaseMigrations(DBO):
    def run(self):
        for migration in migrations:
            self.cursor.execute(migration)


if __name__ == "__main__":
    DatabaseMigrations().run()
