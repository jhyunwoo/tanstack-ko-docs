---
id: QueriesObserver
title: QueriesObserver
---




## `QueriesObserver`

`QueriesObserver`는 여러 queries를 관찰하는 데 사용할 수 있습니다.

```tsx
const observer = new QueriesObserver(queryClient, [
  { queryKey: ['post', 1], queryFn: fetchPost },
  { queryKey: ['post', 2], queryFn: fetchPost },
])

const unsubscribe = observer.subscribe((result) => {
  console.log(result)
  unsubscribe()
})
```
**옵션**

`QueriesObserver`의 옵션은 [useQueries](../framework/react/reference/useQueries.md)의 옵션과 정확히 동일합니다.