<script lang="ts">
	import { page } from '$app/stores';
	import { mobile, showSidebar } from '$lib/stores';

	export let chats: { id: string; title: string }[] = [];

	const items = [
		{ href: '/demo/cases', label: '案例展示', icon: '▧' },
		{ href: '/demo/stats', label: '项目统计', icon: '▥' },
		{ href: '/demo/knowledge', label: '知识库', icon: '◈' },
		{ href: '/demo/skill', label: '技能更新', icon: '✦' },
		{ href: '/demo/other', label: '其他', icon: '⋯' }
	];

	function closeMobileSidebar() {
		if ($mobile) showSidebar.set(false);
	}

	let historyExpanded = true;
</script>

<div class="design-sidebar-group">
	<button class="design-sidebar-fold" aria-expanded={historyExpanded} on:click={() => (historyExpanded = !historyExpanded)}><span class="design-sidebar-fold-arrow">{historyExpanded ? '▾' : '▸'}</span><span>历史项目</span></button>
	{#if historyExpanded}
		{#if chats.length}
			{#each chats as chat}
				<a href={`/c/${chat.id}`} class:active={$page.url.pathname === `/c/${chat.id}`} title={chat.title} on:click={closeMobileSidebar}><span class="design-sidebar-history-icon">◫</span><span class="design-sidebar-history-name">{chat.title}</span></a>
			{/each}
		{:else}
			<div class="design-sidebar-hint">新任务会自动出现在这里</div>
		{/if}
	{/if}
</div>

<div class="design-sidebar-group design-sidebar-main-links">
	{#each items as item}
		<a href={item.href} class:active={$page.url.pathname === item.href || $page.url.pathname.startsWith(`${item.href}/`)} on:click={closeMobileSidebar}><span class="design-sidebar-main-icon">{item.icon}</span><span>{item.label}</span></a>
	{/each}
</div>

<style>
	.design-sidebar-group{padding:9px 8px 5px}
	.design-sidebar-fold{display:flex;align-items:center;gap:6px;width:100%;min-height:31px;padding:5px 9px;border-radius:10px;color:#6d8282;font-size:12px;font-weight:600;line-height:20px;cursor:pointer;transition:background .15s}
	.design-sidebar-fold:hover{background:rgba(112,143,137,.13)}
	.design-sidebar-fold-arrow{font-size:11px;width:16px;flex:none;color:#8ca59f}
	.design-sidebar-group a{display:flex;align-items:center;gap:10px;min-height:35px;padding:6px 9px;border-radius:10px;color:inherit;font-size:13px;line-height:20px;text-decoration:none;transition:background .15s}
	.design-sidebar-group a:hover{background:rgba(112,143,137,.13)}
	.design-sidebar-group a.active{background:rgba(63,143,123,.16);color:#258e78;font-weight:600}
	.design-sidebar-history-icon{color:#8ca59f;font-size:14px;width:16px;flex:none}
	.design-sidebar-history-name{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
	.design-sidebar-main-links{padding-top:5px}
	.design-sidebar-main-icon{display:grid;place-items:center;width:16px;font-size:16px;flex:none}
	.design-sidebar-hint{padding:3px 9px 8px;color:#a8b5b4;font-size:12px}
</style>
