from flask import Blueprint, request, jsonify
from .utils import table_pool

table_list = Blueprint('table_list', __name__)

@table_list.route('/api/table_list', methods=['GET'])
def get_data_by_number():
    number = request.args.get('number')
    if not number:
        return jsonify({"error": "缺少参数 number"}), 400

    # 查询符合条件的所有数据
    results = list(table_pool.find({"number": number}, {"_id": 0}))  # 去掉 _id 字段

    if not results:
        return jsonify({"message": "未找到对应的数据"}), 404

    return jsonify(results), 200