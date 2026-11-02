<template>
  <div class="calendar-container">
    <!-- 年月切换栏 -->
    <div class="calendar-header">
      <button @click="changeMonth(-1)" class="nav-btn">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>
      <h2 class="header-title">
        <span class="year">{{ currentYear }}</span>
        <span class="divider">·</span>
        <span class="month">{{ currentMonth }}月</span>
      </h2>
      <button @click="changeMonth(1)" class="nav-btn">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </button>
      
      <!-- 导出按钮 -->
      <div class="export-buttons">
        <button @click="exportCurrentMonth" class="export-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          导出当月
        </button>
        <button @click="exportCurrentYear" class="export-btn year">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          导出整年
        </button>
      </div>

      <!-- 设置按钮 + 主题选择 -->
      <div class="settings-wrap">
        <button @click="toggleThemePanel" class="settings-btn" :title="'当前主题：' + themeLabel">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
          </svg>
        </button>
        <!-- 主题选择面板 -->
        <div v-if="showThemePanel" class="theme-panel" @click.stop>
          <div class="theme-panel-title">选择风格</div>
          <button 
            @click="applyTheme('night')" 
            class="theme-option" 
            :class="{ active: currentTheme === 'night' }"
          >
            <span class="theme-dot night"></span>
            <span class="theme-name">星夜</span>
            <span class="theme-desc">深邃静谧</span>
          </button>
          <button 
            @click="applyTheme('sunny')" 
            class="theme-option" 
            :class="{ active: currentTheme === 'sunny' }"
          >
            <span class="theme-dot sunny"></span>
            <span class="theme-name">暖阳</span>
            <span class="theme-desc">明亮清新</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- 周数和年份百分比 -->
    <div class="week-info">
      <div v-for="(week, index) in calendarWeeks" :key="index" class="week-row">
        <div class="week-number">
          <div class="week-label">第{{ getWeekNumber(week[0]) }}周</div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: getYearPercentage(week[0]) + '%' }"></div>
          </div>
          <span class="year-percentage">{{ getYearPercentage(week[0]) }}%</span>
        </div>
        
        <!-- 日历格子 -->
        <div class="week-days">
          <div 
            v-for="day in week" 
            :key="day.date" 
            class="day-cell"
            :class="{ 
              'other-month': !day.isCurrentMonth, 
              'today': day.isToday,
              'weekend': day.weekday === 0 || day.weekday === 6
            }"
            @click="handleDayClick(day)"
          >
            <div class="day-number">
              <span class="date-num">{{ day.day }}</span>
              <span class="weekday-label">{{ getWeekdayLabel(day.weekday) }}</span>
            </div>
            
            <!-- 统一任务区域（合并展示 morning + afternoon 历史数据） -->
            <div class="tasks-wrapper">
              <div 
                class="task-section" 
                :class="(day.weekday === 0 || day.weekday === 6) ? 'weekend-task' : 'unified'"
              >
                <div v-if="getMergedTaskContent(day.date)" class="task-content">
                  {{ getMergedTaskContent(day.date) }}
                </div>
                <div v-else class="task-placeholder">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                  </svg>
                  {{ day.weekday === 0 ? '添加重点' : '添加任务' }}
                </div>
              </div>
              <!-- 周日汇总按钮 -->
              <div v-if="day.weekday === 0" class="summary-btn" @click.stop="handleSummaryClick(day.date)">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                汇总本周
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 任务编辑弹窗 -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ editDate }} 当日任务</h3>
          <button @click="closeModal" class="close-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body" style="padding:0">
          <div class="modal-task-section">
            <MdEditor 
              v-model="editContent" 
              placeholder="请输入任务内容（支持 Markdown 格式）..."
              language="zh-CN"
              :toolbars="editorToolbars"
              :screenfull="true"
              :style="{ height: '500px' }"
              class="md-editor"
            />
          </div>
        </div>
        
        <div class="modal-actions">
          <button @click="closeModal" class="btn cancel">取消</button>
          <button @click="copyTaskContent" class="btn copy">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            复制
          </button>
          <button @click="saveTask" class="btn save">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
              <polyline points="17 21 17 13 7 13 7 21"></polyline>
              <polyline points="7 3 7 8 15 8"></polyline>
            </svg>
            保存
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- 周汇总弹窗 -->
  <div v-if="showSummaryModal" class="modal-overlay" @click.self="closeSummaryModal">
    <div class="modal-content">
      <div class="modal-header">
        <div style="display: flex; align-items: center; gap: 12px;">
          <button 
            @click="handleRegenerateSummary" 
            class="btn"
            :disabled="isRegenerating"
            style="background: linear-gradient(135deg, var(--color-accent-orange) 0%, #d97706 100%); padding: 8px 16px; font-size: 12px; border-radius: 8px;"
          >
            <svg v-if="isRegenerating" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" stroke-dasharray="30" stroke-dashoffset="10">
                <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
              </circle>
            </svg>
            <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23 4 23 10 17 10"></polyline>
              <polyline points="1 20 1 14 7 14"></polyline>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
            </svg>
            {{ isRegenerating ? '重新汇总中...' : '重新汇总' }}
          </button>
          <h3>{{ summaryDate }} 周汇总</h3>
        </div>
        <button @click="closeSummaryModal" class="close-btn">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      
      <div class="modal-body" style="padding:0">
        <div class="modal-task-section" style="padding:0">
          <MdEditor 
            v-model="summaryContent" 
            placeholder="点击'重新汇总'按钮生成周汇总..."
            language="zh-CN"
            :toolbars="editorToolbars"
            :style="{ height: '500px' }"
            class="md-editor"
          />
        </div>
      </div>
      
      <div class="modal-actions">
        <button @click="closeSummaryModal" class="btn cancel">关闭</button>
        <button @click="copySummaryContent" class="btn copy">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
          </svg>
          复制
        </button>
        <button 
          @click="handleSaveSummary" 
          class="btn"
          :disabled="isSaving"
          style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);"
        >
          <svg v-if="isSaving" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" stroke-dasharray="30" stroke-dashoffset="10">
              <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
            </circle>
          </svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
            <polyline points="17 21 17 13 7 13 7 21"></polyline>
            <polyline points="7 3 7 8 15 8"></polyline>
          </svg>
          {{ isSaving ? '保存中...' : '保存' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { getTasks, createTask, summarizeWeekTasks, getWeekSummary, regenerateWeekSummary, saveWeekSummary } from '../api';
import { MdEditor } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import * as XLSX from 'xlsx';
import MarkdownIt from 'markdown-it';

// Markdown 渲染器（用于把 Markdown 源码渲染为 HTML，便于复制渲染后的内容）
const md = new MarkdownIt({
  html: false,
  breaks: true,
  linkify: true,
});

const getTodayStr = () => new Date().toISOString().split('T')[0];

// 响应式数据
const currentDate = ref(new Date());
const todayStr = ref(getTodayStr());
let todayCheckTimer: number | undefined;
const tasks = ref<any[]>([]);
const showEditModal = ref(false);
const editDate = ref('');
const editContent = ref('');

// 周汇总弹窗
const showSummaryModal = ref(false);
const summaryDate = ref('');
const summaryContent = ref('');
const isRegenerating = ref(false);
const isSaving = ref(false);

// ===== 主题系统 =====
const currentTheme = ref<'night' | 'sunny'>('night');
const showThemePanel = ref(false);
const THEME_LABEL: Record<string, string> = { night: '星夜', sunny: '暖阳' };
const themeLabel = computed(() => THEME_LABEL[currentTheme.value]);

/** 切换主题选择面板显示 */
const toggleThemePanel = () => { showThemePanel.value = !showThemePanel.value; };

/** 应用指定主题：设置 data-theme + 持久化到 localStorage */
const applyTheme = (theme: 'night' | 'sunny') => {
  currentTheme.value = theme;
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('work_calendar_theme', theme);
  showThemePanel.value = false;
};

/** 初始化主题：从 localStorage 读取，或默认星夜 */
const initTheme = () => {
  const saved = localStorage.getItem('work_calendar_theme') as 'night' | 'sunny' | null;
  const theme = saved || 'night';
  currentTheme.value = theme;
  document.documentElement.setAttribute('data-theme', theme);
};

// 点击面板外部关闭
const handlePanelClickOutside = (e: MouseEvent) => {
  const target = e.target as HTMLElement;
  if (!target.closest('.settings-wrap')) {
    showThemePanel.value = false;
  }
};

// Markdown 编辑器工具栏配置
const editorToolbars = [
  'bold',
  'underline',
  'italic',
  '-',
  'title',
  'strikeThrough',
  'sub',
  'sup',
  'quote',
  'unorderedList',
  'orderedList',
  '-',
  'codeRow',
  'code',
  'link',
  'image',
  'table',
  '-',
  'revoke',
  'next',
  '=',
  'pageFullscreen',
  'fullscreen',
  'syncScroll'
];

// 计算当前年月
const currentYear = computed(() => currentDate.value.getFullYear());
const currentMonth = computed(() => currentDate.value.getMonth() + 1);

// 生成日历数据
const calendarWeeks = computed(() => {
  const year = currentYear.value;
  const month = currentMonth.value - 1;
  
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const startDate = new Date(firstDay);
  
  const dayOfWeek = firstDay.getDay();
  const daysToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
  startDate.setDate(startDate.getDate() - daysToMonday);
  
  const weeks: any[][] = [];
  let currentWeek: any[] = [];
  
  for (let i = 0; i < 42; i++) {
    const date = new Date(startDate);
    date.setDate(startDate.getDate() + i);
    
    const year = date.getFullYear();
    const monthStr = String(date.getMonth() + 1).padStart(2, '0');
    const dayStr = String(date.getDate()).padStart(2, '0');
    const localDateStr = `${year}-${monthStr}-${dayStr}`;
    
    const dayInfo = {
      date: localDateStr,
      day: date.getDate(),
      weekday: date.getDay(),
      isCurrentMonth: date.getMonth() === month,
      isToday: localDateStr === todayStr.value
    };
    
    currentWeek.push(dayInfo);
    
    if (currentWeek.length === 7) {
      weeks.push([...currentWeek]);
      currentWeek = [];
    }
  }
  
  return weeks;
});

// 切换月份
const changeMonth = (delta: number) => {
  const newDate = new Date(currentDate.value);
  newDate.setMonth(newDate.getMonth() + delta);
  currentDate.value = newDate;
  fetchTasks();
};

// 获取任务数据
const fetchTasks = async () => {
  try {
    const result = await getTasks();
    tasks.value = result;
  } catch (error) {
    console.error('获取任务失败:', error);
  }
};

// 根据日期和时间段获取任务
const getTaskByDateAndPart = (date: string, part: string) => {
  return tasks.value.find(task => task.date === date && task.part === part);
};

/**
 * 获取某日合并后的完整任务内容
 * 历史数据中可能同时存在 morning 和 afternoon 两条记录，
 * 新设计统一展示，需要将两部分内容拼接在一起
 */
const getMergedTaskContent = (date: string): string => {
  const morning = getTaskByDateAndPart(date, 'morning')?.task_content?.trim() || '';
  const afternoon = getTaskByDateAndPart(date, 'afternoon')?.task_content?.trim() || '';
  if (morning && afternoon) {
    // 若 morning 已包含 afternoon 内容（历史脏数据），避免重复拼接
    if (morning.includes(afternoon)) {
      return morning;
    }
    return morning + '\n\n' + afternoon;
  }
  return morning || afternoon;
};

// 处理日期点击
const handleDayClick = (day: any) => {
  editDate.value = day.date;
  editContent.value = getMergedTaskContent(day.date);
  showEditModal.value = true;
};

// 关闭弹窗
const closeModal = () => {
  showEditModal.value = false;
  editContent.value = '';
};

// 保存任务
const saveTask = async () => {
  try {
    await createTask({
      date: editDate.value,
      part: 'morning',
      task_content: editContent.value,
      task_type: 'completed'
    });
    
    await fetchTasks();
    closeModal();
  } catch (error) {
    console.error('保存任务失败:', error);
  }
};

// 获取星期标签（0=周日, 1=周一 ... 6=周六）
const getWeekdayLabel = (weekday: number): string => {
  const labels = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  return labels[weekday];
};

// 处理汇总点击
const handleSummaryClick = async (date: string) => {
  summaryDate.value = date;
  await loadSummary();
  showSummaryModal.value = true;
};

// 加载周汇总
const loadSummary = async () => {
  try {
    const summary = await getWeekSummary(summaryDate.value);
    summaryContent.value = summary?.summary_content || '';
  } catch (error) {
    console.error('加载汇总失败:', error);
  }
};

// 重新生成周汇总
const handleRegenerateSummary = async () => {
  isRegenerating.value = true;
  try {
    const summary = await regenerateWeekSummary(summaryDate.value);
    summaryContent.value = summary.summary_content || '';
    await fetchTasks();
  } catch (error) {
    console.error('重新生成汇总失败:', error);
    alert('重新生成汇总失败');
  } finally {
    isRegenerating.value = false;
  }
};

// 关闭汇总弹窗
const closeSummaryModal = () => {
  showSummaryModal.value = false;
  summaryContent.value = '';
};

// 保存周汇总
const handleSaveSummary = async () => {
  isSaving.value = true;
  try {
    await saveWeekSummary(summaryDate.value, summaryContent.value);
    alert('周汇总保存成功！');
  } catch (error) {
    console.error('保存汇总失败:', error);
    alert('保存失败');
  } finally {
    isSaving.value = false;
  }
};

// 复制纯文本到剪贴板（降级方案：textarea + execCommand）
const fallbackCopyText = (text: string): boolean => {
  try {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    return true;
  } catch (e) {
    return false;
  }
};

// 将渲染后的 HTML 转为纯文本（保留段落/换行结构）
const htmlToPlainText = (html: string): string => {
  let text = html;
  // 块级结束标签后补换行
  text = text.replace(/<\/(p|div|h[1-6]|li|blockquote|pre|tr|ul|ol|table)>/gi, '\n');
  // <br> 转为换行
  text = text.replace(/<br\s*\/?>/gi, '\n');
  // 去除其余标签
  text = text.replace(/<[^>]+>/g, '');
  // 解码常见 HTML 实体
  text = text
    .replace(/&nbsp;/g, ' ')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
  // 合并多余空行并去除首尾空白
  return text.replace(/\n{3,}/g, '\n\n').trim();
};

// 复制渲染后的内容（优先富文本 HTML + 纯文本，降级仅纯文本）
const copyRenderedContent = async (markdown: string): Promise<boolean> => {
  const html = md.render(markdown);
  const plainText = htmlToPlainText(html);

  // 优先：写入 HTML 富文本 + 纯文本（粘贴到富文本环境保留格式）
  if (navigator.clipboard && window.isSecureContext && typeof ClipboardItem !== 'undefined') {
    try {
      await navigator.clipboard.write([
        new ClipboardItem({
          'text/html': new Blob([html], { type: 'text/html' }),
          'text/plain': new Blob([plainText], { type: 'text/plain' }),
        }),
      ]);
      return true;
    } catch (e) {
      // 继续走降级方案
    }
  }
  // 降级：仅复制纯文本
  return fallbackCopyText(plainText);
};

// 复制任务内容（渲染后的格式）
const copyTaskContent = async () => {
  if (!editContent.value.trim()) {
    alert('当前没有可复制的内容');
    return;
  }
  const ok = await copyRenderedContent(editContent.value);
  alert(ok ? '复制成功' : '复制失败');
};

// 复制周汇总内容（渲染后的格式）
const copySummaryContent = async () => {
  if (!summaryContent.value.trim()) {
    alert('当前没有可复制的内容');
    return;
  }
  const ok = await copyRenderedContent(summaryContent.value);
  alert(ok ? '复制成功' : '复制失败');
};

// 获取周数
const getWeekNumber = (day: any) => {
  const date = new Date(day.date);
  const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
  const pastDaysOfYear = (date.getTime() - firstDayOfYear.getTime()) / 86400000;
  return Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7);
};

// 获取年份百分比
const getYearPercentage = (day: any) => {
  const date = new Date(day.date);
  const startOfYear = new Date(date.getFullYear(), 0, 1);
  const endOfYear = new Date(date.getFullYear(), 11, 31);
  const totalDays = (endOfYear.getTime() - startOfYear.getTime()) / 86400000;
  const pastDays = (date.getTime() - startOfYear.getTime()) / 86400000;
  return Math.round((pastDays / totalDays) * 100);
};

// 组件挂载时获取任务数据
onMounted(() => {
  initTheme();
  fetchTasks();
  setTimeout(() => {
    scrollToToday();
  }, 100);

  // 点击面板外部关闭
  document.addEventListener('click', handlePanelClickOutside);

  todayCheckTimer = window.setInterval(() => {
    const now = new Date();
    const nowStr = now.toISOString().split('T')[0];
    if (nowStr === todayStr.value) return;

    todayStr.value = nowStr;

    if (showEditModal.value || showSummaryModal.value) return;

    if (currentYear.value !== now.getFullYear() || currentMonth.value !== now.getMonth() + 1) return;

    currentDate.value = now;
    fetchTasks();
    setTimeout(() => {
      scrollToToday();
    }, 100);
  }, 60000);
});

onBeforeUnmount(() => {
  if (todayCheckTimer !== undefined) {
    clearInterval(todayCheckTimer);
  }
  document.removeEventListener('click', handlePanelClickOutside);
});

// 滚动到当日日期
const scrollToToday = () => {
  const todayElement = document.querySelector('.today');
  if (todayElement) {
    todayElement.scrollIntoView({
      behavior: 'smooth',
      block: 'center'
    });
  }
};

// 导出当月数据到Excel
const exportCurrentMonth = () => {
  const year = currentYear.value;
  const month = currentMonth.value;
  exportMonthData(year, month);
};

// 导出整年数据到Excel
const exportCurrentYear = () => {
  const year = currentYear.value;
  for (let month = 1; month <= 12; month++) {
    exportMonthData(year, month);
  }
};

// 导出指定月份的数据
const exportMonthData = (year: number, month: number) => {
  const weeks = generateMonthWeeks(year, month);
  const worksheetData: any[][] = [];
  
  // 添加表头
  worksheetData.push(['周进度', '周一', '周二', '周三', '周四', '周五', '周六', '周日']);
  
  // 添加每周数据
  weeks.forEach(week => {
    const weekNum = getWeekNumberForDate(new Date(week[0].date));
    const yearPercent = getYearPercentage(week[0]);
    const rowData = [`第${weekNum}周 (${yearPercent}%)`];
    
    week.forEach(day => {
      const merged = getMergedTaskContent(day.date);
      
      let cellContent = '';
      if (merged) {
        cellContent = `${day.date}\n${merged}`;
      } else {
        cellContent = day.date;
      }
      rowData.push(cellContent);
    });
    
    worksheetData.push(rowData);
  });
  
  // 创建工作簿
  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.aoa_to_sheet(worksheetData);
  
  // 设置列宽
  ws['!cols'] = [
    { wch: 15 },
    { wch: 30 },
    { wch: 30 },
    { wch: 30 },
    { wch: 30 },
    { wch: 30 },
    { wch: 30 },
    { wch: 30 }
  ];
  
  // 添加工作表
  XLSX.utils.book_append_sheet(wb, ws, `${year}年${month}月`);
  
  // 导出文件
  XLSX.writeFile(wb, `工作日历_${year}年${month}月.xlsx`);
};

// 生成指定月份的周数据
const generateMonthWeeks = (year: number, month: number) => {
  const firstDay = new Date(year, month - 1, 1);
  const lastDay = new Date(year, month, 0);
  const startDate = new Date(firstDay);
  
  const dayOfWeek = firstDay.getDay();
  const daysToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
  startDate.setDate(startDate.getDate() - daysToMonday);
  
  const weeks: any[][] = [];
  let currentWeek: any[] = [];
  
  for (let i = 0; i < 42; i++) {
    const date = new Date(startDate);
    date.setDate(startDate.getDate() + i);
    
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const d = String(date.getDate()).padStart(2, '0');
    const localDateStr = `${y}-${m}-${d}`;
    
    const dayInfo = {
      date: localDateStr,
      day: date.getDate(),
      weekday: date.getDay(),
      isCurrentMonth: date.getMonth() === month - 1,
      isToday: localDateStr === todayStr.value
    };
    
    currentWeek.push(dayInfo);
    
    if (currentWeek.length === 7) {
      weeks.push([...currentWeek]);
      currentWeek = [];
    }
  }
  
  return weeks;
};

// 根据日期获取周数
const getWeekNumberForDate = (date: Date) => {
  const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
  const pastDaysOfYear = (date.getTime() - firstDayOfYear.getTime()) / 86400000;
  return Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7);
};
</script>

