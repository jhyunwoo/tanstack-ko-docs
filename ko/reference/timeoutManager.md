---
id: TimeoutManager
title: TimeoutManager
---




`TimeoutManager`는 TanStack Query의 `setTimeout` 및 `setInterval` 타이머를 처리합니다.

TanStack Query는 타이머를 사용하여 query `staleTime` 및 `gcTime`와 같은 기능은 물론 재시도, 조절 및 디바운싱도 구현합니다.

기본적으로 TimeoutManager는 전역 `setTimeout` 및 `setInterval`를 사용하지만 대신 사용자 지정 구현을 사용하도록 구성할 수 있습니다.

사용 가능한 방법은 다음과 같습니다.

- [`timeoutManager.setTimeoutProvider`](#timeoutmanagersettimeoutprovider)
  - [`TimeoutProvider`](#timeoutprovider)
- [`timeoutManager.setTimeout`](#timeoutmanagersettimeout)
- [`timeoutManager.clearTimeout`](#timeoutmanagercleartimeout)
- [`timeoutManager.setInterval`](#timeoutmanagerset간격)
- [`timeoutManager.clearInterval`](#timeoutmanagerclearinterval)

## `timeoutManager.setTimeoutProvider`

`setTimeoutProvider`를 사용하면 `TimeoutProvider`라고 하는 `setTimeout`, `clearTimeout`, `setInterval`, `clearInterval` 기능의 사용자 지정 구현을 설정하는 데 사용할 수 있습니다.

이는 수천 개의 queries에서 이벤트 루프 성능 문제를 발견한 경우 유용할 수 있습니다. 사용자 정의 TimeoutProvider는 전역 `setTimeout` 최대 지연 값인 약 [24일](https://developer.mozilla.org/en-US/docs/Web/API/Window/setTimeout#maximum_delay_value)보다 긴 타이머 지연을 지원할 수도 있습니다.

QueryClient 또는 queries를 생성하기 전에 `setTimeoutProvider`를 호출하는 것이 중요합니다. 그러면 서로 다른 TimeoutProvider가 서로의 타이머를 취소할 수 없기 때문에 동일한 공급자가 응용 프로그램의 모든 타이머에 일관되게 사용됩니다.

```tsx
import { timeoutManager, QueryClient } from '@tanstack/react-query'
import { CustomTimeoutProvider } from './CustomTimeoutProvider'

timeoutManager.setTimeoutProvider(new CustomTimeoutProvider())

export const queryClient = new QueryClient()
```
### `TimeoutProvider`

타이머는 성능에 매우 민감합니다. 단기 타이머(예: 5초 미만 지연)는 지연 시간에 민감한 경향이 있습니다. 여기서 장기 타이머는 [타이머 병합](https://en.wikipedia.org/wiki/Timer_coalescing) - 비슷한 기한을 가진 타이머 일괄 처리 - [계층적 시간 휠](https://www.npmjs.com/package/timer-wheel)과 같은 데이터 구조를 사용하여 더 많은 이점을 얻을 수 있습니다.

`TimeoutProvider` 유형에서는 구현 시 [Symbol.toPrimitive][toPrimitive]를 통해 `number`로 변환될 수 있는 타이머 ID 객체를 처리해야 합니다. NodeJS와 같은 런타임은 전역 `setTimeout` 및 `setInterval` 함수에서 [객체][nodejs-timeout]를 반환하기 때문입니다. TimeoutProvider 구현은 타이머 ID를 내부적으로 숫자로 강제하거나 `{ [Symbol.toPrimitive]: () => number }`를 구현하는 고유한 사용자 정의 객체 유형을 반환할 수 있습니다.

[nodejs-timeout]: https://nodejs.org/api/timers.html#class-timeout
[toPrimitive]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol/toPrimitive

```tsx
type ManagedTimerId = number | { [Symbol.toPrimitive]: () => number }

type TimeoutProvider<TTimerId extends ManagedTimerId = ManagedTimerId> = {
  readonly setTimeout: (callback: TimeoutCallback, delay: number) => TTimerId
  readonly clearTimeout: (timeoutId: TTimerId | undefined) => void

  readonly setInterval: (callback: TimeoutCallback, delay: number) => TTimerId
  readonly clearInterval: (intervalId: TTimerId | undefined) => void
}
```
## `timeoutManager.setTimeout`

`setTimeout(callback, delayMs)`는 전역 [setTimeout 함수](https://developer.mozilla.org/en-US/docs/Web/API/Window/setTimeout)와 같이 약 `delay` 밀리초 후에 실행되도록 콜백을 예약합니다. 콜백은 `timeoutManager.clearTimeout`를 사용하여 취소할 수 있습니다.

타이머 ID는 숫자이거나 [Symbol.toPrimitive][toPrimitive]를 통해 숫자로 강제 변환될 수 있는 객체일 수 있습니다.

```tsx
import { timeoutManager } from '@tanstack/react-query'

const timeoutId = timeoutManager.setTimeout(
  () => console.log('ran at:', new Date()),
  1000,
)

const timeoutIdNumber: number = Number(timeoutId)
```
## `timeoutManager.clearTimeout`

`clearTimeout(timerId)`는 전역 [clearTimeout 함수](https://developer.mozilla.org/en-US/docs/Web/API/Window/clearTimeout)와 같이 `setTimeout`로 예약된 시간 초과 콜백을 취소합니다. `timeoutManager.setTimeout`에서 반환한 타이머 ID로 호출해야 합니다.

```tsx
import { timeoutManager } from '@tanstack/react-query'

const timeoutId = timeoutManager.setTimeout(
  () => console.log('ran at:', new Date()),
  1000,
)

timeoutManager.clearTimeout(timeoutId)
```
## `timeoutManager.setInterval`

`setInterval(callback, intervalMs)`는 전역 [setInterval 함수](https://developer.mozilla.org/en-US/docs/Web/API/Window/setInterval)와 같이 대략 `intervalMs`마다 호출되도록 콜백을 예약합니다.

`setTimeout`와 마찬가지로 타이머 ID를 반환합니다. 타이머 ID는 숫자일 수도 있고 [Symbol.toPrimitive](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol/toPrimitive)를 통해 숫자로 강제 변환될 수 있는 객체일 수도 있습니다.

```tsx
import { timeoutManager } from '@tanstack/react-query'

const intervalId = timeoutManager.setInterval(
  () => console.log('ran at:', new Date()),
  1000,
)
```
## `timeoutManager.clearInterval`

`clearInterval(intervalId)`는 전역 [clearInterval 함수](https://developer.mozilla.org/en-US/docs/Web/API/Window/clearInterval)와 같이 간격을 취소하는 데 사용할 수 있습니다. `timeoutManager.setInterval`에서 반환한 간격 ID로 호출해야 합니다.

```tsx
import { timeoutManager } from '@tanstack/react-query'

const intervalId = timeoutManager.setInterval(
  () => console.log('ran at:', new Date()),
  1000,
)

timeoutManager.clearInterval(intervalId)
```
