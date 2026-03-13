---
id: persistQueryClient
title: persistQueryClient
---




이는 나중에 사용하기 위해 queryClient를 저장하는 "지속성"과 상호 작용하기 위한 유틸리티 세트입니다. 다양한 **지속성**을 사용하여 클라이언트와 캐시를 다양한 스토리지 계층에 저장할 수 있습니다.

## 지속자 빌드

- [createSyncStoragePersister](createSyncStoragePersister.md)
- [createAsyncStoragePersister](createAsyncStoragePersister.md)
- [사용자 정의 지속기 생성](#persisters)

## 작동 방식

**중요** - 지속이 제대로 작동하려면 hydration 동안 기본값을 재정의하기 위해 `QueryClient`에 `gcTime` 값을 전달하는 것이 좋습니다(위에 표시된 대로).

`QueryClient` 인스턴스 생성 시 설정하지 않으면 hydration의 경우 기본적으로 `300000`(5분)로 설정되며, 저장된 캐시는 5분 동안 활동이 없으면 삭제됩니다. 이는 기본 가비지 수집 동작입니다.

persistQueryClient의 `maxAge` 옵션과 같거나 높은 값으로 설정해야 합니다. 예: `maxAge`가 24시간(기본값)인 경우 `gcTime`는 24시간 이상이어야 합니다. `maxAge`보다 낮으면 가비지 수집이 시작되어 예상보다 일찍 저장된 캐시를 삭제합니다.

`Infinity`를 전달하여 가비지 수집 동작을 완전히 비활성화할 수도 있습니다.

JavaScript 제한으로 인해 허용되는 최대 `gcTime`는 약 [24일](https://developer.mozilla.org/en-US/docs/Web/API/setTimeout#maximum_delay_value)이지만 [TimeoutManager](../../../reference/timeoutManager.md#timeoutmanagersettimeoutprovider)를 사용하여 이 제한을 해결할 수 있습니다.

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      gcTime: 1000 * 60 * 60 * 24, // 24시간
    },
  },
})
```
### 캐시 무효화

때로는 애플리케이션이나 데이터를 변경하여 캐시된 모든 데이터를 즉시 무효화할 수도 있습니다. 이런 일이 발생하면 `buster` 문자열 옵션을 전달할 수 있습니다. 발견된 캐시에 해당 버스터 문자열도 없으면 폐기됩니다. 다음과 같은 여러 기능이 이 옵션을 허용합니다.

```tsx
persistQueryClient({ queryClient, persister, buster: buildHash })
persistQueryClientSave({ queryClient, persister, buster: buildHash })
persistQueryClientRestore({ queryClient, persister, buster: buildHash })
```
### 제거

데이터가 다음 중 하나인 것으로 확인된 경우:

1. 만료됨(`maxAge` 참조)
2. 체포됨(`buster` 참조)
3. 오류(예: `throws ...`)
4. 비어 있음(예: `undefined`)

지속자 `removeClient()`가 호출되고 캐시가 즉시 삭제됩니다.

## API

### `persistQueryClientSave`

- 귀하의 query/mutation는 [hydration](../reference/hydration.md#dehydrate)이며 귀하가 제공한 지속기에 의해 저장됩니다.
- `createSyncStoragePersister` 및 `createAsyncStoragePersister`는 잠재적으로 비용이 많이 드는 쓰기를 절약하기 위해 이 작업이 최대 1초마다 발생하도록 제한합니다. 스로틀 타이밍을 사용자 정의하는 방법을 알아보려면 해당 문서를 검토하세요.

이를 사용하여 선택한 순간에 캐시를 명시적으로 유지할 수 있습니다.

```tsx
persistQueryClientSave({
  queryClient,
  persister,
  buster = '',
  dehydrateOptions = undefined,
})
```
### `persistQueryClientSubscribe`

`queryClient`에 대한 캐시가 변경될 때마다 `persistQueryClientSave`를 실행합니다. 예를 들어, 사용자가 로그인하고 "Remember me"를 확인할 때 `subscribe`를 시작할 수 있습니다.

- 모니터를 중단하는 데 사용할 수 있는 `unsubscribe` 함수를 반환합니다. 지속형 캐시에 대한 업데이트를 종료합니다.
- `unsubscribe` 이후에 지속된 캐시를 삭제하려는 경우 새로운 `buster`를 `persistQueryClientRestore`로 보내 지속자의 `removeClient` 기능을 트리거하고 지속된 캐시를 삭제할 수 있습니다.

```tsx
persistQueryClientSubscribe({
  queryClient,
  persister,
  buster = '',
  dehydrateOptions = undefined,
})
```
### `persistQueryClientRestore`

- 이전에 지속된 디하이드레이션된 query/mutation 캐시를 지속기에서 전달된 query 클라이언트의 query 캐시로 다시 [hydration](../reference/hydration.md#hydrate) 시도합니다.
- `maxAge`(기본적으로 24시간)보다 오래된 캐시가 발견되면 폐기됩니다. 이 타이밍은 귀하가 적절하다고 생각하는 대로 맞춤 설정할 수 있습니다.

이를 사용하여 선택한 순간에 캐시를 복원할 수 있습니다.

```tsx
persistQueryClientRestore({
  queryClient,
  persister,
  maxAge = 1000 * 60 * 60 * 24, // 24시간
  buster = '',
  hydrateOptions = undefined,
})
```
### `persistQueryClient`

다음 작업을 수행합니다.

1. 지속된 캐시를 즉시 복원합니다([`persistQueryClientRestore` 참조](#persistqueryclientrestore)).
2. query 캐시를 구독하고 `unsubscribe` 함수를 반환합니다([`persistQueryClientSubscribe` 참조](#persistqueryclientsubscribe)).

이 기능은 버전 3.x에서 유지됩니다.

```tsx
persistQueryClient({
  queryClient,
  persister,
  maxAge = 1000 * 60 * 60 * 24, // 24시간
  buster = '',
  hydrateOptions = undefined,
  dehydrateOptions = undefined,
})
```
### `Options`

사용 가능한 모든 옵션은 다음과 같습니다.

```tsx
interface PersistQueryClientOptions {
  /* * QueryClient는 지속됩니다. */
  queryClient: QueryClient
  /* * 캐시 저장 및 복원을 위한 Persister 인터페이스
   * 지속되는 위치로/에서 */
  persister: Persister
  /* * 캐시의 최대 허용 기간(밀리초)입니다.
   * 이보다 오래된 지속형 캐시가 발견된 경우
   * 시간이 지나면 **조용히** 폐기됩니다.
   * (기본값은 24시간) */
  maxAge?: number
  /* * 강제로 사용할 수 있는 고유한 문자열
   * 동일한 버스터 문자열을 공유하지 않는 경우 기존 캐시를 무효화합니다. */
  buster?: string
  /* * 수화물 함수에 전달된 옵션
   * `persistQueryClientSave` 또는 `persistQueryClientSubscribe`에는 사용되지 않습니다. */
  hydrateOptions?: HydrateOptions
  /* * 탈수 기능에 전달된 옵션
   * `persistQueryClientRestore`에는 사용되지 않음 */
  dehydrateOptions?: DehydrateOptions
}
```
실제로는 세 가지 인터페이스를 사용할 수 있습니다.

- `PersistedQueryClientSaveOptions`는 `persistQueryClientSave` 및 `persistQueryClientSubscribe`에 사용됩니다(`hydrateOptions`를 사용하지 않음).
- `PersistedQueryClientRestoreOptions`는 `persistQueryClientRestore`에 사용됩니다(`dehydrateOptions`를 사용하지 않음).
- `PersistQueryClientOptions`는 ​​`persistQueryClient`에 사용됩니다.

## React에서의 사용법

[persistQueryClient](#persistQueryClient)는 캐시 복원을 시도하고 추가 변경 사항을 자동으로 구독하여 클라이언트를 제공된 스토리지에 동기화합니다.

그러나 복원은 비동기식입니다. 왜냐하면 모든 지속자는 본질적으로 비동기이기 때문입니다. 즉, 복원하는 동안 앱을 렌더링하는 경우 query가 동시에 마운트되고 가져오는 경우 경쟁 조건이 발생할 수 있습니다.

또한 React 구성 요소 수명 주기 외부의 변경 사항을 구독하는 경우 구독을 취소할 방법이 없습니다.

```tsx
// 🚨 동기화 구독을 취소하지 마세요
persistQueryClient({
  queryClient,
  persister: localStoragePersister,
})

