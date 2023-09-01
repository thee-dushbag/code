CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> f3cc4e3164ef

INSERT INTO alembic_version (version_num) VALUES ('f3cc4e3164ef');

-- Running upgrade f3cc4e3164ef -> b7f12ecee880

CREATE TABLE users (
    uid INTEGER NOT NULL, 
    name VARCHAR(30), 
    email VARCHAR(50), 
    age INTEGER, 
    PRIMARY KEY (uid), 
    UNIQUE (email)
);

CREATE INDEX ix_users_name ON users (name);

UPDATE alembic_version SET version_num='b7f12ecee880' WHERE alembic_version.version_num = 'f3cc4e3164ef';

-- Running upgrade b7f12ecee880 -> 43384e14dfc1

CREATE TABLE products (
    pid INTEGER NOT NULL, 
    name VARCHAR(30), 
    description VARCHAR(255), 
    unit_cost NUMERIC(6, 2), 
    quantity INTEGER, 
    PRIMARY KEY (pid)
);

CREATE INDEX ix_products_name ON products (name);

UPDATE alembic_version SET version_num='43384e14dfc1' WHERE alembic_version.version_num = 'b7f12ecee880';

-- Running upgrade 43384e14dfc1 -> 5688a83419d7

CREATE TABLE orders (
    oid INTEGER NOT NULL, 
    uid INTEGER, 
    pid INTEGER, 
    quantity INTEGER, 
    PRIMARY KEY (oid), 
    FOREIGN KEY(pid) REFERENCES products (pid), 
    FOREIGN KEY(uid) REFERENCES users (uid)
);

UPDATE alembic_version SET version_num='5688a83419d7' WHERE alembic_version.version_num = '43384e14dfc1';