<style scoped>
.calendar-container {
  width: 100%;
  margin: 0 auto;
  padding: 0;
  font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
  position: relative;
  z-index: 1;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px 30px;
  background: var(--color-bg-header);
  border: 1px solid var(--color-border-header);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05);
  position: relative;
  z-index: 20;
  overflow: visible;
}

.nav-btn {
  background: linear-gradient(135deg, rgba(var(--color-cyan-rgb), 0.15) 0%, rgba(var(--color-purple-rgb), 0.15) 100%);
  border: 1px solid rgba(var(--color-cyan-rgb), 0.3);
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  color: var(--color-accent-cyan);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-btn:hover {
  background: linear-gradient(135deg, rgba(var(--color-cyan-rgb), 0.3) 0%, rgba(var(--color-purple-rgb), 0.3) 100%);
  border-color: rgba(var(--color-cyan-rgb), 0.6);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(var(--color-cyan-rgb), 0.3);
}

.nav-btn:active {
  transform: translateY(0);
}

.export-buttons {
  display: flex;
  gap: 12px;
  margin-left: 20px;
}

.export-btn {
  background: linear-gradient(135deg, rgba(var(--color-green-rgb), 0.15) 0%, rgba(16, 185, 129, 0.15) 100%);
  border: 1px solid rgba(var(--color-green-rgb), 0.3);
  padding: 10px 18px;
  border-radius: 10px;
  cursor: pointer;
  color: var(--color-accent-green);
  font-size: 13px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 8px;
}

.export-btn:hover {
  background: linear-gradient(135deg, rgba(var(--color-green-rgb), 0.3) 0%, rgba(16, 185, 129, 0.3) 100%);
  border-color: rgba(var(--color-green-rgb), 0.6);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(var(--color-green-rgb), 0.3);
}

.export-btn.year {
  background: linear-gradient(135deg, rgba(var(--color-orange-rgb), 0.15) 0%, rgba(234, 179, 8, 0.15) 100%);
  border: 1px solid rgba(var(--color-orange-rgb), 0.3);
  color: var(--color-accent-orange);
}

.export-btn.year:hover {
  background: linear-gradient(135deg, rgba(var(--color-orange-rgb), 0.3) 0%, rgba(234, 179, 8, 0.3) 100%);
  border-color: rgba(var(--color-orange-rgb), 0.6);
  box-shadow: 0 8px 24px rgba(var(--color-orange-rgb), 0.3);
}

.header-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: 2px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-title .year {
  color: var(--color-accent-cyan);
  text-shadow: 0 0 20px rgba(var(--color-cyan-rgb), 0.5);
}

.header-title .divider {
  color: var(--color-text-muted);
  font-weight: 300;
}

.header-title .month {
  color: var(--color-accent-purple);
  text-shadow: 0 0 20px rgba(var(--color-purple-rgb), 0.5);
}

.week-header {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.week-number-header {
  width: 80px;
  flex-shrink: 0;
  padding: 12px 8px;
  background: linear-gradient(135deg, rgba(var(--color-cyan-rgb), 0.1) 0%, rgba(var(--color-purple-rgb), 0.1) 100%);
  border: 1px solid rgba(var(--color-cyan-rgb), 0.2);
  border-radius: 12px;
  text-align: center;
  font-weight: 600;
  font-size: 13px;
  color: var(--color-accent-cyan);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.week-number-header .mini {
  font-size: 11px;
  color: rgba(var(--color-cyan-rgb), 0.6);
  font-weight: 400;
}

.week-days-header {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  padding-left: 8px;
  min-width: 0;
}

.week-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.week-row {
  display: flex;
  align-items: stretch;
}

.week-number {
  width: 80px;
  flex-shrink: 0;
  padding: 12px 8px;
  background: var(--color-bg-task-section);
  border: 1px solid var(--color-border-cell);
  border-radius: 12px;
  text-align: center;
  font-weight: 600;
  color: var(--color-text-primary);
  display: flex;
  flex-direction: column;
  gap: 8px;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.week-label {
  font-size: 13px;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-accent-cyan) 0%, var(--color-accent-purple) 100%);
  border-radius: 2px;
  transition: width 0.5s ease;
}

.year-percentage {
  font-size: 12px;
  color: var(--color-accent-cyan);
  font-weight: 500;
}

.week-days {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  padding-left: 8px;
  min-width: 0;
}

.day-cell {
  background: var(--color-bg-cell);
  border: 1px solid var(--color-border-cell);
  border-radius: 16px;
  padding: 12px;
  min-height: 320px;
  max-height: 400px;
  position: relative;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.day-cell::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent 0%, rgba(var(--color-cyan-rgb), 0.5) 50%, transparent 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.day-cell:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(var(--color-cyan-rgb), 0.2), 0 8px 24px rgba(0, 0, 0, 0.4);
  border-color: rgba(var(--color-cyan-rgb), 0.4);
}

.day-cell:hover::before {
  opacity: 1;
}

.other-month {
  background: var(--color-bg-other-month);
  border-color: var(--color-border-other-month);
  opacity: var(--color-opacity-other-month);
}

.other-month .day-number {
  opacity: 0.6;
}

.other-month .task-section {
  opacity: 0.5;
}

.other-month .task-placeholder {
  opacity: 0.4;
}

.other-month:hover {
  opacity: 0.7;
}

.today {
  background: var(--color-bg-today);
  border: 2px solid var(--color-border-today);
  box-shadow: 0 0 30px rgba(var(--color-cyan-rgb), 0.3), inset 0 0 20px rgba(var(--color-cyan-rgb), 0.08);
}

.today::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(var(--color-cyan-rgb), 0.1) 0%, transparent 60%);
  animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.5;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
}

