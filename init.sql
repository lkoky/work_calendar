-- 工作日历数据库建表脚本

-- 创建工作任务表
CREATE TABLE IF NOT EXISTS work_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL, -- 日期，格式：YYYY-MM-DD
    part TEXT NOT NULL, -- 上午/下午，值为 'morning' 或 'afternoon'
    task_content TEXT, -- 任务内容
    task_type TEXT, -- 任务类型：'completed'（完成内容）或 'planned'（预计任务）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_work_tasks_date ON work_tasks(date);
CREATE INDEX IF NOT EXISTS idx_work_tasks_date_part ON work_tasks(date, part);

-- 创建周汇总表
CREATE TABLE IF NOT EXISTS week_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_end_date TEXT NOT NULL UNIQUE, -- 周结束日期（周日），格式：YYYY-MM-DD
    summary_content TEXT, -- 汇总内容
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建周汇总表索引
CREATE INDEX IF NOT EXISTS idx_week_summaries_week_end_date ON week_summaries(week_end_date);
