CREATE USER swim;
CREATE USER test;

CREATE DATABASE testdb WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';
CREATE DATABASE aimdb WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';

GRANT ALL PRIVILEGES ON DATABASE aimdb TO swim;
GRANT ALL PRIVILEGES ON DATABASE testdb TO test;