CREATE TABLE IF NOT EXISTS leaderboard (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    points INT DEFAULT 0,
    datetime_stamp DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

-- Initial data
INSERT INTO leaderboard (username, points)
VALUES ('py_user', 10), ('c_user', 10)
ON DUPLICATE KEY UPDATE points = 10;