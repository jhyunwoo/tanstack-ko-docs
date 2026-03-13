---
id: createMutation
title: createMutation
---




# 함수: createMutation()

```ts
function createMutation<TData, TError, TVariables, TContext>(options, queryClient?): CreateMutationResult<TData, TError, TVariables, TContext>;
```
정의 위치: [packages/svelte-query/src/createMutation.svelte.ts:17](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/createMutation.svelte.ts#L17)

## 타입 매개변수

### TData

`TData` = `unknown`

### TError

`TError` = `Error`

### T변수

`TVariables` = `void`

### TContext

`TContext` = `unknown`

## 매개변수

### 옵션

[Accessor](../../../../_source-only/docs/framework/svelte/reference/type-aliases/Accessor.md)\<[CreateMutationOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TContext`\>\>

mutation 옵션을 반환하는 함수

### queryClient?

[Accessor](../../../../_source-only/docs/framework/svelte/reference/type-aliases/Accessor.md)\<`QueryClient`\>

공급자를 재정의하는 사용자 정의 query 클라이언트

## 반환값

[CreateMutationResult](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateMutationResult.md)\<`TData`, `TError`, `TVariables`, `TContext`\>