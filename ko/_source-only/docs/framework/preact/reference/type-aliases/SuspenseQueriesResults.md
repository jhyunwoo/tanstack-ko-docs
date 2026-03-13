---
id: SuspenseQueriesResults
title: SuspenseQueriesResults
---




# 타입 별칭: SuspenseQueriesResults\<T, TResults, TDepth\>

```ts
type SuspenseQueriesResults<T, TResults, TDepth> = TDepth["length"] extends MAXIMUM_DEPTH ? UseSuspenseQueryResult[] : T extends [] ? [] : T extends [infer Head] ? [...TResults, GetUseSuspenseQueryResult<Head>] : T extends [infer Head, ...(infer Tails)] ? SuspenseQueriesResults<[...Tails], [...TResults, GetUseSuspenseQueryResult<Head>], [...TDepth, 1]> : { [K in keyof T]: GetUseSuspenseQueryResult<T[K]> };
```
정의 위치: [preact-query/src/useSuspenseQueries.ts:146](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useSuspenseQueries.ts#L146)

SuspenseQueriesResults 감속기는 타입 매개변수를 결과에 반복적으로 매핑합니다.

## 타입 매개변수

### 티

`T` *extends* `any`[]

### TResults

`TResults` *extends* `any`[] = \[\]

### T깊이

`TDepth` *extends* `ReadonlyArray`\<`number`\> = \[\]