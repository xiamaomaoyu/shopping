import src.db_hdl as DB
import src.item as ITEM

def all_item_name():
    sql = "SELECT name FROM item WHERE status = \"online\";"
    result = DB.query_db(sql)
    res_list = DB.dic2List(result)
    return res_list

def all_item():
    forms = DB.query_db("SELECT * FROM item WHERE status = \"online\";")

    res_list = []
    for form in forms:
        res_list.append(ITEM.Item(form).json())
    return res_list


def items_by_keyword(keyword):
    def rate_name(item):
        keyword_list = list(keyword)
        name_list = list(item["name"])
        count = 0
        for character in name_list:
            if character in keyword_list:
                count += 1
            elif character.lower() in keyword_list or character.upper() in keyword_list:
                count += 0.8

        for tag in item["tags"].strip().split(","):
            if tag == keyword:
                count += 10

        rate = (count / len(name_list)) * 100
        return rate


    items = all_item()
    items.sort(key=rate_name,reverse=True)
    return items




#items = items_by_keyword("奶")
