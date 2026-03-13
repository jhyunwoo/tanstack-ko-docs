---
id: createAsyncStoragePersister
title: createAsyncStoragePersister
---




## 설치

이 유틸리티는 별도의 패키지로 제공되며 `'@tanstack/query-async-storage-persister'` 가져오기에서 사용할 수 있습니다.

```bash
npm install @tanstack/query-async-storage-persister @tanstack/react-query-persist-client
```
또는

```bash
pnpm add @tanstack/query-async-storage-persister @tanstack/react-query-persist-client
```
또는

```bash
yarn add @tanstack/query-async-storage-persister @tanstack/react-query-persist-client
```
또는

```bash
bun add @tanstack/query-async-storage-persister @tanstack/react-query-persist-client
```
## 용법

- `createAsyncStoragePersister` 기능 가져오기
- 새로운 asyncStoragePersister를 생성합니다.
  - `AsyncStorage` 인터페이스를 준수하는 모든 `storage`를 전달할 수 있습니다. 아래 예에서는 React Native의 async-storage를 사용합니다.
  - `window.localstorage`와 같이 동기적으로 읽고 쓰는 스토리지도 `AsyncStorage` 인터페이스를 준수하므로 `createAsyncStoragePersister`와 함께 사용할 수도 있습니다.
- [persistQueryClient](persistQueryClient.md#persistqueryclientprovider) 구성 요소를 사용하여 앱을 래핑합니다.

```tsx
import AsyncStorage from '@react-native-async-storage/async-storage'
import { QueryClient } from '@tanstack/react-query'
import { PersistQueryClientProvider } from '@tanstack/react-query-persist-client'
import { createAsyncStoragePersister } from '@tanstack/query-async-storage-persister'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      gcTime: 1000 * 60 * 60 * 24, // 24시간
    },
  },
})

const asyncStoragePersister = createAsyncStoragePersister({
  storage: AsyncStorage,
})

const Root = () => (
  <PersistQueryClientProvider
    client={queryClient}
    persistOptions={{ persister: asyncStoragePersister }}
  >
    <App />
  </PersistQueryClientProvider>
)

export default Root
```
## 재시도

재시도는 비동기식일 수도 있다는 점을 제외하면 [createSyncStoragePersister](createSyncStoragePersister.md)와 동일하게 작동합니다. 미리 정의된 모든 재시도 처리기를 사용할 수도 있습니다.

## API

### `createAsyncStoragePersister`

나중에 `persistQueryClient`와 함께 사용할 수 있는 asyncStoragePersister를 생성하려면 이 함수를 호출하세요.

```tsx
createAsyncStoragePersister(options: CreateAsyncStoragePersisterOptions)
```
### `Options`

```tsx
interface CreateAsyncStoragePersisterOptions {
  /* * 캐시에서 항목 검색을 설정하는 데 사용되는 스토리지 클라이언트 */
  storage: AsyncStorage | undefined | null
  /* * 캐시를 localStorage에 저장할 때 사용하는 키 */
  key?: string
  /* * localStorage 스팸을 방지하려면,
   * 캐시를 디스크에 저장하는 것을 제한하기 위해 ms 단위의 시간을 전달합니다. */
  throttleTime?: number
  /* * 데이터를 스토리지에 직렬화하는 방법 */
  serialize?: (client: PersistedClient) => string
  /* * 저장소에서 데이터를 역직렬화하는 방법 */
  deserialize?: (cachedString: string) => PersistedClient
  /* * 오류 발생 시 지속성을 재시도하는 방법 * */
  retry?: AsyncPersistRetryer
}

interface AsyncStorage<TStorageValue = string> {
  getItem: (key: string) => MaybePromise<TStorageValue | undefined | null>
  setItem: (key: string, value: TStorageValue) => MaybePromise<unknown>
  removeItem: (key: string) => MaybePromise<void>
  entries?: () => MaybePromise<Array<[key: string, value: TStorageValue]>>
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
