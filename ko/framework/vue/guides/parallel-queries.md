---
id: parallel-queries
title: 병렬 Queries
---




"병렬" queries는 동시에 가져오기를 최대화하기 위해 병렬로 또는 동시에 실행되는 queries입니다.

## 수동 병렬 Queries

병렬 queries의 개수가 변하지 않으면 **추가 노력** 없이 병렬 queries를 사용할 수 있습니다. TanStack Query의 `useQuery` 및 `useInfiniteQuery` 후크를 원하는 만큼 나란히 사용하세요!



```vue
<script setup lang="ts">
// 다음 queries는 병렬로 실행됩니다.
const usersQuery = useQuery({ queryKey: ['users'], queryFn: fetchUsers })
const teamsQuery = useQuery({ queryKey: ['teams'], queryFn: fetchTeams })
const projectsQuery = useQuery({
  queryKey: ['projects'],
  queryFn: fetchProjects,
})
</script>
```





## `useQueries`를 사용한 동적 병렬 Queries



실행해야 하는 queries의 수가 렌더링마다 변경되는 경우 후크 규칙을 위반하므로 수동 쿼리를 사용할 수 없습니다. 대신, TanStack Query는 원하는 만큼 많은 queries를 동적으로 병렬로 실행하는 데 사용할 수 있는 `useQueries` 후크를 제공합니다.




`useQueries`는 값이 **query 개체 배열**인 **queries 키**가 있는 **옵션 개체**를 허용합니다. **query 결과 배열**을 반환합니다.




```js
const users = computed(...)
const queries = computed(() => users.value.map(user => {
    return {
      queryKey: ['user', user.id],
      queryFn: () => fetchUserById(user.id),
    }
  })
);
const userQueries = useQueries({queries: queries})
```


