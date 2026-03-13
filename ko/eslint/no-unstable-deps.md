---
id: no-unstable-deps
title: query 후크 결과를 React 후크 종속성 배열에 직접 넣는 것을 허용하지 않습니다.
---




다음 query 후크에서 반환된 개체는 참조적으로 안정적이지 **않습니다**.

- `useQuery`
- `useSuspenseQuery`
- `useQueries`
- `useSuspenseQueries`
- `useInfiniteQuery`
- `useSuspenseInfiniteQuery`
- `useMutation`

해당 후크에서 반환된 객체는 React 후크의 종속성 배열(예: `useEffect`, `useMemo`, `useCallback`)에 직접 배치되어서는 **안 됩니다**.
대신, query 후크의 반환 값을 구조 해제하고 구조 해제된 값을 React 후크의 종속성 배열에 전달하세요.

## 규칙 세부정보

이 규칙에 대한 **잘못된** 코드의 예:

```tsx
/* eslint "@tanstack/query/no-unstable-deps": "경고" */
import { useCallback } from 'React'
import { useMutation } from '@tanstack/react-query'

function Component() {
  const mutation = useMutation({ mutationFn: (value: string) => value })
  const callback = useCallback(() => {
    mutation.mutate('hello')
  }, [mutation])
  return null
}
```
이 규칙에 대한 **올바른** 코드의 예:

```tsx
/* eslint "@tanstack/query/no-unstable-deps": "경고" */
import { useCallback } from 'React'
import { useMutation } from '@tanstack/react-query'

function Component() {
  const { mutate } = useMutation({ mutationFn: (value: string) => value })
  const callback = useCallback(() => {
    mutate('hello')
  }, [mutate])
  return null
}
```
## 속성

- [x] ✅ 추천
- [ ] 🔧 수정 가능