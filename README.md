# Callback Debug Server

一个基于 FastAPI 的回调调试服务器，用于捕获和记录所有传入的 HTTP 请求，方便调试 Webhook、回调接口等。

## 功能特性

- **全路径捕获**: 接收任意路径的请求 (`/{path:path}`)
- **全方法支持**: GET、POST、PUT、DELETE、PATCH、OPTIONS、HEAD
- **详细日志记录**:
  - 请求时间、方法和 URL
  - 请求头信息
  - 查询参数
  - 请求体内容 (自动尝试 JSON 格式化)
  - 客户端 IP 和端口
  - 响应状态码和处理时间
- **日志输出**: 同时输出到控制台和文件
- **日志轮转**: 自动轮转，单文件最大 10MB，保留 10 个备份

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务器

```bash
python main.py
```

服务器将在 `http://localhost:8000` 启动。

### 发送测试请求

```bash
# GET 请求
curl http://localhost:8000/test

# POST 请求 (JSON)
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"event": "payment", "data": {"id": 123, "amount": 99.99}}'

# POST 请求 (表单)
curl -X POST http://localhost:8000/callback \
  -d "name=test&value=hello"

# 带查询参数的请求
curl "http://localhost:8000/api?token=abc123&version=2"
```

### 查看日志

所有请求日志会保存在 `callback.log` 文件中，同时也会输出到控制台。

## 项目结构

```
callback-printer/
├── main.py           # 主程序入口
├── requirements.txt  # Python 依赖
└── callback.log      # 运行后自动生成的日志文件
```

## 配置

如需修改服务器配置，可以编辑 `main.py` 中的以下参数:

- **端口**: 修改 `uvicorn.run()` 中的 `port=8000`
- **日志文件大小**: 修改 `maxBytes=10*1024*1024` (默认 10MB)
- **日志备份数量**: 修改 `backupCount=10`

## API 响应格式

任意路径的请求都会返回以下格式的响应:

```json
{
  "status": "success",
  "message": "路径 /xxx 的 POST 请求已接收",
  "received_at": "2026-03-14T12:00:00",
  "path": "xxx",
  "method": "POST"
}
```

## 适用场景

- 调试第三方 API 的回调通知
- 测试 Webhook 集成
- 捕获和分析 HTTP 请求数据
- 接口联调测试
- 查看请求头和请求体内容

## Docker 部署

### 运行容器

```bash
docker run -d -p 8000:8000 --name callback-printer ghcr.io/tursom/callback-printer:latest
```
