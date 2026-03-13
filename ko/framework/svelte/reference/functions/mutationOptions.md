---
id: mutationOptions
title: mutationOptions
---




# 함수: mutationOptions()

## 호출 시그니처

```ts
function mutationOptions<TData, TError, TVariables, TOnMutateResult>(options): WithRequired<CreateMutationOptions<TData, TError, TVariables, TOnMutateResult>, 'mutationKey'>
```
정의 위치: [packages/svelte-query/src/mutationOptions.ts](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/mutationOptions.ts)

### 타입 매개변수

#### TData

`TData` = `unknown`

#### TError

`TError` = `Error`

#### T변수

`TVariables` = `void`

#### TOnMutateResult

`TOnMutateResult` = `unknown`

### 매개변수

#### 옵션

`WithRequired`\<[CreateMutationOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>, `'mutationKey'`\>

### 반환값

`WithRequired`\<[CreateMutationOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>, `'mutationKey'`\>

## 호출 시그니처

```ts
function mutationOptions<TData, TError, TVariables, TOnMutateResult>(options): Omit<CreateMutationOptions<TData, TError, TVariables, TOnMutateResult>, 'mutationKey'>
```
정의 위치: [packages/svelte-query/src/mutationOptions.ts](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/mutationOptions.ts)

### 타입 매개변수

#### TData

`TData` = `unknown`

#### TError

`TError` = `Error`

#### T변수

`TVariables` = `void`

#### TOnMutateResult

`TOnMutateResult` = `unknown`

### 매개변수

#### 옵션

`Omit`\<[CreateMutationOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>, `'mutationKey'`\>

### 반환값

`Omit`\<[CreateMutationOptions](../../../../_source-only/docs/framework/svelte/reference/type-aliases/CreateMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>, `'mutationKey'`\>