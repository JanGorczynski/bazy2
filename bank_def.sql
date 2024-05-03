CREATE TABLE client (
    id INT PRIMARY KEY,
    username NVARCHAR(MAX),
    pass NVARCHAR(MAX),
    fname NVARCHAR(MAX),
    lname NVARCHAR(MAX)
);

CREATE TABLE account (
    account_number INT PRIMARY KEY,
    account_name NVARCHAR(MAX),
    balance FLOAT,
    client_id INT,
    FOREIGN KEY (client_id) REFERENCES client(id)
);

CREATE TABLE bank_transfer (
    id INT PRIMARY KEY IDENTITY,
    sender_id INT,
    recipient_id INT,
    timestamp DATETIME,
    FOREIGN KEY (sender_id) REFERENCES account(account_number),
    FOREIGN KEY (recipient_id) REFERENCES account(account_number)
);