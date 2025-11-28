from fastapi import FastAPI, Request
import uvicorn
import json
from datetime import datetime
import logging
import logging.handlers

# 配置根日志器，确保所有日志都能被捕获
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),  # 控制台输出
        logging.handlers.RotatingFileHandler(
            "callback.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
    ]
)

# 获取应用特定的日志器
logger = logging.getLogger("callback_printer")

# 配置 uvicorn 使用自定义日志器
# 方法1：禁用 uvicorn 的默认日志配置，让 uvicorn 使用我们配置的根日志器
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers = []  # 清除 uvicorn 默认的处理器
uvicorn_logger.propagate = True  # 允许日志传播到根日志器

# 同样配置 uvicorn.access 和 uvicorn.error 日志器
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = []
uvicorn_access_logger.propagate = True

uvicorn_error_logger = logging.getLogger("uvicorn.error")
uvicorn_error_logger.handlers = []
uvicorn_error_logger.propagate = True

app = FastAPI(title="Callback Debug Server", description="用于调试回调请求的服务器")

@app.middleware("http")
async def log_request_info(request: Request, call_next):
    """中间件：记录所有请求的详细信息"""
    start_time = datetime.now()
    
    # 获取请求体内容
    body = await request.body()
    
    # 记录请求信息
    request_info = {
        "timestamp": start_time.isoformat(),
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "client": f"{request.client.host}:{request.client.port}" if request.client else "unknown",
        "body_size": len(body),
        "body_content": body.decode('utf-8', errors='ignore') if body else None
    }
    
    # 使用 logger 记录请求信息
    logger.info("="*80)
    logger.info(f"📨 收到请求 - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"📍 方法: {request.method}")
    logger.info(f"🔗 URL: {request.url}")
    logger.info(f"🌐 客户端: {request_info['client']}")
    logger.info(f"📏 请求体大小: {len(body)} bytes")
    logger.info("-"*80)
    
    # 记录头部信息
    logger.info("📋 请求头:")
    for key, value in request_info['headers'].items():
        logger.info(f"   {key}: {value}")
    
    # 记录查询参数
    if request_info['query_params']:
        logger.info("🔍 查询参数:")
        for key, value in request_info['query_params'].items():
            logger.info(f"   {key}: {value}")
    
    # 记录请求体
    if request_info['body_content']:
        logger.info("📄 请求体内容:")
        try:
            # 尝试解析为 JSON 并美化输出
            json_body = json.loads(request_info['body_content'])
            logger.info(json.dumps(json_body, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            # 如果不是 JSON，直接输出
            logger.info(request_info['body_content'])
    
    logger.info("="*80)
    
    # 记录请求详情
    logger.info(f"请求详情: {request_info}")
    
    # 继续处理请求
    response = await call_next(request)
    
    # 记录响应信息
    end_time = datetime.now()
    process_time = (end_time - start_time).total_seconds()
    
    response_info = {
        "timestamp": end_time.isoformat(),
        "status_code": response.status_code,
        "process_time": f"{process_time:.3f}s"
    }
    
    logger.info(f"📤 响应 - 状态码: {response.status_code}, 处理时间: {process_time:.3f}s")
    logger.info(f"响应详情: {response_info}")
    
    return response

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def catch_all_endpoint(request: Request, path: str):
    """捕获所有路由，返回简单的成功响应"""
    return {
        "status": "success",
        "message": f"路径 /{path} 的 {request.method} 请求已接收",
        "received_at": datetime.now().isoformat(),
        "path": path,
        "method": request.method
    }

if __name__ == "__main__":
    logger.info("🚀 启动回调调试服务器...")
    logger.info("📝 服务器将记录所有请求的详细信息")
    logger.info("📍 访问 http://localhost:8000 查看服务器信息")
    logger.info("📚 所有路径和方法都会被捕获和记录")
    logger.info("📊 所有请求信息将记录到 callback.log 文件")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        log_config=None,  # 禁用 uvicorn 的默认日志配置
        access_log=True   # 启用访问日志，但使用我们的自定义配置
    )
