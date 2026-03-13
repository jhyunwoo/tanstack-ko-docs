---
id: QueriesResults
title: QueriesResults
---




# 타입 별칭: QueriesResults\<T, TResults, TDepth\>

```ts
type QueriesResults<T, TResults, TDepth> = TDepth["length"] extends MAXIMUM_DEPTH ? UseQueryResult[] : T extends [] ? [] : T extends [infer Head] ? [...TResults, GetUseQueryResult<Head>] : T extends [infer Head, ...(infer Tails)] ? QueriesResults<[...Tails], [...TResults, GetUseQueryResult<Head>], [...TDepth, 1]> : { [K in keyof T]: GetUseQueryResult<T[K]> };
```
정의 위치: [preact-query/src/useQueries.ts:189](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/useQueries.ts#L189)

QueriesResults 감속기는 타입 매개변수를 결과에 재귀적으로 매핑합니다.

## 타입 매개변수

### 티

`T` *extends* `any`[]

### TResults

`TResults` *extends* `any`[] = \[\]

### T깊이

`TDepth` *extends* `ReadonlyArray`\<`number`\> = \[\]