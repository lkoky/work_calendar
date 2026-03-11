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
    </div>
    
    <!-- 周标题 -->
    <div class="week-header">
      <div class="week-number-header">
        <span>周</span>
        <span class="mini">进度</span>
      </div>
      <div class="week-days-header">
        <div class="day-header">周一</div>
        <div class="day-header">周二</div>
        <div class="day-header">周三</div>
        <div class="day-header">周四</div>
        <div class="day-header">周五</div>
        <div class="day-header weekend">周六</div>
        <div class="day-header weekend">周日</div>
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
              'sunday': day.weekday === 0
            }"
            @click="handleDayClick(day)"
          >
            <div class="day-number">
              <span class="date-num">{{ day.day }}</span>
              <span class="lunar-date">{{ day.lunarDate }}</span>
            </div>
            
            <!-- 周日不区分上午下午，只显示一个任务区域 -->
            <div class="tasks-wrapper">
              <template v-if="day.weekday === 0">
                <div class="task-section sunday-task" style='height:240px'>
                  <div v-if="getTaskByDateAndPart(day.date, 'morning')" class="task-content">
                    {{ getTaskByDateAndPart(day.date, 'morning').task_content }}
                  </div>
                  <div v-else class="task-placeholder">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="12" y1="8" x2="12" y2="12"></line>
                      <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    点击添加汇总任务
                  </div>
                </div>
                <!-- 周日汇总按钮 -->
                <div class="summary-btn" @click.stop="handleSummaryClick(day.date)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                  </svg>
                  汇总本周
                </div>
              </template>
              
              <!-- 非周日区分上午下午 -->
              <template v-else>
                <!-- 上午任务 -->
                <div class="task-section morning">
                  <div class="section-label">AM</div>
                  <div v-if="getTaskByDateAndPart(day.date, 'morning')" class="task-content">
                    {{ getTaskByDateAndPart(day.date, 'morning').task_content }}
                  </div>
                  <div v-else class="task-placeholder">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="12" y1="8" x2="12" y2="12"></line>
                      <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    点击添加
                  </div>
                </div>
                
                <!-- 下午任务 -->
                <div class="task-section afternoon">
                  <div class="section-label">PM</div>
                  <div v-if="getTaskByDateAndPart(day.date, 'afternoon')" class="task-content">
                    {{ getTaskByDateAndPart(day.date, 'afternoon').task_content }}
                  </div>
                  <div v-else class="task-placeholder">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="12" y1="8" x2="12" y2="12"></line>
                      <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    点击添加
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 任务编辑弹窗 -->
    <div v-if="showEditModal" class="modal-overlay">
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
          <!-- 周日不区分上午下午，只显示一个任务区域 -->
          <template v-if="isSunday">
            <div class="modal-task-section" >
              <MdEditor 
                v-model="editMorningContent" 
                placeholder="请输入任务内容（支持 Markdown 格式）..."
                language="zh-CN"
                :toolbars="editorToolbars"
                :screenfull="true"
                :style="{ height: '500px' }"
                class="md-editor"
              />
            </div>
          </template>
          
          <!-- 非周日区分上午下午 -->
          <template v-else>
            <!-- 上午任务 -->
            <div class="modal-task-section" style="padding:0">
              <MdEditor 
                v-model="editMorningContent" 
                placeholder="请输入上午任务内容（支持 Markdown 格式）..."
                language="zh-CN"
                :toolbars="editorToolbars"
                :screenfull="true"
                :style="{ height: '250px' }"
                class="md-editor md-editor-morning"
              />
            </div>
            
            <!-- 下午任务 -->
            <div class="modal-task-section"  style="padding:4px 0 0 0">
              <MdEditor 
                v-model="editAfternoonContent" 
                placeholder="请输入下午任务内容（支持 Markdown 格式）..."
                language="zh-CN"
                :toolbars="editorToolbars"
                :screenfull="true"
                :style="{ height: '350px' }"
                class="md-editor md-editor-afternoon"
              />
            </div>
          </template>
        </div>
        
        <div class="modal-actions">
          <button @click="closeModal" class="btn cancel">取消</button>
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
  <div v-if="showSummaryModal" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <div style="display: flex; align-items: center; gap: 12px;">
          <button 
            @click="handleRegenerateSummary" 
            class="btn"
            :disabled="isRegenerating"
            style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 8px 16px; font-size: 12px; border-radius: 8px;"
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
import { ref, computed, onMounted } from 'vue';
import { getTasks, createTask, summarizeWeekTasks, getWeekSummary, regenerateWeekSummary, saveWeekSummary } from '../api';
import { MdEditor } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import * as XLSX from 'xlsx';

