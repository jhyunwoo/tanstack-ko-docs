---
id: SuspenseQueriesOptions
title: SuspenseQueriesOptions
---




# 타입 별칭: SuspenseQueriesOptions\<T, TResults, TDepth\>

```ts
type SuspenseQueriesOptions<T, TResults, TDepth> = TDepth["length"] extends MAXIMUM_DEPTH ? UseSuspenseQueryOptions[] : T extends [] ? [] : T extends [infer Head] ? [...TResults, GetUseSuspenseQueryOptions<Head>] : T extends [infer Head, ...(infer Tails)] ? SuspenseQueriesOptions<[...Tails], [...TResults, GetUseSuspenseQueryOptions<Head>], [...TDepth, 1]> : unknown[] extends T ? T : T extends UseSuspenseQueryOptions<infer TQueryFnData, infer TError, infer TData, infer TQueryKey>[] ? UseSuspenseQueryOptions<TQueryFnData, TError, TData, TQueryKey>[] : UseSuspenseQueryOptions[];
```
정의 위치: [preact-query/src/useSuspenseQueries.ts:109](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useSuspenseQueries.ts#L109)

SuspenseQueriesOptions 감속기는 함수 인수를 반복적으로 풀어 타입 매개변수를 추론/적용합니다.

## 타입 매개변수

### 티

`T` *extends* `any`[]

### TResults

`TResults` *extends* `any`[] = \[\]

### T깊이

`TDepth` *extends* `ReadonlyArray`\<`number`\> = \[\]