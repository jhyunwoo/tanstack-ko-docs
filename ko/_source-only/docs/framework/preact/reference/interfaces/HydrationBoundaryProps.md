---
id: HydrationBoundaryProps
title: HydrationBoundaryProps
---




# 인터페이스: HydrationBoundaryProps

정의 위치: [preact-query/src/HydrationBoundary.tsx:12](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/HydrationBoundary.tsx#L12)

## 속성

### 어린이들?

```ts
optional children: ComponentChildren;
```
정의 위치: [preact-query/src/HydrationBoundary.tsx:20](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/HydrationBoundary.tsx#L20)

***

### 옵션?

```ts
optional options: OmitKeyof<HydrateOptions, "defaultOptions"> & object;
```
정의 위치: [preact-query/src/HydrationBoundary.tsx:14](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/HydrationBoundary.tsx#L14)

#### 유형 선언

##### defaultOptions?

```ts
optional defaultOptions: OmitKeyof<{
}, "mutations">;
```
***

### queryClient?

```ts
optional queryClient: QueryClient;
```
정의 위치: [preact-query/src/HydrationBoundary.tsx:21](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/HydrationBoundary.tsx#L21)

***

### 상태

```ts
state: DehydratedState | null | undefined;
```
정의 위치: [preact-query/src/HydrationBoundary.tsx:13](https://github.com/theVedanta/query/blob/main/packages/preact-query/src/HydrationBoundary.tsx#L13)