// 响应式数据
const currentDate = ref(new Date());
const tasks = ref<any[]>([]);
const showEditModal = ref(false);
const editDate = ref('');
const editMorningContent = ref('');
const editAfternoonContent = ref('');
const isSunday = ref(false);

// 周汇总弹窗
const showSummaryModal = ref(false);
const summaryDate = ref('');
const summaryContent = ref('');
const isRegenerating = ref(false);
const isSaving = ref(false);

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
    
    const lunarDate = getLunarDate(date);
    
    const dayInfo = {
      date: localDateStr,
      day: date.getDate(),
      lunarDate: lunarDate,
      weekday: date.getDay(),
      isCurrentMonth: date.getMonth() === month,
      isToday: localDateStr === new Date().toISOString().split('T')[0]
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

// 处理日期点击
const handleDayClick = (day: any) => {
  editDate.value = day.date;
  isSunday.value = day.weekday === 0;
  
  const morningTask = getTaskByDateAndPart(day.date, 'morning');
  editMorningContent.value = morningTask?.task_content || '';
  
  if (!isSunday.value) {
    const afternoonTask = getTaskByDateAndPart(day.date, 'afternoon');
    editAfternoonContent.value = afternoonTask?.task_content || '';
  }
  
  showEditModal.value = true;
};

// 关闭弹窗
const closeModal = () => {
  showEditModal.value = false;
  editMorningContent.value = '';
  editAfternoonContent.value = '';
};

// 保存任务
const saveTask = async () => {
  try {
    await createTask({
      date: editDate.value,
      part: 'morning',
      task_content: editMorningContent.value,
      task_type: 'completed'
    });
    
    if (!isSunday.value) {
      await createTask({
        date: editDate.value,
        part: 'afternoon',
        task_content: editAfternoonContent.value,
        task_type: 'completed'
      });
    }
    
    await fetchTasks();
    closeModal();
  } catch (error) {
    console.error('保存任务失败:', error);
  }
};

// 计算农历日期（简化版）
const getLunarDate = (date: Date): string => {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  
  const lunarMonths = ['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
  const lunarDays = ['初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
                     '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
                     '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'];
  
  return `${lunarMonths[month - 1]}${lunarDays[day - 1]}`;
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
  fetchTasks();
  setTimeout(() => {
    scrollToToday();
  }, 100);
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
      const morningTask = getTaskByDateAndPart(day.date, 'morning');
      const afternoonTask = getTaskByDateAndPart(day.date, 'afternoon');
      
      let cellContent = '';
      if (day.weekday === 0) {
        // 周日只有汇总任务
        if (morningTask) {
          cellContent = `${day.date}\n${morningTask.task_content || ''}`;
        } else {
          cellContent = day.date;
        }
      } else {
        // 其他日期区分上午下午
        const morning = morningTask ? morningTask.task_content : '';
        const afternoon = afternoonTask ? afternoonTask.task_content : '';
        cellContent = `${day.date}\nAM: ${morning}\nPM: ${afternoon}`;
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
    
    const lunarDate = getLunarDate(date);
    
    const dayInfo = {
      date: localDateStr,
      day: date.getDate(),
      lunarDate: lunarDate,
      weekday: date.getDay(),
      isCurrentMonth: date.getMonth() === month - 1,
      isToday: localDateStr === new Date().toISOString().split('T')[0]
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
  background: linear-gradient(135deg, rgba(26, 31, 58, 0.8) 0%, rgba(10, 14, 39, 0.9) 100%);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.nav-btn {
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
  border: 1px solid rgba(0, 212, 255, 0.3);
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  color: #00d4ff;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-btn:hover {
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%);
  border-color: rgba(0, 212, 255, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 212, 255, 0.3);
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
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(16, 185, 129, 0.15) 100%);
  border: 1px solid rgba(34, 197, 94, 0.3);
  padding: 10px 18px;
  border-radius: 10px;
  cursor: pointer;
  color: #22c55e;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 8px;
}

.export-btn:hover {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.3) 0%, rgba(16, 185, 129, 0.3) 100%);
  border-color: rgba(34, 197, 94, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(34, 197, 94, 0.3);
}

.export-btn.year {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(234, 179, 8, 0.15) 100%);
  border: 1px solid rgba(245, 158, 11, 0.3);
  color: #f59e0b;
}

.export-btn.year:hover {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.3) 0%, rgba(234, 179, 8, 0.3) 100%);
  border-color: rgba(245, 158, 11, 0.6);
  box-shadow: 0 8px 24px rgba(245, 158, 11, 0.3);
}

