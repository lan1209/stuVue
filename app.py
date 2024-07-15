from flask import *
from flask_cors import CORS
import os
import subprocess
from flask import send_from_directory
from config_generator import generate_config, save_config
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
CONFIG_FOLDER = 'config'
RESULTS_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(CONFIG_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return redirect(url_for('static', filename='./index.html'))

@app.route('/test/axios')
def msg():
    return '需要传递给前端的数据'


@app.route('/test/msg', methods={'POST'})
def message():
    if request.data:
        res = request.data
        print(res)
        # 这里传过来的是bytes类型数据，所以简单处理了一下，但这里主要说明数据是成功传输了过来
        res1 = res.decode('utf-8')
        print(res1)
        return '获取数据成功'
    else:
        return '没有数据'


@app.route('/test/upload', methods=['POST',"GET"])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        processed_path = os.path.join(PROCESSED_FOLDER, file.filename)
        config_path = os.path.join(CONFIG_FOLDER, f'{os.path.splitext(file.filename)[0]}_config.yaml')
        print("config_path--",config_path)
        # 生成配置文件
        config_data = generate_config(file_path, processed_path)
        save_config(config_data, config_path)
        # 调用 run_net.py
        command = f"python tools/run_net.py --cfg {config_path}"
        print("1")
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("2")
        stdout, stderr = process.communicate()
        print("stderr.decode('utf-8')--",stderr.decode('utf-8'))
        if process.returncode != 0:
            error_message = stderr.decode('utf-8') if stderr else 'Unknown error'
            print(f'Error running command: {error_message}')
            return jsonify({'error': 'Error running detection'}), 500

        # processed_url = f'http://127.0.0.1:5000/test/processed/s2.mp4'
        processed_url = f'/test/processed/{os.path.basename(processed_path)}'
        print("2222",processed_url)
        # 传值到前端
        result = make_response(jsonify({
            'result': {'processed_video_path': processed_url,
                       'code': 0},
        }))
        return result
        # return jsonify({
        #     'processed_video_path': processed_url
        # })


    return jsonify({'error': 'Unknown error occurred'}), 500



@app.route('/test/processed/<filename>',methods=['GET'])
def processed_video(filename):
    return send_from_directory(PROCESSED_FOLDER, filename, mimetype='video/mp4')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
# @app.route('/test/processed/<path:filename>', methods=['GET'])
# def show_video(filename):
#     try:
#         return send_from_directory(PROCESSED_FOLDER, filename, mimetype='video/mp4')
#     except FileNotFoundError:
#         return jsonify({'error': 'File not found'}), 404
