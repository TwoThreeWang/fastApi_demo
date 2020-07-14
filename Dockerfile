#基于的基础镜像
FROM python:3.7-slim-stretch

#代码添加到code文件夹
ADD ./ /code

# 设置code文件夹是工作目录
WORKDIR /code

# 创建宿主机的挂载点
VOLUME /code/data

# 安装支持
RUN pip install --upgrade pip
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD ["python", "./main.py"]