// 🚨 복원과 동시에 발생
ReactDOM.createRoot(rootElement).render(App /)
```
### PersistQueryClientProvider

이 사용 사례에서는 `PersistQueryClientProvider`를 사용할 수 있습니다. 이는 React 구성 요소 수명 주기에 따라 올바르게 구독/구독 취소를 확인하고 복원하는 동안 queries가 가져오기를 시작하지 않도록 합니다. Queries는 계속 렌더링되지만 데이터가 복원될 때까지 `fetchingState: 'idle'`에 저장됩니다. 그런 다음 복원된 데이터가 충분히 _신선_하지 않으면 다시 가져오며 _initialData_도 존중됩니다. 일반 [QueryClientProvider](../reference/QueryClientProvider.md) _대신_ 사용할 수 있습니다.

```tsx
import { PersistQueryClientProvider } from '@tanstack/react-query-persist-client'
import { createAsyncStoragePersister } from '@tanstack/query-async-storage-persister'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      gcTime: 1000 * 60 * 60 * 24, // 24시간
    },
  },
})

const persister = createAsyncStoragePersister({
  storage: window.localStorage,
})

ReactDOM.createRoot(rootElement).render(
  <PersistQueryClientProvider
    client={queryClient}
    persistOptions={{ persister }}
  >
    <App />
  </PersistQueryClientProvider>,
)
```
#### 소품

`PersistQueryClientProvider`는 [QueryClientProvider](../reference/QueryClientProvider.md)와 동일한 소품을 사용하며 추가로 다음을 수행합니다.

- `persistOptions: PersistQueryClientOptions`
  - QueryClient 자체를 제외하고 [persistQueryClient](#persistqueryclient)에 전달할 수 있는 모든 [옵션](#options)
- `onSuccess?: () => Promise<unknown> | unknown`
  - 선택사항
  - 초기 복원이 완료되면 호출됩니다.
  - [QueryClient](../../../reference/QueryClient.md#queryclientresumepausedmutations)에 사용할 수 있습니다.
  - Promise가 반환되면 대기하게 됩니다. 복원은 그때까지 진행 중인 것으로 간주됩니다.
- `onError?: () => Promise<unknown> | unknown`
  - 선택사항
  - 복원 중에 오류가 발생하면 호출됩니다.
  - Promise가 반환되면 기다리게 됩니다.

### useIsRestoring

`PersistQueryClientProvider`를 사용하는 경우 `useIsRestoring` 후크를 함께 사용하여 복원이 현재 진행 중인지 확인할 수도 있습니다. `useQuery`와 친구들은 복원과 queries 마운트 간의 경쟁 조건을 피하기 위해 내부적으로 이를 확인합니다.

## Persisters

### 지속성 인터페이스

Persister에는 다음과 같은 인터페이스가 있습니다:

```tsx
export interface Persister {
  persistClient(persistClient: PersistedClient): Promisable<void>
  restoreClient(): Promisable<PersistedClient | undefined>
  removeClient(): Promisable<void>
}
```
지속 클라이언트 항목에는 다음과 같은 인터페이스가 있습니다.

```tsx
export interface PersistedClient {
  timestamp: number
  buster: string
  clientState: DehydratedState
}
```
지속자를 구축하기 위해 다음을 가져올 수 있습니다.

```tsx
import {
  PersistedClient,
  Persister,
} from '@tanstack/react-query-persist-client'
```
### 지속성 구축

원하는 대로 지속할 수 있습니다. 다음은 [인덱스된 DB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API) 지속기를 구축하는 방법에 대한 예입니다. `Web Storage API`에 비해 Indexed DB는 더 빠르고 5MB 이상을 저장하며 직렬화가 필요하지 않습니다. 이는 `Date` 및 `File`와 같은 Javascript 기본 유형을 쉽게 저장할 수 있음을 의미합니다.

```tsx
import { get, set, del } from 'idb-keyval'
import {
  PersistedClient,
  Persister,
} from '@tanstack/react-query-persist-client'

/* *
 * 인덱싱된 DB 지속자를 생성합니다.
 * @see https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API */
export function createIDBPersister(idbValidKey: IDBValidKey = 'reactQuery') {
  return {
    persistClient: async (client: PersistedClient) => {
      await set(idbValidKey, client)
    },
    restoreClient: async () => {
      return await get<PersistedClient>(idbValidKey)
    },
    removeClient: async () => {
      await del(idbValidKey)
    },
  } satisfies Persister
}
```
