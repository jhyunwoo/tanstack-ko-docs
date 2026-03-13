---
id: no-rest-destructuring
title: query 결과에서 객체 나머지 구조 분해를 허용하지 않습니다.
---




query 결과에서 객체 나머지 구조 분해를 사용하면 query 결과의 모든 필드를 자동으로 구독하므로 불필요한 재렌더링이 발생할 수 있습니다.
이렇게 하면 실제로 필요한 필드만 구독할 수 있습니다.

## 규칙 세부정보

이 규칙에 대한 **잘못된** 코드의 예:

```tsx
/* eslint "@tanstack/query/no-rest-destructuring": "경고" */

const useTodos = () => {
  const { data: todos, ...rest } = useQuery({
    queryKey: ['todos'],
    queryFn: () => api.getTodos(),
  })
  return { todos, ...rest }
}
```
이 규칙에 대한 **올바른** 코드의 예:

```tsx
const todosQuery = useQuery({
  queryKey: ['todos'],
  queryFn: () => api.getTodos(),
})

// 일반적인 객체 구조 분해는 괜찮습니다.
const { data: todos } = todosQuery
```
## 사용하지 말아야 할 경우

`notifyOnChangeProps` 옵션을 수동으로 설정하는 경우 이 규칙을 비활성화할 수 있습니다.
추적된 queries를 사용하지 않으므로 재렌더링을 트리거해야 하는 prop을 지정해야 합니다.

## 속성

- [x] ✅ 추천
- [ ] 🔧 수정 가능