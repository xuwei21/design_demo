<script lang="ts">
	import '$lib/design-demo/demo.css';
	import { mobile, showSidebar } from '$lib/stores';
</script>

<div class="design-demo-shell" class:sidebar-open={$showSidebar && !$mobile}>
	{#if !$showSidebar}
		<button class="design-sidebar-toggle" type="button" aria-label="展开侧边栏" title="展开侧边栏" on:click={() => showSidebar.set(true)}>☰</button>
	{/if}
	<slot />
</div>

<style>
	.design-demo-shell { width: 100%; height: 100%; overflow: auto; flex: 1 1 0%; min-width: 0; }
	.design-demo-shell.sidebar-open { max-width: calc(100% - var(--sidebar-width, 245px)); }
	@media (min-width: 768px) {
		.design-demo-shell:not(.sidebar-open) { max-width: calc(100% - 42px); }
	}
	.design-sidebar-toggle { position: fixed; top: 12px; left: 14px; z-index: 40; display: grid; place-items: center; width: 34px; height: 34px; border: 1px solid #dce8e4; border-radius: 10px; background: #fff; color: #42665f; box-shadow: 0 4px 18px rgba(27, 62, 55, .08); font-size: 17px; }
	:global(.dark) .design-sidebar-toggle { background: #263432; border-color: #40504b; color: #d6e9e2; }
</style>
