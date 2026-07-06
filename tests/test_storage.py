from app.storage import repositories as storage_repositories


def test_init_db_resets_legacy_numeric_id_schema(db_path) -> None:
    with storage_repositories.get_connection() as conn:
        conn.execute("DROP TABLE IF EXISTS transfers")
        conn.execute("DROP TABLE IF EXISTS deposits")
        conn.execute("DROP TABLE IF EXISTS users")
        conn.execute(
            """
            CREATE TABLE users (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                legal_name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                balance REAL NOT NULL DEFAULT 0.0
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE deposits (
                tid INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                user_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(uid)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE transfers (
                tid INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(sender_id) REFERENCES users(uid),
                FOREIGN KEY(receiver_id) REFERENCES users(uid)
            )
            """
        )
        conn.commit()

    storage_repositories.init_db()

    with storage_repositories.get_connection() as conn:
        users_columns = {row[1]: row[2].upper() for row in conn.execute("PRAGMA table_info(users)")}
        deposits_columns = {row[1]: row[2].upper() for row in conn.execute("PRAGMA table_info(deposits)")}
        transfers_columns = {row[1]: row[2].upper() for row in conn.execute("PRAGMA table_info(transfers)")}

    assert users_columns["uid"] == "TEXT"
    assert deposits_columns["user_id"] == "TEXT"
    assert transfers_columns["sender_id"] == "TEXT"
    assert transfers_columns["receiver_id"] == "TEXT"
