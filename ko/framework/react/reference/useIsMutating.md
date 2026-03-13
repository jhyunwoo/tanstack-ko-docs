---
id: useIsMutating
title: useIsMutating
---




`useIsMutating`는 애플리케이션이 가져오는 mutations의 `number`를 반환하는 선택적 후크입니다(앱 전체 로딩 표시기에 유용함).

```tsx
import { useIsMutating } from '@tanstack/react-query'
// 얼마나 많은 mutations를 가져오고 있나요?
const isMutating = useIsMutating()
// 게시물 접두사와 일치하는 mutations를 몇 개 가져오나요?
const isMutatingPosts = useIsMutating({ mutationKey: ['posts'] })
```
**옵션**

- `filters?: MutationFilters`: [Mutation 필터](../guides/filters.md#mutation-필터)
- `queryClient?: QueryClient`
  - 사용자 정의 QueryClient를 사용하려면 이를 사용합니다. 그렇지 않으면 가장 가까운 컨텍스트의 컨텍스트가 사용됩니다.

**보고**

- `isMutating: number`
  - 귀하의 애플리케이션이 현재 가져오는 mutations의 `number`가 됩니다.