---
id: QueriesOptions
title: QueriesOptions
---




# 타입 별칭: QueriesOptions\<T, TResults, TDepth\>

```ts
type QueriesOptions<T, TResults, TDepth> = TDepth["length"] extends MAXIMUM_DEPTH ? UseQueryOptionsForUseQueries[] : T extends [] ? [] : T extends [infer Head] ? [...TResults, GetUseQueryOptionsForUseQueries<Head>] : T extends [infer Head, ...(infer Tails)] ? QueriesOptions<[...Tails], [...TResults, GetUseQueryOptionsForUseQueries<Head>], [...TDepth, 1]> : ReadonlyArray<unknown> extends T ? T : T extends UseQueryOptionsForUseQueries<infer TQueryFnData, infer TError, infer TData, infer TQueryKey>[] ? UseQueryOptionsForUseQueries<TQueryFnData, TError, TData, TQueryKey>[] : UseQueryOptionsForUseQueries[];
```
정의 위치: [preact-query/src/useQueries.ts:147](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useQueries.ts#L147)

QueriesOptions 감속기는 함수 인수를 반복적으로 풀어 타입 매개변수를 추론/적용합니다.

## 타입 매개변수

### 티

`T` *extends* `any`[]

### TResults

`TResults` *extends* `any`[] = \[\]

### T깊이

`TDepth` *extends* `ReadonlyArray`\<`number`\> = \[\]