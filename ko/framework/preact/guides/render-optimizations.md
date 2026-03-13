---
id: render-optimizations
title: 렌더링 최적화
---




Preact Query는 구성 요소가 실제로 필요할 때만 다시 렌더링되도록 몇 가지 최적화를 자동으로 적용합니다. 이는 다음과 같은 방법으로 수행됩니다.

## 구조적 공유

Preact Query는 "구조적 공유"라는 기술을 사용하여 재렌더링 간에 최대한 많은 참조가 그대로 유지되도록 합니다. 네트워크를 통해 데이터를 가져오는 경우 일반적으로 json이 응답을 구문 분석하여 완전히 새로운 참조를 얻게 됩니다. 그러나 Preact Query는 데이터에서 아무것도 변경되지 않은 경우 원래 참조를 유지합니다. 하위 세트가 변경된 경우 Preact Query는 변경되지 않은 부품을 유지하고 변경된 부품만 교체합니다.

> 참고: 이 최적화는 `queryFn`가 JSON 호환 데이터를 반환하는 경우에만 작동합니다. `structuralSharing: false`를 전역적으로 설정하거나 query별로 설정하여 이 기능을 끌 수도 있고, 함수를 전달하여 고유한 구조 공유를 구현할 수도 있습니다.

### 참조 ID

`useQuery`, `useInfiniteQuery`, `useMutation`에서 반환된 최상위 개체와 `useQueries`에서 반환된 배열은 **참조적으로 안정적이지 않습니다**. 이는 모든 렌더링에서 새로운 참조가 됩니다. 그러나 이러한 후크에서 반환된 `data` 속성은 최대한 안정적입니다.

## 추적된 속성

Preact Query는 `useQuery`에서 반환된 속성 중 하나가 실제로 "사용"되는 경우에만 다시 렌더링을 트리거합니다. 이는 [프록시 개체](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy)를 사용하여 수행됩니다. 이렇게 하면 불필요한 재렌더링을 많이 피할 수 있습니다. `isFetching` 또는 `isStale`와 같은 속성은 자주 변경될 수 있지만 구성 요소에서는 사용되지 않기 때문입니다.

`notifyOnChangeProps`를 수동으로 전역적으로 설정하거나 query별로 설정하여 이 기능을 사용자 정의할 수 있습니다. 해당 기능을 끄려면 `notifyOnChangeProps: 'all'`를 설정하면 됩니다.

> 참고: 프록시의 get 트랩은 구조 분해를 통해 또는 속성에 직접 액세스하여 속성에 액세스하여 호출됩니다. 객체 나머지 구조 분해를 사용하는 경우 이 최적화가 비활성화됩니다. 이러한 함정을 방지하기 위한 [린트 규칙](../../../eslint/no-rest-destructuring.md)이 있습니다.

## 선택하다

`select` 옵션을 사용하여 구성 요소가 구독해야 하는 데이터의 하위 집합을 선택할 수 있습니다. 이는 고도로 최적화된 데이터 변환에 유용하거나 불필요한 재렌더링을 방지하는 데 유용합니다.

```js
export const useTodos = (select) => {
  return useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
    select,
  })
}

export const useTodoCount = () => {
  return useTodos((data) => data.length)
}
```
`useTodoCount` 사용자 정의 후크를 사용하는 구성 요소는 할 일의 길이가 변경되는 경우에만 다시 렌더링됩니다. 예를 들어 다음과 같은 경우에는 다시 렌더링되지 **않습니다**. 할 일의 이름이 변경되었습니다.

> 참고: `select`는 성공적으로 캐시된 데이터에서 작동하며 오류를 발생시키는 적절한 위치가 아닙니다. 오류에 대한 진실의 출처는 `queryFn`이며 오류 결과를 반환하는 `select` 함수는 `data`가 `undefined`이고 `isSuccess`가 `true`입니다. 잘못된 데이터로 인해 query가 실패하도록 하려면 `queryFn`에서 오류를 처리하고, 캐싱과 관련되지 않은 오류 사례가 있는 경우 query 후크 외부에서 오류를 처리하는 것이 좋습니다.

### 메모이제이션

`select` 기능은 다음과 같은 경우에만 다시 실행됩니다.

- `select` 함수 자체가 참조적으로 변경되었습니다.
- `data` 변경됨

이는 위에 표시된 대로 인라인된 `select` 함수가 모든 렌더링에서 실행된다는 것을 의미합니다. 이를 방지하려면 `select` 함수를 `useCallback`에 래핑하거나 종속성이 없는 경우 안정적인 함수 참조로 추출할 수 있습니다.

```js
// useCallback에 래핑됨
export const useTodoCount = () => {
  return useTodos(useCallback((data) => data.length, []))
}
```

```js
// 안정적인 함수 참조로 추출됨
const selectTodoCount = (data) => data.length

export const useTodoCount = () => {
  return useTodos(selectTodoCount)
}
```
## 추가 자료

이러한 주제에 대한 심층 가이드를 보려면 [Preact Query 렌더 최적화](https://tkdodo.eu/blog/preact-query-render-optimizations)를 읽어보세요.
TkDodo. `select` 옵션을 가장 잘 최적화하는 방법을 알아보려면 [Preact Query 선택기, 슈퍼차지](https://tkdodo.eu/blog/preact-query-selectors-supercharged)를 읽어보세요.