---
id: useSuspenseQueries
title: useSuspenseQueries
---





```tsx
const result = useSuspenseQueries(options)
```
**옵션**

각 `query`가 다음을 가질 수 없다는 점을 제외하면 [useQueries](useQueries.md)와 동일합니다.

- `suspense`
- `throwOnError`
- `enabled`
- `placeholderData`

**보고**

각 `query`에 대해 다음을 제외하고 [useQueries](useQueries.md)와 구조가 동일합니다.

- `data`는 정의가 보장됩니다.
- `isPlaceholderData`가 없습니다.
- `status`는 `success` 또는 `error`입니다.
  - 파생된 플래그가 그에 따라 설정됩니다.

**주의사항**

구성 요소는 **모든 queries** 로드가 완료된 후에만 다시 마운트된다는 점을 명심하세요. 따라서 모든 queries를 완료하는 데 걸린 시간 동안 query가 오래되면 다시 마운트할 때 다시 가져옵니다. 이를 방지하려면 `staleTime`를 충분히 높게 설정하십시오.

[취소](../guides/query-cancellation.md)가 작동하지 않습니다.