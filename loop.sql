select * from users;
create table userscopy as select * from users; 
delete from userscopy;
select * from userscopy;


DO $$
 DECLARE
     user_id	  userscopy.user_id%TYPE;
	 user_age     userscopy.user_age%TYPE;
	 user_gender       userscopy.user_gender%TYPE;
     user_lang   userscopy.user_lang%TYPE;

 BEGIN
 	 
     FOR counter IN 1..5
         LOOP
            INSERT INTO userscopy
             VALUES (counter + 6, counter * 3 + 20, NULL, 'en');
         END LOOP;
 END;
 $$