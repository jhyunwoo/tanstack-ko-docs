---
id: UseSuspenseQueryResult
title: UseSuspenseQueryResult
---




# 타입 별칭: UseSuspenseQueryResult\<TData, TError\>

```ts
type UseSuspenseQueryResult<TData, TError> = DistributiveOmit<DefinedQueryObserverResult<TData, TError>, "isPlaceholderData" | "promise">;
```
정의 위치: [preact-query/src/types.ts:160](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/types.ts#L160)

## 타입 매개변수

### TData

`TData` = `unknown`

### TError

`TError` = `DefaultError`