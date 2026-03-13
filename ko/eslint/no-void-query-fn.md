---
id: no-void-query-fn
title: query 함수에서 void 반환을 허용하지 않음
---




Query 함수는 TanStack Query에 의해 캐시되는 값을 반환해야 합니다. 값을 반환하지 않는 함수(void 함수)는 예기치 않은 동작을 초래할 수 있으며 구현 시 실수가 있음을 나타낼 수 있습니다.

## 규칙 세부정보

이 규칙에 대한 **잘못된** 코드의 예:

```tsx
/* eslint "@tanstack/query/no-void-query-fn": "오류" */

useQuery({
  queryKey: ['todos'],
  queryFn: async () => {
    await api.todos.fetch() // 함수가 가져온 데이터를 반환하지 않습니다.
  },
})
```
이 규칙에 대한 **올바른** 코드의 예:

```tsx
/* eslint "@tanstack/query/no-void-query-fn": "오류" */
useQuery({
  queryKey: ['todos'],
  queryFn: async () => {
    const todos = await api.todos.fetch()
    return todos
  },
})
```
## 속성

- [x] ✅ 추천
- [ ] 🔧 수정 가능