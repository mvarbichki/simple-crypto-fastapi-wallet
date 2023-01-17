CREATE TABLE IF NOT EXISTS crypto (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    crypto_name VARCHAR(20) NOT NULL UNIQUE,
    quantity INT NOT NULL,
    privet_key VARCHAR(6) NOT NULL
);

CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    activity VARCHAR(10) NOT NULL,
    crypto_name VARCHAR(20) NOT NULL,
    transferred_quantity INT NOT NULL,
    recipient VARCHAR(20) NOT NULL,
    transferred_at TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE OR REPLACE VIEW all_transactions AS
    SELECT
        recipient,
        activity,
        transferred_quantity,
        crypto_name,
        transferred_at
    FROM
        activities
    ORDER BY transferred_at DESC
    LIMIT 50;
