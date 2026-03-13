---
id: suspense
title: Suspense
---




Solid Query는 Solid의 [Suspense](https://docs.solidjs.com/reference/comComponents/suspense) API와 함께 사용할 수도 있습니다.

그렇게 하려면 일시 중단 가능한 구성 요소를 Solid에서 제공하는 `Suspense` 구성 요소로 래핑해야 합니다.

```tsx
import { Suspense } from 'solid-js'
;<Suspense fallback={<LoadingSpinner />}>
  <SuspendableComponent />
</Suspense>
```
`solid-query`에서 제공하는 비동기 `suspense` 기능을 사용할 수 있습니다.

```tsx
import { useQuery } from '@tanstack/solid-query'

const todoFetcher = async () =>
  await fetch('https://jsonplaceholder.cypress.io/todos').then((response) =>
    response.json(),
  )

function SuspendableComponent() {
  const todosQuery = useQuery(() => ({
    queryKey: ['todos'],
    queryFn: todoFetcher,
  }))

  // <Suspense> 경계 내에서 직접 todosQuery.data에 액세스
  // 데이터가 준비될 때까지 자동으로 정지를 트리거합니다.
  return <div>Data: {JSON.stringify(todosQuery.data)}</div>
}
```
## 렌더링할 때 가져오기 vs 가져올 때 렌더링

기본적으로 `suspense` 모드의 Solid Query는 추가 구성 없이 **Fetch-on-render** 솔루션으로 매우 잘 작동합니다. 이는 구성요소가 마운트를 시도할 때 query 가져오기 및 일시중단을 트리거하지만 해당 구성요소를 가져오고 마운트한 후에만 가능함을 의미합니다. 다음 단계로 나아가서 **가져오는 대로 렌더링** 모델을 구현하려면 라우팅 콜백 및/또는 사용자 상호 작용 이벤트에 [프리페칭](prefetching.md)을 구현하여 queries가 마운트되기 전, 상위 구성 요소 가져오기 또는 마운트를 시작하기 전에 로드를 시작하는 것이 좋습니다.