---
id: infinite-query-property-order
title: 무한 queries에 대한 추론 민감 속성의 올바른 순서를 보장합니다.
---




다음 함수의 경우 유형 추론으로 인해 전달된 객체의 속성 순서가 중요합니다.

- `useInfiniteQuery`
- `useSuspenseInfiniteQuery`
- `infiniteQueryOptions`

올바른 속성 순서는 다음과 같습니다.

- `queryFn`
- `getPreviousPageParam`
- `getNextPageParam`

다른 모든 속성은 유형 추론에 의존하지 않으므로 순서에 영향을 받지 않습니다.

## 규칙 세부정보

이 규칙에 대한 **잘못된** 코드의 예:

```tsx
/* eslint "@tanstack/query/infinite-query-property-order": "경고" */
import { useInfiniteQuery } from '@tanstack/react-query'

const query = useInfiniteQuery({
  queryKey: ['projects'],
  getNextPageParam: (lastPage) => lastPage.nextId ?? undefined,
  queryFn: async ({ pageParam }) => {
    const response = await fetch(`/api/projects?cursor=${pageParam}`)
    return await response.json()
  },
  initialPageParam: 0,
  getPreviousPageParam: (firstPage) => firstPage.previousId ?? undefined,
  maxPages: 3,
})
```
이 규칙에 대한 **올바른** 코드의 예:

```tsx
/* eslint "@tanstack/query/infinite-query-property-order": "경고" */
import { useInfiniteQuery } from '@tanstack/react-query'

const query = useInfiniteQuery({
  queryKey: ['projects'],
  queryFn: async ({ pageParam }) => {
    const response = await fetch(`/api/projects?cursor=${pageParam}`)
    return await response.json()
  },
  initialPageParam: 0,
  getPreviousPageParam: (firstPage) => firstPage.previousId ?? undefined,
  getNextPageParam: (lastPage) => lastPage.nextId ?? undefined,
  maxPages: 3,
})
```
## 속성

- [x] ✅ 추천
- [x] 🔧 수정 가능