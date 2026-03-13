---
id: FocusManager
title: FocusManager
---




`FocusManager`는 TanStack Query 내에서 포커스 상태를 관리합니다.

기본 이벤트 리스너를 변경하거나 포커스 상태를 수동으로 변경하는 데 사용할 수 있습니다.

사용 가능한 방법은 다음과 같습니다.

- [`setEventListener`](#focusmanagerseteventlistener)
- [`subscribe`](#focusmanager구독)
- [`setFocused`](#focusmanagersetfocused)
- [`isFocused`](#focusmanagerisfocused)

## `focusManager.setEventListener`

`setEventListener`를 사용하여 사용자 정의 이벤트 리스너를 설정할 수 있습니다.

```tsx
import { focusManager } from '@tanstack/react-query'

focusManager.setEventListener((handleFocus) => {
  // 가시성 변경 듣기
  if (typeof window !== 'undefined' && window.addEventListener) {
    window.addEventListener('visibilitychange', handleFocus, false)
  }

  return () => {
    // 새로운 핸들러가 설정되면 구독을 취소하세요.
    window.removeEventListener('visibilitychange', handleFocus)
  }
})
```
## `focusManager.subscribe`

`subscribe`를 사용하여 가시성 상태의 변경 사항을 구독할 수 있습니다. 구독 취소 함수를 반환합니다.

```tsx
import { focusManager } from '@tanstack/react-query'

const unsubscribe = focusManager.subscribe((isVisible) => {
  console.log('isVisible', isVisible)
})
```
## `focusManager.setFocused`

`setFocused`를 사용하여 초점 상태를 수동으로 설정할 수 있습니다. 기본 초점 확인으로 돌아가도록 `undefined`를 설정합니다.

```tsx
import { focusManager } from '@tanstack/react-query'

// 집중 설정
focusManager.setFocused(true)

// 초점이 맞지 않게 설정
focusManager.setFocused(false)

// 기본 초점 확인으로 대체
focusManager.setFocused(undefined)
```
**옵션**

- `focused: boolean | undefined`

## `focusManager.isFocused`

`isFocused`를 사용하여 현재 초점 상태를 얻을 수 있습니다.

```tsx
const isFocused = focusManager.isFocused()
```
