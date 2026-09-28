<script lang="ts">
	import { page } from '$app/stores';
	import { knowledgeArticles } from '$lib/design-demo/data';

	$: article = knowledgeArticles.find((entry) => entry.slug === $page.params.slug);
</script>

<svelte:head><title>{article?.title ?? '知识内容'} · 设计院工作台</title></svelte:head>

<div class="design-page design-article-page"><a href="/demo/knowledge" class="design-back">← 返回知识库</a>{#if article}<article class="design-panel"><span class="design-stage">{article.category}</span><h1>{article.title}</h1><p class="design-article-summary">{article.summary}</p><div class="design-article-meta">企业知识库 · 更新于 {article.updated}</div><div class="design-article-body">{#each article.content.split('。').filter(Boolean) as sentence}<p>{sentence}。</p>{/each}</div></article>{:else}<div class="design-empty">内容不存在。<a href="/demo/knowledge">返回知识库</a></div>{/if}</div>