.weekend {
  border-color: var(--color-border-weekend);
  background: var(--color-bg-weekend);
}

.weekend .weekday-label {
  color: var(--color-text-weekend);
  font-weight: 600;
}

.day-number {
  font-weight: 700;
  margin-bottom: 16px;
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 1;
}

.date-num {
  font-size: 20px;
  color: var(--color-text-primary);
}

.weekday-label {
  font-size: 11px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.today .day-number {
  background: linear-gradient(135deg, var(--color-accent-cyan) 0%, var(--color-accent-purple) 100%);
  color: white;
  padding: 8px 14px;
  border-radius: 24px;
  margin-bottom: 16px;
  box-shadow: 0 4px 16px rgba(var(--color-cyan-rgb), 0.4);
}

.task-section {
  margin-bottom: 10px;
  padding: 14px;
  border-radius: 12px;
  position: relative;
  z-index: 1;
  max-height: 250px;
  overflow-y: auto;
  flex-shrink: 0;
}

.tasks-wrapper {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
}

.tasks-wrapper::-webkit-scrollbar {
  width: 4px;
}

.tasks-wrapper::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 2px;
}

.tasks-wrapper::-webkit-scrollbar-thumb {
  background: rgba(var(--color-cyan-rgb), 0.3);
  border-radius: 2px;
}

