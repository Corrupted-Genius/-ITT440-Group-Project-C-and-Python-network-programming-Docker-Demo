# THIS IS THE WEB SECTION
# THIS IS ADDITIONAL FEATURE

# WHAT DOES THIS SECTION DO?
# - Display live leaderboard into a web
# - Refreshes every 5 seconds

# HOW TO ACCESS WEB?
# http://localhost:5000

from flask import Flask, render_template_string
import pymysql
import time

app = Flask(__name__)

# HTML TEMPLATE -----------------------------------------------------------------------------------------------------
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>^W^ Live Leaderboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            text-align: center; 
            background: #f0f8f0; 
            margin: 0; 
            padding: 30px;
        }
        h1 { color: #1b5e20; margin-bottom: 5px; }
        p { color: #555; }
        table { 
            margin: 20px auto; 
            border-collapse: collapse; 
            width: 75%;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            background: white;
        }
        th, td { 
            padding: 16px; 
            border: 1px solid #ddd; 
            font-size: 1.05em;
        }
        th { 
            background: #4CAF50; 
            color: white; 
        }
        tr:nth-child(even) { background: #f9fff9; }
        .points { 
            font-weight: bold; 
            font-size: 1.3em; 
            color: #d32f2f; 
        }
        .rank { font-weight: bold; color: #2e7d32; }
    </style>
</head>
<body>
    <h1>^W^ Live Leaderboard</h1>
    <p>Last refreshed: {{ time }}</p>
    
    <table>
        <tr>
            <th>Rank</th>
            <th>Username</th>
            <th>Points</th>
            <th>Last Update</th>
        </tr>
        {% for row in data %}
        <tr>
            <td class="rank">{{ loop.index }}</td>
            <td>{{ row['username'] }}</td>
            <td class="points">{{ row['points'] }}</td>
            <td>{{ row['datetime_stamp'] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''
# MAIN ROUTE ----------------------------------------------------------------------------------------------------
@app.route('/') # Handle requests to the root URL (http://localhost:5000)

def leaderboard():
    try:
        db = pymysql.connect( # connect to MySQL database
            host="mysql_db", 
            user="root", 
            password="", 
            database="itt440",
            cursorclass=pymysql.cursors.DictCursor # return rows as dictionary
        )
        cursor = db.cursor()
        
# SHOW ONLY LATEST SCORE RECORD ----------------------------------------------------------------------------------
        cursor.execute("""
            SELECT username, points, datetime_stamp 
            FROM leaderboard 
            WHERE id IN (
                SELECT MAX(id) 
                FROM leaderboard 
                GROUP BY username
            )
            ORDER BY points DESC
        """)
        
        data = cursor.fetchall() # fetch all rows as list of dictionary
        db.close() # close database connection

# RENDER HTML TEMPLATE WITH DATA ---------------------------------------------------------------------------------
        return render_template_string(HTML_TEMPLATE, data=data, time=time.strftime("%H:%M:%S"))
    
# SHOW MESSAGES IF DATABASE IS NOT READY -------------------------------------------------------------------------
    except Exception as e:
        return f"<h2>Waiting for data... <br><small>{str(e)}</small></h2>"

# START WEB SERVER -----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)