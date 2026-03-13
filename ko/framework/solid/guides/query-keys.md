---
id: query-keys
title: Query 키
---




핵심적으로 TanStack Query는 query 키를 기반으로 query 캐싱을 관리합니다. Query 키는 최상위 수준의 배열이어야 하며 단일 문자열이 포함된 배열처럼 단순할 수도 있고 많은 문자열과 중첩된 개체의 배열만큼 복잡할 수도 있습니다. query 키가 `JSON.stringify`를 사용하여 직렬화 가능하고 **query의 데이터에 고유**하다면 사용할 수 있습니다!

## 간단한 Query 키

키의 가장 간단한 형태는 상수 값이 포함된 배열입니다. 이 형식은 다음과 같은 경우에 유용합니다.

- 일반 목록/인덱스 리소스
- 비계층적 자원



```tsx
// 할 일 목록
useQuery(() => ({ queryKey: ['todos'], ... }))

// 다른 것, 뭐든지!
useQuery(() => ({ queryKey: ['something', 'special'], ... }))
```



## 변수가 포함된 배열 키

query에 해당 데이터를 고유하게 설명하기 위해 추가 정보가 필요한 경우 문자열과 직렬화 가능한 개체가 포함된 배열을 사용하여 이를 설명할 수 있습니다. 이는 다음과 같은 경우에 유용합니다.

- 계층적 또는 중첩된 리소스
  - 항목을 고유하게 식별하기 위해 ID, 색인 또는 기타 기본 요소를 전달하는 것이 일반적입니다.
- 추가 매개변수가 있는 Queries
  - 추가 옵션의 객체를 전달하는 것이 일반적입니다.



```tsx
// 개별 할 일
useQuery(() => ({ queryKey: ['todo', 5], ... }))

// "미리보기" 형식의 개별 할일
useQuery(() => ({ queryKey: ['todo', 5, { preview: true }], ...}))

// "완료"된 할일 목록
useQuery(() => ({ queryKey: ['todos', { type: 'done' }], ... }))
```



## Query 키는 결정론적으로 해시됩니다!

즉, 객체의 키 순서에 관계없이 다음 queries는 모두 동일한 것으로 간주됩니다.



```tsx
useQuery(() => ({ queryKey: ['todos', { status, page }], ... }))
useQuery(() => ({ queryKey: ['todos', { page, status }], ...}))
useQuery(() => ({ queryKey: ['todos', { page, status, other: undefined }], ... }))
```



그러나 다음 query 키는 동일하지 않습니다. 배열 항목 순서가 중요합니다!



```tsx
useQuery(() => ({ queryKey: ['todos', status, page], ... }))
useQuery(() => ({ queryKey: ['todos', page, status], ...}))
useQuery(() => ({ queryKey: ['todos', undefined, page, status], ...}))
```



## query 함수가 변수에 의존하는 경우 이를 query 키에 포함하세요.

query 키는 가져오는 데이터를 고유하게 설명하므로 **변경**하는 query 함수에서 사용하는 모든 변수를 포함해야 합니다. 예를 들어:



```tsx
function Todos(props) {
  const todosQuery = useQuery(() => ({
    queryKey: ['todos', props.todoId],
    queryFn: () => fetchTodoById(props.todoId),
  }))
}
```



query 키는 query 기능에 대한 종속성 역할을 합니다. query 키에 종속 변수를 추가하면 queries가 독립적으로 캐시되고 변수가 변경될 때마다 _queries가 자동으로 다시 가져옵니다_(`staleTime` 설정에 따라 다름). 자세한 내용과 예제는 [exhaustive-deps](../../../eslint/exhaustive-deps.md) 섹션을 참조하세요.



## 추가 자료

대규모 애플리케이션에서 Query 키를 구성하는 방법에 대한 팁은 [Effective TanStack Query Keys](https://tkdodo.eu/blog/ Effective-react-query-keys)를 살펴보고 [Query Key Factory를 확인하세요. 패키지](https://github.com/lukemorales/query-key-factory)
[커뮤니티 리소스](../../../_source-only/docs/community-resources.md).