.tasks-wrapper::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--color-cyan-rgb), 0.5);
}

.task-section::-webkit-scrollbar {
  width: 4px;
}

.task-section::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 2px;
}

.task-section::-webkit-scrollbar-thumb {
  background: rgba(var(--color-cyan-rgb), 0.3);
  border-radius: 2px;
}

.task-section::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--color-cyan-rgb), 0.5);
}

.weekend-task {
  background: var(--color-bg-weekend-task);
  border: 1px solid var(--color-border-weekend-task);
}

.task-content {
  font-size: 13px;
  line-height: 1.6;
  text-align: left;
  color: var(--color-text-primary);
  word-break: break-word;
  white-space: pre-wrap;
}

.task-placeholder {
  font-size: 12px;
  color: var(--color-text-muted);
  font-style: normal;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 6px;
}

.summary-btn {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: linear-gradient(135deg, var(--color-accent-orange) 0%, #d97706 100%);
  color: white;
  padding: 8px 14px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  z-index: 2;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(var(--color-orange-rgb), 0.3);
}

.summary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(var(--color-orange-rgb), 0.4);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: var(--color-bg-modal);
  border: 1px solid var(--color-border-modal);
  padding: 0;
  border-radius: 20px;
  width: 90%;
  max-width: 900px;
  max-height: 85vh;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.5), 0 0 60px rgba(var(--color-cyan-rgb), 0.1);
  overflow: hidden;
  animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 11px 14px;
  border-bottom: 1px solid rgba(var(--color-cyan-rgb), 0.15);
  background: linear-gradient(135deg, rgba(var(--color-cyan-rgb), 0.05) 0%, rgba(var(--color-purple-rgb), 0.05) 100%);
  flex-shrink: 0;
}

