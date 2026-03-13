---
id: createSyncStoragePersister
title: createSyncStoragePersister
---




## 더 이상 사용되지 않음

이 플러그인은 더 이상 사용되지 않으며 다음 주요 버전에서 제거될 예정입니다.
대신 [createAsyncStoragePersister](createAsyncStoragePersister.md)를 사용할 수 있습니다.

## 설치

이 유틸리티는 별도의 패키지로 제공되며 `'@tanstack/query-sync-storage-persister'` 가져오기에서 사용할 수 있습니다.

```bash
npm install @tanstack/query-sync-storage-persister @tanstack/react-query-persist-client
```
또는

```bash
pnpm add @tanstack/query-sync-storage-persister @tanstack/react-query-persist-client
```
또는

```bash
yarn add @tanstack/query-sync-storage-persister @tanstack/react-query-persist-client
```
또는

```bash
bun add @tanstack/query-sync-storage-persister @tanstack/react-query-persist-client
```
## 용법

- `createSyncStoragePersister` 기능 가져오기
- 새로운 syncStoragePersister를 생성합니다.
- [persistQueryClient](persistQueryClient.md) 함수에 전달합니다.

```tsx
import { persistQueryClient } from '@tanstack/react-query-persist-client'
import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      gcTime: 1000 * 60 * 60 * 24, // 24시간
    },
  },
})

const localStoragePersister = createSyncStoragePersister({
  storage: window.localStorage,
})
// const sessionStoragePersister = createSyncStoragePersister({ 저장소: window.sessionStorage })

persistQueryClient({
  queryClient,
  persister: localStoragePersister,
})
```
## 재시도

지속성이 실패할 수 있습니다. 크기가 저장소의 사용 가능한 공간을 초과하는 경우. 지속기에 `retry` 함수를 제공하여 오류를 적절하게 처리할 수 있습니다.

재시도 기능은 저장하려고 시도한 `persistedClient`와 `error` 및 `errorCount`를 입력으로 받습니다. 다시 지속하려고 시도하는 _new_ `PersistedClient`를 반환할 것으로 예상됩니다. _undefine_이 반환되면 더 이상 지속을 시도하지 않습니다.

```tsx
export type PersistRetryer = (props: {
  persistedClient: PersistedClient
  error: Error
  errorCount: number
}) => PersistedClient | undefined
```
### 사전 정의된 전략

기본적으로 재시도는 발생하지 않습니다. 사전 정의된 전략 중 하나를 사용하여 재시도를 처리할 수 있습니다. `from '@tanstack/react-query-persist-client'`를 가져올 수 있습니다.

- `removeOldestQuery`
  - 가장 오래된 query가 제거된 새 `PersistedClient`를 반환합니다.

```tsx
const localStoragePersister = createSyncStoragePersister({
  storage: window.localStorage,
  retry: removeOldestQuery,
})
```
## API

### `createSyncStoragePersister`

나중에 `persistQueryClient`와 함께 사용할 수 있는 syncStoragePersister를 생성하려면 이 함수를 호출하세요.

```tsx
createSyncStoragePersister(options: CreateSyncStoragePersisterOptions)
```
### `Options`

```tsx
interface CreateSyncStoragePersisterOptions {
  /* * 캐시에서 항목 검색을 설정하는 데 사용되는 스토리지 클라이언트(window.localStorage 또는 window.sessionStorage) */
  storage: Storage | undefined | null
  /* * 캐시를 저장할 때 사용하는 키 */
  key?: string
  /* * 스팸메일 방지를 위해,
   * 캐시를 디스크에 저장하는 것을 제한하기 위해 ms 단위의 시간을 전달합니다. */
  throttleTime?: number
  /* * 데이터를 스토리지에 직렬화하는 방법 */
  serialize?: (client: PersistedClient) => string
  /* * 저장소에서 데이터를 역직렬화하는 방법 */
  deserialize?: (cachedString: string) => PersistedClient
  /* * 오류 발생 시 지속성을 재시도하는 방법 * */
  retry?: PersistRetryer
}
```
기본 옵션은 다음과 같습니다.

```tsx
{
  key = `REACT_QUERY_OFFLINE_CACHE`,
  throttleTime = 1000,
  serialize = JSON.stringify,
  deserialize = JSON.parse,
}
```
#### `serialize` 및 `deserialize` 옵션

`localStorage`에 저장할 수 있는 데이터 양에는 제한이 있습니다.
`localStorage`에 더 많은 데이터를 저장해야 하는 경우 `serialize` 및 `deserialize` 함수를 재정의하여 [lz-string](https://github.com/pieroxy/lz-string/)과 같은 라이브러리를 사용하여 데이터를 압축 및 압축 해제할 수 있습니다.

```tsx
import { QueryClient } from '@tanstack/react-query'
import { persistQueryClient } from '@tanstack/react-query-persist-client'
import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister'

import { compress, decompress } from 'lz-string'

const queryClient = new QueryClient({
  defaultOptions: { queries: { staleTime: Infinity } },
})

persistQueryClient({
  queryClient: queryClient,
  persister: createSyncStoragePersister({
    storage: window.localStorage,
    serialize: (data) => compress(JSON.stringify(data)),
    deserialize: (data) => JSON.parse(decompress(data)),
  }),
  maxAge: Infinity,
})
```
