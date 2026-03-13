---
id: network-mode
title: 네트워크 모드
---




TanStack Query는 네트워크에 연결되지 않은 경우 [Queries](queries.md) 및 [Mutations](mutations.md)가 어떻게 작동해야 하는지 구별하기 위해 세 가지 네트워크 모드를 제공합니다. 이 모드는 각 Query / Mutation에 대해 개별적으로 설정하거나 query / mutation 기본값을 통해 전체적으로 설정할 수 있습니다.

TanStack Query는 데이터 가져오기 라이브러리와 함께 데이터 가져오기에 가장 자주 사용되므로 기본 네트워크 모드는 [online](#network-mode-online)입니다.

## 네트워크 모드: 온라인

이 모드에서는 네트워크에 연결되어 있지 않으면 Queries 및 Mutations가 실행되지 않습니다. 이것이 기본 모드입니다. query에 대해 가져오기가 시작된 경우 네트워크 연결이 없어 가져오기를 수행할 수 없는 경우 항상 해당 `state`(`pending`, `error`, `success`)에 유지됩니다. 다만, [Queries](queries.md#fetchstatus)가 추가로 노출됩니다. 다음 중 하나일 수 있습니다.

- `fetching`: `queryFn`가 실제로 실행 중입니다. 요청이 진행 중입니다.
- `paused`: query가 실행되고 있지 않습니다. 다시 연결될 때까지 `paused`입니다.
- `idle`: query가 가져오지 않고 일시 중지되지 않습니다.

플래그 `isFetching` 및 `isPaused`는 이 상태에서 파생되며 편의상 노출됩니다.

> 로딩 스피너를 표시하기 위해 `pending` 상태를 확인하는 것만으로는 충분하지 않을 수 있다는 점을 명심하세요. Queries는 `state: 'pending'`에 있을 수 있지만 `fetchStatus: 'paused'`가 처음으로 마운트되고 네트워크 연결이 없는 경우에는 `fetchStatus: 'paused'`가 있을 수 있습니다.

온라인 상태이므로 query가 실행되지만 가져오기가 계속 진행되는 동안 오프라인으로 전환되는 경우 TanStack Query는 재시도 메커니즘도 일시 중지합니다. 일시 중지된 queries는 네트워크에 다시 연결되면 계속 실행됩니다. 이는 `refetch`가 아니라 `continue`이기 때문에 `refetchOnReconnect`(이 모드에서는 기본값도 `true`임)와 독립적입니다. 그 동안 query가 [취소](query-cancellation.md)된 경우 더 이상 진행되지 않습니다.

## 네트워크 모드: 항상

이 모드에서 TanStack Query는 항상 온라인/오프라인 상태를 가져오고 무시합니다. 이는 Queries가 작동하기 위해 활성 네트워크 연결이 필요하지 않은 환경에서 TanStack Query를 사용하는 경우 선택하려는 모드일 가능성이 높습니다. 방금 `AsyncStorage`에서 읽었거나 `queryFn`에서 `Promise.resolve(5)`를 반환하려는 경우.

- Queries는 네트워크 연결이 없기 때문에 `paused`가 될 수 없습니다.
- 재시도도 일시 중지되지 않습니다. 실패하면 Query가 `error` 상태로 전환됩니다.
- 이 모드에서는 `refetchOnReconnect`가 기본적으로 `false`로 설정됩니다. 네트워크에 다시 연결하는 것은 더 이상 오래된 queries를 다시 가져와야 한다는 좋은 지표가 아니기 때문입니다. 원한다면 계속 켤 수 있습니다.

## 네트워크 모드: 오프라인 우선

이 모드는 TanStack Query가 `queryFn`를 한 번 실행한 다음 재시도를 일시 중지하는 처음 두 옵션 사이의 중간 지점입니다. 이는 [오프라인 우선 PWA](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Offline_Service_workers)와 같이 캐싱 요청을 가로채는 serviceWorker가 있거나 [Cache-Control]을 통해 HTTP 캐싱을 사용하는 경우 매우 유용합니다. 헤더](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching#the_cache-control_header).

이러한 상황에서는 오프라인 저장소/캐시에서 가져오기 때문에 첫 번째 가져오기가 성공할 수 있습니다. 그러나 캐시 누락이 있는 경우 네트워크 요청이 나가고 실패하며, 이 경우 이 모드는 `online` query처럼 작동하여 재시도를 일시 중지합니다.

## 개발자 도구

[TanStack Query Devtools](../devtools.md)는 가져오는 중이지만 네트워크 연결이 없는 경우 Queries를 `paused` 상태로 표시합니다. _오프라인 동작 모의_ 토글 버튼도 있습니다. 이 버튼은 실제로 네트워크 연결을 방해하지 _않지만_(브라우저 개발자 도구에서 수행 가능) [OnlineManager](../../../reference/onlineManager.md)를 오프라인 상태로 설정합니다.

## 서명

- `networkMode: 'online' | 'always' | 'offlineFirst'`
  - 선택사항
  - 기본값은 `'online'`입니다.