.modal-header h3 {
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
}

.close-btn {
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--color-text-primary);
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.modal-task-section {
  margin-bottom: 0;
}

.modal-task-section:last-child {
  margin-bottom: 0;
}

.modal-task-section h4 {
  margin-bottom: 16px;
  color: var(--color-text-primary);
  font-size: 15px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 12px;
}

.tag {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
}

.tag.am {
  background: rgba(var(--color-purple-rgb), 0.2);
  color: var(--color-accent-purple);
  border: 1px solid rgba(var(--color-purple-rgb), 0.3);
}

.tag.pm {
  background: rgba(var(--color-cyan-rgb), 0.2);
  color: var(--color-accent-cyan);
  border: 1px solid rgba(var(--color-cyan-rgb), 0.3);
}

.md-editor {
  width: 100%;
  height: 200px;
  border: 1px solid rgba(var(--color-cyan-rgb), 0.2);
  border-radius: 12px;
  overflow: hidden;
  background: rgba(10, 14, 39, 0.6);
}

.md-editor-morning {
  border: 1px solid rgba(var(--color-purple-rgb), 0.4);
  background: linear-gradient(135deg, rgba(var(--color-purple-rgb), 0.1) 0%, rgba(var(--color-purple-rgb), 0.05) 100%);
}

