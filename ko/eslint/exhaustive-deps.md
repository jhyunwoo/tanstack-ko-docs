---
id: exhaustive-deps
title: query 키에 대한 철저한 종속성
---




Query 키는 query 함수에 대한 종속성 배열처럼 표시되어야 합니다. queryFn 내부에서 사용되는 모든 변수는 query 키에 추가되어야 합니다.
이렇게 하면 queries가 독립적으로 캐시되고 변수가 변경될 때 queries가 자동으로 다시 가져오게 됩니다.

## 규칙 세부정보

이 규칙에 대한 **잘못된** 코드의 예:

```tsx
/* eslint "@tanstack/query/exhaustive-deps": "오류" */

useQuery({
  queryKey: ['todo'],
  queryFn: () => api.getTodo(todoId),
})

const todoQueries = {
  detail: (id) => ({ queryKey: ['todo'], queryFn: () => api.getTodo(id) }),
}
```
이 규칙에 대한 **올바른** 코드의 예:

```tsx
useQuery({
  queryKey: ['todo', todoId],
  queryFn: () => api.getTodo(todoId),
})

const todoQueries = {
  detail: (id) => ({ queryKey: ['todo', id], queryFn: () => api.getTodo(id) }),
}
```
## 사용하지 말아야 할 경우

query 키의 규칙에 관심이 없다면 이 규칙이 필요하지 않습니다.

## 속성

- [x] ✅ 추천
- [x] 🔧 수정 가능