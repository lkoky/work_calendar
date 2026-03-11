#!/bin/bash
set -e

echo "=========================================="
echo "工作日历 - 一键部署脚本"
echo "=========================================="

# 配置变量
PROJECT_DIR="/opt/work_calendar"
SERVICE_NAME="work-calendar-api"
NGINX_CONF_NAME="work-calendar"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}[成功]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[警告]${NC} $1"
}

print_error() {
    echo -e "${RED}[错误]${NC} $1"
}

print_info() {
    echo -e "[信息] $1"
}

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then 
    print_error "请使用root用户运行此脚本"
    print_info "使用命令: sudo $0"
    exit 1
fi

# 1. 检查项目目录
echo ""
print_info "1. 检查项目目录..."
if [ ! -d "$PROJECT_DIR" ]; then
    print_error "项目目录不存在: $PROJECT_DIR"
    print_info "请先将项目上传到 $PROJECT_DIR"
    exit 1
fi
print_success "项目目录检查完成"

# 2. 创建并激活Python虚拟环境
echo ""
print_info "2. 创建Python虚拟环境..."
cd "$PROJECT_DIR"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    print_success "虚拟环境创建完成"
else
    print_warning "虚拟环境已存在，跳过创建"
fi

# 3. 安装Python依赖
echo ""
print_info "3. 安装Python依赖..."
source "$PROJECT_DIR/.venv/bin/activate"
pip install -r requirements.txt
print_success "Python依赖安装完成"

# 4. 创建数据库（如果不存在）
echo ""
print_info "4. 初始化数据库..."
if [ ! -f "$PROJECT_DIR/work_calendar.db" ]; then
    print_warning "数据库文件不存在，将在首次运行时自动创建"
fi
print_success "数据库初始化完成"

# 5. 配置Systemd服务
echo ""
print_info "5. 配置Systemd服务..."
cp "$PROJECT_DIR/deploy/systemd/work-calendar-api.service" "/etc/systemd/system/$SERVICE_NAME.service"

# 设置虚拟环境目录权限
chown -R www-data:www-data "$PROJECT_DIR/.venv"

systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl start "$SERVICE_NAME"
print_success "Systemd服务配置完成"

# 等待服务启动
print_info "等待服务启动..."
sleep 3

# 检查服务状态
if systemctl is-active --quiet "$SERVICE_NAME"; then
    print_success "后端服务已启动"
else
    print_error "后端服务启动失败"
    print_info "查看日志: journalctl -u $SERVICE_NAME -n 50"
    exit 1
fi

# 6. 编译前端
echo ""
print_info "6. 编译前端..."
cd "$PROJECT_DIR/frontend"
if [ ! -d "node_modules" ]; then
    print_info "安装前端依赖..."
    npm install
fi
npm run build
print_success "前端编译完成"

# 7. 配置Nginx
echo ""
print_info "7. 配置Nginx..."
cp "$PROJECT_DIR/deploy/nginx.conf" "/etc/nginx/sites-available/$NGINX_CONF_NAME"

# 删除默认站点（如果存在）
if [ -f "/etc/nginx/sites-enabled/default" ]; then
    rm -f "/etc/nginx/sites-enabled/default"
fi

# 创建符号链接
ln -sf "/etc/nginx/sites-available/$NGINX_CONF_NAME" "/etc/nginx/sites-enabled/$NGINX_CONF_NAME"

# 测试Nginx配置
if nginx -t; then
    systemctl reload nginx
    print_success "Nginx配置完成"
else
    print_error "Nginx配置错误"
    exit 1
fi

# 8. 设置权限
echo ""
print_info "8. 设置文件权限..."
# chown -R www-data:www-data "$PROJECT_DIR"
chmod -R 755 "$PROJECT_DIR"
if [ -f "$PROJECT_DIR/work_calendar.db" ]; then
    chmod 644 "$PROJECT_DIR/work_calendar.db"
fi
print_success "文件权限设置完成"

# 获取服务器IP
SERVER_IP=$(hostname -I | awk '{print $1}')

echo ""
echo "=========================================="
print_success "部署完成！"
echo "=========================================="
echo ""
echo "访问地址（注意统一使用 /wc/ 上下文路径）："
echo "  前端: http://$SERVER_IP/wc/"
echo "  后端API: http://$SERVER_IP/wc/api/"
echo "  API文档: http://$SERVER_IP/wc/api/docs"
echo ""
echo "管理命令："
echo "  查看后端状态: systemctl status $SERVICE_NAME"
echo "  查看后端日志: journalctl -u $SERVICE_NAME -f"
echo "  重启后端: systemctl restart $SERVICE_NAME"
echo "  重启Nginx: systemctl reload nginx"
echo ""
