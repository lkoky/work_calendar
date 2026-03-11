#!/bin/bash

# 工作日历系统服务管理脚本 (Linux/Mac)

# 配置
INST_DIR=$(pwd)
LOG_DIR="${INST_DIR}/logs"
LOG_FILE="${LOG_DIR}/app.log"
ERROR_LOG_FILE="${LOG_DIR}/error.log"
PID_FILE="${LOG_DIR}/app.pid"
PYTHON_CMD="python"
APP_SCRIPT="main.py"
SERVICE_NAME="work-calendar"

# 创建日志目录
mkdir -p "${LOG_DIR}"

# 获取进程ID
get_pid() {
    ps aux | grep "${INST_DIR}" | grep "${APP_SCRIPT}" | grep -v grep | awk '{print $2}'
}

# 检查服务状态
check_status() {
    local pid=$(get_pid)
    if [ -n "$pid" ]; then
        echo "running"
        return 0
    else
        echo "stopped"
        return 1
    fi
}

# 启动服务
start_service() {
    echo "正在启动 ${SERVICE_NAME}..."
    
    # 检查是否已在运行
    if [ "$(check_status)" = "running" ]; then
        local pid=$(get_pid)
        echo "服务已在运行，PID: ${pid}"
        return 1
    fi
    
    # 备份旧日志
    if [ -f "${LOG_FILE}" ]; then
        mv "${LOG_FILE}" "${LOG_FILE}.bak"
        echo "备份旧日志: ${LOG_FILE}.bak"
    fi
    
    # 启动服务
    echo "启动时间: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # 检查虚拟环境
    if [ -d ".venv" ]; then
        source .venv/bin/activate
        PYTHON_CMD="${INST_DIR}/.venv/bin/python"
        echo "使用虚拟环境: ${PYTHON_CMD}"
    fi
    
    # 后台启动并记录日志
    nohup ${PYTHON_CMD} ${APP_SCRIPT} > "${LOG_FILE}" 2>&1 &
    local pid=$!
    
    # 保存PID
    echo ${pid} > "${PID_FILE}"
    
    # 等待启动
    sleep 3
    
    # 验证启动
    if [ "$(check_status)" = "running" ]; then
        local new_pid=$(get_pid)
        echo "服务启动成功，PID: ${new_pid}"
        echo "访问地址: http://localhost:5035/wc/api/docs"
        echo "日志文件: ${LOG_FILE}"
        echo "错误日志: ${ERROR_LOG_FILE}"
        return 0
    else
        echo "服务启动失败，请查看日志: ${ERROR_LOG_FILE}"
        return 1
    fi
}

# 停止服务
stop_service() {
    echo "正在停止 ${SERVICE_NAME}..."
    
    local pid=$(get_pid)
    if [ -z "$pid" ]; then
        echo "服务未运行"
        return 0
    fi
    
    echo "停止时间: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # 停止进程
    kill ${pid}
    sleep 2
    
    # 验证停止
    if [ "$(check_status)" = "stopped" ]; then
        echo "服务停止成功"
        
        # 删除PID文件
        if [ -f "${PID_FILE}" ]; then
            rm -f "${PID_FILE}"
        fi
        return 0
    else
        echo "服务停止失败，PID: ${pid}"
        return 1
    fi
}

# 重启服务
restart_service() {
    echo "正在重启 ${SERVICE_NAME}..."
    stop_service
    sleep 2
    start_service
}

# 显示服务状态
show_status() {
    local pid=$(get_pid)
    
    if [ -n "$pid" ]; then
        echo "服务状态: 运行中"
        echo "进程ID: ${pid}"
        
        # 显示进程信息
        if command -v ps &> /dev/null; then
            local start_time=$(ps -p ${pid} -o lstart= | tail -n 1)
            local cpu_usage=$(ps -p ${pid} -o %cpu= | tail -n 1)
            local mem_usage=$(ps -p ${pid} -o %mem= | tail -n 1)
            
            echo "启动时间: ${start_time}"
            echo "CPU使用率: ${cpu_usage}%"
            echo "内存使用: ${mem_usage}%"
        fi
        
        # 显示日志最后几行
        if [ -f "${LOG_FILE}" ]; then
            echo ""
            echo "最近日志:"
            tail -n 10 "${LOG_FILE}"
        fi
        
        return 0
    else
        echo "服务状态: 未运行"
        return 1
    fi
}

# 查看日志
show_logs() {
    if [ ! -f "${LOG_FILE}" ]; then
        echo "日志文件不存在: ${LOG_FILE}"
        return 1
    fi
    
    echo "实时监控日志 (Ctrl+C 退出)..."
    tail -f "${LOG_FILE}"
}

# 显示帮助信息
show_help() {
    cat << EOF
工作日历系统服务管理脚本

用法:
  ./service.sh [命令]

命令:
  start      启动服务
  stop       停止服务
  restart    重启服务
  status     查看服务状态
  logs       实时查看日志
  help       显示帮助信息

示例:
  ./service.sh start      # 启动服务
  ./service.sh stop       # 停止服务
  ./service.sh restart    # 重启服务
  ./service.sh status     # 查看状态
  ./service.sh logs       # 查看日志

注意事项:
  1. 确保已安装Python 3.8+
  2. 首次使用前请创建虚拟环境: python3 -m venv venv
  3. 激活虚拟环境并安装依赖: source venv/bin/activate && pip install -r requirements.txt
  4. 生产环境建议使用systemd管理服务

EOF
}

# 主程序
case "$1" in
    start)
        start_service
        exit $?
        ;;
    stop)
        stop_service
        exit $?
        ;;
    restart)
        restart_service
        exit $?
        ;;
    status)
        show_status
        exit $?
        ;;
    logs)
        show_logs
        exit 0
        ;;
    help|-h|--help)
        show_help
        exit 0
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

exit 0
