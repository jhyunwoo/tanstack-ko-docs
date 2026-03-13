---
id: query-options
title: Query 옵션
---




여러 장소 간에 `queryKey` 및 `queryFn`를 공유하면서도 서로 같은 위치에 유지하는 가장 좋은 방법 중 하나는 `queryOptions` 도우미를 사용하는 것입니다. 런타임 시 이 도우미는 전달된 모든 것을 반환하지만 [TypeScript](../../react/typescript.md#typing-query-options) 사용할 때 많은 이점이 있습니다. query에 대해 가능한 모든 옵션을 한 곳에서 정의할 수 있으며 모든 옵션에 대한 유형 추론 및 유형 안전성도 얻을 수 있습니다.



```ts
import { queryOptions } from '@tanstack/vue-query'

function groupOptions(id: number) {
  return queryOptions({
    queryKey: ['groups', id],
    queryFn: () => fetchGroups(id),
    staleTime: 5 * 1000,
  })
}

// 용법:

useQuery(groupOptions(1))
useSuspenseQuery(groupOptions(5))
useQueries({
  queries: [groupOptions(1), groupOptions(2)],
})
queryClient.prefetchQuery(groupOptions(23))
queryClient.setQueryData(groupOptions(42).queryKey, newGroups)
```



Infinite Queries의 경우 별도의 [infiniteQueryOptions](../../react/reference/infiniteQueryOptions.md) 도우미를 사용할 수 있습니다.



여전히 구성 요소 수준에서 일부 옵션을 재정의할 수 있습니다. 매우 일반적이고 유용한 패턴은 구성 요소별 [`select`](../../react/guides/render-optimizations.md#select) 함수를 생성하는 것입니다.




```ts
// 유형 추론은 계속 작동하므로 query.data는 queryFn 대신 select의 반환 유형이 됩니다.

const query = useQuery({
  ...groupOptions(1),
  select: (data) => data.groupName,
})
```


