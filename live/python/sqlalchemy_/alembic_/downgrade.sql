-- Running downgrade 5688a83419d7 -> 43384e14dfc1

DROP TABLE orders;

UPDATE alembic_version SET version_num='43384e14dfc1' WHERE alembic_version.version_num = '5688a83419d7';

-- Running downgrade 43384e14dfc1 -> b7f12ecee880

DROP INDEX ix_products_name;

DROP TABLE products;

UPDATE alembic_version SET version_num='b7f12ecee880' WHERE alembic_version.version_num = '43384e14dfc1';

-- Running downgrade b7f12ecee880 -> f3cc4e3164ef

DROP INDEX ix_users_name;

DROP TABLE users;

UPDATE alembic_version SET version_num='f3cc4e3164ef' WHERE alembic_version.version_num = 'b7f12ecee880';

-- Running downgrade f3cc4e3164ef -> 

DELETE FROM alembic_version WHERE alembic_version.version_num = 'f3cc4e3164ef';

DROP TABLE alembic_version;

