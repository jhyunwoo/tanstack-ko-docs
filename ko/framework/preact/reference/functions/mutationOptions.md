---
id: mutationOptions
title: mutationOptions
---




# 함수: mutationOptions()

## 호출 시그니처

```ts
function mutationOptions<TData, TError, TVariables, TOnMutateResult>(options): WithRequired<UseMutationOptions<TData, TError, TVariables, TOnMutateResult>, "mutationKey">;
```
정의 위치: [preact-query/src/mutationOptions.ts:4](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/mutationOptions.ts#L4)

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

`WithRequired`\<[UseMutationOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>, `"mutationKey"`\>

### 반환값

`WithRequired`\<[UseMutationOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>, `"mutationKey"`\>

## 호출 시그니처

```ts
function mutationOptions<TData, TError, TVariables, TOnMutateResult>(options): Omit<UseMutationOptions<TData, TError, TVariables, TOnMutateResult>, "mutationKey">;
```
정의 위치: [preact-query/src/mutationOptions.ts:18](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/mutationOptions.ts#L18)

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

`Omit`\<[UseMutationOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>, `"mutationKey"`\>

### 반환값

`Omit`\<[UseMutationOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseMutationOptions.md)\<`TData`, `TError`, `TVariables`, `TOnMutateResult`\>, `"mutationKey"`\>