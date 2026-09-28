<script lang="ts">
	import { projects, projectStatuses } from '$lib/design-demo/data';

	const activeProjects = projects.filter((project) => project.status !== '已交付');
	let statusFilter = '全部';
	let viewingProject: (typeof projects)[number] | null = null;
	$: visibleProjects = activeProjects.filter((project) => statusFilter === '全部' || project.status === statusFilter);
</script>

<svelte:head><title>项目统计 · 设计院工作台</title></svelte:head>

<div class="design-page">
	<header class="design-page-head"><div><p class="design-eyebrow">PROJECT OVERVIEW / 项目总览</p><h1>项目统计</h1><p class="design-muted">掌握每个项目的进展与交付节奏。</p></div><span class="design-date-badge">2026 年度项目数据 · 演示</span></header>
	<div class="design-stats-grid"><div class="design-stat-card total"><div class="design-stat-icon">▦</div><p>项目总计</p><strong>{projects.length}</strong><small>全部登记项目</small></div>{#each projectStatuses as status}<button class="design-stat-card {status.tone}" class:selected={statusFilter === status.key} on:click={() => (statusFilter = statusFilter === status.key ? '全部' : status.key)}><div class="design-stat-icon">{status.icon}</div><p>{status.key}</p><strong>{projects.filter((project) => project.status === status.key).length}</strong><small>点击筛选明细</small></button>{/each}</div>
	<section class="design-panel design-project-table"><div class="design-section-title"><span>进行中的项目</span><div><small>{visibleProjects.length} 个项目</small>{#if statusFilter !== '全部'}<button on:click={() => (statusFilter = '全部')}>清除“{statusFilter}”筛选</button>{/if}</div></div><div class="design-table-scroll"><table><thead><tr><th>项目名称</th><th>负责人</th><th>状态</th><th>进度</th><th>最近更新</th><th>操作</th></tr></thead><tbody>{#each visibleProjects as project}<tr><td class="project-name">{project.name}</td><td>{project.owner}</td><td><span class="design-status {project.status}">{project.status}</span></td><td><div class="design-progress"><span style={`width: ${project.progress}%`}></span></div><small>{project.progress}%</small></td><td>{project.updated}</td><td><button class="design-project-view" on:click={() => (viewingProject = project)}>查看</button></td></tr>{/each}</tbody></table>{#if visibleProjects.length === 0}<div class="design-empty">当前筛选下没有进行中的项目。</div>{/if}</div></section>
{#if viewingProject}
	<div class="design-modal-backdrop">
		<button class="design-modal-dismiss" type="button" aria-label="关闭查看弹框" on:click={() => (viewingProject = null)}></button>
		<div class="design-modal" role="dialog" tabindex="-1" aria-modal="true" aria-label="查看项目详情">
			<div class="design-modal-head">
				<div>
					<h2>{viewingProject.name}</h2>
					<p>{viewingProject.owner} · 最近更新 {viewingProject.updated}</p>
				</div>
				<button aria-label="关闭" on:click={() => (viewingProject = null)}>×</button>
			</div>
			<div class="design-project-detail">
				<div class="design-project-detail-row"><span>状态</span><strong class="design-status {viewingProject.status}">{viewingProject.status}</strong></div>
				<div class="design-project-detail-row"><span>进度</span><strong>{viewingProject.progress}%</strong></div>
				<div class="design-progress"><span style={`width: ${viewingProject.progress}%`}></span></div>
				<p class="design-project-desc">{viewingProject.desc}</p>
			</div>
			<div class="design-modal-actions">
				<button on:click={() => (viewingProject = null)}>关闭</button>
			</div>
		</div>
	</div>
{/if}

<style>
	.design-project-view {
		font-size: 11px;
		color: #fff;
		background: #257e70;
		border-radius: 8px;
		padding: 6px 14px;
		transition: background 0.15s;
	}

	.design-project-view:hover {
		background: #17685c;
	}

	.design-project-detail {
		display: flex;
		flex-direction: column;
		gap: 9px;
		margin-bottom: 17px;
	}

	.design-project-detail-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		font-size: 12px;
	}

	.design-project-detail-row > span {
		color: #6d8282;
	}

	.design-project-detail-row > strong {
		color: #26393e;
	}

	.design-project-desc {
		margin-top: 4px;
		padding-top: 11px;
		border-top: 1px solid #edf1f0;
		font-size: 12px;
		line-height: 1.7;
		color: #4a5a5e;
	}

	:global(.dark) .design-project-detail-row > strong {
		color: #dce9e5;
	}

	:global(.dark) .design-project-desc {
		border-color: #344244;
		color: #c2d3cf;
	}
</style>
</div>
