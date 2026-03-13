---
id: DefinedCreateInfiniteQueryResult
title: DefinedCreateInfiniteQueryResult
---




# 타입 별칭: DefinedCreateInfiniteQueryResult\<TData, TError, TDefinedInfiniteQueryObserver\>

```ts
type DefinedCreateInfiniteQueryResult<TData, TError, TDefinedInfiniteQueryObserver> = MapToSignals<TDefinedInfiniteQueryObserver>;
```
정의 위치: [types.ts:123](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L123)

## 타입 매개변수

### TData

`TData` = `unknown`

### TError

`TError` = `DefaultError`

### TDefinedInfiniteQueryObserver

`TDefinedInfiniteQueryObserver` = `DefinedInfiniteQueryObserverResult`\<`TData`, `TError`\>