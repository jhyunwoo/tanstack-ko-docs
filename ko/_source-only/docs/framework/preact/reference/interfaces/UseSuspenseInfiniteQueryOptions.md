---
id: UseSuspenseInfiniteQueryOptions
title: UseSuspenseInfiniteQueryOptions
---




# 인터페이스: UseSuspenseInfiniteQueryOptions\<TQueryFnData, TError, TData, TQueryKey, TPageParam\>

정의 위치: [preact-query/src/types.ts:128](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/types.ts#L128)

## 확장

- `OmitKeyof`\<[UseInfiniteQueryOptions](UseInfiniteQueryOptions.md)\<`TQueryFnData`, `TError`, `TData`, `TQueryKey`, `TPageParam`\>, `"queryFn"` \| `"enabled"` \| `"throwOnError"` \| `"placeholderData"`\>

## 타입 매개변수

### TQueryFnData

`TQueryFnData` = `unknown`

### TError

`TError` = `DefaultError`

### TData

`TData` = `TQueryFnData`

### TQueryKey

`TQueryKey` *extends* `QueryKey` = `QueryKey`

### TPageParam

`TPageParam` = `unknown`

## 속성

### queryFn?

```ts
optional queryFn: QueryFunction<TQueryFnData, TQueryKey, TPageParam>;
```
정의 위치: [preact-query/src/types.ts:138](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/types.ts#L138)

***

### 구독하셨나요?

```ts
optional subscribed: boolean;
```
정의 위치: [preact-query/src/types.ts:123](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/types.ts#L123)

query 캐시 업데이트에서 이 관찰자의 구독을 취소하려면 이를 `false`로 설정합니다.
기본값은 `true`입니다.

#### 상속됨

```ts
OmitKeyof.subscribed
```
