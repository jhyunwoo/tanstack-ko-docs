---
id: parallel-queries
title: 병렬 Queries
---




"병렬" queries는 동시에 가져오기를 최대화하기 위해 병렬로 또는 동시에 실행되는 queries입니다.

## 수동 병렬 Queries

병렬 queries의 개수가 변하지 않으면 **추가 노력** 없이 병렬 queries를 사용할 수 있습니다. 원하는 수만큼 TanStack Query의 `injectQuery` 및 `injectInfiniteQuery` 기능을 나란히 사용하세요!



```ts
export class AppComponent {
  // 다음 queries는 병렬로 실행됩니다.
  usersQuery = injectQuery(() => ({ queryKey: ['users'], queryFn: fetchUsers }))
  teamsQuery = injectQuery(() => ({ queryKey: ['teams'], queryFn: fetchTeams }))
  projectsQuery = injectQuery(() => ({
    queryKey: ['projects'],
    queryFn: fetchProjects,
  }))
}
```





## `injectQueries`를 사용한 동적 병렬 Queries



TanStack Query는 원하는 만큼 많은 queries를 동적으로 병렬로 실행하는 데 사용할 수 있는 `injectQueries`를 제공합니다.




`injectQueries`는 값이 **query 개체 배열**인 **queries 키**가 있는 **옵션 개체**를 허용합니다. **query 결과 배열**을 반환합니다.




```ts
export class AppComponent {
  users = signal<Array<User>>([])

  // injectQueries는 개발 중이며 이 코드는 아직 작동하지 않습니다.
  userQueries = injectQueries(() => ({
    queries: users().map((user) => {
      return {
        queryKey: ['user', user.id],
        queryFn: () => fetchUserById(user.id),
      }
    }),
  }))
}
```


