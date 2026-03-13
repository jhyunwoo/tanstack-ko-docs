---
id: useSuspenseInfiniteQuery
title: useSuspenseInfiniteQuery
---





```tsx
const result = useSuspenseInfiniteQuery(options)
```
**옵션**

다음을 제외하고 [useInfiniteQuery](useInfiniteQuery.md)와 동일합니다.

- `suspense`
- `throwOnError`
- `enabled`
- `placeholderData`

**보고**

다음을 제외하고 [useInfiniteQuery](useInfiniteQuery.md)와 동일한 개체입니다.

- `data`는 정의가 보장됩니다.
- `isPlaceholderData`가 없습니다.
- `status`는 `success` 또는 `error`입니다.
  - 파생된 플래그가 그에 따라 설정됩니다.

**경고**

[취소](../guides/query-cancellation.md)가 작동하지 않습니다.