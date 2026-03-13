---
id: quick-start
title: 빠른 시작
---




이 코드 조각은 Vue Query의 3가지 핵심 개념을 매우 간략하게 보여줍니다.

- [Queries](../react/guides/queries.md)
- [Mutations](../react/guides/mutations.md)
- [Query 무효화](../react/guides/query-invalidation.md)



완벽하게 작동하는 예제를 찾고 있다면 [기본 코드샌드박스 예제](examples/basic.md)를 살펴보세요.

```vue
<script setup>
import { useQueryClient, useQuery, useMutation } from '@tanstack/vue-query'

// QueryClient 인스턴스에 액세스
const queryClient = useQueryClient()

// Query
const { isPending, isError, data, error } = useQuery({
  queryKey: ['todos'],
  queryFn: getTodos,
})

// Mutation
const mutation = useMutation({
  mutationFn: postTodo,
  onSuccess: () => {
    // 무효화하고 다시 가져오기
    queryClient.invalidateQueries({ queryKey: ['todos'] })
  },
})

function onButtonClick() {
  mutation.mutate({
    id: Date.now(),
    title: 'Do Laundry',
  })
}
</script>

<template>
  <span v-if="isPending">Loading...</span>
  <span v-else-if="isError">Error: {{ error.message }}</span>
  <!-- 이 시점에서 우리는 `isSuccess === true`라고 가정할 수 있습니다. -->
  <ul v-else>
    <li v-for="todo in data" :key="todo.id">{{ todo.title }}</li>
  </ul>
  <button @click="onButtonClick">Add Todo</button>
</template>
```



이 세 가지 개념이 Vue Query의 핵심 기능의 대부분을 구성합니다. 문서의 다음 섹션에서는 이러한 핵심 개념 각각에 대해 자세히 설명합니다.