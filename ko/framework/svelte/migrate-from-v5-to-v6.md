Svelte v5는 Svelte v3/v4의 Store 구문과 레거시 호환성을 갖고 있지만 이 어댑터에서는 다소 버그가 있었고 신뢰할 수 없었습니다. `@tanstack/svelte-query` v6 어댑터는 신호에 의존하는 룬 구문으로 완전히 마이그레이션됩니다. 또한 이번 재작성은 query 입력이 계속 반응하도록 보장하는 데 필요한 코드를 단순화해야 합니다.

## 설치

프로젝트에 [Svelte v5.25.0](https://github.com/sveltejs/svelte/releases/tag/svelte%405.25.0) 이상이 있는지 확인하세요.

`pnpm add @tanstack/svelte-query@latest`(또는 패키지 관리자의 이에 상응하는 항목)를 실행합니다.

> `@tanstack/svelte-query` v6은 `@tanstack/query-core` v5에 종속됩니다.

## 기능 입력

Angular 및 Solid 어댑터와 마찬가지로 Svelte 어댑터의 대부분 기능에는 이제 반응성을 제공하기 위해 "썽크"(`() => options`)로 제공되는 옵션이 필요합니다. TypeScript는 여기에서 여러분의 친구가 되어 이 표기법이 누락된 경우 경고합니다.

```ts
- const query = createQuery({  // [!코드-]
+ const query = createQuery(() => ({ // [!코드 ++]
    queryKey: ['todos'],
    queryFn: () => fetchTodos(),
- }) // [!코드-]
+ })) // [!코드 ++]
```
## 속성에 접근하기

어댑터가 더 이상 저장소를 사용하지 않는 경우 더 이상 `$` 접두사를 붙일 필요가 없습니다.

```svelte
- {#if $todos.isSuccess} // [!코드-]
+ {#if todos.isSuccess} // [!코드 ++]
    <ul>
-     {#each $todos.data.items as item} // [!코드-]
+     {#each todos.data.items as item} // [!코드 ++]
        <li>{item}</li>
      {/each}
    </ul>
  {/if}
```
## 반응성

이전에는 입력에 대한 반응성을 달성하기 위해 매장에서 몇 가지 펑키한 작업을 수행해야 했습니다. 더 이상 그렇지 않습니다! `$derived`에 query를 포장할 필요조차 없습니다.

```ts
- const intervalMs = writable(1000) // [!코드-]
+ let intervalMs = $state(1000) // [!코드 ++]

- const query = createQuery(derived(intervalMs, ($intervalMs) => ({ // [!코드-]
+ const query = createQuery(() => ({ // [!코드 ++]
    queryKey: ['refetch'],
    queryFn: async () => await fetch('/api/data').then((r) => r.json()),
-   refetchInterval: $intervalMs, // [!코드-]
+   refetchInterval: intervalMs, // [!코드 ++]
- }))) // [!코드-]
+ })) // [!코드 ++]
```
## 레거시 모드 비활성화

구성 요소에 저장소가 있는 경우 룬 모드로 제대로 전환되지 않을 수 있습니다. 다음 두 가지 방법으로 애플리케이션이 룬을 사용하고 있는지 확인할 수 있습니다.

### 파일별로

각 `.svelte` 파일에서 룬으로 마이그레이션한 후 `<svelte:options runes={true} />`를 추가합니다. 이는 점진적인 마이그레이션이 필요한 대규모 애플리케이션에 더 좋습니다.

### 프로젝트 전체 기준

`svelte.config.js`에서 구성에 다음을 추가합니다.

```json
  compilerOptions: {
    runes: true,
  },
```
앱에서 상점 구문을 100% 제거한 후에 추가할 수 있습니다.