CREATE TABLE IF NOT EXISTS "item" (
    id INTEGER PRIMARY KEY autoincrement,
    name TEXT,
    tags TEXT,
    weight TEXT,
    product_name TEXT,
    bar TEXT,
    status TEXT
);

CREATE TABLE IF NOT EXISTS "item_price" (
    item  integer REFERENCES item(id),
    price_type TEXT,
    price FLOAT
);

CREATE TABLE IF NOT EXISTS "user" (
    phone_number  TEXT,
    verification_code TEXT,
    password TEXT,
    nick_name TEXT,
    receiver_detail INTEGER references receiver_detail(id)
);

CREATE TABLE IF NOT EXISTS "admin" (
    admin_name  TEXT,
    password TEXT
);



CREATE TABLE IF NOT EXISTS staff (
    username TEXT PRIMARY KEY ,
    password TEXT,
    phone TEXT,
    token TEXT
);


INSERT INTO staff(username, password, phone, token) VALUES ('admin', 'admin', '0449969879', '');

CREATE TABLE IF NOT EXISTS "cart_records" (
    phone_number  TEXT references user(phone_number),
    item  integer REFERENCES item(id),
    item_price_type TEXT,
    quantity integer
);

CREATE TABLE IF NOT EXISTS "orders" (
    order_id INTEGER,
    phone_number  TEXT references user(phone_number),
    item  integer REFERENCES item(id),
    item_price_type TEXT,
    quantity integer,
    receiver_name TEXT,
    receiver_address TEXT,
    receiver_phone TEXT,
    order_time TEXT,
    status TEXT,
    order_no TEXT,
    delivery_no TEXT
);

CREATE TABLE IF NOT EXISTS "feedbacks" (
    order_id INTEGER,
    comment TEXT,
    rating INTEGER
);

CREATE TABLE IF NOT EXISTS "receiver_detail" (
    id INTEGER PRIMARY KEY,
    phone_number  TEXT references user(phone_number),
    receiver_name TEXT,
    receiver_address TEXT,
    receiver_phone TEXT
);

CREATE TABLE IF NOT EXISTS "system_log" (
    id INTEGER PRIMARY KEY autoincrement,
    username  TEXT,
    action TEXT,
    detail TEXT,
    datetime TEXT
);


INSERT INTO user(phone_number,verification_code, password, nick_name) VALUES ('450539776', '123456','123','HaoMengMeng');

INSERT INTO item(name, tags, weight, product_name, bar, status) VALUES ('爱他美铂金一段', '奶,奶粉,母婴', '900g', '爱他美', '123', 'online');
INSERT INTO item_price(item,price_type,price) VALUES (1,'单罐',34.50);
INSERT INTO item_price(item,price_type,price) VALUES (1,'单罐包邮',38.70);
INSERT INTO item_price(item,price_type,price) VALUES (1,'三罐包邮',115.50);
INSERT INTO item_price(item,price_type,price) VALUES (1,'六罐包邮',231.00);