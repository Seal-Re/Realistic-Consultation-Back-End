import re
import os
import logging
from pymongo import MongoClient
from .MongoBase import mongo_url, DBbase

client = None

def connect_to_mongodb():
    global client
    try:
        # 连接到MongoDB数据库
        client = MongoClient(mongo_url)
        logging.debug("Connected to MongoDB successfully")
        return client
    except Exception as e:
        logging.error(f"Error connecting to MongoDB: {e}")
        return None

def close_mongodb_connection():
    global client
    if client:
        client.close()
        logging.debug("MongoDB connection closed")

def read_mongo_data(collection):
    try:
        data = list(collection.find({}, {"_id": 0}))  # 不返回_id字段
        logging.debug(f"Read {len(data)} documents from collection {collection.name}")
        return data if data else []
    except Exception as e:
        logging.error(f"Error reading from MongoDB collection {collection.name}: {e}")
        return []
    

voiceMap = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",
    "xiaoyi": "zh-CN-XiaoyiNeural",
    "yunjian": "zh-CN-YunjianNeural",
    "yunxi": "zh-CN-YunxiNeural",
    "yunxia": "zh-CN-YunxiaNeural",
    "yunyang": "zh-CN-YunyangNeural",
    "xiaobei": "zh-CN-liaoning-XiaobeiNeural",
    "xiaoni": "zh-CN-shaanxi-XiaoniNeural",
    "hiugaai": "zh-HK-HiuGaaiNeural",
    "hiumaan": "zh-HK-HiuMaanNeural",
    "wanlung": "zh-HK-WanLungNeural",
    "hsiaochen": "zh-TW-HsiaoChenNeural",
    "hsioayu": "zh-TW-HsiaoYuNeural",
    "yunjhe": "zh-TW-YunJheNeural",
}

def getVoiceById(voiceId):
    return voiceMap.get(voiceId)

def remove_html(string):
    regex = re.compile(r'<[^>]+>')
    cleaned = regex.sub('', string)
    return cleaned

def createAudio(text, file_name, voiceId):
    new_text = remove_html(text)
    print(f"Text without html tags: {new_text}")
    voice = getVoiceById(voiceId)
    if not voice:
        return "error params"

    pwdPath = os.getcwd()
    filePath = pwdPath + "/tts/" + file_name
    relativePath = "/tts/" + file_name
    dirPath = os.path.dirname(filePath)
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    if not os.path.exists(filePath):
        open(filePath, 'a').close()

    try:
        script = [
            'edge-tts',
            '--voice', voice,
            '--text', new_text,
            '--write-media', filePath
        ]
        import subprocess
        subprocess.run(script, check=True)
        url = f'http://127.0.0.1:2020{relativePath}'
        return url
    except subprocess.CalledProcessError as e:
        import logging
        logging.error(f"创建音频失败: {e}")
        return "创建音频失败"
    except Exception as e:
        import logging
        logging.error(f"处理音频时发生其他错误: {e}")
        return "处理音频时发生错误"

def getParameter(request, paramName):
    if request.args.__contains__(paramName):
        return request.args[paramName]
    return ""

connect_to_mongodb()
if client:
    db = client[DBbase]
    ai_history = db["ai_history"]
    table_pool = db["TablePool"]
