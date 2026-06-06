import sqlite3
from datetime import datetime

class HistoryChat:
    def __init__(self, session_id: str, id: int, role: str, chat: str) -> None:
        self.session_id = session_id
        self.chat_id = id
        self.role = role
        self.content = chat
        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

class HistoryChatDatabase:
    def __init__(self, database_path: str) -> None:
        self.conn = sqlite3.connect(database_path)
        self.corsur = self.conn.cursor()

    def create_table(self) -> None:
        self.corsur.execute(
            """
            CREATE TABLE IF NOT EXISTS HistoryChat(
                session_id TEXT,
                chat_id INTEGER,
                role TEXT,
                chat TEXT,
                time TEXT
            );
            """
        )
        self.conn.commit()

    def insert_history(self, history: HistoryChat) -> None:
        self.corsur.execute(
            """
            INSERT INTO HistoryChat VALUES
            (?, ?, ?, ?, ?);
            """,
            (history.session_id, history.chat_id, history.role, history.content, history.time)
        )
        self.conn.commit()

    def get_history(self,session_id: str, limit: int = 5) -> list[tuple] | None:
        self.corsur.execute(
            """
            SELECT * 
            FROM HistoryChat
            WHERE session_id = ?;
            """,
            (session_id,)
        )
        history_chat = self.corsur.fetchall()
        if len(history_chat) <= limit:
            return history_chat
        return history_chat[-limit:]