.md-editor-morning :deep(.md-editor-toolbar-wrapper) {
  background: rgba(var(--color-purple-rgb), 0.15);
  border-bottom: 1px solid rgba(var(--color-purple-rgb), 0.2);
}

.md-editor-afternoon {
  border: 1px solid rgba(var(--color-cyan-rgb), 0.4);
  background: linear-gradient(135deg, rgba(var(--color-cyan-rgb), 0.1) 0%, rgba(var(--color-cyan-rgb), 0.05) 100%);
}

.md-editor-afternoon :deep(.md-editor-toolbar-wrapper) {
  background: rgba(var(--color-cyan-rgb), 0.15);
  border-bottom: 1px solid rgba(var(--color-cyan-rgb), 0.2);
}

.md-editor :deep(.md-editor-toolbar-wrapper) {
  background: rgba(26, 31, 58, 0.8);
  border-bottom: 1px solid rgba(var(--color-cyan-rgb), 0.15);
}

.md-editor :deep(.md-editor-toolbar) {
  background: transparent;
}

.md-editor :deep(.md-editor-content) {
  background: rgba(10, 14, 39, 0.4);
  height: calc(100% - 42px);
}

.md-editor :deep(.md-editor-input-wrapper) {
  height: 100%;
}

.md-editor :deep(.md-editor-preview-wrapper) {
  height: 100%;
  overflow-y: auto;
  background: rgba(20, 25, 50, 0.5);
}

.md-editor :deep(.md-editor-preview) {
  padding: 12px;
  height: 100%;
  overflow-y: auto;
  background: transparent;
  color: rgba(255, 255, 255, 0.95);
}

.md-editor :deep(.md-editor-preview h1),
.md-editor :deep(.md-editor-preview h2),
.md-editor :deep(.md-editor-preview h3),
.md-editor :deep(.md-editor-preview h4),
.md-editor :deep(.md-editor-preview h5),
.md-editor :deep(.md-editor-preview h6) {
  color: var(--color-accent-cyan);
  border-bottom: 1px solid rgba(var(--color-cyan-rgb), 0.2);
}

