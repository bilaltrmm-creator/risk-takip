from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# YENİ KLASÖR YOLU
BASE_DIR = r"Y:\Risk Takip\Yeni klasör\SİTE"

@app.route('/files/<category>', methods=['GET'])
def list_files(category):
    cat_path = os.path.join(BASE_DIR, category)
    if not os.path.exists(cat_path):
        os.makedirs(cat_path, exist_ok=True)
        return jsonify([])
    
    files_list = []
    for filename in os.listdir(cat_path):
        file_path = os.path.join(cat_path, filename)
        if os.path.isfile(file_path):
            stat = os.stat(file_path)
            files_list.append({
                'name': filename,
                'size': stat.st_size,
                'mtime': os.path.strftime('%d.%m.%Y %H:%M', os.path.localtime(stat.st_mtime))
            })
    return jsonify(files_list)

@app.route('/view/<category>/<filename>', methods=['GET'])
def view_file(category, filename):
    return send_from_directory(os.path.join(BASE_DIR, category), filename)

@app.route('/download/<category>/<filename>', methods=['GET'])
def download_file(category, filename):
    return send_from_directory(os.path.join(BASE_DIR, category), filename, as_attachment=True)

@app.route('/get_table/<table_name>', methods=['GET'])
def get_table(table_name):
    json_path = os.path.join(BASE_DIR, f"{table_name}.json")
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route('/save_table/<table_name>', methods=['POST'])
def save_table(table_name):
    data = request.json
    json_path = os.path.join(BASE_DIR, f"{table_name}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)