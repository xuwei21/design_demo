<script lang="ts">
	import { designCases } from '$lib/design-demo/data';

	let query = '';
	$: normalizedQuery = query.trim().toLocaleLowerCase();
	$: results = designCases.filter((item) =>
		[item.title, item.summary, item.category, item.author, item.location]
			.join(' ')
			.toLocaleLowerCase()
			.includes(normalizedQuery)
	);
</script>

<svelte:head><title>案例展示 · 设计院工作台</title></svelte:head>

<div class="design-page">
	<header class="design-page-head">
		<div>
			<p class="design-eyebrow">DESIGN ARCHIVE / 案例库</p>
			<h1>案例展示</h1>
			<p class="design-muted">从概念到交付，探索设计团队的项目实践。</p>
		</div>
		<div class="design-search compact">
			<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 4.4 4.4"/></svg>
			<input aria-label="搜索案例" placeholder="搜索项目、类型或设计师" bind:value={query} />
		</div>
	</header>

	<div class="design-section-title"><span>精选项目</span><small>{results.length} 个案例</small></div>
	{#if results.length}
		<div class="design-case-grid">
			{#each results as item}
				<a class="design-case-card" href={`/demo/cases/${item.slug}`}>
					<div class="design-case-cover"><img src={item.cover} alt={item.title} loading="lazy" /></div>
					<div class="design-case-body"><h2>{item.title}</h2><p>{item.summary}</p><div class="design-case-meta"><span>{item.author}</span><time datetime={item.date}>{item.date}</time></div></div>
				</a>
			{/each}
		</div>
	{:else}
		<div class="design-empty">没有找到相关案例，试试其他关键词。</div>
	{/if}
</div>
