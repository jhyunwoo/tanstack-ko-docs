---
id: CreateInfiniteQueryResult
title: CreateInfiniteQueryResult
---




# 타입 별칭: CreateInfiniteQueryResult\<TData, TError\>

```ts
type CreateInfiniteQueryResult<TData, TError> = BaseQueryNarrowing<TData, TError> & MapToSignals<InfiniteQueryObserverResult<TData, TError>>;
```
정의 위치: [types.ts:117](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L117)

## 타입 매개변수

### TData

`TData` = `unknown`

### TError

`TError` = `DefaultError`