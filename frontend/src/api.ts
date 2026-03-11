/**
 * API服务
 * 与后端API的交互功能
 */

import config from './config';

// API基础URL - 使用环境配置
const API_BASE_URL = config.apiBaseUrl;

// 任务类型定义
export interface Task {
  id: number;
  date: string;
  part: string;
  task_content: string;
  task_type: string;
  created_at: string;
  updated_at: string;
}

// 周汇总类型定义
export interface WeekSummary {
  id: number;
  week_end_date: string;
  summary_content: string;
  created_at: string;
  updated_at: string;
}

// 创建任务请求参数
export interface TaskCreate {
  date: string;
  part: string;
  task_content: string;
  task_type: string;
}

/**
 * 获取所有任务
 * @returns 任务列表
 */
export async function getTasks(): Promise<Task[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/tasks`);
    if (!response.ok) {
      throw new Error('获取任务失败');
    }
    return await response.json();
  } catch (error) {
    console.error('获取任务失败:', error);
    return [];
  }
}

/**
 * 按日期获取任务
 * @param date 日期，格式：YYYY-MM-DD
 * @returns 任务列表
 */
export async function getTasksByDate(date: string): Promise<Task[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/tasks/${date}`);
    if (!response.ok) {
      throw new Error('获取任务失败');
    }
    return await response.json();
  } catch (error) {
    console.error('获取任务失败:', error);
    return [];
  }
}

/**
 * 创建或更新任务
 * @param task 任务数据
 * @returns 创建或更新的任务
 */
export async function createTask(task: TaskCreate): Promise<Task> {
  try {
    const response = await fetch(`${API_BASE_URL}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(task)
    });
    if (!response.ok) {
      throw new Error('创建任务失败');
    }
    return await response.json();
  } catch (error) {
    console.error('创建任务失败:', error);
    throw error;
  }
}

/**
 * 汇总本周任务到周日
 * @param weekEndDate 周日的日期，格式：YYYY-MM-DD
 * @returns 汇总结果
 */
export async function summarizeWeekTasks(weekEndDate: string): Promise<{ message: string; summary: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/tasks/summary/${weekEndDate}`, {
      method: 'POST'
    });
    if (!response.ok) {
      throw new Error('汇总任务失败');
    }
    return await response.json();
  } catch (error) {
    console.error('汇总任务失败:', error);
    throw error;
  }
}

/**
 * 获取周汇总
 * @param weekEndDate 周日的日期，格式：YYYY-MM-DD
 * @returns 周汇总数据
 */
export async function getWeekSummary(weekEndDate: string): Promise<WeekSummary | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/week-summaries/${weekEndDate}`);
    if (!response.ok) {
      throw new Error('获取周汇总失败');
    }
    const data = await response.json();
    return data || null;
  } catch (error) {
    console.error('获取周汇总失败:', error);
    return null;
  }
}

/**
 * 重新生成本周汇总
 * @param weekEndDate 周日的日期，格式：YYYY-MM-DD
 * @returns 周汇总数据
 */
export async function regenerateWeekSummary(weekEndDate: string): Promise<WeekSummary> {
  try {
    const response = await fetch(`${API_BASE_URL}/week-summaries/regenerate/${weekEndDate}`, {
      method: 'POST'
    });
    if (!response.ok) {
      throw new Error('重新生成汇总失败');
    }
    return await response.json();
  } catch (error) {
    console.error('重新生成汇总失败:', error);
    throw error;
  }
}

/**
 * 保存周汇总
 * @param weekEndDate 周日的日期，格式：YYYY-MM-DD
 * @param summaryContent 汇总内容
 * @returns 周汇总数据
 */
export async function saveWeekSummary(weekEndDate: string, summaryContent: string): Promise<WeekSummary> {
  try {
    const response = await fetch(`${API_BASE_URL}/week-summaries`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        week_end_date: weekEndDate,
        summary_content: summaryContent
      })
    });
    if (!response.ok) {
      throw new Error('保存汇总失败');
    }
    return await response.json();
  } catch (error) {
    console.error('保存汇总失败:', error);
    throw error;
  }
}
