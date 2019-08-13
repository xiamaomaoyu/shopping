import src.db_hdl as DB


class ReceiverDetail(object):

    def __init__(self,form):
        self.phone_number = form["phone_number"]
        self.receiver_name = form["receiver_name"]
        self.receiver_address = form["receiver_address"]
        self.receiver_phone = form["receiver_phone"]


    def json(self):
        return self.__dict__


def get_receiver_details(phone_number):
    return DB.query_db("select * from receiver_detail where phone_number=?;",(phone_number,))

def add_receiver_details(phone_number, receiver_name, receiver_address, receiver_phone):
    DB.query_db("INSERT INTO receiver_detail(phone_number,receiver_name, receiver_address, receiver_phone) VALUES (?, ?,?,?);",(phone_number,receiver_name, receiver_address, receiver_phone))
    max_id = DB.query_db("select max(id) from receiver_detail where phone_number=?;",(phone_number,))[0]['max(id)']
    set_as_receiver(phone_number, max_id)

def set_as_receiver(phone_number, id):
    DB.query_db(
        "UPDATE user set receiver_detail=? where phone_number=? ;",
        (id, phone_number))


def delete_detail(detail_id):
    DB.query_db("DELETE from receiver_detail where id=?", (detail_id,))