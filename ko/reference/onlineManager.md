---
id: OnlineManager
title: OnlineManager
---




`OnlineManager`는 TanStack Query 내의 온라인 상태를 관리합니다. 기본 이벤트 리스너를 변경하거나 온라인 상태를 수동으로 변경하는 데 사용할 수 있습니다.

> 기본적으로 `onlineManager`는 활성 네트워크 연결을 가정하고 `window` 개체에서 `online` 및 `offline` 이벤트를 수신하여 변경 사항을 감지합니다.

> 이전 버전에서는 `navigator.onLine`를 사용하여 네트워크 상태를 확인했습니다. 하지만 Chromium 기반 브라우저에서는 제대로 작동하지 않습니다. 거짓 부정과 관련된 [많은 문제](https://bugs.chromium.org/p/chromium/issues/list?q=navigator.online)가 있으며 이로 인해 Queries가 `offline`로 잘못 표시됩니다.

> 이를 방지하기 위해 이제 항상 `online: true`로 시작하고 `online` 및 `offline` 이벤트만 수신하여 상태를 업데이트합니다.

> 이는 거짓 부정의 가능성을 줄여야 하지만, 인터넷 연결 없이도 작동할 수 있는 serviceWorkers를 통해 로드되는 오프라인 앱의 경우 거짓 긍정을 의미할 수 있습니다.

사용 가능한 방법은 다음과 같습니다.

- [`setEventListener`](#onlinemanagerseteventlistener)
- [`subscribe`](#onlinemanager구독)
- [`setOnline`](#onlinemanagersetonline)
- [`isOnline`](#onlinemanagerisonline)

## `onlineManager.setEventListener`

`setEventListener`를 사용하여 사용자 정의 이벤트 리스너를 설정할 수 있습니다.

```tsx
import NetInfo from '@react-native-community/netinfo'
import { onlineManager } from '@tanstack/react-query'

onlineManager.setEventListener((setOnline) => {
  return NetInfo.addEventListener((state) => {
    setOnline(!!state.isConnected)
  })
})
```
## `onlineManager.subscribe`

`subscribe`를 사용하여 온라인 상태의 변경 사항을 구독할 수 있습니다. 구독 취소 함수를 반환합니다.

```tsx
import { onlineManager } from '@tanstack/react-query'

const unsubscribe = onlineManager.subscribe((isOnline) => {
  console.log('isOnline', isOnline)
})
```
## `onlineManager.setOnline`

`setOnline`를 사용하여 온라인 상태를 수동으로 설정할 수 있습니다.

```tsx
import { onlineManager } from '@tanstack/react-query'

// 온라인으로 설정
onlineManager.setOnline(true)

// 오프라인으로 설정
onlineManager.setOnline(false)
```
**옵션**

- `online: boolean`

## `onlineManager.isOnline`

`isOnline`를 사용하여 현재 온라인 상태를 가져올 수 있습니다.

```tsx
const isOnline = onlineManager.isOnline()
```
