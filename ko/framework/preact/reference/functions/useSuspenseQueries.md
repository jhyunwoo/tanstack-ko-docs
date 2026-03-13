---
id: useSuspenseQueries
title: useSuspenseQueries
---




# 함수: useSuspenseQueries()

## 호출 시그니처

```ts
function useSuspenseQueries<T, TCombinedResult>(options, queryClient?): TCombinedResult;
```
정의 위치: [preact-query/src/useSuspenseQueries.ts:164](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useSuspenseQueries.ts#L164)

### 타입 매개변수

#### 티

`T` *extends* `any`[]

#### TCombinedResult

`TCombinedResult` = `T` *extends* \[\] ? \[\] : `T` *extends* \[`Head`\] ? \[`GetUseSuspenseQueryResult`\<`Head`\>\] : `T` *extends* \[`Head`, `...Tails[]`\] ? \[`...Tails[]`\] *extends* \[\] ? \[\] : \[`...Tails[]`\] *extends* \[`Head`\] ? \[`GetUseSuspenseQueryResult`\<`Head`\>, `GetUseSuspenseQueryResult`\<`Head`\>\] : \[`...Tails[]`\] *extends* \[`Head`, `...Tails[]`\] ? \[`...Tails[]`\] *extends* \[\] ? \[\] : \[`...Tails[]`\] *extends* \[`Head`\] ? \[`GetUseSuspenseQueryResult`\<`Head`\>, `GetUseSuspenseQueryResult`\<`Head`\>, `GetUseSuspenseQueryResult`\<`Head`\>\] : \[`...Tails[]`\] *extends* \[`Head`, `...Tails[]`\] ? \[`...(...)[]`\] *extends* \[\] ? \[\] : ... *extends* ... ? ... : ... : \[`...{ [K in (...)]: (...) }[]`\] : \[...\{ \[문자열의 K \| 번호 \| 기호\]: GetUseSuspenseQueryResult\<Tails\[K\<(...)\>\]\> \}\[\]\] : \{ \[K in string \| 번호 \| 기호\]: GetUseSuspenseQueryResult\<T\[K\<K\>\]\> \}

### 매개변수

#### 옵션

##### 결합하다?

(`result`) => `TCombinedResult`

##### queries

\| readonly \[`T` *extends* \[\] ? \[\] : `T` *extends* \[`Head`\] ? \[`GetUseSuspenseQueryOptions`\<`Head`\>\] : `T` *extends* \[`Head`, `...Tails[]`\] ? \[`...Tails[]`\] *extends* \[\] ? \[\] : \[`...Tails[]`\] *extends* \[`Head`\] ? \[`GetUseSuspenseQueryOptions`\<`Head`\>, `GetUseSuspenseQueryOptions`\<`Head`\>\] : \[`...Tails[]`\] *extends* \[`Head`, `...Tails[]`\] ? \[`...(...)[]`\] *extends* \[\] ? \[\] : ... *extends* ... ? ... : ... : ...[] *extends* \[`...(...)[]`\] ? \[`...(...)[]`\] : ... *extends* ... ? ... : ... : `unknown`[] *extends* `T` ? `T` : `T` *extends* [UseSuspenseQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseSuspenseQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>[] ? [UseSuspenseQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseSuspenseQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>[]: [UseSuspenseQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseSuspenseQueryOptions.md)\<`unknown`, `Error`, `unknown`, readonly ...[]\>[]\]
  \| readonly \[\{ \[K 문자열 \| 번호 \| 기호\]: GetUseSuspenseQueryOptions\<T\[K\<K\>\]\> \}\]

#### queryClient?

`QueryClient`

### 반환값

`TCombinedResult`

## 호출 시그니처

```ts
function useSuspenseQueries<T, TCombinedResult>(options, queryClient?): TCombinedResult;
```
정의 위치: [preact-query/src/useSuspenseQueries.ts:177](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useSuspenseQueries.ts#L177)

### 타입 매개변수

#### 티

`T` *extends* `any`[]

#### TCombinedResult

`TCombinedResult` = `T` *extends* \[\] ? \[\] : `T` *extends* \[`Head`\] ? \[`GetUseSuspenseQueryResult`\<`Head`\>\] : `T` *extends* \[`Head`, `...Tails[]`\] ? \[`...Tails[]`\] *extends* \[\] ? \[\] : \[`...Tails[]`\] *extends* \[`Head`\] ? \[`GetUseSuspenseQueryResult`\<`Head`\>, `GetUseSuspenseQueryResult`\<`Head`\>\] : \[`...Tails[]`\] *extends* \[`Head`, `...Tails[]`\] ? \[`...Tails[]`\] *extends* \[\] ? \[\] : \[`...Tails[]`\] *extends* \[`Head`\] ? \[`GetUseSuspenseQueryResult`\<`Head`\>, `GetUseSuspenseQueryResult`\<`Head`\>, `GetUseSuspenseQueryResult`\<`Head`\>\] : \[`...Tails[]`\] *extends* \[`Head`, `...Tails[]`\] ? \[`...(...)[]`\] *extends* \[\] ? \[\] : ... *extends* ... ? ... : ... : \[`...{ [K in (...)]: (...) }[]`\] : \[...\{ \[문자열의 K \| 번호 \| 기호\]: GetUseSuspenseQueryResult\<Tails\[K\<(...)\>\]\> \}\[\]\] : \{ \[K in string \| 번호 \| 기호\]: GetUseSuspenseQueryResult\<T\[K\<K\>\]\> \}

### 매개변수

#### 옵션

##### 결합하다?

(`result`) => `TCombinedResult`

##### queries

readonly \[`T` *extends* \[\] ? \[\] : `T` *extends* \[`Head`\] ? \[`GetUseSuspenseQueryOptions`\<`Head`\>\] : `T` *extends* \[`Head`, `...Tails[]`\] ? \[`...Tails[]`\] *extends* \[\] ? \[\] : \[`...Tails[]`\] *extends* \[`Head`\] ? \[`GetUseSuspenseQueryOptions`\<`Head`\>, `GetUseSuspenseQueryOptions`\<`Head`\>\] : \[`...Tails[]`\] *extends* \[`Head`, `...Tails[]`\] ? \[`...Tails[]`\] *extends* \[\] ? \[\] : \[`...(...)[]`\] *extends* \[...\] ? \[..., ..., ...\] : ... *extends* ... ? ... : ... : `unknown`[] *extends* \[`...Tails[]`\] ? \[`...Tails[]`\] : \[`...(...)[]`\] *extends* ...[] ? ...[] : ...[] : `unknown`[] *extends* `T` ? `T` : `T` *extends* [UseSuspenseQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseSuspenseQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>[] ? [UseSuspenseQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseSuspenseQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`\>[]: [UseSuspenseQueryOptions](../../../../_source-only/docs/framework/preact/reference/interfaces/UseSuspenseQueryOptions.md)\<`unknown`, `Error`, `unknown`, readonly `unknown`[]\>[]\]

#### queryClient?

`QueryClient`

### 반환값

`TCombinedResult`