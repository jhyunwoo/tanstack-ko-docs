---
id: QueriesResults
title: QueriesResults
---




# 타입 별칭: QueriesResults\<T, TResults, TDepth\>

```ts
type QueriesResults<T, TResults, TDepth> = TDepth["length"] extends MAXIMUM_DEPTH ? CreateQueryResult[] : T extends [] ? [] : T extends [infer Head] ? [...TResults, GetCreateQueryResult<Head>] : T extends [infer Head, ...(infer Tails)] ? QueriesResults<[...Tails], [...TResults, GetCreateQueryResult<Head>], [...TDepth, 1]> : { [K in keyof T]: GetCreateQueryResult<T[K]> };
```
정의 위치: [packages/svelte-query/src/createQueries.svelte.ts:171](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/svelte-query/src/createQueries.svelte.ts#L171)

QueriesResults 감속기는 타입 매개변수를 결과에 재귀적으로 매핑합니다.

## 타입 매개변수

### 티

`T` *extends* `any`[]

### TResults

`TResults` *extends* `any`[] = \[\]

### T깊이

`TDepth` *extends* `ReadonlyArray`\<`number`\> = \[\]