.header-title {
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 2px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-title .year {
  color: #00d4ff;
  text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
}

.header-title .divider {
  color: rgba(255, 255, 255, 0.3);
  font-weight: 300;
}

.header-title .month {
  color: #8b5cf6;
  text-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
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
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 12px;
  text-align: center;
  font-weight: 600;
  font-size: 13px;
  color: #00d4ff;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.week-number-header .mini {
  font-size: 11px;
  color: rgba(0, 212, 255, 0.6);
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

.day-header {
  padding: 16px 12px;
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%);
  border: 1px solid rgba(0, 212, 255, 0.15);
  border-radius: 12px;
  text-align: center;
  font-weight: 600;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  letter-spacing: 1px;
}

.day-header.weekend {
  color: #f472b6;
  border-color: rgba(244, 114, 182, 0.3);
  background: linear-gradient(135deg, rgba(244, 114, 182, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
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
  background: linear-gradient(135deg, rgba(26, 31, 58, 0.6) 0%, rgba(10, 14, 39, 0.8) 100%);
  border: 1px solid rgba(0, 212, 255, 0.15);
  border-radius: 12px;
  text-align: center;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  gap: 8px;
  justify-content: center;
  align-items: center;
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
  background: linear-gradient(90deg, #00d4ff 0%, #8b5cf6 100%);
  border-radius: 2px;
  transition: width 0.5s ease;
}

.year-percentage {
  font-size: 12px;
  color: #00d4ff;
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
  background: linear-gradient(135deg, rgba(26, 31, 58, 0.7) 0%, rgba(10, 14, 39, 0.9) 100%);
  border: 1px solid rgba(0, 212, 255, 0.15);
  border-radius: 16px;
  padding: 12px;
  min-height: 320px;
  max-height: 400px;
  position: relative;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
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
  background: linear-gradient(90deg, transparent 0%, rgba(0, 212, 255, 0.5) 50%, transparent 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.day-cell:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(0, 212, 255, 0.2), 0 8px 24px rgba(0, 0, 0, 0.4);
  border-color: rgba(0, 212, 255, 0.4);
}

.day-cell:hover::before {
  opacity: 1;
}

.other-month {
  background: linear-gradient(135deg, rgba(15, 18, 35, 0.6) 0%, rgba(8, 10, 22, 0.7) 100%);
  border-color: rgba(255, 255, 255, 0.03);
  opacity: 0.6;
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
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
  border-color: rgba(0, 212, 255, 0.6);
  box-shadow: 0 0 30px rgba(0, 212, 255, 0.2), inset 0 0 20px rgba(0, 212, 255, 0.05);
}

.today::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(0, 212, 255, 0.1) 0%, transparent 60%);
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

.sunday {
  border-color: rgba(244, 114, 182, 0.3);
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
  color: #fff;
}

.lunar-date {
  font-size: 11px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.5);
}

.today .day-number {
  background: linear-gradient(135deg, #00d4ff 0%, #8b5cf6 100%);
  color: white;
  padding: 8px 14px;
  border-radius: 24px;
  margin-bottom: 16px;
  box-shadow: 0 4px 16px rgba(0, 212, 255, 0.4);
}

.today .lunar-date {
  color: rgba(255, 255, 255, 0.9);
  font-size: 10px;
}

.other-month .lunar-date {
  color: rgba(255, 255, 255, 0.3);
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
  background: rgba(0, 212, 255, 0.3);
  border-radius: 2px;
}

.tasks-wrapper::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 212, 255, 0.5);
}

.task-section::-webkit-scrollbar {
  width: 4px;
}

.task-section::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 2px;
}

.task-section::-webkit-scrollbar-thumb {
  background: rgba(0, 212, 255, 0.3);
  border-radius: 2px;
}

.task-section::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 212, 255, 0.5);
}

