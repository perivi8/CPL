from flask import Flask, request, render_template, redirect, url_for
import pyodbc
import os
import sqlite3

app = Flask(__name__)

# Database connection
# def get_db_connection():
#     return pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
#                           "Server=DESKTOP-6KV2EF8;"
#                           "Database=CPL;"
#                           "Trusted_Connection=yes;")

def get_db_connection():
    conn = sqlite3.connect('cpl.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home - Player List
@app.route('/')
def player_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT player_id, name, team_id, no_bid FROM Players")
    players = cursor.fetchall()

    cursor.execute("SELECT team_id, team_name, color, points FROM Teams")
    teams = cursor.fetchall()

    conn.close()
    return render_template('player_list.html', players=players, teams=teams)

# Player Profile
@app.route('/player/<int:player_id>')
def player_profile(player_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT player_id, name, team_id, no_bid FROM Players WHERE player_id=?", (player_id,))
    player = cursor.fetchone()

    cursor.execute("SELECT team_id, team_name, color, points FROM Teams")
    teams = cursor.fetchall()

    conn.close()
    return render_template('player_profile.html', player=player, teams=teams)

# Assign Player to Team
@app.route('/assign_player', methods=['POST'])
def assign_player():
    player_id = int(request.form['player_id'])
    team_color = request.form['team_color']
    bid_points = int(request.form['bid_points'])

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT team_id, points FROM Teams WHERE color=?", (team_color,))
    team = cursor.fetchone()

    if team and team.points >= bid_points:
        new_points = team.points - bid_points
        cursor.execute("UPDATE Teams SET points=? WHERE team_id=?", (new_points, team.team_id))
        cursor.execute("UPDATE Players SET team_id=?, no_bid=0 WHERE player_id=?", (team.team_id, player_id))
        conn.commit()

    conn.close()
    return redirect(url_for('player_list'))

# No Bid Route
@app.route('/no_bid', methods=['POST'])
def no_bid():
    player_id = int(request.form['player_id'])
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Players SET no_bid=1 WHERE player_id=?", (player_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('player_list'))

if __name__ == "__main__":
    app.run(debug=True)
