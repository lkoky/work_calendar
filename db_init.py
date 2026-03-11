#!/usr/bin/env python3
"""
数据库初始化脚本
用于执行init.sql建表脚本，初始化数据库结构
"""

import sqlite3
import os

def init_database():
    """
    初始化数据库，执行建表脚本
    """
    # 数据库文件路径
    db_path = os.path.join(os.path.dirname(__file__), 'work_calendar.db')
    
    # 读取init.sql脚本内容
    with open('init.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 执行SQL脚本
        cursor.executescript(sql_script)
        
        # 提交事务
        conn.commit()
        
        print("数据库初始化成功！")
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
    finally:
        # 关闭连接
        if conn:
            conn.close()

if __name__ == "__main__":
    init_database()
