---
id: QueryObserver
title: QueryObserver
---




`QueryObserver`는 queries를 관찰하고 전환하는 데 사용할 수 있습니다.

```tsx
const observer = new QueryObserver(queryClient, { queryKey: ['posts'] })

const unsubscribe = observer.subscribe((result) => {
  console.log(result)
  unsubscribe()
})
```
**옵션**

`QueryObserver`의 옵션은 [useQuery](../framework/react/reference/useQuery.md)의 옵션과 정확히 동일합니다.