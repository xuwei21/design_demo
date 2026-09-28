<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { designCases } from '$lib/design-demo/data';

	$: item = designCases.find((entry) => entry.slug === $page.params.slug);
	let activeImage = 0;
	let modelViewer: HTMLElement | null = null;

	onMount(async () => {
		await import('@google/model-viewer');
	});

	function resetCamera() {
		const viewer = modelViewer as (HTMLElement & { cameraOrbit?: string; fieldOfView?: string }) | null;
		if (viewer) {
			viewer.cameraOrbit = '45deg 72deg 105%';
			viewer.fieldOfView = '30deg';
		}
	}
</script>

<svelte:head><title>{item?.title ?? '案例详情'} · 设计院工作台</title></svelte:head>

{#if item}
	<div class="design-page">
		<a href="/demo/cases" class="design-back">← 返回案例展示</a>
		<header class="design-detail-head"><div><p class="design-eyebrow">PROJECT CASE / {item.category}</p><h1>{item.title}</h1><p>{item.summary}</p></div><span class="design-stage">{item.stage}</span></header>
		<div class="design-detail-grid">
			<div class="design-detail-main">
				<div class="design-gallery-main"><img src={item.images[activeImage]} alt={`${item.title}展示图 ${activeImage + 1}`} /></div>
				<div class="design-gallery-thumbs">{#each item.images as image, index}<button class:active={activeImage === index} on:click={() => (activeImage = index)} aria-label={`查看第 ${index + 1} 张图片`}><img src={image} alt="" /></button>{/each}</div>
				<section class="design-panel"><div class="design-section-title"><span>3D 模型预览</span><small>可拖拽旋转 · 滚轮缩放</small></div><div class="design-model-wrap"><svelte:element this={'model-viewer'} bind:this={modelViewer} src="/design-demo/civic-building.glb" alt="建筑体量 3D 模型" camera-controls auto-rotate shadow-intensity="0.8" camera-orbit="45deg 72deg 105%" field-of-view="30deg" interaction-prompt="none" /><button class="design-reset" on:click={resetCamera}>重置视角</button></div><p class="design-model-note">示意模型用于展示 3D 浏览交互，具体设计以项目交付模型为准。</p></section>
			</div>
			<aside class="design-detail-aside"><section class="design-panel"><h2>项目概况</h2><dl><div><dt>项目类型</dt><dd>{item.category}</dd></div><div><dt>项目地点</dt><dd>{item.location}</dd></div><div><dt>建筑面积</dt><dd>{item.area}</dd></div><div><dt>设计团队</dt><dd>{item.author}</dd></div><div><dt>更新日期</dt><dd>{item.date}</dd></div></dl></section><section class="design-panel"><h2>设计亮点</h2><ul class="design-highlight-list">{#each item.highlights as highlight}<li>{highlight}</li>{/each}</ul></section></aside>
		</div>
	</div>
{:else}
	<div class="design-page"><div class="design-empty">案例不存在。<a href="/demo/cases">返回案例列表</a></div></div>
{/if}
