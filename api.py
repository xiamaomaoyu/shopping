from flask import jsonify, Blueprint, request
import src.search as search
import src.item as item

api = Blueprint('api',__name__)


@api.route('/api/search/all_items',methods=['POST', 'GET'])
def all_items():
    return jsonify(search.all_item())

@api.route('/api/search/all_item_names',methods=['POST', 'GET'])
def all_item_name():
    return jsonify(search.all_item_name())

@api.route('/api/search/keyword/',methods=['POST', 'GET'])
@api.route('/api/search/keyword/<keyword>',methods=['POST', 'GET'])
def items_by_keyword(keyword=None):
    if keyword:
        return jsonify(search.items_by_keyword(keyword))
    else:
        return all_items()

@api.route('/api/item/<id>',methods=['POST', 'GET'])
def item_by_id(id):
    return jsonify(item.get_item_by_id(id).json())

