export type DesignCase = {
	slug: string;
	title: string;
	summary: string;
	category: string;
	author: string;
	date: string;
	location: string;
	area: string;
	stage: string;
	cover: string;
	images: string[];
	highlights: string[];
};

const assets = '/design-demo';

export const designCases: DesignCase[] = [
	{
		slug: 'jiangwan-cultural-center',
		title: '江湾文化艺术中心',
		summary: '以开放的滨水界面连接展览、表演与日常公共生活。',
		category: '公共建筑',
		author: '建筑一院 · 林知远',
		date: '2026-08-18',
		location: '上海 · 杨浦',
		area: '42,600 ㎡',
		stage: '方案深化',
		cover: `${assets}/cultural-center.png`,
		images: [`${assets}/cultural-center.png`, `${assets}/cultural-plan.svg`, `${assets}/cultural-section.svg`],
		highlights: ['连续屋面组织滨水步行系统', '展厅与剧场共享弹性前厅', '低碳材料与遮阳一体化设计']
	},
	{
		slug: 'green-valley-campus',
		title: '绿谷科创园区',
		summary: '围绕中央绿谷布置研发空间，形成可步行、可交流的创新社区。',
		category: '产业园区',
		author: '规划二院 · 陈墨',
		date: '2026-07-26',
		location: '杭州 · 余杭',
		area: '118,000 ㎡',
		stage: '设计中',
		cover: `${assets}/innovation-campus.png`,
		images: [`${assets}/innovation-campus.png`, `${assets}/campus-plan.svg`, `${assets}/campus-section.svg`],
		highlights: ['雨水花园贯穿园区', '模块化研发单元灵活组合', '慢行网络衔接城市交通']
	},
	{
		slug: 'south-station-renewal',
		title: '南站城市更新综合体',
		summary: '让交通枢纽、商业街区和城市客厅在同一屋檐下相遇。',
		category: '城市更新',
		author: '城市更新中心 · 周芮',
		date: '2026-06-12',
		location: '南京 · 雨花台',
		area: '86,500 ㎡',
		stage: '施工图设计',
		cover: `${assets}/station-renewal.png`,
		images: [`${assets}/station-renewal.png`, `${assets}/station-plan.svg`, `${assets}/station-section.svg`],
		highlights: ['立体交通实现无缝换乘', '保留原有工业构筑物记忆', '开放首层强化街区活力']
	},
	{
		slug: 'lakefront-library',
		title: '湖畔社区图书馆',
		summary: '一座融入湿地景观的开放式阅读空间，为城市留出安静的角落。',
		category: '文化教育',
		author: '建筑三院 · 许文',
		date: '2026-05-08',
		location: '苏州 · 工业园区',
		area: '12,800 ㎡',
		stage: '已交付',
		cover: `${assets}/lake-library.png`,
		images: [`${assets}/lake-library.png`, `${assets}/library-plan.svg`, `${assets}/library-section.svg`],
		highlights: ['木结构与湖岸地形相融合', '全天候共享阅读阶梯', '自然通风与采光优化']
	}
];

export const projectStatuses = [
	{ key: '设计中', icon: '✦', tone: 'blue' },
	{ key: '待交付', icon: '◷', tone: 'amber' },
	{ key: '验收中', icon: '✓', tone: 'violet' },
	{ key: '返修中', icon: '↻', tone: 'rose' },
	{ key: '已交付', icon: '▣', tone: 'green' }
] as const;

