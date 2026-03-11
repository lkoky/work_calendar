# 工作日历 - Linux 部署指南

## 访问路径说明

本应用统一使用 `/wc/` 作为上下文路径：

| 服务 | 访问地址 |
|------|----------|
| 前端页面 | http://your-ip/wc/ |
| 后端API | http://your-ip/wc/api/ |
| API文档 | http://your-ip/wc/api/docs |

## 目录结构

```
work_calendar/
├── main.py              # 后端服务
├── requirements.txt     # Python依赖
├── work_calendar.db    # 数据库文件
├── frontend/            # 前端项目
│   ├── dist/           # 编译后的前端文件
│   └── ...
└── deploy/             # 部署配置
    ├── nginx.conf      # Nginx配置
    └── systemd/        # Systemd服务配置
```

## 1. 准备工作

### 1.1 安装基础软件

```bash
# 安装Python3、Pip、Nginx
sudo apt update
sudo apt install -y python3 python3-pip nginx git

# 验证版本
python3 --version
nginx -v
```

### 1.2 上传代码

```bash
# 使用scp或git上传代码到服务器
cd /opt
git clone <your-repo-url> work_calendar
# 或
scp -r work_calendar user@your-server:/opt/
```

## 2. 后端部署

### 2.1 创建Python虚拟环境

```bash
cd /opt/work_calendar

# 创建虚拟环境（如果不存在）
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# 激活虚拟环境
source .venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt
```

### 2.2 创建Systemd服务

创建 `/etc/systemd/system/work-calendar-api.service`：

```ini
[Unit]
Description=Work Calendar Backend API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/work_calendar
Environment="PATH=/opt/work_calendar/venv/bin"
ExecStart=/opt/work_calendar/venv/bin/python /opt/work_calendar/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2.3 启动后端服务

```bash
# 重载systemd配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start work-calendar-api

# 设置开机自启
sudo systemctl enable work-calendar-api

# 查看服务状态
sudo systemctl status work-calendar-api

# 查看日志
sudo journalctl -u work-calendar-api -f
```

## 3. 前端部署

### 3.1 编译前端

```bash
cd /opt/work_calendar/frontend

# 安装依赖（如果需要）
npm install

# 编译生产版本
npm run build
```

### 3.2 配置Nginx

创建 `/etc/nginx/sites-available/work-calendar`：

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 或使用IP地址

    # 前端静态文件
    location /wc/ {
        alias /opt/work_calendar/frontend/dist/;
        try_files $uri $uri/ /wc/index.html;
        index index.html;
        
        # 缓存静态资源
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # 后端API代理 - /wc/api/ 路径
    location /wc/api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持（如果需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # 禁止访问敏感文件
    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

### 3.3 启用Nginx配置

```bash
# 创建符号链接
sudo ln -s /etc/nginx/sites-available/work-calendar /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx

# 设置开机自启
sudo systemctl enable nginx
```

## 4. 访问地址

配置完成后，可通过以下地址访问（注意统一使用 `/wc/` 上下文路径）：

| 服务 | 地址 |
|------|------|
| 前端 | http://your-ip/wc/ |
| 后端API | http://your-ip/wc/api/ |
| 健康检查 | http://your-ip/wc/api/docs |

> **重要提示**：
> - 所有访问路径都必须包含 `/wc/` 前缀
> - Nginx 会自动将 `/wc/api/` 代理到后端的 `/api/`

## 5. 安全加固（可选）

### 5.1 防火墙配置

```bash
# 允许HTTP
sudo ufw allow 80/tcp

# 允许HTTPS（如果配置）
sudo ufw allow 443/tcp

# 启用防火墙
sudo ufw enable
```

### 5.2 配置HTTPS（推荐）

使用 Let's Encrypt 免费证书：

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书并自动配置Nginx
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

### 5.3 数据库权限

```bash
# 设置数据库文件权限
cd /opt/work_calendar
sudo chown www-data:www-data work_calendar.db
sudo chmod 644 work_calendar.db
```

## 6. 常见问题

### 6.1 后端服务无法启动

```bash
# 检查端口占用
sudo netstat -tlnp | grep 8000

# 查看详细错误日志
sudo journalctl -u work-calendar-api -n 50
```

### 6.2 前端404错误

```bash
# 检查Nginx配置
sudo nginx -t

# 查看Nginx错误日志
sudo tail -f /var/log/nginx/error.log
```

### 6.3 数据库权限问题

```bash
# 检查目录权限
ls -la /opt/work_calendar/

# 修复权限
sudo chown -R www-data:www-data /opt/work_calendar/
```

## 7. 备份策略

### 7.1 数据库备份

创建 `/opt/work_calendar/backup.sh`：

```bash
#!/bin/bash
BACKUP_DIR="/opt/work_calendar/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp /opt/work_calendar/work_calendar.db $BACKUP_DIR/work_calendar_$DATE.db

# 保留最近7天的备份
find $BACKUP_DIR -name "work_calendar_*.db" -mtime +7 -delete
```

添加定时任务：

```bash
# 编辑crontab
crontab -e

# 每天凌晨2点备份
0 2 * * * /opt/work_calendar/backup.sh
```

## 8. 版本更新流程

```bash
# 1. 拉取最新代码
cd /opt/work_calendar
git pull origin main

# 2. 更新依赖
pip3 install -r requirements.txt
cd frontend
npm install
npm run build

# 3. 重启服务
sudo systemctl restart work-calendar-api
sudo systemctl reload nginx
```

---

部署完成！如有问题请查看日志文件。
