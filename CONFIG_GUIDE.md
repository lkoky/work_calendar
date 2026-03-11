# 前端配置说明

## 如何切换后端请求地址

### 方案 1：修改 `public/config.js`（推荐）

这是最简单的方式，无需重新编译前端。

```javascript
// 编辑 frontend/public/config.js
window.__WC_CONFIG__ = {
  // 修改下面这一行
  apiBaseUrl: 'http://你的后端IP:8000/api',
};
```

**修改后重新编译部署：**

```bash
cd frontend
npm run build
```

---

### 方案 2：部署后直接修改 `dist/config.js`

如果前端已经编译并部署到服务器，可以直接在服务器上修改：

```bash
# 登录服务器
ssh user@your-server

# 编辑配置文件
cd /opt/work_calendar/frontend/dist
sudo nano config.js
```

修改内容：

```javascript
window.__WC_CONFIG__ = {
  apiBaseUrl: 'http://你的后端IP:8000/api',
};
```

保存后刷新浏览器即可生效，无需重启服务！

---

### 方案 3：使用环境变量（开发时）

修改 `frontend/src/config.ts`：

```typescript
const configs = {
  test: {
    apiBaseUrl: 'http://192.168.1.100:8000/api',
  },
  // ...
};
```

编译时指定环境：

```bash
cd frontend
npm run build -- --mode test
```

---

## 配置优先级

1. **最高优先级**：`public/config.js` 中的 `window.__WC_CONFIG__`
2. **次优先级**：`src/config.ts` 中的环境配置

---

## Nginx 配置说明

Nginx 配置文件：`deploy/nginx.conf`

```nginx
# 前端静态文件
location /wc/ {
    alias /opt/work_calendar/frontend/dist/;
    try_files $uri $uri/ /wc/index.html;
}

# 后端API代理
location /wc/api/ {
    proxy_pass http://127.0.0.1:8000/;
}
```

### 如果后端在其他服务器

修改 `proxy_pass`：

```nginx
location /wc/api/ {
    proxy_pass http://192.168.1.100:8000/;  # 修改为你的后端IP
}
```

重载 Nginx：

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## 完整配置示例

### 示例 1：前后端同一台服务器（默认）

```javascript
// config.js
window.__WC_CONFIG__ = {
  apiBaseUrl: '/wc/api',
};
```

```nginx
// nginx.conf
location /wc/api/ {
    proxy_pass http://127.0.0.1:8000/;
}
```

---

### 示例 2：前后端分离，后端在 192.168.1.100

```javascript
// config.js
window.__WC_CONFIG__ = {
  apiBaseUrl: 'http://192.168.1.100:8000/api',
};
```

```nginx
// nginx.conf（可选，如果仍然想用 Nginx 代理）
location /wc/api/ {
    proxy_pass http://192.168.1.100:8000/;
}
```

---

### 示例 3：后端使用域名

```javascript
// config.js
window.__WC_CONFIG__ = {
  apiBaseUrl: 'https://api.your-domain.com/wc/api',
};
```

---

## 常见问题

### Q: 修改 config.js 后不生效？

A: 请强制刷新浏览器（Ctrl+F5 或 Cmd+Shift+R）清除缓存。

### Q: 可以不使用 Nginx 代理吗？

A: 可以！直接在 config.js 中指定完整的后端地址即可：

```javascript
window.__WC_CONFIG__ = {
  apiBaseUrl: 'http://192.168.1.100:8000/api',
};
```

注意：此时需要后端配置 CORS 允许跨域请求。

### Q: 如何验证配置是否生效？

A: 打开浏览器开发者工具（F12），在控制台输入：

```javascript
console.log(window.__WC_CONFIG__);
```

查看输出的 `apiBaseUrl` 是否正确。
