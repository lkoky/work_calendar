/**
 * 环境配置
 * 用于配置不同环境的后端地址
 */

// 当前环境类型
const ENV = import.meta.env.MODE || 'development';

// 环境配置
const configs = {
  // 开发环境 - 使用 Vite 代理
  development: {
    apiBaseUrl: '/wc/api',
  },
  
  // 生产环境 - 使用相对路径（Nginx 代理）
  production: {
    apiBaseUrl: '/wc/api',
  },
  
  // 测试环境 - 可以直接指定后端地址
  test: {
    apiBaseUrl: 'http://localhost:5035/api',
  },
};

// 获取当前环境配置
const currentConfig = configs[ENV as keyof typeof configs] || configs.development;

export default {
  ...currentConfig,
  // 也可以直接通过 window.__WC_CONFIG__ 注入（由 Nginx 或后端提供）
  ...(typeof window !== 'undefined' && (window as any).__WC_CONFIG__),
};
