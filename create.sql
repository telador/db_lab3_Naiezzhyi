CREATE TABLE langs(
	user_lang CHAR(10) not null PRIMARY KEY,
	lang_name CHAR(20) not null
);

CREATE TABLE users(
	user_id INT not null PRIMARY KEY,
	user_age FLOAT not null,
	user_gender CHAR(10),
	user_lang CHAR(10) not null,
	
	CONSTRAINT FK_lang_user FOREIGN KEY (user_lang) REFERENCES langs(user_lang)
);

CREATE TABLE accounts(
	acc_id INT not null PRIMARY KEY,
	acc_followers INT not null,
	acc_age FLOAT not null,
	user_id INT not null,
	CONSTRAINT FK_user_acc FOREIGN KEY (user_id) REFERENCES users(user_id)
);

