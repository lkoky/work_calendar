# 工作日历系统

一个现代化的工作日历管理系统，支持任务管理和周汇总功能。

## 功能特性

### 核心功能

- 📅 日历视图 - 月历展示，查看每日任务
- ✏️ 任务编辑 - 支持 Markdown 格式的富文本编辑
- 📊 周汇总 - 自动汇总本周任务，支持重新生成和编辑
- 📱 响应式设计 - 适配不同屏幕尺寸

### 任务管理

- 上午/下午任务分离
- Markdown 格式支持
- 周日汇总按钮
- 任务类型标记

### 周汇总功能

- 周一到周六自动汇总
- 独立的周汇总表存储
- 重新汇总按钮
- 可编辑的汇总内容
- 保存功能

## 技术栈

### 后端

- **框架**: FastAPI (Python)
- **数据库**: SQLite
- **服务器**: Uvicorn

### 前端

- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **Markdown 编辑器**: md-editor-v3
- **UI 样式**: 自定义 CSS（深色主题）

### 部署

- **Web 服务器**: Nginx
- **进程管理**: Systemd
- **Python 环境**: 虚拟环境 (venv)

## 快速开始

### 开发环境

#### 1. 后端启动

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

后端运行在: <http://localhost:5035>

#### 2. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端运行在: <http://localhost:5173/wc/>

***

## 项目结构

```
work_calendar/
├── main.py                      # 后端服务入口
├── requirements.txt             # Python 依赖
├── work_calendar.db            # SQLite 数据库
├── init.sql                    # 数据库初始化脚本
├── README.md                   # 本文档
├── DEPLOY.md                   # 完整部署文档
├── DEPLOY_QUICK.md            # 快速部署参考
├── CONFIG_GUIDE.md             # 配置指南
├── frontend/                   # 前端项目
│   ├── src/
│   │   ├── components/
│   │   │   └── Calendar.vue    # 日历主组件
│   │   ├── api.ts             # API 调用
│   │   ├── config.ts          # 环境配置
│   │   └── main.ts            # 入口文件
│   ├── public/
│   │   └── config.js         # 运行时配置
│   ├── vite.config.ts        # Vite 配置
│   ├── package.json          # Node.js 依赖
│   └── dist/                 # 编译产物
└── deploy/                   # 部署配置
    ├── install.sh            # 一键部署脚本
    ├── nginx.conf            # Nginx 配置
    ├── systemd/
    │   └── work-calendar-api.service  # Systemd 服务
    └── service.sh            # 服务管理脚本
```

***

## API 接口

### 任务接口

| 方法     | 路径                                   | 说明          |
| ------ | ------------------------------------ | ----------- |
| GET    | `/api/tasks`                         | 获取所有任务      |
| GET    | `/api/tasks/{date}`                  | 按日期获取任务     |
| POST   | `/api/tasks`                         | 创建或更新任务     |
| PUT    | `/api/tasks/{task_id}`               | 更新任务        |
| DELETE | `/api/tasks/{task_id}`               | 删除任务        |
| POST   | `/api/tasks/summary/{week_end_date}` | 汇总本周任务（旧接口） |

### 周汇总接口

| 方法   | 路径                                               | 说明       |
| ---- | ------------------------------------------------ | -------- |
| GET  | `/api/week-summaries/{week_end_date}`            | 获取周汇总    |
| POST | `/api/week-summaries`                            | 创建或更新周汇总 |
| POST | `/api/week-summaries/regenerate/{week_end_date}` | 重新生成本周汇总 |

***

## 部署指南

### 一键部署（推荐）

```bash
# 1. 上传项目到服务器
cd /opt
git clone <your-repo-url> work_calendar

# 2. 执行一键部署
cd /opt/work_calendar
chmod +x deploy/install.sh
sudo deploy/install.sh
```

### 访问地址

部署完成后访问：

| 服务     | 地址                           |
| ------ | ---------------------------- |
| 前端     | <http://your-ip/wc/>         |
| 后端 API | <http://your-ip/wc/api/>     |
| API 文档 | <http://your-ip/wc/api/docs> |

***

## 数据库

### 表结构

#### work\_tasks（任务表）

| 字段            | 类型        | 说明                         |
| ------------- | --------- | -------------------------- |
| id            | INTEGER   | 主键，自增                      |
| date          | TEXT      | 日期 (YYYY-MM-DD)            |
| part          | TEXT      | 时间段: 'morning'/'afternoon' |
| task\_content | TEXT      | 任务内容 (Markdown)            |
| task\_type    | TEXT      | 任务类型                       |
| created\_at   | TIMESTAMP | 创建时间                       |
| updated\_at   | TIMESTAMP | 更新时间                       |

#### week\_summaries（周汇总表）

| 字段               | 类型        | 说明              |
| ---------------- | --------- | --------------- |
| id               | INTEGER   | 主键，自增           |
| week\_end\_date  | TEXT      | 周结束日期（周日）       |
| summary\_content | TEXT      | 汇总内容 (Markdown) |
| created\_at      | TIMESTAMP | 创建时间            |
| updated\_at      | TIMESTAMP | 更新时间            |

***

## 配置说明

### 前端环境配置

编辑 `frontend/public/config.js`：

```javascript
window.__WC_CONFIG__ = {
  apiBaseUrl: '/wc/api',
};
```

### 前端开发配置

编辑 `frontend/src/config.ts` 可配置不同环境。

### 后端配置

后端默认端口：5035，可在 `main.py` 末尾修改。

***

## 管理命令

### 使用 service.sh

```bash
# 启动服务
./service.sh start

# 停止服务
./service.sh stop

# 重启服务
./service.sh restart

# 查看状态
./service.sh status

# 查看日志
./service.sh logs
```

### Systemd 管理

```bash
# 查看状态
sudo systemctl status work-calendar-api

# 查看日志
sudo journalctl -u work-calendar-api -f

# 重启
sudo systemctl restart work-calendar-api

# 重载 Nginx
sudo systemctl reload nginx
```

***

## 开发说明

### 前端编译

```bash
cd frontend
npm run build
```

编译产物：`frontend/dist/`

### 后端开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python main.py
```

***

## 常见问题

### Q: 数据库在哪里？

A: `work_calendar.db` 在项目根目录。

### Q: 如何切换后端地址？

A: 编辑 `frontend/public/config.js` 中的 `apiBaseUrl`。

### Q: 前端编译后 vite.config.ts 还需要吗？

A: 不需要，只在开发和编译时使用。

***

## 许可证

MIT License

***

## 联系方式

如有问题，请查看：

- [DEPLOY.md](DEPLOY.md) - 完整部署文档
- [DEPLOY\_QUICK.md](DEPLOY_QUICK.md) - 快速部署参考
- [CONFIG\_GUIDE.md](CONFIG_GUIDE.md) - 配置指南

