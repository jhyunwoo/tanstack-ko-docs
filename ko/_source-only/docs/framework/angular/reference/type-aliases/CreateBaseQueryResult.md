---
id: CreateBaseQueryResult
title: CreateBaseQueryResult
---




# 타입 별칭: CreateBaseQueryResult\<TData, TError, TState\>

```ts
type CreateBaseQueryResult<TData, TError, TState> = BaseQueryNarrowing<TData, TError> & MapToSignals<OmitKeyof<TState, keyof BaseQueryNarrowing, "safely">>;
```
정의 위치: [types.ts:98](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/types.ts#L98)

## 타입 매개변수

### TData

`TData` = `unknown`

### TError

`TError` = `DefaultError`

### TState

`TState` = `QueryObserverResult`\<`TData`, `TError`\>