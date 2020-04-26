import src.db_hdl as DB
import os

class Item():

    def __init__(self,form):
        self.id = form["id"]
        self.name = form["name"]
        self.tags = form["tags"]
        self.weight = form["weight"]
        self.product_name = form["product_name"]
        self.bar = form["bar"]
        self.status = form["status"]
        self.price_list = get_price_list(self.id)
        self.display_price = min_price(self.price_list)
        self.discription_list = get_discription_img_list(self.id)

    def json(self):
        return self.__dict__


def get_discription_img_list(id):
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"static/img/")
    path += str(id) + "/DetailImg/"
    img_list = []
    files = os.scandir(path)
    for file in files:
        if file.name.endswith("jpg") or file.name.endswith("png") or file.name.endswith("jpeg"):
            img_list.append(file.name)
    img_list.sort()
    return img_list


def min_price(price_list):
    return min(DB.dic2ListByCol(price_list,"price"))

def get_price_list(id):
    return DB.query_db("select price_type,price from item_price where item=?;",(id,))


def get_item_by_id(id):
    return Item(DB.query_db("select * from item where id=?;",(id,),one=True))

