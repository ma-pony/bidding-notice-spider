FROM registry.cn-hangzhou.aliyuncs.com/pony-ma/python-playwright

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "main.py"]