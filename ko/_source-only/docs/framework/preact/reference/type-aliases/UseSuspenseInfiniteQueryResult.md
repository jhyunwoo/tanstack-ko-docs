---
id: UseSuspenseInfiniteQueryResult
title: UseSuspenseInfiniteQueryResult
---




# 타입 별칭: UseSuspenseInfiniteQueryResult\<TData, TError\>

```ts
type UseSuspenseInfiniteQueryResult<TData, TError> = OmitKeyof<DefinedInfiniteQueryObserverResult<TData, TError>, "isPlaceholderData" | "promise">;
```
정의 위치: [preact-query/src/types.ts:183](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/types.ts#L183)

## 타입 매개변수

### TData

`TData` = `unknown`

### TError

`TError` = `DefaultError`