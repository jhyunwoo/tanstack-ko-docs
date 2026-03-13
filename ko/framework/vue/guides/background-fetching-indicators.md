---
id: background-fetching-indicators
title: 배경 가져오기 표시기
---




query의 `status === 'pending'` 상태는 query의 초기 하드 로딩 상태를 표시하기에 충분하지만 때로는 query가 백그라운드에서 다시 가져오고 있다는 추가 표시기를 표시할 수도 있습니다. 이를 위해 queries는 `status` 변수의 상태에 관계없이 가져오기 상태에 있음을 표시하는 데 사용할 수 있는 `isFetching` boolean도 제공합니다.



```vue
<script setup>
import { useQuery } from '@tanstack/vue-query'

const { isPending, isFetching, isError, data, error } = useQuery({
  queryKey: ['todos'],
  queryFn: getTodos,
})
</script>

<template>
  <div v-if="isFetching">Refreshing...</div>
  <span v-if="isPending">Loading...</span>
  <span v-else-if="isError">Error: {{ error.message }}</span>
  <!-- 이 시점에서 우리는 `isSuccess === true`라고 가정할 수 있습니다. -->
  <ul v-else-if="data">
    <li v-for="todo in data" :key="todo.id">{{ todo.title }}</li>
  </ul>
</template>
```



## 전역 배경 가져오기 로드 상태 표시

개별 query 로딩 상태 외에도 **모든** queries가 페치 중일 때(백그라운드 포함) 전역 로딩 표시기를 표시하려면 `useIsFetching` 후크를 사용할 수 있습니다.



```vue
<script setup>
import { useIsFetching } from '@tanstack/vue-query'

const isFetching = useIsFetching()
</script>

<template>
  <div v-if="isFetching">Queries are fetching in the background...</div>
</template>
```


