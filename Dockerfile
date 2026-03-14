# 阶段1: 构建可执行文件
FROM python:3.13-alpine AS builder

WORKDIR /app
RUN apk add binutils musl-dev && pip install --no-cache-dir pyinstaller

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

RUN pyinstaller -w -F -s -p . main.py

# 阶段2: 运行
FROM alpine:latest

WORKDIR /app

COPY --from=builder /app/dist/main callback-printer

EXPOSE 8000

CMD ["./callback-printer"]
