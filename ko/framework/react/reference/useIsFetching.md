---
id: useIsFetching
title: useIsFetching
---




`useIsFetching`는 애플리케이션이 백그라운드에서 로드하거나 가져오는 queries의 `number`를 반환하는 선택적 후크입니다(앱 전체 로딩 표시기에 유용함).

```tsx
import { useIsFetching } from '@tanstack/react-query'
// 얼마나 많은 queries를 가져오고 있나요?
const isFetching = useIsFetching()
// 게시물 접두사와 일치하는 queries를 몇 개 가져오고 있습니까?
const isFetchingPosts = useIsFetching({ queryKey: ['posts'] })
```
**옵션**

- `filters?: QueryFilters`: [Query 필터](../guides/filters.md#query-필터)
- `queryClient?: QueryClient`
  - 사용자 정의 QueryClient를 사용하려면 이를 사용합니다. 그렇지 않으면 가장 가까운 컨텍스트의 컨텍스트가 사용됩니다.

**보고**

- `isFetching: number`
  - 애플리케이션이 현재 백그라운드에서 로드하거나 가져오는 queries의 `number`입니다.