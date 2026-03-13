---
id: MutationCache
title: MutationCache
---




`MutationCache`는 mutations용 스토리지입니다.

**일반적으로 MutationCache와 직접 상호 작용하지 않고 대신 `QueryClient`를 사용합니다.**

```tsx
import { MutationCache } from '@tanstack/react-query'

const mutationCache = new MutationCache({
  onError: (error) => {
    console.log(error)
  },
  onSuccess: (data) => {
    console.log(data)
  },
})
```
사용 가능한 방법은 다음과 같습니다.

- [`getAll`](#mutationcachegetall)
- [`subscribe`](#mutationcache구독)
- [`clear`](#mutationcacheclear)

**옵션**

- `onError?: (error: unknown, variables: unknown, onMutateResult: unknown, mutation: Mutation, mutationFnContext: MutationFunctionContext) => Promise<unknown> | unknown`
  - 선택사항
  - 일부 mutation에서 오류가 발생하면 이 함수가 호출됩니다.
  - Promise를 반환하면 대기하게 됩니다.
- `onSuccess?: (data: unknown, variables: unknown, onMutateResult: unknown, mutation: Mutation, mutationFnContext: MutationFunctionContext) => Promise<unknown> | unknown`
  - 선택사항
  - 일부 mutation가 성공하면 이 함수가 호출됩니다.
  - Promise를 반환하면 대기하게 됩니다.
- `onSettled?: (data: unknown | undefined, error: unknown | null, variables: unknown, onMutateResult: unknown, mutation: Mutation, mutationFnContext: MutationFunctionContext) => Promise<unknown> | unknown`
  - 선택사항
  - 일부 mutation가 해결되면(성공 또는 오류 발생) 이 함수가 호출됩니다.
  - Promise를 반환하면 대기하게 됩니다.
- `onMutate?: (variables: unknown, mutation: Mutation, mutationFnContext: MutationFunctionContext) => Promise<unknown> | unknown`
  - 선택사항
  - 이 함수는 일부 mutation가 실행되기 전에 호출됩니다.
  - Promise를 반환하면 대기하게 됩니다.

## 전역 콜백

MutationCache의 `onError`, `onSuccess`, `onSettled` 및 `onMutate` 콜백을 사용하여 전역 수준에서 이러한 이벤트를 처리할 수 있습니다. 다음과 같은 이유로 QueryClient에 제공된 `defaultOptions`와 다릅니다.

- `defaultOptions`는 각 Mutation에 의해 재정의될 수 있습니다. 전역 콜백은 **항상** 호출됩니다.
- `onMutate`는 결과 반환을 허용하지 않습니다.

## `mutationCache.getAll`

`getAll`는 캐시 내의 모든 mutations를 반환합니다.

> 참고: 이는 일반적으로 대부분의 애플리케이션에 필요하지 않지만 드물게 mutation에 대한 추가 정보가 필요할 때 유용할 수 있습니다.

```tsx
const mutations = mutationCache.getAll()
```
**보고**

- `Mutation[]`
  - 캐시의 Mutation 인스턴스

## `mutationCache.subscribe`

`subscribe` 메서드를 사용하면 mutation 캐시를 전체적으로 구독하고 mutation 상태 변경 또는 mutations 업데이트, 추가 또는 제거와 같은 캐시에 대한 안전한/알려진 업데이트에 대한 알림을 받을 수 있습니다.

```tsx
const callback = (event) => {
  console.log(event.type, event.mutation)
}

const unsubscribe = mutationCache.subscribe(callback)
```
**옵션**

- `callback: (mutation?: MutationCacheNotifyEvent) => void`
  - 이 함수는 업데이트될 때마다 mutation 캐시와 함께 호출됩니다.

**보고**

- `unsubscribe: Function => void`
  - 이 함수는 mutation 캐시에서 콜백 구독을 취소합니다.

## `mutationCache.clear`

`clear` 방법을 사용하면 캐시를 완전히 지우고 새로 시작할 수 있습니다.

```tsx
mutationCache.clear()
```
