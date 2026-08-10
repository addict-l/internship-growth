# Day 04: FastAPI Robot Service

使用 FastAPI 实现的学习用机器人云端接口模拟服务。

## Features

- 服务健康检查
- 查询机器人列表
- 查询机器人状态
- 发送机器人控制指令
- 模拟机器人状态上报
- Pydantic 数据校验
- HTTP 错误状态处理

## Run

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload