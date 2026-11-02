#!/usr/bin/env python3
"""
后端API服务
使用FastAPI框架实现任务的增删改查接口
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
from pydantic import BaseModel
from typing import List, Optional

# 创建FastAPI应用
app = FastAPI(
    title="工作日历API",
    description="工作日历后端API服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库连接
DB_PATH = os.path.join(os.path.dirname(__file__), 'work_calendar.db')

def get_db():
    """
    获取数据库连接
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 使返回的结果可以通过列名访问
    return conn

def init_db():
    """
    初始化数据库表
    """
    conn = get_db()
    try:
        cursor = conn.cursor()
        
        # 创建任务表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS work_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                part TEXT NOT NULL,
                task_content TEXT,
                task_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建周汇总表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS week_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_end_date TEXT NOT NULL UNIQUE,
                summary_content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
    finally:
        conn.close()

# 初始化数据库
init_db()

# 数据模型
class TaskBase(BaseModel):
    """
    任务基础模型
    """
    date: str
    part: str
    task_content: Optional[str] = None
    task_type: Optional[str] = None

class TaskCreate(TaskBase):
    """
    创建任务模型
    """
    pass

class TaskUpdate(BaseModel):
    """
    更新任务模型
    """
    task_content: Optional[str] = None
    task_type: Optional[str] = None

class Task(TaskBase):
    """
    任务响应模型
    """
    id: int
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

# 周汇总数据模型
class WeekSummaryBase(BaseModel):
    """
    周汇总基础模型
    """
    week_end_date: str
    summary_content: Optional[str] = None

class WeekSummaryUpdate(BaseModel):
    """
    周汇总更新模型
    """
    summary_content: Optional[str] = None

class WeekSummary(WeekSummaryBase):
    """
    周汇总响应模型
    """
    id: int
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

# API接口
@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    """
    获取所有任务
    """
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM work_tasks ORDER BY date, part")
        tasks = cursor.fetchall()
        return [dict(task) for task in tasks]
    finally:
        conn.close()

@app.get("/api/tasks/{date}", response_model=List[Task])
def get_tasks_by_date(date: str):
    """
    按日期获取任务
    """
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM work_tasks WHERE date = ? ORDER BY part", (date,))
        tasks = cursor.fetchall()
        return [dict(task) for task in tasks]
    finally:
        conn.close()

@app.post("/api/tasks", response_model=Task)
def create_task(task: TaskCreate):
    """
    创建任务
    """
    conn = get_db()
    try:
        cursor = conn.cursor()
        # 检查是否已存在相同日期和时间段的任务
        cursor.execute(
            "SELECT id FROM work_tasks WHERE date = ? AND part = ?",
            (task.date, task.part)
        )
        existing_task = cursor.fetchone()
        
        if existing_task:
            # 更新现有任务
            cursor.execute(
                """
                UPDATE work_tasks 
                SET task_content = ?, task_type = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
                """,
                (task.task_content, task.task_type, existing_task["id"])
            )
            task_id = existing_task["id"]
        else:
            # 创建新任务
            cursor.execute(
                """
                INSERT INTO work_tasks (date, part, task_content, task_type) 
                VALUES (?, ?, ?, ?)
                """,
                (task.date, task.part, task.task_content, task.task_type)
            )
            task_id = cursor.lastrowid

        # 迁移清理：保存 morning 时，自动删除同日期的 afternoon 残留记录
        # 新设计不再区分上午/下午，统一存一条 morning 记录
        if task.part == 'morning':
            cursor.execute(
                "DELETE FROM work_tasks WHERE date = ? AND part = 'afternoon'",
                (task.date,)
            )
        
        conn.commit()
        
        # 查询并返回创建/更新的任务
        cursor.execute("SELECT * FROM work_tasks WHERE id = ?", (task_id,))
        created_task = cursor.fetchone()
        return dict(created_task)
    finally:
        conn.close()

@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate):
    """
    更新任务
    """
    conn = get_db()
    try:
        cursor = conn.cursor()
        # 检查任务是否存在
        cursor.execute("SELECT id FROM work_tasks WHERE id = ?", (task_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="任务不存在")
        
        # 更新任务
        cursor.execute(
            """
            UPDATE work_tasks 
            SET task_content = ?, task_type = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
            """,
            (task.task_content, task.task_type, task_id)
        )
        conn.commit()
        
        # 查询并返回更新后的任务
        cursor.execute("SELECT * FROM work_tasks WHERE id = ?", (task_id,))
        updated_task = cursor.fetchone()
        return dict(updated_task)
    finally:
        conn.close()

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    """
    删除任务
    """
    conn = get_db()
    try:
        cursor = conn.cursor()
        # 检查任务是否存在
        cursor.execute("SELECT id FROM work_tasks WHERE id = ?", (task_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="任务不存在")
        
        # 删除任务
        cursor.execute("DELETE FROM work_tasks WHERE id = ?", (task_id,))
        conn.commit()
        
        return {"message": "任务删除成功"}
    finally:
        conn.close()

@app.post("/api/tasks/summary/{week_end_date}")
def summarize_week_tasks(week_end_date: str):
    """
    汇总本周任务到周日
    """
    conn = get_db()
    try:
        cursor = conn.cursor()
        
        # 解析日期，计算本周一到周五的日期
        import datetime
        end_date = datetime.datetime.strptime(week_end_date, "%Y-%m-%d")
        
        # 确保输入的是周日
        if end_date.weekday() != 6:  # 0=周一, 6=周日
            raise HTTPException(status_code=400, detail="请输入周日的日期")
        
        # 计算本周一到周五的日期（只汇总周一到周五，排除周六）
        dates = []
        for i in range(5):  # 0-4 = 周一到周五
            date = end_date - datetime.timedelta(days=6-i)  # 周日-6天=周一
            dates.append(date.strftime("%Y-%m-%d"))
        
        # 查询本周一到周五的所有任务
        placeholders = ",".join(["?"] * len(dates))
        cursor.execute(
            f"SELECT * FROM work_tasks WHERE date IN ({placeholders}) ORDER BY date, part",
            dates
        )
        week_tasks = cursor.fetchall()
        
        # 按日期和时间段分组
        tasks_by_date = {}
        for task in week_tasks:
            task_dict = dict(task)
            date = task_dict['date']
            part = task_dict['part']
            
            if date not in tasks_by_date:
                tasks_by_date[date] = {'morning': '', 'afternoon': ''}
            
            if part == 'morning':
                tasks_by_date[date]['morning'] = task_dict.get('task_content', '')
            elif part == 'afternoon':
                tasks_by_date[date]['afternoon'] = task_dict.get('task_content', '')
        
        # 生成汇总内容
        summary_lines = []
        
        for date in dates:  # 按周一到周五的顺序
            if date not in tasks_by_date:
                continue
            
            date_tasks = tasks_by_date[date]
            morning_content = date_tasks.get('morning', '').strip()
            afternoon_content = date_tasks.get('afternoon', '').strip()
            
            # 如果当天无任务，跳过
            if not morning_content and not afternoon_content:
                continue
            
            # 添加日期
            summary_lines.append(f"{date}：")
            
            # 添加上午内容
            if morning_content:
                summary_lines.append(f"\n{morning_content}")
            
            # 添加下午内容
            if afternoon_content:
                summary_lines.append(f"\n{afternoon_content}")
            
            # 添加空行分隔
            summary_lines.append("")
        
        # 移除最后一个空行
        if summary_lines and summary_lines[-1] == "":
            summary_lines.pop()
        
        summary = "\n".join(summary_lines)
        
        # 检查周日是否已有任务记录
        cursor.execute(
            "SELECT id FROM work_tasks WHERE date = ? AND part = 'morning'",
            (week_end_date,)
        )
        existing_task = cursor.fetchone()
        
        if existing_task:
            # 更新现有任务
            cursor.execute(
                """
                UPDATE work_tasks 
                SET task_content = ?, task_type = 'completed', updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
                """,
                (summary, existing_task["id"])
            )
        else:
            # 创建新任务
            cursor.execute(
                """
                INSERT INTO work_tasks (date, part, task_content, task_type) 
                VALUES (?, ?, ?, ?)
                """,
                (week_end_date, 'morning', summary, 'completed')
            )
        
        conn.commit()
        
        return {"message": "本周任务汇总成功", "summary": summary}
    finally:
        conn.close()

# 周汇总API
@app.get("/api/week-summaries/{week_end_date}", response_model=Optional[WeekSummary])
def get_week_summary(week_end_date: str):
    """
    获取指定周的汇总
    """
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM week_summaries WHERE week_end_date = ?",
            (week_end_date,)
        )
        summary = cursor.fetchone()
        if summary:
            return dict(summary)
        return None
    finally:
        conn.close()

@app.post("/api/week-summaries", response_model=WeekSummary)
def create_or_update_week_summary(summary: WeekSummaryBase):
    """
    创建或更新周汇总
    """
    conn = get_db()
    try:
        cursor = conn.cursor()
        
        # 检查是否已存在
        cursor.execute(
            "SELECT id FROM week_summaries WHERE week_end_date = ?",
            (summary.week_end_date,)
        )
        existing = cursor.fetchone()
        
        if existing:
            # 更新
            cursor.execute(
                """
                UPDATE week_summaries 
                SET summary_content = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE week_end_date = ?
                """,
                (summary.summary_content, summary.week_end_date)
            )
            summary_id = existing["id"]
        else:
            # 创建
            cursor.execute(
                """
                INSERT INTO week_summaries (week_end_date, summary_content) 
                VALUES (?, ?)
                """,
                (summary.week_end_date, summary.summary_content)
            )
            summary_id = cursor.lastrowid
        
        conn.commit()
        
        # 返回创建/更新的汇总
        cursor.execute("SELECT * FROM week_summaries WHERE id = ?", (summary_id,))
        result = cursor.fetchone()
        return dict(result)
    finally:
        conn.close()

@app.post("/api/week-summaries/regenerate/{week_end_date}", response_model=WeekSummary)
def regenerate_week_summary(week_end_date: str):
    """
    重新生成本周汇总
    """
    conn = get_db()
    try:
        cursor = conn.cursor()
        
        # 解析日期，计算本周一到周六的日期（包含周六）
        import datetime
        end_date = datetime.datetime.strptime(week_end_date, "%Y-%m-%d")
        
        # 确保输入的是周日
        if end_date.weekday() != 6:  # 0=周一, 6=周日
            raise HTTPException(status_code=400, detail="请输入周日的日期")
        
        # 计算本周一到周六的日期
        dates = []
        for i in range(6):  # 0-5 = 周一到周六
            date = end_date - datetime.timedelta(days=6-i)  # 周日-6天=周一
            dates.append(date.strftime("%Y-%m-%d"))
        
        # 查询本周一到周六的所有任务
        placeholders = ",".join(["?"] * len(dates))
        cursor.execute(
            f"SELECT * FROM work_tasks WHERE date IN ({placeholders}) ORDER BY date, part",
            dates
        )
        week_tasks = cursor.fetchall()
        
        # 按日期和时间段分组
        tasks_by_date = {}
        for task in week_tasks:
            task_dict = dict(task)
            date = task_dict['date']
            part = task_dict['part']
            
            if date not in tasks_by_date:
                tasks_by_date[date] = {'morning': '', 'afternoon': ''}
            
            if part == 'morning':
                tasks_by_date[date]['morning'] = task_dict.get('task_content', '')
            elif part == 'afternoon':
                tasks_by_date[date]['afternoon'] = task_dict.get('task_content', '')
        
        # 生成汇总内容
        summary_lines = []
        
        for date in dates:  # 按周一到周六的顺序
            if date not in tasks_by_date:
                continue
            
            date_tasks = tasks_by_date[date]
            morning_content = date_tasks.get('morning', '').strip()
            afternoon_content = date_tasks.get('afternoon', '').strip()
            
            # 如果当天无任务，跳过
            if not morning_content and not afternoon_content:
                continue
            
            # 添加日期
            summary_lines.append(f"{date}：")
            
            # 添加上午内容
            if morning_content:
                summary_lines.append(f"\n{morning_content}")
            
            # 添加下午内容
            if afternoon_content:
                summary_lines.append(f"\n{afternoon_content}")
            
            # 添加空行分隔
            summary_lines.append("")
        
        # 移除最后一个空行
        if summary_lines and summary_lines[-1] == "":
            summary_lines.pop()
        
        summary = "\n".join(summary_lines)
        
        # 检查是否已存在汇总
        cursor.execute(
            "SELECT id FROM week_summaries WHERE week_end_date = ?",
            (week_end_date,)
        )
        existing = cursor.fetchone()
        
        if existing:
            # 更新
            cursor.execute(
                """
                UPDATE week_summaries 
                SET summary_content = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE week_end_date = ?
                """,
                (summary, week_end_date)
            )
            summary_id = existing["id"]
        else:
            # 创建
            cursor.execute(
                """
                INSERT INTO week_summaries (week_end_date, summary_content) 
                VALUES (?, ?)
                """,
                (week_end_date, summary)
            )
            summary_id = cursor.lastrowid
        
        conn.commit()
        
        # 返回创建/更新的汇总
        cursor.execute("SELECT * FROM week_summaries WHERE id = ?", (summary_id,))
        result = cursor.fetchone()
        return dict(result)
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5035)
