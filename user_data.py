import sqlite3

def add_game_alert(user_id, target_user_id, game_name):
    conn = sqlite3.connect('database/atom.db')
    c = conn.cursor()

    c.execute('''
        SELECT 1 FROM alerts WHERE user_id = ? AND target_user_id = ? AND game_name = ?
    ''', (user_id, target_user_id, game_name))
    
    if not c.fetchone():
        c.execute('''
            INSERT INTO alerts (user_id, target_user_id, game_name)
            VALUES (?, ?, ?)
        ''', (user_id, target_user_id, game_name))
        conn.commit()

    conn.close()

def remove_game_alert(user_id, target_user_id, game_name):
    conn = sqlite3.connect('database/atom.db')
    c = conn.cursor()
    c.execute('''
        DELETE FROM alerts
        WHERE user_id = ? AND target_user_id = ? AND game_name = ?
    ''', (user_id, target_user_id, game_name))
    conn.commit()
    conn.close()


def get_game_alerts_for_user(user_id):
    """Get all game alerts for a specific user."""
    conn = sqlite3.connect('database/atom.db')
    c = conn.cursor()

    c.execute('''
        SELECT target_user_id, game_name FROM alerts WHERE user_id = ?
    ''', (user_id,))
    alerts = c.fetchall()

    conn.close()
    return alerts
