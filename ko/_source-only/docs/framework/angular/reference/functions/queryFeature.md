---
id: queryFeature
title: queryFeature
---




# 함수: queryFeature()

```ts
function queryFeature<TFeatureKind>(kind, providers): QueryFeature<TFeatureKind>;
```
정의 위치: [providers.ts:146](https://github.com/TanStack/query/blob/489359a569fd865f3afd7aac8fa43dfc429309e3/packages/angular-query-experimental/src/providers.ts#L146)

Query 기능을 나타내는 개체를 생성하는 도우미 함수입니다.

## 타입 매개변수

### TFeatureKind

`TFeatureKind` *extends* `"Devtools"` \| `"PersistQueryClient"`

## 매개변수

### 친절한

`TFeatureKind`

### 제공업체

`Provider`[]

## 반환값

[QueryFeature](../interfaces/QueryFeature.md)\<`TFeatureKind`\>

Query 기능.