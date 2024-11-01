/*
This section provides the bot with its own database and builds tables that are specific to the bot itself, 
not related to the ones in Telegram. 
Note: Some tables’ code has not been fully completed.
*/
CREATE DATABASE TelegramBotInteractions;
USE TelegramBotInteractions;
CREATE TABLE Users (
    user_id INT PRIMARY KEY,           
    username VARCHAR(255) NOT NULL,   
    interaction_count INT DEFAULT 0,  
    is_banned BIT DEFAULT 0            
);

CREATE TABLE users_interaction (
    user_id BIGINT PRIMARY KEY,
    username NVARCHAR(255) NOT NULL,
    interaction_count INT DEFAULT 0
);
CREATE TABLE groups_interaction (
    group_id BIGINT PRIMARY KEY,
    group_name NVARCHAR(255) NOT NULL,
    interaction_count INT DEFAULT 0
);

CREATE TABLE User_Group_Interactions (
    interaction_id INT IDENTITY PRIMARY KEY,
    user_id INT,                             
    group_id BIGINT,                         
    message_count INT DEFAULT 0,            
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (group_id) REFERENCES Groups(group_id)
);


CREATE TABLE Mutes (
    mute_id INT IDENTITY PRIMARY KEY,   
    user_id INT,                       
    group_id BIGINT NULL,               
    mute_end_time DATETIME,            
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (group_id) REFERENCES Groups(group_id)
);


CREATE TABLE Bans (
    ban_id INT IDENTITY PRIMARY KEY,   
    user_id INT,                       
    group_id BIGINT NULL,               
    ban_reason VARCHAR(255) NULL,       
    ban_start_time DATETIME DEFAULT GETDATE(), 
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (group_id) REFERENCES Groups(group_id)
);


CREATE TABLE Group_Settings (
    setting_id INT IDENTITY PRIMARY KEY,
    group_id BIGINT,                    
    media_restricted BIT DEFAULT 0,     
    FOREIGN KEY (group_id) REFERENCES Groups(group_id)
);


