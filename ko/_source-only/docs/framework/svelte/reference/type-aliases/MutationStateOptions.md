---
id: MutationStateOptions
title: MutationStateOptions
---




# 타입 별칭: MutationStateOptions\<TResult\>

```ts
type MutationStateOptions<TResult> = object;
```
정의 위치: [packages/svelte-query/src/types.ts:140](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/types.ts#L140)

useMutationState에 대한 옵션

## 타입 매개변수

### TResult

`TResult` = `MutationState`

## 속성

### 필터?

```ts
optional filters: MutationFilters;
```
정의 위치: [packages/svelte-query/src/types.ts:141](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/types.ts#L141)

***

### select()?

```ts
optional select: (mutation) => TResult;
```
정의 위치: [packages/svelte-query/src/types.ts:142](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/types.ts#L142)

#### 매개변수

##### mutation

`Mutation`\<`unknown`, `DefaultError`, `unknown`, `unknown`\>

#### 반환값

`TResult`