---
id: mutation-property-order
title: useMutation()에서 추론에 민감한 속성의 올바른 순서를 확인하세요.
---




다음 함수의 경우 유형 추론으로 인해 전달된 객체의 속성 순서가 중요합니다.

- `useMutation()`

올바른 속성 순서는 다음과 같습니다.

- `onMutate`
- `onError`
- `onSettled`

다른 모든 속성은 유형 추론에 의존하지 않으므로 순서에 영향을 받지 않습니다.

## 규칙 세부정보

이 규칙에 대한 **잘못된** 코드의 예:

```tsx
/* eslint "@tanstack/query/mutation-property-order": "경고" */
import { useMutation } from '@tanstack/react-query'

const mutation = useMutation({
  mutationFn: () => Promise.resolve('success'),
  onSettled: () => {
    results.push('onSettled-promise')
    return Promise.resolve('also-ignored') // Promise<string> (무시해야 함)
  },
  onMutate: async () => {
    results.push('onMutate-async')
    await sleep(1)
    return { backup: 'async-data' }
  },
  onError: async () => {
    results.push('onError-async-start')
    await sleep(1)
    results.push('onError-async-end')
  },
})
```
이 규칙에 대한 **올바른** 코드의 예:

```tsx
/* eslint "@tanstack/query/mutation-property-order": "경고" */
import { useMutation } from '@tanstack/react-query'

const mutation = useMutation({
  mutationFn: () => Promise.resolve('success'),
  onMutate: async () => {
    results.push('onMutate-async')
    await sleep(1)
    return { backup: 'async-data' }
  },
  onError: async () => {
    results.push('onError-async-start')
    await sleep(1)
    results.push('onError-async-end')
  },
  onSettled: () => {
    results.push('onSettled-promise')
    return Promise.resolve('also-ignored') // Promise<string> (무시해야 함)
  },
})
```
## 속성

- [x] ✅ 추천
- [x] 🔧 수정 가능