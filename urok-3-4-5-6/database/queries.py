CATEGORIES_TABLE_SQL = '''
create table if not exists categories(
    id serial primary key,
    title varchar(50) unique not null
);
'''
PRODUCTS_TABLE_SQL = '''
create table if not exists products(
    id serial primary key,
    title varchar(60) not null unique,
    quantity integer not null,
    price numeric(5, 2) not null,
    category_id integer not null references categories(id) on delete cascade
);
'''
# 45.55
USERS_TABLE_SQL = '''
create table if not exists users(
    id serial primary key,
    chat_id bigint unique not null,
    username varchar(50) unique
);
'''

TABLE_EXISTS_SQL = '''
select exists(
    select 1
    from information_schema.tables
    where table_schema = 'public' and
          table_name = %s
);
'''

TABLES_DATA = {
    'categories': CATEGORIES_TABLE_SQL,
    'products': PRODUCTS_TABLE_SQL,
    'users': USERS_TABLE_SQL
}