---
id: dependent-queries
title: 종속 Queries
---




## injectQuery 종속 Query

종속(또는 직렬) queries는 이전 항목에 의존하여 실행되기 전에 완료됩니다. 이를 달성하려면 `enabled` 옵션을 사용하여 실행할 준비가 되었을 때 query에 알리는 것만큼 쉽습니다.



```ts
// 사용자 확보
userQuery = injectQuery(() => ({
  queryKey: ['user', email],
  queryFn: getUserByEmail,
}))

// 그런 다음 사용자의 프로젝트를 가져옵니다.
projectsQuery = injectQuery(() => ({
  queryKey: ['projects', this.userQuery.data()?.id],
  queryFn: getProjectsByUser,
  // query는 사용자 ID가 존재할 때까지 실행되지 않습니다.
  enabled: !!this.userQuery.data()?.id,
}))
```



`projects` query는 다음에서 시작됩니다.

```tsx
status: 'pending'
isPending: true
fetchStatus: 'idle'
```
`user`를 사용할 수 있게 되면 `projects` query는 `enabled`로 바뀌고 다음으로 전환됩니다.

```tsx
status: 'pending'
isPending: true
fetchStatus: 'fetching'
```
프로젝트가 있으면 다음으로 이동합니다.

```tsx
status: 'success'
isPending: false
fetchStatus: 'idle'
```
## injectQueries 종속 Query

동적 병렬 query - `injectQueries`는 이전 query에도 종속될 수 있습니다. 이를 달성하는 방법은 다음과 같습니다.



```ts
// injectQueries는 Angular Query용으로 개발 중입니다.
```



**참고** `injectQueries`는 **query 결과 배열**을 반환합니다.

## 성능에 대한 참고사항

정의에 따라 종속 queries는 성능을 저하시키는 [요청 폭포](../../react/guides/request-waterfalls.md) 형식을 구성합니다. 두 queries 모두 동일한 시간이 걸리는 것으로 가정하면 병렬이 아닌 직렬로 수행하면 항상 두 배의 시간이 소요됩니다. 이는 대기 시간이 긴 클라이언트에서 발생할 때 특히 해롭습니다. 가능하다면 두 queries를 병렬로 가져올 수 있도록 백엔드 API를 재구성하는 것이 항상 더 좋지만 실제로는 항상 가능하지는 않습니다.

위의 예에서 `getProjectsByUser`를 사용할 수 있도록 먼저 `getUserByEmail`를 가져오는 대신 새 `getProjectsByUserEmail` query를 도입하면 폭포가 평탄해집니다.