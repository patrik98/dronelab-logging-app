USE cs_db;

CREATE TABLE IF NOT EXISTS positions
(
    id INT PRIMARY KEY,
    session_id NVARCHAR(255) NOT NULL,
    crazyflie_id NVARCHAR(255) NOT NULL,
    x FLOAT NOT NULL,
    y FLOAT NOT NULL,
    z FLOAT NOT NULL,
    timestamp INT NOT NULL
);