.morning {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(139, 92, 246, 0.05) 100%);
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.afternoon {
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(0, 212, 255, 0.05) 100%);
  border: 1px solid rgba(0, 212, 255, 0.2);
}

.sunday-task {
  background: linear-gradient(135deg, rgba(244, 114, 182, 0.15) 0%, rgba(244, 114, 182, 0.05) 100%);
  border: 1px solid rgba(244, 114, 182, 0.2);
  max-height: 240px;
}

.section-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 8px;
  opacity: 0.7;
}

.morning .section-label {
  color: #8b5cf6;
}

.afternoon .section-label {
  color: #00d4ff;
}

.task-content {
  font-size: 13px;
  line-height: 1.6;
  text-align: left;
  color: rgba(255, 255, 255, 0.9);
  word-break: break-word;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  max-height: 8.8em;
}

.task-placeholder {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.3);
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
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
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
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.summary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(245, 158, 11, 0.4);
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
  background: linear-gradient(135deg, rgba(26, 31, 58, 0.95) 0%, rgba(10, 14, 39, 0.98) 100%);
  border: 1px solid rgba(0, 212, 255, 0.3);
  padding: 0;
  border-radius: 20px;
  width: 90%;
  max-width: 900px;
  max-height: 85vh;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.5), 0 0 60px rgba(0, 212, 255, 0.1);
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
  border-bottom: 1px solid rgba(0, 212, 255, 0.15);
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
  flex-shrink: 0;
}

.modal-header h3 {
  font-size: 15px;
  font-weight: 700;
  color: #fff;
  margin: 0;
}

.close-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
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
  color: #fff;
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
  background: rgba(139, 92, 246, 0.2);
  color: #8b5cf6;
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.tag.pm {
  background: rgba(0, 212, 255, 0.2);
  color: #00d4ff;
  border: 1px solid rgba(0, 212, 255, 0.3);
}

.md-editor {
  width: 100%;
  height: 200px;
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 12px;
  overflow: hidden;
  background: rgba(10, 14, 39, 0.6);
}

.md-editor-morning {
  border: 1px solid rgba(139, 92, 246, 0.4);
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
}

.md-editor-morning :deep(.md-editor-toolbar-wrapper) {
  background: rgba(139, 92, 246, 0.15);
  border-bottom: 1px solid rgba(139, 92, 246, 0.2);
}

.md-editor-afternoon {
  border: 1px solid rgba(0, 212, 255, 0.4);
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 212, 255, 0.05) 100%);
}

.md-editor-afternoon :deep(.md-editor-toolbar-wrapper) {
  background: rgba(0, 212, 255, 0.15);
  border-bottom: 1px solid rgba(0, 212, 255, 0.2);
}

.md-editor :deep(.md-editor-toolbar-wrapper) {
  background: rgba(26, 31, 58, 0.8);
  border-bottom: 1px solid rgba(0, 212, 255, 0.15);
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
  color: #00d4ff;
  border-bottom: 1px solid rgba(0, 212, 255, 0.2);
}

.md-editor :deep(.md-editor-preview code) {
  background: rgba(0, 212, 255, 0.1);
  color: #f472b6;
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
  border-left: 4px solid #00d4ff;
  background: rgba(0, 212, 255, 0.05);
  padding: 8px 12px;
  margin: 8px 0;
  color: rgba(255, 255, 255, 0.85);
}

.md-editor :deep(.md-editor-preview a) {
  color: #00d4ff;
}

.md-editor :deep(.md-editor-preview ul),
.md-editor :deep(.md-editor-preview ol) {
  color: rgba(255, 255, 255, 0.9);
}

.md-editor :deep(.md-editor-preview table) {
  border-color: rgba(0, 212, 255, 0.3);
}

.md-editor :deep(.md-editor-preview th) {
  background: rgba(0, 212, 255, 0.1);
  color: #00d4ff;
}

.md-editor :deep(.md-editor-preview td) {
  border-color: rgba(0, 212, 255, 0.2);
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
  color: #00d4ff;
  background: rgba(0, 212, 255, 0.1);
}

.md-editor :deep(.md-editor-fullscreen .md-editor-toolbar-item),
.md-editor :deep(.md-editor-pagefullscreen .md-editor-toolbar-item) {
  color: rgba(0, 0, 0, 0.85) !important;
}

.md-editor :deep(.md-editor-fullscreen .md-editor-toolbar-item:hover),
.md-editor :deep(.md-editor-pagefullscreen .md-editor-toolbar-item:hover) {
  color: #00d4ff !important;
  background: rgba(0, 212, 255, 0.15) !important;
}

.md-editor :deep(.md-editor-footer) {
  background: rgba(35, 40, 70, 0.98);
  border-top: 1px solid rgba(0, 212, 255, 0.3);
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
  accent-color: #00d4ff;
  background-color: rgba(0, 0, 0, 0.5);
  border: 2px solid rgba(0, 212, 255, 0.5);
  border-radius: 4px;
}

.md-editor :deep(.md-editor-footer-item input[type="checkbox"]:checked) {
  accent-color: #00d4ff;
  background-color: #00d4ff;
  border-color: #00d4ff;
  box-shadow: 0 0 12px rgba(0, 212, 255, 0.7), inset 0 0 0 2px white;
}

.md-editor :deep(.md-editor-footer-item strong) {
  color: #00d4ff;
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
  background: rgba(0, 212, 255, 0.4);
  border-radius: 3px;
}

.md-editor :deep(.md-editor-input-wrapper::-webkit-scrollbar-thumb:hover) {
  background: rgba(0, 212, 255, 0.6);
}

.md-editor :deep(.md-editor-preview-wrapper::-webkit-scrollbar) {
  width: 6px;
}

.md-editor :deep(.md-editor-preview-wrapper::-webkit-scrollbar-track) {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
}

.md-editor :deep(.md-editor-preview-wrapper::-webkit-scrollbar-thumb) {
  background: rgba(0, 212, 255, 0.4);
  border-radius: 3px;
}

.md-editor :deep(.md-editor-preview-wrapper::-webkit-scrollbar-thumb:hover) {
  background: rgba(0, 212, 255, 0.6);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 10px 14px;
  border-top: 1px solid rgba(0, 212, 255, 0.15);
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

.btn.save {
  background: linear-gradient(135deg, #00d4ff 0%, #8b5cf6 100%);
  color: white;
  box-shadow: 0 4px 16px rgba(0, 212, 255, 0.3);
}

.btn.save:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 212, 255, 0.4);
}

.btn.save:active {
  transform: translateY(0);
}
</style>