.md-editor :deep(.md-editor-preview code) {
  background: rgba(var(--color-cyan-rgb), 0.1);
  color: var(--color-accent-pink);
  padding: 2px 6px;
  border-radius: 4px;
}

.md-editor :deep(.md-editor-preview pre) {
  background: rgba(0, 0, 0, 0.3);
  padding: 12px;
  border-radius: 8px;
}

.md-editor :deep(.md-editor-preview pre code) {
  background: transparent;
  color: rgba(255, 255, 255, 0.9);
}

.md-editor :deep(.md-editor-preview blockquote) {
  border-left: 4px solid var(--color-accent-cyan);
  background: rgba(var(--color-cyan-rgb), 0.05);
  padding: 8px 12px;
  margin: 8px 0;
  color: rgba(255, 255, 255, 0.85);
}

.md-editor :deep(.md-editor-preview a) {
  color: var(--color-accent-cyan);
}

.md-editor :deep(.md-editor-preview ul),
.md-editor :deep(.md-editor-preview ol) {
  color: rgba(255, 255, 255, 0.9);
}

.md-editor :deep(.md-editor-preview table) {
  border-color: rgba(var(--color-cyan-rgb), 0.3);
}

.md-editor :deep(.md-editor-preview th) {
  background: rgba(var(--color-cyan-rgb), 0.1);
  color: var(--color-accent-cyan);
}

.md-editor :deep(.md-editor-preview td) {
  border-color: rgba(var(--color-cyan-rgb), 0.2);
}

.md-editor :deep(.md-editor-input) {
  background: transparent;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  line-height: 1.6;
  padding: 12px;
}

.md-editor :deep(.md-editor-input::placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

.md-editor :deep(.md-editor-toolbar-item) {
  color: rgba(255, 255, 255, 0.85);
}

.md-editor :deep(.md-editor-toolbar-item:hover) {
  color: var(--color-accent-cyan);
  background: rgba(var(--color-cyan-rgb), 0.1);
}

.md-editor :deep(.md-editor-fullscreen .md-editor-toolbar-item),
.md-editor :deep(.md-editor-pagefullscreen .md-editor-toolbar-item) {
  color: rgba(0, 0, 0, 0.85) !important;
}

.md-editor :deep(.md-editor-fullscreen .md-editor-toolbar-item:hover),
.md-editor :deep(.md-editor-pagefullscreen .md-editor-toolbar-item:hover) {
  color: var(--color-accent-cyan) !important;
  background: rgba(var(--color-cyan-rgb), 0.15) !important;
}

.md-editor :deep(.md-editor-footer) {
  background: rgba(35, 40, 70, 0.98);
  border-top: 1px solid rgba(var(--color-cyan-rgb), 0.3);
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
}

.md-editor :deep(.md-editor-footer-item) {
  color: rgba(207, 134, 104, 0.95);
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 500;
}

.md-editor :deep(.md-editor-footer-item input[type="checkbox"]) {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: var(--color-accent-cyan);
  background-color: rgba(0, 0, 0, 0.5);
  border: 2px solid rgba(var(--color-cyan-rgb), 0.5);
  border-radius: 4px;
}

.md-editor :deep(.md-editor-footer-item input[type="checkbox"]:checked) {
  accent-color: var(--color-accent-cyan);
  background-color: var(--color-accent-cyan);
  border-color: var(--color-accent-cyan);
  box-shadow: 0 0 12px rgba(var(--color-cyan-rgb), 0.7), inset 0 0 0 2px white;
}

.md-editor :deep(.md-editor-footer-item strong) {
  color: var(--color-accent-cyan);
  font-weight: 700;
}

.md-editor :deep(.md-editor-input-wrapper::-webkit-scrollbar) {
  width: 6px;
}

.md-editor :deep(.md-editor-input-wrapper::-webkit-scrollbar-track) {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
}

.md-editor :deep(.md-editor-input-wrapper::-webkit-scrollbar-thumb) {
  background: rgba(var(--color-cyan-rgb), 0.4);
  border-radius: 3px;
}

.md-editor :deep(.md-editor-input-wrapper::-webkit-scrollbar-thumb:hover) {
  background: rgba(var(--color-cyan-rgb), 0.6);
}

.md-editor :deep(.md-editor-preview-wrapper::-webkit-scrollbar) {
  width: 6px;
}

.md-editor :deep(.md-editor-preview-wrapper::-webkit-scrollbar-track) {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
}

.md-editor :deep(.md-editor-preview-wrapper::-webkit-scrollbar-thumb) {
  background: rgba(var(--color-cyan-rgb), 0.4);
  border-radius: 3px;
}

.md-editor :deep(.md-editor-preview-wrapper::-webkit-scrollbar-thumb:hover) {
  background: rgba(var(--color-cyan-rgb), 0.6);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 10px 14px;
  border-top: 1px solid rgba(var(--color-cyan-rgb), 0.15);
  flex-shrink: 0;
}

.btn {
  padding: 7px 15px;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
}

.btn.cancel {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.btn.cancel:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
}

.btn.copy {
  background: rgba(var(--color-cyan-rgb), 0.12);
  color: var(--color-accent-cyan);
  border: 1px solid rgba(var(--color-cyan-rgb), 0.3);
}

.btn.copy:hover {
  background: rgba(var(--color-cyan-rgb), 0.22);
}

.btn.save {
  background: linear-gradient(135deg, var(--color-accent-cyan) 0%, var(--color-accent-purple) 100%);
  color: white;
  box-shadow: 0 4px 16px rgba(var(--color-cyan-rgb), 0.3);
}

.btn.save:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(var(--color-cyan-rgb), 0.4);
}

