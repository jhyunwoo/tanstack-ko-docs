---
id: UseBaseQueryOptions
title: UseBaseQueryOptions
---




# 인터페이스: UseBaseQueryOptions\<TQueryFnData, TError, TData, TQueryData, TQueryKey\>

정의 위치: [preact-query/src/types.ts:29](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/types.ts#L29)

## 확장

- `QueryObserverOptions`\<`TQueryFnData`, `TError`, `TData`, `TQueryData`, `TQueryKey`\>

## 타입 매개변수

### TQueryFnData

`TQueryFnData` = `unknown`

### TError

`TError` = `DefaultError`

### TData

`TData` = `TQueryFnData`

### TQueryData

`TQueryData` = `TQueryFnData`

### TQueryKey

`TQueryKey` *extends* `QueryKey` = `QueryKey`

## 속성

### 구독하셨나요?

```ts
optional subscribed: boolean;
```
정의 위치: [preact-query/src/types.ts:46](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/types.ts#L46)

query 캐시 업데이트에서 이 관찰자의 구독을 취소하려면 이를 `false`로 설정합니다.
기본값은 `true`입니다.