"""
 * TicTacToe game
 * Assignment 2
 *
 * Revision History
 * Bishwajit Barua, 2018.09.22: Created
"""

from werkzeug.security import safe_str_cmp
from user import User

#in memory table
users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}

def authenticate (username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id= payload['identity']
    return userid_mapping.get(user_id, None)