.btn.save:active {
  transform: translateY(0);
}

/* ===== 设置按钮 + 主题面板 ===== */
.settings-wrap {
  position: relative;
  margin-left: 20px;
}

.settings-btn {
  background: var(--color-nav-btn-bg);
  border: 1px solid var(--color-nav-btn-border);
  padding: 10px 12px;
  border-radius: 10px;
  cursor: pointer;
  color: var(--color-accent-cyan);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.settings-btn:hover {
  transform: rotate(45deg);
  border-color: var(--color-accent-cyan);
  box-shadow: 0 4px 16px rgba(var(--color-cyan-rgb), 0.2);
}

.theme-panel {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  width: 220px;
  background: var(--color-bg-modal);
  border: 1px solid var(--color-border-modal);
  border-radius: 14px;
  padding: 8px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
  z-index: 500;
  animation: themePanelIn 0.2s ease;
}

@keyframes themePanelIn {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

.theme-panel-title {
  font-size: 12px;
  color: var(--color-text-secondary);
  font-weight: 600;
  letter-spacing: 1px;
  padding: 8px 10px 6px;
  text-align: center;
}

.theme-option {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border: 1px solid transparent;
  border-radius: 10px;
  background: transparent;
  cursor: pointer;
  color: var(--color-text-primary);
  transition: all 0.25s ease;
}

.theme-option:hover {
  background: rgba(var(--color-cyan-rgb), 0.08);
}

.theme-option.active {
  background: rgba(var(--color-cyan-rgb), 0.12);
  border-color: rgba(var(--color-cyan-rgb), 0.4);
}

.theme-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 0 2px rgba(var(--color-cyan-rgb), 0.2);
}

.theme-dot.night {
  background: linear-gradient(135deg, #0a0e27 0%, #00d4ff 50%, #8b5cf6 100%);
}

.theme-dot.sunny {
  background: linear-gradient(135deg, #f5f7fa 0%, #3b82f6 50%, #f59e0b 100%);
}

.theme-name {
  font-size: 14px;
  font-weight: 600;
  flex: 1;
  text-align: left;
}

.theme-desc {
  font-size: 11px;
  color: var(--color-text-muted);
}

/* ===== 暖阳主题：Markdown 编辑器浅色适配 ===== */
[data-theme="sunny"] .md-editor {
  background: #ffffff;
  border-color: rgba(59, 130, 246, 0.15);
}

[data-theme="sunny"] .md-editor :deep(.md-editor-toolbar-wrapper) {
  background: #f8fafc;
  border-bottom: 1px solid rgba(59, 130, 246, 0.12);
}

[data-theme="sunny"] .md-editor :deep(.md-editor-content) {
  background: #ffffff;
}

[data-theme="sunny"] .md-editor :deep(.md-editor-preview-wrapper) {
  background: #fafbfc;
}

[data-theme="sunny"] .md-editor :deep(.md-editor-preview) {
  color: #1f2937;
}

[data-theme="sunny"] .md-editor :deep(.md-editor-preview pre) {
  background: #f3f4f6;
}

[data-theme="sunny"] .md-editor :deep(.md-editor-preview pre code) {
  color: #1f2937;
}

[data-theme="sunny"] .md-editor :deep(.md-editor-preview blockquote) {
  background: rgba(59, 130, 246, 0.04);
  color: #4b5563;
}

[data-theme="sunny"] .md-editor :deep(.md-editor-preview ul),
[data-theme="sunny"] .md-editor :deep(.md-editor-preview ol) {
  color: #1f2937;
}

[data-theme="sunny"] .md-editor :deep(.md-editor-input) {
  color: #1f2937;
}

[data-theme="sunny"] .md-editor :deep(.md-editor-input::placeholder) {
  color: #9ca3af;
}

[data-theme="sunny"] .md-editor :deep(.md-editor-toolbar-item) {
  color: #4b5563;
}

[data-theme="sunny"] .md-editor :deep(.md-editor-toolbar-item:hover) {
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.08);
}

[data-theme="sunny"] .md-editor :deep(.md-editor-footer) {
  background: #f8fafc;
  border-top: 1px solid rgba(59, 130, 246, 0.12);
}

[data-theme="sunny"] .md-editor :deep(.md-editor-footer-item) {
  color: #6b7280;
}

[data-theme="sunny"] .md-editor :deep(.md-editor-input-wrapper::-webkit-scrollbar-track),
[data-theme="sunny"] .md-editor :deep(.md-editor-preview-wrapper::-webkit-scrollbar-track) {
  background: #f1f5f9;
}

/* ===== 暖阳主题：卡片浮起阴影（增强层次感） ===== */
[data-theme="sunny"] .calendar-header {
  box-shadow: 0 4px 20px rgba(31, 41, 55, 0.08);
}

[data-theme="sunny"] .day-cell {
  box-shadow: 0 2px 10px rgba(31, 41, 55, 0.06);
}

[data-theme="sunny"] .day-cell:hover {
  box-shadow: 0 10px 28px rgba(31, 41, 55, 0.12);
}

[data-theme="sunny"] .week-number {
  box-shadow: 0 2px 8px rgba(31, 41, 55, 0.05);
}

[data-theme="sunny"] .modal-content {
  box-shadow: 0 24px 64px rgba(31, 41, 55, 0.18);
}
</style>


