<script lang="ts">
	import { designCases, frequentQuestions, knowledgeArticles } from '$lib/design-demo/data';

	let query = '';
	$: term = query.trim().toLocaleLowerCase();
	$: caseMatches = term ? designCases.filter((item) => [item.title, item.summary, item.category].join(' ').toLocaleLowerCase().includes(term)) : [];
	$: articleMatches = term ? knowledgeArticles.filter((item) => [item.title, item.summary, item.category, item.content].join(' ').toLocaleLowerCase().includes(term)) : [];
</script>

<svelte:head><title>知识库 · 设计院工作台</title></svelte:head>

<div class="design-page design-knowledge-page">
	<div class="design-knowledge-hero"><div class="design-knowledge-mark">✳</div><p class="design-eyebrow">DESIGN INTELLIGENCE / 企业知识资产</p><h1>XXX 企业知识库</h1><p class="design-muted">搜索案例、标准和经验，让每一次设计都有据可循。</p><div class="design-search large"><input aria-label="实时搜索知识库" placeholder="试试搜索：幕墙防火、BIM 交付、绿色建筑…" bind:value={query} /><span class="design-search-indicator" aria-label="输入后实时搜索"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 4.4 4.4"/></svg></span></div></div>
	{#if term}
		<div class="design-knowledge-results"><div class="design-section-title"><span>搜索结果</span><small>{caseMatches.length + articleMatches.length} 条匹配</small></div>{#if caseMatches.length + articleMatches.length}<div class="design-result-list">{#each caseMatches as item}<a href={`/demo/cases/${item.slug}`} class="design-result"><img src={item.cover} alt="" /><div><small>设计案例 · {item.category}</small><h2>{item.title}</h2><p>{item.summary}</p></div><span>↗</span></a>{/each}{#each articleMatches as item}<a href={`/demo/knowledge/${item.slug}`} class="design-result"><div class="design-result-doc-icon">▤</div><div><small>知识文档 · {item.category}</small><h2>{item.title}</h2><p>{item.summary}</p></div><span>↗</span></a>{/each}</div>{:else}<div class="design-empty">没有找到相关内容，请换一个关键词。</div>{/if}</div>
	{:else}
		<div class="design-knowledge-content"><div class="design-section-title"><span>推荐案例</span><a href="/demo/cases">查看全部 ↗</a></div><div class="design-recommend-grid">{#each designCases.slice(0, 3) as item}<a href={`/demo/cases/${item.slug}`}><img src={item.cover} alt={item.title} /><div><strong>{item.title}</strong><small>{item.category} · {item.location}</small></div></a>{/each}</div><div class="design-section-title design-faq-title"><span>高频查询</span><small>从这里开始探索</small></div><div class="design-faq-list">{#each frequentQuestions as question, index}<a href={`/demo/knowledge/${question.article}`}><span class="design-faq-index">0{index + 1}</span><span>{question.label}</span><span class="design-faq-arrow">↗</span></a>{/each}</div></div>
	{/if}
</div>
