---
id: QueryCache
title: QueryCache
---




`QueryCache`는 TanStack Query의 저장 메커니즘입니다. 여기에는 포함된 queries의 모든 데이터, 메타 정보 및 상태가 저장됩니다.

**일반적으로 QueryCache와 직접 상호 작용하지 않고 대신 특정 캐시에 `QueryClient`를 사용합니다.**

```tsx
import { QueryCache } from '@tanstack/react-query'

const queryCache = new QueryCache({
  onError: (error) => {
    console.log(error)
  },
  onSuccess: (data) => {
    console.log(data)
  },
  onSettled: (data, error) => {
    console.log(data, error)
  },
})

const query = queryCache.find(['posts'])
```
사용 가능한 방법은 다음과 같습니다.

- [`queryCache.find`](#querycachefind)
- [`queryCache.findAll`](#querycachefindall)
- [`queryCache.subscribe`](#querycache구독)
- [`queryCache.clear`](#querycacheclear)
- [더 읽어보기](#더 읽어보기)

**옵션**

- `onError?: (error: unknown, query: Query) => void`
  - 선택사항
  - 일부 query에서 오류가 발생하면 이 함수가 호출됩니다.
- `onSuccess?: (data: unknown, query: Query) => void`
  - 선택사항
  - 일부 query가 성공하면 이 함수가 호출됩니다.
- `onSettled?: (data: unknown | undefined, error: unknown | null, query: Query) => void`
  - 선택사항
  - 일부 query가 해결되면(성공 또는 오류 발생) 이 함수가 호출됩니다.

## `queryCache.find`

`find`는 캐시에서 기존 query 인스턴스를 가져오는 데 사용할 수 있는 약간 더 발전된 동기 방법입니다. 이 인스턴스에는 query의 상태 **모두**뿐만 아니라 모든 인스턴스와 query의 기본 내장도 포함됩니다. query가 존재하지 않으면 `undefined`가 반환됩니다.

> 참고: 이는 일반적으로 대부분의 애플리케이션에 필요하지 않지만 드문 시나리오에서 query에 대한 추가 정보가 필요할 때 유용할 수 있습니다(예: query.state.dataUpdatedAt 타임스탬프를 보고 query가 초기 값으로 사용될 수 있을 만큼 최신인지 결정).

```tsx
const query = queryCache.find(queryKey)
```
**옵션**

- `filters?: QueryFilters`: [Query 필터](../framework/react/guides/filters.md#query-filters)

**보고**

- `Query`
  - 캐시의 query 인스턴스

## `queryCache.findAll`

`findAll`는 query 키와 부분적으로 일치하는 캐시에서 기존 query 인스턴스를 가져오는 데 사용할 수 있는 훨씬 더 고급 동기 방법입니다. queries가 존재하지 않으면 빈 배열이 반환됩니다.

> 참고: 이는 일반적으로 대부분의 애플리케이션에 필요하지 않지만 드문 시나리오에서 query에 대한 추가 정보가 필요할 때 유용할 수 있습니다.

```tsx
const queries = queryCache.findAll(queryKey)
```
**옵션**

- `queryKey?: QueryKey`: [Query 키](../framework/react/guides/query-keys.md)
- `filters?: QueryFilters`: [Query 필터](../framework/react/guides/filters.md#query-filters)

**보고**

- `Query[]`
  - 캐시의 Query 인스턴스

## `queryCache.subscribe`

`subscribe` 메소드는 query 캐시를 전체적으로 구독하고 query 상태 변경 또는 queries 업데이트, 추가 또는 제거와 같은 캐시에 대한 안전한/알려진 업데이트에 대한 알림을 받는 데 사용할 수 있습니다.

```tsx
const callback = (event) => {
  console.log(event.type, event.query)
}

const unsubscribe = queryCache.subscribe(callback)
```
**옵션**

- `callback: (event: QueryCacheNotifyEvent) => void`
  - 이 함수는 추적된 업데이트 메커니즘(예: `query.setState`, `queryClient.removeQueries` 등)을 통해 업데이트될 때마다 query 캐시와 함께 호출됩니다. 캐시에 대한 범위 외 mutations는 ​​권장되지 않으며 구독 콜백을 실행하지 않습니다.

**보고**

- `unsubscribe: Function => void`
  - 이 함수는 query 캐시에서 콜백 구독을 취소합니다.

## `queryCache.clear`

`clear` 방법을 사용하면 캐시를 완전히 지우고 새로 시작할 수 있습니다.

```tsx
queryCache.clear()
```
[//]: # 'Materials'

## 추가 자료

QueryCache가 내부적으로 어떻게 작동하는지 더 잘 이해하려면 [TkDodo의 Inside React Query 기사](https://tkdodo.eu/blog/inside-react-query)를 살펴보세요.

[//]: # 'Materials'