export const projects = [
	{ name: '江湾文化艺术中心', owner: '王珂', status: '设计中', updated: '09-26', progress: 68, desc: '文化演艺综合体，含歌剧院与滨水演艺广场，正在深化方案设计。'},
	{ name: '绿谷科创园区', owner: '陈墨', status: '设计中', updated: '09-25', progress: 42, desc: '生态科创产业园，聚焦绿色建筑与智慧办公，处于概念设计阶段。'},
	{ name: '南站城市更新综合体', owner: '周芮', status: '待交付', updated: '09-24', progress: 91, desc: 'TOD 综合开发项目，涵盖商业、办公与交通枢纽，即将交付。'},
	{ name: '东岸医疗中心', owner: '小王', status: '验收中', updated: '09-22', progress: 95, desc: '三级综合医院，含门诊、住院与医技中心，处于验收阶段。'},
	{ name: '滨江人才社区', owner: '刘畅', status: '返修中', updated: '09-21', progress: 76, desc: '青年人才公寓社区，配建共享服务设施，正在进行返修完善。'},
	{ name: '湖畔社区图书馆', owner: '许文', status: '已交付', updated: '09-18', progress: 100, desc: '社区公共文化空间，融合阅读与活动功能，已交付使用。'},
	{ name: '临港低碳展厅', owner: '林知远', status: '设计中', updated: '09-18', progress: 33, desc: '低碳技术展示馆，示范近零能耗建造，设计推进中。'},
	{ name: '北城体育公园', owner: '沈晴', status: '待交付', updated: '09-16', progress: 88, desc: '全民健身公园，含体育场馆与户外场地，即将交付。'},
	{ name: '云山学校扩建', owner: '赵颖', status: '验收中', updated: '09-14', progress: 97, desc: '九年制学校扩建工程，新增教学与实验组团，正在验收。'},
	{ name: '智慧制造展示中心', owner: '叶恒', status: '已交付', updated: '09-11', progress: 100, desc: '智能制造示范展示与研发基地，已完成交付。'},
	{ name: '山海连廊景观工程', owner: '何夏', status: '设计中', updated: '09-10', progress: 56, desc: '滨水景观带，串联山海生态廊道，方案深化中。'},
	{ name: '老港仓库活化项目', owner: '张禾', status: '返修中', updated: '09-08', progress: 82, desc: '历史仓库更新为文创商业街区，处于返修收尾阶段。'}
] as const;

export const knowledgeArticles = [
	{
		slug: 'facade-fire-safety',
		title: '公共建筑幕墙防火设计要点',
		category: '规范解读',
		updated: '2026-08-20',
		summary: '梳理防火分隔、材料选型、节点构造与多专业协同检查项。',
		content: '设计幕墙时，应把防火分隔、结构连接和检修需求作为同一套节点问题处理。方案阶段先明确建筑高度与使用功能，深化阶段逐层核对楼板边缘、防火封堵及开启扇位置。提交前使用跨专业校核表确认建筑、幕墙、机电图纸的一致性。'
	},
	{
		slug: 'green-building-process',
		title: '绿色建筑方案阶段工作清单',
		category: '工作流程',
		updated: '2026-07-15',
		summary: '从场地、围护结构、日照与水资源四个维度组织早期决策。',
		content: '绿色建筑评估应在体量推敲时同步启动。场地组提供微气候与慢行分析，建筑组确认遮阳、自然采光和围护性能，机电组评估能耗与水资源回收策略。每次方案评审保留关键指标的版本记录。'
	},
	{
		slug: 'bim-delivery',
		title: 'BIM 模型交付命名与校核规范',
		category: '交付标准',
		updated: '2026-06-28',
		summary: '统一专业模型命名、坐标、构件信息和交付前的碰撞检查。',
		content: '各专业模型使用统一项目代号和版本号，交付坐标采用项目基点。关键构件补齐分类、材料及楼层字段。提交前执行模型完整性检查和重点区域碰撞检查，并附问题清单与修复记录。'
	},
	{
		slug: 'cost-estimation',
		title: '方案估算常见问题与报价口径',
		category: '成本控制',
		updated: '2026-05-30',
		summary: '明确建筑面积、单方指标和暂估项的使用边界。',
		content: '报价估算应注明面积口径、价格基准时间和不包含项目。对结构形式、幕墙系统及特殊设备分别列出假设条件。对不确定性高的项目采用区间表达，并在下一轮设计中核实。'
	}
];

export const frequentQuestions = [
	{ label: '公共建筑幕墙防火节点应如何校核？', article: 'facade-fire-safety' },
	{ label: '绿色建筑方案阶段需要先完成哪些分析？', article: 'green-building-process' },
	{ label: 'BIM 模型交付前有哪些必查项？', article: 'bim-delivery' },
	{ label: '方案报价估算应注明哪些假设条件？', article: 'cost-estimation' }
];

export const defaultSkillMarkdown = `# 我的设计协作 Skill

## 工作目标
作为建筑设计院的协作助手，先理解项目阶段、场地条件和交付要求，再给出可执行的建议。

## 工作方法
1. 明确任务背景、设计范围、时间节点与现有资料。
2. 区分已确认信息与待核实假设。
3. 按方案、深化、交付三个层次组织输出。
4. 发现规范或成本风险时，写清风险、依据和建议的复核动作。

## 输出偏好
- 使用简洁中文和清晰的小标题。
- 对尺寸、面积、金额保留单位和计算口径。
- 图片与 3D 渲染建议说明视角、材质和光照条件。
- 报价预估注明所依据的假设，不把估算表述为最终报价。
`;
