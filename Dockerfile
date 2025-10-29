FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# 创建启动脚本
RUN echo '#!/bin/bash\n\
python manage.py migrate --noinput\n\
python create_admin.py\n\
exec gunicorn --bind 0.0.0.0:8000 --workers 4 k8sui.wsgi:application' > /app/start.sh \
    && chmod +x /app/start.sh

CMD ["/app/start.sh"]


# # 使用阿里云 Python 镜像
# FROM registry.cn-hangzhou.aliyuncs.com/library/python:3.11-slim

# WORKDIR /app

# # 使用阿里云 apt 源（加速软件包安装）
# RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
#     apt-get update && apt-get install -y --no-install-recommends \
#     gcc \
#     default-libmysqlclient-dev \
#     pkg-config \
#     && rm -rf /var/lib/apt/lists/*

# # 复制依赖文件
# COPY requirements.txt .

# # 使用阿里云 pip 源（加速 Python 包安装）
# RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ \
#     -r requirements.txt

# # 复制项目文件
# COPY . .

# # 收集静态文件
# RUN python manage.py collectstatic --noinput

# EXPOSE 8000

# # 创建启动脚本（自动执行迁移和创建管理员）
# RUN echo '#!/bin/bash\n\
# set -e\n\
# echo "🔄 执行数据库迁移..."\n\
# python manage.py migrate --noinput\n\
# echo "✅ 数据库迁移完成"\n\
# \n\
# echo "👤 创建管理员用户..."\n\
# python create_admin.py\n\
# \n\
# echo "🚀 启动应用服务器..."\n\
# exec gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 k8sui.wsgi:application' > /app/start.sh \
#     && chmod +x /app/start.sh

# CMD ["/app/start.sh"]