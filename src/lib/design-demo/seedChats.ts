import { v4 as uuidv4 } from 'uuid';
import { createNewChat } from '$lib/apis/chats';
import { designCases } from './data';

const samplePrompts = [
	'请梳理江湾文化艺术中心方案深化阶段的重点工作。',
	'绿谷科创园区的中央绿谷适合如何组织慢行流线？',
	'南站城市更新综合体需要准备哪些交付资料？',
	'湖畔社区图书馆的自然采光方案有哪些优化方向？'
];

const sampleResponses = [
	'建议先核对滨水界面、剧场与展厅的功能流线，再集中深化结构网格、幕墙遮阳和屋面排水。下一轮成果可包括总图、典型平剖面、关键节点及材料样板。',
	'可把中央绿谷作为主要步行轴线，让研发楼入口、共享会议空间和雨水花园沿线展开。桥梁连接应优先服务日常通勤，并预留无障碍坡道。',
	'建议形成建筑、结构、机电三专业图纸清单，附上 BIM 模型版本、碰撞问题闭环记录及成本假设。交通换乘界面和保留工业构筑物节点需要单独校核。',
	'优先核对阅览区的眩光与夏季热负荷。沿湖侧可采用连续遮阳构件，深进深区域结合高侧窗和天窗；模型计算结果应与实际使用时段对应。'
];

export async function seedDesignDemoChats(token: string, userId: string, modelId = '') {
	const key = `design-demo-sample-chats:${userId}`;
	if (!token || !userId || localStorage.getItem(key) === 'done') return false;
	const archiveModelId = modelId || 'design-demo-archive';

	for (const [index, item] of designCases.entries()) {
		const userMessageId = uuidv4();
		const assistantMessageId = uuidv4();
		const timestamp = Math.floor(Date.now() / 1000) - (designCases.length - index) * 86_400;
		const userMessage = {
			id: userMessageId,
			parentId: null,
			childrenIds: [assistantMessageId],
			role: 'user',
			content: samplePrompts[index],
			timestamp,
			models: [archiveModelId]
		};
		const assistantMessage = {
			id: assistantMessageId,
			parentId: userMessageId,
			childrenIds: [],
			role: 'assistant',
			content: sampleResponses[index],
			timestamp: timestamp + 15,
			model: archiveModelId,
			modelIdx: 0,
			done: true
		};
		await createNewChat(
			token,
			{
				id: uuidv4(),
				title: item.title,
				models: [archiveModelId],
				history: {
					messages: { [userMessageId]: userMessage, [assistantMessageId]: assistantMessage },
					currentId: assistantMessageId
				},
				messages: [userMessage, assistantMessage],
				tags: [],
				timestamp: timestamp * 1000
			},
			null
		);
	}

	localStorage.setItem(key, 'done');
	return true;
}
