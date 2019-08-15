CREATE TABLE IF NOT EXISTS "item" (
    id INTEGER PRIMARY KEY,
    name TEXT,
    tags TEXT
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
    order_time TEXT
);

CREATE TABLE IF NOT EXISTS "receiver_detail" (
    id INTEGER PRIMARY KEY,
    phone_number  TEXT references user(phone_number),
    receiver_name TEXT,
    receiver_address TEXT,
    receiver_phone TEXT
);

INSERT INTO user(phone_number,verification_code, password, nick_name) VALUES ("450539776", "123456","123","HaoMengMeng");
INSERT INTO cart_records(phone_number, item, item_price_type, quantity) VALUES ("450539776", 5, "单罐包邮", 4);
INSERT INTO cart_records(phone_number, item, item_price_type, quantity) VALUES ("450539776", 8, "单罐包邮", 4);



INSERT INTO item(name, tags) VALUES ("爱他美铂金一段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("爱他美铂金二段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("爱他美铂金三段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("爱他美铂金四段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("爱他美金装一段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("爱他美金装二段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("爱他美金装三段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("爱他美金装四段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("A2一段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("A2二段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("A2三段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("A2四段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("Karicare可瑞康羊奶一段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("Karicare可瑞康羊奶二段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("Karicare可瑞康羊奶三段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("Munchkin麦满趣草饲一段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("Munchkin麦满趣草饲二段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("Munchkin麦满趣草饲三段", "奶,奶粉,母婴");

INSERT INTO item(name, tags) VALUES ("S26一段新版Alula(配方不变)", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("S26二段新版Alula(配方不变)", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("S26三段新版Alula(配方不变)", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("S26四段新版Alula(配方不变)", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("雀巢能欣NAN有机一段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("雀巢能欣NAN有机二段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("雀巢能欣NAN有机三段", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("雀巢能欣成长奶粉kid‘s essential", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("贝拉米有机一段(新版)", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("贝拉米有机二段(新版)", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("贝拉米有机三段(新版)", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("A2全脂奶粉", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("A2脱脂奶粉", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("A2蜂蜜奶粉 400g", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("A2蜂蜜奶粉礼盒(400g X 2)", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("A2孕妇奶粉", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("蓝胖子脱脂奶粉", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("蓝胖子全脂奶粉", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("雅培小安素香草味(含气柱)", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("雅培小安素巧克力味(含气柱)", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("雅培小安素草莓味(含气柱)", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("雅培糖尿病奶粉(含气柱)", "奶,奶粉,母婴");
INSERT INTO item(name, tags) VALUES ("雅培Ensure全安素营养奶粉(含气柱)", "奶,奶粉,母婴");

INSERT INTO item_price(item,price_type,price) VALUES (1,"单罐",34.50);
INSERT INTO item_price(item,price_type,price) VALUES (1,"单罐包邮",38.70);
INSERT INTO item_price(item,price_type,price) VALUES (1,"三罐包邮",115.50);
INSERT INTO item_price(item,price_type,price) VALUES (1,"六罐包邮",231.00);

INSERT INTO item_price(item,price_type,price) VALUES (2,"单罐",36.50);
INSERT INTO item_price(item,price_type,price) VALUES (2,"单罐包邮",40.70);
INSERT INTO item_price(item,price_type,price) VALUES (2,"三罐包邮",121.50);
INSERT INTO item_price(item,price_type,price) VALUES (2,"六罐包邮",243.00);

INSERT INTO item_price(item,price_type,price) VALUES (3,"单罐",36.50);
INSERT INTO item_price(item,price_type,price) VALUES (3,"单罐包邮",40.70);
INSERT INTO item_price(item,price_type,price) VALUES (3,"三罐包邮",121.50);
INSERT INTO item_price(item,price_type,price) VALUES (3,"六罐包邮",243.00);

INSERT INTO item_price(item,price_type,price) VALUES (4,"单罐",34.50);
INSERT INTO item_price(item,price_type,price) VALUES (4,"单罐包邮",38.70);
INSERT INTO item_price(item,price_type,price) VALUES (4,"三罐包邮",115.50);
INSERT INTO item_price(item,price_type,price) VALUES (4,"六罐包邮",231.00);

INSERT INTO item_price(item,price_type,price) VALUES (5,"单罐",25.50);
INSERT INTO item_price(item,price_type,price) VALUES (5,"单罐包邮",29.70);
INSERT INTO item_price(item,price_type,price) VALUES (5,"三罐包邮",88.50);
INSERT INTO item_price(item,price_type,price) VALUES (5,"六罐包邮",177.00);

INSERT INTO item_price(item,price_type,price) VALUES (6,"单罐",25.50);
INSERT INTO item_price(item,price_type,price) VALUES (6,"单罐包邮",29.70);
INSERT INTO item_price(item,price_type,price) VALUES (6,"三罐包邮",88.50);
INSERT INTO item_price(item,price_type,price) VALUES (6,"六罐包邮",177.00);

INSERT INTO item_price(item,price_type,price) VALUES (7,"单罐",26.50);
INSERT INTO item_price(item,price_type,price) VALUES (7,"单罐包邮",30.70);
INSERT INTO item_price(item,price_type,price) VALUES (7,"三罐包邮",91.50);
INSERT INTO item_price(item,price_type,price) VALUES (7,"六罐包邮",183.00);

INSERT INTO item_price(item,price_type,price) VALUES (8,"单罐",25.50);
INSERT INTO item_price(item,price_type,price) VALUES (8,"单罐包邮",29.70);
INSERT INTO item_price(item,price_type,price) VALUES (8,"三罐包邮",88.50);
INSERT INTO item_price(item,price_type,price) VALUES (8,"六罐包邮",177.00);


INSERT INTO item_price(item,price_type,price) VALUES (9,"单罐",36.50);
INSERT INTO item_price(item,price_type,price) VALUES (9,"单罐包邮",40.70);
INSERT INTO item_price(item,price_type,price) VALUES (9,"三罐包邮",121.50);
INSERT INTO item_price(item,price_type,price) VALUES (9,"六罐包邮",243.00);

INSERT INTO item_price(item,price_type,price) VALUES (10,"单罐",37.00);
INSERT INTO item_price(item,price_type,price) VALUES (10,"单罐包邮",41.20);
INSERT INTO item_price(item,price_type,price) VALUES (10,"三罐包邮",123.00);
INSERT INTO item_price(item,price_type,price) VALUES (10,"六罐包邮",246.00);

INSERT INTO item_price(item,price_type,price) VALUES (11,"单罐",32.00);
INSERT INTO item_price(item,price_type,price) VALUES (11,"单罐包邮",36.70);
INSERT INTO item_price(item,price_type,price) VALUES (11,"三罐包邮",109.50);
INSERT INTO item_price(item,price_type,price) VALUES (11,"六罐包邮",219.00);

INSERT INTO item_price(item,price_type,price) VALUES (12,"单罐",31.00);
INSERT INTO item_price(item,price_type,price) VALUES (12,"单罐包邮",35.20);
INSERT INTO item_price(item,price_type,price) VALUES (12,"三罐包邮",105.00);
INSERT INTO item_price(item,price_type,price) VALUES (12,"六罐包邮",210.00);

INSERT INTO item_price(item,price_type,price) VALUES (13,"单罐",37.50);
INSERT INTO item_price(item,price_type,price) VALUES (13,"单罐包邮",41.70);
INSERT INTO item_price(item,price_type,price) VALUES (13,"三罐包邮",124.50);
INSERT INTO item_price(item,price_type,price) VALUES (13,"六罐包邮",249.00);


INSERT INTO item_price(item,price_type,price) VALUES (14,"单罐",38.50);
INSERT INTO item_price(item,price_type,price) VALUES (14,"单罐包邮",42.70);
INSERT INTO item_price(item,price_type,price) VALUES (14,"三罐包邮",127.50);
INSERT INTO item_price(item,price_type,price) VALUES (14,"六罐包邮",255.00);

INSERT INTO item_price(item,price_type,price) VALUES (15,"单罐",58.00);
INSERT INTO item_price(item,price_type,price) VALUES (15,"单罐包邮",62.20);
INSERT INTO item_price(item,price_type,price) VALUES (15,"三罐包邮",186.00);
INSERT INTO item_price(item,price_type,price) VALUES (15,"六罐包邮",372.00);


INSERT INTO item_price(item,price_type,price) VALUES (16,"单罐",21.50);
INSERT INTO item_price(item,price_type,price) VALUES (16,"单罐包邮",25.70);
INSERT INTO item_price(item,price_type,price) VALUES (16,"三罐包邮",76.50);
INSERT INTO item_price(item,price_type,price) VALUES (16,"六罐包邮",153.00);

INSERT INTO item_price(item,price_type,price) VALUES (17,"单罐",20.50);
INSERT INTO item_price(item,price_type,price) VALUES (17,"单罐包邮",24.70);
INSERT INTO item_price(item,price_type,price) VALUES (17,"三罐包邮",73.50);
INSERT INTO item_price(item,price_type,price) VALUES (17,"六罐包邮",147.00);

INSERT INTO item_price(item,price_type,price) VALUES (18,"单罐",21.50);
INSERT INTO item_price(item,price_type,price) VALUES (18,"单罐包邮",25.70);
INSERT INTO item_price(item,price_type,price) VALUES (18,"三罐包邮",76.50);
INSERT INTO item_price(item,price_type,price) VALUES (18,"六罐包邮",153.00);

INSERT INTO item_price(item,price_type,price) VALUES (19,"单罐",20.50);
INSERT INTO item_price(item,price_type,price) VALUES (19,"单罐包邮",24.70);
INSERT INTO item_price(item,price_type,price) VALUES (19,"三罐包邮",73.50);
INSERT INTO item_price(item,price_type,price) VALUES (19,"六罐包邮",147.00);

INSERT INTO item_price(item,price_type,price) VALUES (20,"单罐",20.50);
INSERT INTO item_price(item,price_type,price) VALUES (20,"单罐包邮",24.70);
INSERT INTO item_price(item,price_type,price) VALUES (20,"三罐包邮",73.50);
INSERT INTO item_price(item,price_type,price) VALUES (20,"六罐包邮",147.00);

INSERT INTO item_price(item,price_type,price) VALUES (21,"单罐",14.50);
INSERT INTO item_price(item,price_type,price) VALUES (21,"单罐包邮",18.70);
INSERT INTO item_price(item,price_type,price) VALUES (21,"三罐包邮",55.50);
INSERT INTO item_price(item,price_type,price) VALUES (21,"六罐包邮",111.00);

INSERT INTO item_price(item,price_type,price) VALUES (22,"单罐",14.50);
INSERT INTO item_price(item,price_type,price) VALUES (22,"单罐包邮",18.70);
INSERT INTO item_price(item,price_type,price) VALUES (22,"三罐包邮",55.50);
INSERT INTO item_price(item,price_type,price) VALUES (22,"六罐包邮",111.00);


INSERT INTO item_price(item,price_type,price) VALUES (23,"单罐",25.50);
INSERT INTO item_price(item,price_type,price) VALUES (23,"单罐包邮",29.70);
INSERT INTO item_price(item,price_type,price) VALUES (23,"三罐包邮",88.50);
INSERT INTO item_price(item,price_type,price) VALUES (23,"六罐包邮",177.00);

INSERT INTO item_price(item,price_type,price) VALUES (24,"单罐",25.50);
INSERT INTO item_price(item,price_type,price) VALUES (24,"单罐包邮",29.70);
INSERT INTO item_price(item,price_type,price) VALUES (24,"三罐包邮",88.50);
INSERT INTO item_price(item,price_type,price) VALUES (24,"六罐包邮",177.00);

INSERT INTO item_price(item,price_type,price) VALUES (25,"单罐",22.50);
INSERT INTO item_price(item,price_type,price) VALUES (25,"单罐包邮",26.70);
INSERT INTO item_price(item,price_type,price) VALUES (25,"三罐包邮",79.50);
INSERT INTO item_price(item,price_type,price) VALUES (25,"六罐包邮",259.00);

INSERT INTO item_price(item,price_type,price) VALUES (26,"单罐",26.50);
INSERT INTO item_price(item,price_type,price) VALUES (26,"单罐包邮",30.70);
INSERT INTO item_price(item,price_type,price) VALUES (26,"三罐包邮",91.50);
INSERT INTO item_price(item,price_type,price) VALUES (26,"六罐包邮",183.00);

INSERT INTO item_price(item,price_type,price) VALUES (27,"单罐",30.30);
INSERT INTO item_price(item,price_type,price) VALUES (27,"单罐包邮",34.50);
INSERT INTO item_price(item,price_type,price) VALUES (27,"三罐包邮",102.90);
INSERT INTO item_price(item,price_type,price) VALUES (27,"六罐包邮",205.80);

INSERT INTO item_price(item,price_type,price) VALUES (28,"单罐",30.30);
INSERT INTO item_price(item,price_type,price) VALUES (28,"单罐包邮",34.50);
INSERT INTO item_price(item,price_type,price) VALUES (28,"三罐包邮",102.90);
INSERT INTO item_price(item,price_type,price) VALUES (28,"六罐包邮",205.80);

INSERT INTO item_price(item,price_type,price) VALUES (29,"单罐",30.50);
INSERT INTO item_price(item,price_type,price) VALUES (29,"单罐包邮",34.70);
INSERT INTO item_price(item,price_type,price) VALUES (29,"三罐包邮",103.50);
INSERT INTO item_price(item,price_type,price) VALUES (29,"六罐包邮",207.00);


INSERT INTO item_price(item,price_type,price) VALUES (30,"单罐",12.00);
INSERT INTO item_price(item,price_type,price) VALUES (30,"单罐包邮",16.20);
INSERT INTO item_price(item,price_type,price) VALUES (30,"三罐包邮",48.00);
INSERT INTO item_price(item,price_type,price) VALUES (30,"六罐包邮",96.00);

INSERT INTO item_price(item,price_type,price) VALUES (31,"单罐",11.50);
INSERT INTO item_price(item,price_type,price) VALUES (31,"单罐包邮",15.70);
INSERT INTO item_price(item,price_type,price) VALUES (31,"三罐包邮",46.50);
INSERT INTO item_price(item,price_type,price) VALUES (31,"六罐包邮",93.00);

INSERT INTO item_price(item,price_type,price) VALUES (32,"单罐",15.00);
INSERT INTO item_price(item,price_type,price) VALUES (32,"单罐包邮",19.20);
INSERT INTO item_price(item,price_type,price) VALUES (32,"三罐包邮",57.00);
INSERT INTO item_price(item,price_type,price) VALUES (32,"六罐包邮",114.00);


INSERT INTO item_price(item,price_type,price) VALUES (33,"礼盒",35.00);



INSERT INTO item_price(item,price_type,price) VALUES (34,"单罐",8.00);
INSERT INTO item_price(item,price_type,price) VALUES (34,"单罐包邮",12.20);
INSERT INTO item_price(item,price_type,price) VALUES (34,"三罐包邮",36.00);
INSERT INTO item_price(item,price_type,price) VALUES (34,"六罐包邮",72.00);

INSERT INTO item_price(item,price_type,price) VALUES (35,"单罐",15.50);
INSERT INTO item_price(item,price_type,price) VALUES (35,"单罐包邮",20.40);
INSERT INTO item_price(item,price_type,price) VALUES (35,"三罐包邮",58.50);
INSERT INTO item_price(item,price_type,price) VALUES (35,"六罐包邮",117.00);

INSERT INTO item_price(item,price_type,price) VALUES (36,"单罐",15.50);
INSERT INTO item_price(item,price_type,price) VALUES (36,"单罐包邮",20.40);
INSERT INTO item_price(item,price_type,price) VALUES (36,"三罐包邮",58.50);
INSERT INTO item_price(item,price_type,price) VALUES (36,"六罐包邮",117.00);

INSERT INTO item_price(item,price_type,price) VALUES (37,"单罐",39.50);
INSERT INTO item_price(item,price_type,price) VALUES (37,"单罐包邮",43.70);
INSERT INTO item_price(item,price_type,price) VALUES (37,"三罐包邮",130.50);
INSERT INTO item_price(item,price_type,price) VALUES (37,"六罐包邮",261.00);

INSERT INTO item_price(item,price_type,price) VALUES (38,"单罐",39.50);
INSERT INTO item_price(item,price_type,price) VALUES (38,"单罐包邮",43.70);
INSERT INTO item_price(item,price_type,price) VALUES (38,"三罐包邮",130.50);
INSERT INTO item_price(item,price_type,price) VALUES (38,"六罐包邮",261.00);

INSERT INTO item_price(item,price_type,price) VALUES (39,"单罐",39.50);
INSERT INTO item_price(item,price_type,price) VALUES (39,"单罐包邮",43.70);
INSERT INTO item_price(item,price_type,price) VALUES (39,"三罐包邮",130.50);
INSERT INTO item_price(item,price_type,price) VALUES (39,"六罐包邮",261.00);

INSERT INTO item_price(item,price_type,price) VALUES (40,"单罐",35.50);
INSERT INTO item_price(item,price_type,price) VALUES (40,"单罐包邮",39.70);
INSERT INTO item_price(item,price_type,price) VALUES (40,"三罐包邮",118.50);
INSERT INTO item_price(item,price_type,price) VALUES (40,"六罐包邮",237.00);

INSERT INTO item_price(item,price_type,price) VALUES (41,"单罐",34.50);
INSERT INTO item_price(item,price_type,price) VALUES (41,"单罐包邮",38.70);
INSERT INTO item_price(item,price_type,price) VALUES (41,"三罐包邮",115.50);
INSERT INTO item_price(item,price_type,price) VALUES (41,"六罐包邮",231.00);
