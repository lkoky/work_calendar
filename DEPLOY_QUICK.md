# Linux 部署快速参考

## 前置条件

- 一台 Linux 服务器（Ubuntu/Debian 推荐）
- 服务器有 root 或 sudo 权限
- 服务器已开放 80 端口（HTTP）

## 快速部署（3步）

### 第1步：上传项目

```bash
# 方式1：使用Git克隆
cd /opt
git clone <你的仓库地址> work_calendar

# 方式2：使用SCP上传（本地执行）
scp -r work_calendar user@你的服务器IP:/opt/
```

### 第2步：执行一键部署

```bash
cd /opt/work_calendar
chmod +x deploy/install.sh
sudo deploy/install.sh
```

### 第3步：访问应用

部署完成后，通过以下地址访问（注意统一使用 `/wc/` 上下文路径）：

| 服务 | 地址 |
|------|------|
| 工作日历前端 | http://你的服务器IP/wc/ |
| 后端API文档 | http://你的服务器IP/wc/api/docs |

> **重要提示**：
> - 所有访问路径都必须包含 `/wc/` 前缀
> - Nginx 会自动将 `/wc/api/` 代理到后端的 `/api/`

---

## 手动部署（如果一键脚本失败）

### 1. 安装基础软件

```bash
sudo apt update
sudo apt install -y python3 python3-pip nginx git
```

### 2. 安装Python依赖

```bash
cd /opt/work_calendar
pip3 install -r requirements.txt
```

### 3. 配置后端服务

```bash
# 复制systemd服务文件
sudo cp deploy/systemd/work-calendar-api.service /etc/systemd/system/

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable work-calendar-api
sudo systemctl start work-calendar-api

# 检查状态
sudo systemctl status work-calendar-api
```

### 4. 编译前端

```bash
cd /opt/work_calendar/frontend
npm install
npm run build
```

### 5. 配置Nginx

```bash
# 复制Nginx配置
sudo cp deploy/nginx.conf /etc/nginx/sites-available/work-calendar

# 启用站点
sudo ln -s /etc/nginx/sites-available/work-calendar /etc/nginx/sites-enabled/

# 删除默认站点
sudo rm -f /etc/nginx/sites-enabled/default

# 测试并重启Nginx
sudo nginx -t
sudo systemctl reload nginx
```

### 6. 设置权限

```bash
sudo chown -R www-data:www-data /opt/work_calendar
sudo chmod -R 755 /opt/work_calendar
```

---

## 常用管理命令

### 后端服务管理

```bash
# 查看状态
sudo systemctl status work-calendar-api

# 启动
sudo systemctl start work-calendar-api

# 停止
sudo systemctl stop work-calendar-api

# 重启
sudo systemctl restart work-calendar-api

# 查看日志
sudo journalctl -u work-calendar-api -f

# 查看最近50条日志
sudo journalctl -u work-calendar-api -n 50
```

### Nginx管理

```bash
# 查看状态
sudo systemctl status nginx

# 重新加载配置
sudo systemctl reload nginx

# 重启
sudo systemctl restart nginx

# 查看错误日志
sudo tail -f /var/log/nginx/error.log

# 查看访问日志
sudo tail -f /var/log/nginx/access.log
```

---

## 访问地址配置

### 使用IP地址访问

```
http://你的服务器IP/wc/
```

### 使用域名访问（推荐）

1. 将域名解析到服务器IP
2. 修改 Nginx 配置中的 `server_name`

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 修改为你的域名
    # ... 其他配置
}
```

3. 重载 Nginx

```bash
sudo nginx -t
sudo systemctl reload nginx
```

4. 访问：`http://your-domain.com/wc/`

---

## 配置HTTPS（推荐）

### 使用Let's Encrypt免费证书

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书并自动配置
sudo certbot --nginx -d your-domain.com

# 测试自动续期
sudo certbot renew --dry-run
```

配置完成后，访问：`https://your-domain.com/wc/`

---

## 故障排查

### 问题1：页面404

**检查清单：**
- [ ] 前端是否已编译？`ls -la /opt/work_calendar/frontend/dist/`
- [ ] Nginx配置是否正确？`sudo nginx -t`
- [ ] Nginx是否已重启？`sudo systemctl reload nginx`
- [ ] 访问路径是否正确？需要加上 `/wc/`

