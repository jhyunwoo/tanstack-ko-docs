---
id: suspense
title: Suspense(실험적)
---




> 참고: Vue Query에 대한 Suspense 모드는 Vue의 Suspense 자체와 동일하게 실험적입니다. 이러한 API는 변경될 예정이며 Vue 및 Vue Query 버전을 서로 호환되는 패치 수준 버전으로 잠그지 않는 한 프로덕션에서 사용해서는 안 됩니다.

Vue Query는 Vue의 새로운 [Suspense](https://vuejs.org/guide/built-ins/suspense.html) API와 함께 사용할 수도 있습니다.

그렇게 하려면 Vue에서 제공하는 `Suspense` 구성 요소로 일시 중단 가능한 구성 요소를 래핑해야 합니다.

```vue
<script setup>
import SuspendableComponent from './SuspendableComponent.vue'
</script>

<template>
  <Suspense>
    <template #default>
      <SuspendableComponent />
    </template>
    <template #fallback>
      <div>Loading...</div>
    </template>
  </Suspense>
</template>
```
일시 중단 가능한 구성 요소의 `setup` 기능을 `async`로 변경하세요. 그런 다음 `vue-query`에서 제공하는 비동기 `suspense` 기능을 사용할 수 있습니다.

```vue
<script>
import { defineComponent } from 'vue'
import { useQuery } from '@tanstack/vue-query'

const todoFetcher = async () =>
  await fetch('https://jsonplaceholder.cypress.io/todos').then((response) =>
    response.json(),
  )
export default defineComponent({
  name: 'SuspendableComponent',
  async setup() {
    const { data, suspense } = useQuery(['todos'], todoFetcher)
    await suspense()

    return { data }
  },
})
</script>
```
## 렌더링할 때 가져오기 vs 가져올 때 렌더링

기본적으로 `suspense` 모드의 Vue Query는 추가 구성 없이 **Fetch-on-render** 솔루션으로 매우 잘 작동합니다. 이는 구성요소가 마운트를 시도할 때 query 가져오기 및 일시중단을 트리거하지만 해당 구성요소를 가져오고 마운트한 후에만 가능함을 의미합니다. 다음 단계로 나아가서 **가져오는 대로 렌더링** 모델을 구현하려면 라우팅 콜백 및/또는 사용자 상호 작용 이벤트에 [프리페칭](prefetching.md)을 구현하여 queries가 마운트되기 전, 상위 구성 요소 가져오기 또는 마운트를 시작하기 전에 로드를 시작하는 것이 좋습니다.