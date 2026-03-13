---
id: broadcastQueryClient
title: broadcastQueryClient (Experimental)
---




> 매우 중요: 이 유틸리티는 현재 실험 단계에 있습니다. 즉, 마이너 AND 패치 릴리스에서 주요 변경 사항이 발생합니다. 자신의 책임하에 사용하십시오. 실험 단계의 프로덕션에서 이 기능을 사용하기로 선택한 경우 예상치 못한 중단을 방지하기 위해 버전을 패치 수준 버전으로 잠그십시오.

`broadcastQueryClient`는 동일한 출처를 가진 브라우저 탭/창 간에 queryClient의 상태를 브로드캐스팅하고 동기화하기 위한 유틸리티입니다.

## 설치

이 유틸리티는 별도의 패키지로 제공되며 `'@tanstack/query-broadcast-client-experimental'` 가져오기에서 사용할 수 있습니다.

## 용법

`broadcastQueryClient` 함수를 가져와서 `QueryClient` 인스턴스에 전달하고 선택적으로 `broadcastChannel`를 설정합니다.

```tsx
import { broadcastQueryClient } from '@tanstack/query-broadcast-client-experimental'

const queryClient = new QueryClient()

broadcastQueryClient({
  queryClient,
  broadcastChannel: 'my-app',
})
```
## API

### `broadcastQueryClient`

이 함수에 `QueryClient` 인스턴스를 전달하고 선택적으로 `broadcastChannel`를 전달합니다.

```tsx
broadcastQueryClient({ queryClient, broadcastChannel })
```
### `Options`

옵션 개체:

```tsx
interface BroadcastQueryClientOptions {
  /* * 동기화할 QueryClient */
  queryClient: QueryClient
  /* * 사용될 고유한 채널 이름입니다.
   * 탭과 창 사이의 통신을 위해 */
  broadcastChannel?: string
  /* * BroadcastChannel API 옵션 */
  options?: BroadcastChannelOptions
}
```
기본 옵션은 다음과 같습니다.

```tsx
{
  broadcastChannel = 'tanstack-query',
}
```
