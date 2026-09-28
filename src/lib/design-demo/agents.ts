export const designAgents = [
	{ id: 'design-agent-requirements', label: '需求分析', description: '梳理需求、范围与约束' },
	{ id: 'design-agent-3d', label: '3D制作', description: '组织建模与体量表达' },
	{ id: 'design-agent-render', label: '图片渲染', description: '规划视角、材质和光照' },
	{ id: 'design-agent-quote', label: '报价预估', description: '明确估算口径和假设' },
	{ id: 'design-agent-report', label: '报告生成', description: '生成结构化设计报告' }
] as const;

export const getDesignAgentFromPrompt = (prompt: string) => {
	const matches = [...String(prompt).matchAll(/<@(design-agent-[\w-]+)(?:\|[^>]*)?>/g)];
	return designAgents.find((agent) => agent.id === matches.at(-1)?.[1]);
};
