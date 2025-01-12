"""
    https://stackoverflow.com/questions/15856976/transactions-with-python-sqlite3
"""
import sqlite3


def execute(): 
    connection = sqlite3.connect('../db.sqlite3')
    connection.isolation_level = None

    cursor = connection.cursor()

    create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) PRIMARY KEY NOT NULL UNIQUE,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL 
        );
    """

    create_user_sessions_table = """
        CREATE TABLE IF NOT EXISTS user_sessions (
            user_id VARCHAR(36) NOT NULL,
            session_id VARCHAR(36) NOT NULL,
            status VARCHAR(36) NOT NULL DEFAULT 'ACTIVE',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """

    create_chats_table = """
        CREATE TABLE IF NOT EXISTS chats (
            id VARCHAR(36) PRIMARY KEY NOT NULL UNIQUE,
            name VARCHAR(255) NOT NULL UNIQUE
        );
    """

    create_private_messages_table = """
        CREATE TABLE IF NOT EXISTS private_messages (
            sender_id VARCHAR(36) NOT NULL,
            receiver_id VARCHAR(36) NOT NULL,
            content TEXT,
            attachment_id VARCHAR(36) DEFAULT '',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(sender_id) REFERENCES user_sessions(session_id),
            FOREIGN KEY(receiver_id) REFERENCES user_sessions(session_id),
            FOREIGN KEY(attachment_id) REFERENCES attachments(id)
        );
    """
  
    create_group_messages_table = """
        CREATE TABLE IF NOT EXISTS group_messages (
            sender_id VARCHAR(36) NOT NULL,
            chat_id VARCHAR(36) NOT NULL,
            receiver_id VARCHAR(36) NOT NULL,
            content TEXT,
            attachment_id VARCHAR(36) DEFAULT '',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(chat_id) REFERENCES chats(id)
            FOREIGN KEY(attachment_id) REFERENCES attachments(id),
            FOREIGN KEY(sender_id) REFERENCES user_sessions(session_id)
            FOREIGN KEY(receiver_id) REFERENCES user_sessions(session_id)
        );
    """

    create_attachments_table = """
        CREATE TABLE IF NOT EXISTS attachments (
            id VARCHAR(36) PRIMARY KEY NOT NULL UNIQUE,
            file_format VARCHAR(255) NOT NULL,
            file_size VARCHAR(255) NOT NULL,
            file_name VARCHAR(255) NOT NULL,
            file_path TEXT NOT NULL
        );
    """

    user_chats_query = """
        CREATE TABLE IF NOT EXISTS chat_users (
            user_session_id VARCHAR(36) NOT NULL,
            chat_id VARCHAR(36) NOT NULL,
            FOREIGN KEY(chat_id) REFERENCES chats(id),
            FOREIGN KEY(user_session_id) REFERENCES user_sessions(session_id)
            UNIQUE(user_session_id, chat_id)
        )
    """

    create_detailed_chats_info_view = """
    """
    
    create_detailed_chats_info_view = """
    """

    cursor.execute("BEGIN")

    try:
        cursor.execute(create_users_table)
        cursor.execute(create_chats_table)
        cursor.execute(create_attachments_table)
        cursor.execute(create_private_messages_table)
        cursor.execute(create_group_messages_table)
        cursor.execute(create_user_sessions_table)
        cursor.execute(user_chats_query)
        cursor.execute("COMMIT")
    except Exception as e:
        cursor.execute("ROLLBACK")
        print(e)
        raise e
    
execute()