**查看日志：**
```bash
sudo tail -f /var/log/nginx/error.log
```

### 问题2：API请求失败

**检查清单：**
- [ ] 后端服务是否运行？`sudo systemctl status work-calendar-api`
- [ ] 后端端口是否监听？`sudo netstat -tlnp | grep 8000`
- [ ] Nginx代理配置是否正确？

**查看后端日志：**
```bash
sudo journalctl -u work-calendar-api -n 50
```

### 问题3：数据库权限错误

**修复：**
```bash
sudo chown -R www-data:www-data /opt/work_calendar
sudo chmod 644 /opt/work_calendar/work_calendar.db
```

### 问题4：端口被占用

**检查端口：**
```bash
sudo netstat -tlnp | grep -E ':(80|8000)'
```

**停止占用端口的进程：**
```bash
# 找到PID后
sudo kill -9 <PID>
```

---

## 备份与恢复

### 备份数据库

```bash
# 手动备份
cp /opt/work_calendar/work_calendar.db /opt/work_calendar/backups/work_calendar_$(date +%Y%m%d).db

# 查看备份
ls -la /opt/work_calendar/backups/
```

### 恢复数据库

```bash
# 停止服务
sudo systemctl stop work-calendar-api

# 恢复备份
cp /opt/work_calendar/backups/work_calendar_20260310.db /opt/work_calendar/work_calendar.db

# 设置权限
sudo chown www-data:www-data /opt/work_calendar/work_calendar.db
sudo chmod 644 /opt/work_calendar/work_calendar.db

# 启动服务
sudo systemctl start work-calendar-api
```

---

## 更新应用

### 从Git更新

```bash
cd /opt/work_calendar

# 拉取最新代码
git pull origin main

# 更新依赖
pip3 install -r requirements.txt
cd frontend
npm install
npm run build

# 重启服务
sudo systemctl restart work-calendar-api
sudo systemctl reload nginx
```

### 手动上传更新

```bash
# 1. 停止服务
sudo systemctl stop work-calendar-api

# 2. 备份数据库
cp /opt/work_calendar/work_calendar.db /opt/work_calendar/work_calendar.db.backup

# 3. 上传新代码（本地执行）
scp -r work_calendar/* user@你的服务器IP:/opt/work_calendar/

# 4. 恢复数据库
cp /opt/work_calendar/work_calendar.db.backup /opt/work_calendar/work_calendar.db

# 5. 更新依赖
cd /opt/work_calendar
pip3 install -r requirements.txt
cd frontend
npm install
npm run build

# 6. 设置权限
sudo chown -R www-data:www-data /opt/work_calendar

# 7. 启动服务
sudo systemctl start work-calendar-api
sudo systemctl reload nginx
```

---

## 防火墙配置

### 允许HTTP/HTTPS

```bash
# 使用UFW（Ubuntu）
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# 查看状态
sudo ufw status
```

### 使用iptables

```bash
# 允许HTTP
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# 允许HTTPS
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# 保存规则
sudo iptables-save > /etc/iptables/rules.v4
```

---

## 文件结构说明

```
/opt/work_calendar/
├── main.py                          # 后端服务入口
├── requirements.txt                 # Python依赖
├── work_calendar.db                # SQLite数据库
├── DEPLOY.md                       # 完整部署文档
├── DEPLOY_QUICK.md                 # 本文档（快速参考）
├── frontend/                        # 前端项目
│   ├── dist/                       # 编译后的静态文件（生产环境使用）
│   ├── src/                        # 源代码
│   ├── package.json                # Node.js依赖
│   └── vite.config.ts              # Vite配置
└── deploy/                          # 部署配置
    ├── install.sh                  # 一键部署脚本
    ├── nginx.conf                  # Nginx配置
    └── systemd/
        └── work-calendar-api.service  # Systemd服务配置
```

---

## 技术支持

如遇到问题：

1. 查看日志文件
2. 检查本文档的"故障排查"部分
3. 查看完整文档：`DEPLOY.md`

---

祝你部署顺利！🎉
