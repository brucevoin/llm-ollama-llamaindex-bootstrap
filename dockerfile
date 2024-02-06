FROM python:3.9-slim-buster

# 准备工作目录
WORKDIR /app
RUN mkdir -p /app/data
# 安装依赖项
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制代码
COPY . .

# 运行应用程序
CMD ["python", "webserver.py"]
