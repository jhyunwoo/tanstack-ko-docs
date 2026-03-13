---
id: queryOptions
title: queryOptions
---





```tsx
queryOptions({
  queryKey,
  ...options,
})
```
**옵션**

일반적으로 [useQuery](useQuery.md)에도 전달할 수 있는 모든 것을 `queryOptions`에 전달할 수 있습니다. 일부 옵션은 `queryClient.prefetchQuery`와 같은 함수로 전달될 때 아무런 효과가 없지만 TypeScript는 이러한 초과 속성에도 여전히 문제가 없습니다.

- `queryKey: QueryKey`
  - **필수**
  - 옵션을 생성할 query 키입니다.
- `experimental_prefetchInRender?: boolean`
  - 선택사항
  - 기본값은 `false`입니다.
  - `true`로 설정하면 렌더링 중에 queries가 프리페치되어 특정 최적화 시나리오에 유용할 수 있습니다.
  - 실험적인 `useQuery().promise` 기능을 사용하려면 켜져야 합니다.

[//]: # 'Materials'

## 추가 자료

`QueryOptions`에 대해 자세히 알아보려면 [TkDodo의 Query 옵션 API 기사](https://tkdodo.eu/blog/the-query-options-api)를 살펴보세요.

[//]: # 'Materials'
