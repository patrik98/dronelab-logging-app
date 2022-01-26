USE cs_db;

CREATE TABLE IF NOT EXISTS positions
(
    id INT NOT NULL AUTO_INCREMENT,
    session_id NVARCHAR(255) NOT NULL,
    crazyflie_id NVARCHAR(255) NOT NULL,
    x FLOAT NOT NULL,
    y FLOAT NOT NULL,
    z FLOAT NOT NULL,
    timestamp INT NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB;