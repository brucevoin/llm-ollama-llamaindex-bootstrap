from flask import Flask, request
import timeit
from rag.pipeline import build_rag_pipeline
import yaml
import box


app = Flask(__name__)

rag_chain = build_rag_pipeline()


@app.route('/chat', methods=['GET'])
def chat():
    prompt = request.args.get('prompt')

    if prompt is not None:
        print('Retrieving answer...')
        answer = rag_chain.query(prompt)
        answer = str(answer).strip()
        print('answer is: \n' + answer)
        return answer, 200
    else:
        return "error: prompt is None", 400




# 启动开发服务器（调试模式）
if __name__ == '__main__':
    with open('webconfig.yml', 'r', encoding='utf8') as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))
    app.run(port=cfg.SERVER_PORT, debug=True)