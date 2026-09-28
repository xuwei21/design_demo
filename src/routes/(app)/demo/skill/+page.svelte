<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { marked } from 'marked';
	import DOMPurify from 'dompurify';
	import { user } from '$lib/stores';
	import { WEBUI_API_BASE_URL } from '$lib/constants';
	import { defaultSkillMarkdown } from '$lib/design-demo/data';

	type EditMode = 'manual' | 'ai';
	type HistoryItem = { id: string; savedAt: number; source: EditMode; content: string };

	let markdown = defaultSkillMarkdown;
	let rendered = '';
	let editing = false;
	let editMode: EditMode = 'manual';
	let draft = '';
	let submitting = false;
	let showAvatar = true;
	let history: HistoryItem[] = [];
	let viewingItem: HistoryItem | null = null;

	$: storageKey = `design-demo-skill:${$user?.id ?? 'guest'}`;
	$: historyKey = `design-demo-skill-history:${$user?.id ?? 'guest'}`;

	const MAX_HISTORY = 50;

	async function renderSkill() {
		rendered = DOMPurify.sanitize(await marked.parse(markdown));
	}

	function loadHistory() {
		try {
			const raw = localStorage.getItem(historyKey);
			history = raw ? (JSON.parse(raw) as HistoryItem[]) : [];
		} catch {
			history = [];
		}
	}

	function saveHistory() {
		localStorage.setItem(historyKey, JSON.stringify(history.slice(0, MAX_HISTORY)));
	}

	/** 把指定内容作为历史版本记录（最新在前） */
	function pushHistory(content: string, source: EditMode) {
		const item: HistoryItem = {
			id: `v${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
			savedAt: Date.now(),
			source,
			content
		};
		history = [item, ...history].slice(0, MAX_HISTORY);
		saveHistory();
	}

	onMount(() => {
		markdown = localStorage.getItem(storageKey) ?? defaultSkillMarkdown;
		loadHistory();
		void renderSkill();
	});

	function openEditor(mode: EditMode) {
		if (submitting) return;
		editMode = mode;
		draft = mode === 'ai' ? '' : markdown;
		editing = true;
		void tick().then(() => document.getElementById('design-skill-textarea')?.focus());
	}

	function submitEdit() {
		if (submitting) return;
		const nextValue = draft.trim();
		if (!nextValue) {
			toast.error(editMode === 'ai' ? 'AI 修改内容不能为空' : '修改内容不能为空');
			return;
		}
		editing = false;
		submitting = true;
		toast.info('已提交，请等待');
		const savedSource = editMode;
		window.setTimeout(async () => {
			try {
				// 当前内容入历史，再写入新内容
				pushHistory(markdown, savedSource);
				markdown = nextValue;
				localStorage.setItem(storageKey, nextValue);
				await renderSkill();
				toast.success(savedSource === 'ai' ? 'AI 修改已完成' : '技能更新已完成');
			} catch {
				toast.error('本地保存失败，请重试');
			} finally {
				submitting = false;
			}
		}, 2200);
	}

	async function restoreHistory(item: HistoryItem) {
		if (submitting) return;
		if (item.content === markdown) {
			toast.info('该版本已是当前版本');
			return;
		}
		submitting = true;
		toast.info('正在恢复历史版本…');
		await new Promise((resolve) => setTimeout(resolve, 400));
		try {
			// 当前内容入历史，再恢复目标版本
			pushHistory(markdown, 'manual');
			markdown = item.content;
			localStorage.setItem(storageKey, item.content);
			await renderSkill();
			toast.success('已恢复该历史版本');
		} catch {
			toast.error('恢复失败，请重试');
		} finally {
			submitting = false;
		}
	}

	function formatHistoryTime(ts: number) {
		const d = new Date(ts);
		const pad = (n: number) => String(n).padStart(2, '0');
		return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
	}
</script>

<svelte:head><title>技能更新 · 设计院工作台</title></svelte:head>

<div class="design-page design-profile-page">
	<header class="design-page-head">
		<div>
			<p class="design-eyebrow">PERSONAL SKILL / 个人工作流</p>
			<h1>技能更新</h1>
			<p class="design-muted">维护你的设计协作方法和输出偏好。</p>
		</div>
	</header>

	<section class="design-profile-card">
		<div class="design-avatar">
			{#if $user?.id && showAvatar}
				<img
					src={`${WEBUI_API_BASE_URL}/users/${$user.id}/profile/image`}
					alt="用户头像"
					on:error={() => (showAvatar = false)}
				/>
			{:else}
				<span>{($user?.name ?? '设计师').slice(0, 1)}</span>
			{/if}
		</div>
		<div>
			<div class="design-profile-name">{$user?.name ?? '演示用户'}</div>
			<p>{$user?.email ?? 'demo@design-institute.example'}</p>
			<span>个人设计协作空间</span>
		</div>
	</section>

	<section class="design-panel design-skill-panel">
		<div class="design-section-title">
			<span>个人 Skill</span>
			<small>Markdown 工作说明</small>
		</div>
		<div class="design-skill-markdown prose dark:prose-invert max-w-none">{@html rendered}</div>
		<div class="design-skill-actions">
			<small>{submitting ? '处理中，请稍候…' : '当前内容保存在此浏览器中，修改或 AI 修改会自动留存历史版本'}</small>
			<div class="design-skill-action-buttons">
				<button
					class="design-secondary-button"
					disabled={submitting}
					on:click={() => openEditor('ai')}
				>
					AI 修改
				</button>
				<button
					class="design-primary-button"
					disabled={submitting}
					on:click={() => openEditor('manual')}
				>
					修改
				</button>
			</div>
		</div>
	</section>

	<section class="design-panel design-history-panel">
		<div class="design-section-title">
			<span>历史版本</span>
			<small>共 {history.length} 条记录</small>
		</div>
		{#if history.length === 0}
			<div class="design-empty design-history-empty">暂无历史版本，修改或 AI 修改后会在此自动留存。</div>
		{:else}
			<div class="design-history-list">
				{#each history as item, index (item.id)}
					<div class="design-history-item">
						<div class="design-history-index">#{history.length - index}</div>
						<div class="design-history-info">
							<div class="design-history-time">{formatHistoryTime(item.savedAt)}</div>
							<div class="design-history-tag {item.source === 'ai' ? 'ai' : ''}">
								{item.source === 'ai' ? 'AI 修改' : '手动修改'}
							</div>
						</div>
						<div class="design-history-actions">
							<button type="button" class="design-history-view" on:click={() => (viewingItem = item)}>
								查看
							</button>
							<button
								type="button"
								class="design-history-restore"
								disabled={submitting || item.content === markdown}
								on:click={() => restoreHistory(item)}
							>
								{item.content === markdown ? '当前版本' : '恢复'}
							</button>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</section>
</div>

{#if editing}
	<div class="design-modal-backdrop">
		<button class="design-modal-dismiss" type="button" aria-label="关闭修改弹框" on:click={() => (editing = false)}></button>
		<div class="design-modal" role="dialog" tabindex="-1" aria-modal="true" aria-label="修改个人 Skill">
			<div class="design-modal-head">
				<div>
					<h2>{editMode === 'ai' ? 'AI 修改个人 Skill' : '修改个人 Skill'}</h2>
					<p>
						{editMode === 'ai'
							? '描述你想让 AI 如何修改，或直接编写新的技能内容。'
							: '使用 Markdown 描述你的工作方法。'}
					</p>
				</div>
				<button aria-label="关闭" on:click={() => (editing = false)}>×</button>
			</div>
			<textarea
				id="design-skill-textarea"
				rows="10"
				bind:value={draft}
				placeholder={editMode === 'ai' ? '输入 AI 修改要求或新的技能内容…' : ''}
				aria-label="Skill Markdown 内容"
			></textarea>
			<div class="design-modal-actions">
				<button on:click={() => (editing = false)}>取消</button>
				<button class="design-primary-button" disabled={!draft.trim()} on:click={submitEdit}>确认提交</button>
			</div>
		</div>
	</div>
{/if}

{#if viewingItem}
	<div class="design-modal-backdrop">
		<button class="design-modal-dismiss" type="button" aria-label="关闭查看弹框" on:click={() => (viewingItem = null)}></button>
		<div class="design-modal" role="dialog" tabindex="-1" aria-modal="true" aria-label="查看历史版本">
			<div class="design-modal-head">
				<div>
					<h2>历史版本 · {formatHistoryTime(viewingItem.savedAt)}</h2>
					<p>{viewingItem.source === 'ai' ? 'AI 修改生成' : '手动修改'} · 可在此查看内容，或恢复为当前版本</p>
				</div>
				<button aria-label="关闭" on:click={() => (viewingItem = null)}>×</button>
			</div>
			<pre class="design-history-viewer">{viewingItem.content}</pre>
			<div class="design-modal-actions">
				<button on:click={() => (viewingItem = null)}>关闭</button>
				<button
					class="design-primary-button"
					disabled={submitting || viewingItem.content === markdown}
					on:click={() => {
						if (!viewingItem) return;
						const item = viewingItem;
						viewingItem = null;
						void restoreHistory(item);
					}}
				>
					{viewingItem.content === markdown ? '当前版本' : '恢复此版本'}
				</button>
			</div>
		</div>
	</div>
{/if}

<style>
	.design-skill-action-buttons {
		display: flex;
		align-items: center;
		gap: 9px;
		flex: none;
	}

	.design-secondary-button {
		background: #eef3f1;
		color: #1e776d;
		border: 1px solid #d5e5e0;
		border-radius: 9px;
		padding: 10px 22px;
		font-size: 12px;
		font-weight: 600;
		transition: background 0.15s;
	}

	.design-secondary-button:hover:not(:disabled) {
		background: #e3efeb;
	}

	.design-secondary-button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.design-history-panel {
		margin-top: 14px;
	}

	.design-history-empty {
		padding: 30px 20px;
	}

	.design-history-list {
		display: flex;
		flex-direction: column;
	}

	.design-history-item {
		display: flex;
		align-items: center;
		gap: 12px;
		padding: 12px 4px;
		border-bottom: 1px solid #edf1f0;
	}

	.design-history-item:last-child {
		border-bottom: 0;
	}

	.design-history-index {
		flex: none;
		width: 30px;
		height: 30px;
		display: grid;
		place-items: center;
		border-radius: 9px;
		background: #eef4f2;
		color: #2e8375;
		font-size: 11px;
		font-weight: 700;
	}

	.design-history-info {
		flex: 1;
		min-width: 0;
		display: flex;
		align-items: center;
		gap: 10px;
	}

	.design-history-time {
		font-size: 12px;
		color: #364b51;
		white-space: nowrap;
	}

	.design-history-tag {
		flex: none;
		font-size: 10px;
		color: #4d8f83;
		background: #e6f2ee;
		border-radius: 999px;
		padding: 3px 9px;
		white-space: nowrap;
	}

	.design-history-tag.ai {
		color: #7465b2;
		background: #eeeafa;
	}

	.design-history-actions {
		flex: none;
		display: flex;
		align-items: center;
		gap: 6px;
	}

	.design-history-actions button {
		font-size: 11px;
		border-radius: 8px;
		padding: 6px 12px;
		transition: background 0.15s;
	}

	.design-history-view {
		color: #4a5a5e;
		background: #f2f6f5;
	}

	.design-history-view:hover {
		background: #e8efed;
	}

	.design-history-restore {
		color: #fff;
		background: #257e70;
	}

	.design-history-restore:hover:not(:disabled) {
		background: #17685c;
	}

	.design-history-restore:disabled {
		background: #aabbb7;
		cursor: not-allowed;
	}

	.design-history-viewer {
		width: 100%;
		max-height: 46vh;
		overflow: auto;
		margin: 0 0 17px;
		padding: 13px;
		background: #f7faf8;
		border: 1px solid #e9efec;
		border-radius: 10px;
		font-size: 13px;
		line-height: 1.7;
		color: #385058;
		white-space: pre-wrap;
		word-break: break-word;
	}

	:global(.dark) .design-secondary-button {
		background: #243331;
		color: #9fd4c9;
		border-color: #40504b;
	}

	:global(.dark) .design-secondary-button:hover:not(:disabled) {
		background: #2b3d3a;
	}

	:global(.dark) .design-history-item {
		border-color: #344244;
	}

	:global(.dark) .design-history-index {
		background: #22312f;
		color: #7fc3b5;
	}

	:global(.dark) .design-history-time {
		color: #dce9e5;
	}

	:global(.dark) .design-history-tag {
		background: #1f312e;
		color: #7fc3b5;
	}

	:global(.dark) .design-history-tag.ai {
		background: #2a2740;
		color: #a99de0;
	}

	:global(.dark) .design-history-view {
		background: #22302f;
		color: #d6e5e0;
	}

	:global(.dark) .design-history-view:hover {
		background: #2a3a38;
	}

	:global(.dark) .design-history-viewer {
		background: #1a2526;
		border-color: #334143;
		color: #cbdcd8;
	}
</style>
