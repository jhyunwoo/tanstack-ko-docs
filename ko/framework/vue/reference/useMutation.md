---
id: useMutation
title: useMutation
---





```tsx
const {
  data,
  error,
  isError,
  isIdle,
  isPending,
  isPaused,
  isSuccess,
  failureCount,
  failureReason,
  mutate,
  mutateAsync,
  reset,
  status,
  submittedAt,
  variables,
} = useMutation(
  {
    mutationFn,
    gcTime,
    meta,
    mutationKey,
    networkMode,
    onError,
    onMutate,
    onSettled,
    onSuccess,
    retry,
    retryDelay,
    scope,
    throwOnError,
  },
  queryClient,
)

mutate(variables, {
  onError,
  onSettled,
  onSuccess,
})
```
**매개변수1(옵션)**

- `mutationFn: (variables: TVariables, context: MutationFunctionContext) => Promise<TData>`
  - **필수이지만 기본 mutation 기능이 정의되지 않은 경우에만 해당**
  - 비동기 작업을 수행하고 Promise을 반환하는 함수입니다.
  - `variables`는 `mutate`가 `mutationFn`에 전달하는 개체입니다.
  - `context`는 `mutate`가 `mutationFn`에 전달하는 객체입니다. `QueryClient`, `mutationKey` 및 선택적 `meta` 개체에 대한 참조가 포함되어 있습니다.
- `gcTime: number | Infinity`
  - 사용되지 않은/비활성 캐시 데이터가 메모리에 남아 있는 시간(밀리초)입니다. mutation의 캐시가 사용되지 않거나 비활성화되면 해당 캐시 데이터는 이 기간 이후에 가비지 수집됩니다. 다른 캐시 시간이 지정되면 가장 긴 캐시 시간이 사용됩니다.
  - `Infinity`로 설정하면 가비지 수집이 비활성화됩니다.
  - 참고: 최대 허용 시간은 약 [24일](https://developer.mozilla.org/en-US/docs/Web/API/setTimeout#maximum_delay_value)이지만 [TimeoutManager](../../../reference/timeoutManager.md#timeoutmanagersettimeoutprovider)를 사용하여 이 제한을 해결할 수 있습니다.
- `mutationKey: unknown[]`
  - 선택사항
  - mutation 키는 `queryClient.setMutationDefaults`로 설정된 기본값을 상속하도록 설정할 수 있습니다.
- `networkMode: 'online' | 'always' | 'offlineFirst'`
  - 선택사항
  - 기본값은 `'online'`입니다.
  - 자세한 내용은 [네트워크 모드](../../react/guides/network-mode.md)를 참조하세요.
- `onMutate: (variables: TVariables, context: MutationFunctionContext) => Promise<TOnMutateResult | void> | TOnMutateResult | void`
  - 선택사항
  - 이 함수는 mutation 함수가 실행되기 전에 실행되며 mutation 함수가 수신하는 것과 동일한 변수가 전달됩니다.
  - mutation가 성공하기를 바라며 리소스에 대한 낙관적 업데이트를 수행하는 데 유용합니다.
  - 이 함수에서 반환된 값은 mutation 오류 발생 시 `onError` 및 `onSettled` 함수 모두에 전달되며 낙관적 업데이트를 롤백하는 데 유용할 수 있습니다.
- `onSuccess: (data: TData, variables: TVariables, onMutateResult: TOnMutateResult | undefined, context: MutationFunctionContext) => Promise<unknown> | unknown`
  - 선택사항
  - 이 함수는 mutation가 성공하면 실행되고 mutation의 결과가 전달됩니다.
  - Promise가 반환되면 계속 진행하기 전에 기다렸다가 해결됩니다.
- `onError: (err: TError, variables: TVariables, onMutateResult: TOnMutateResult | undefined, context: MutationFunctionContext) => Promise<unknown> | unknown`
  - 선택사항
  - mutation에 오류가 발생하면 이 함수가 실행되고 오류가 전달됩니다.
  - Promise가 반환되면 계속 진행하기 전에 기다렸다가 해결됩니다.
- `onSettled: (data: TData, error: TError, variables: TVariables, onMutateResult: TOnMutateResult | undefined, context: MutationFunctionContext) => Promise<unknown> | unknown`
  - 선택사항
  - 이 함수는 mutation가 성공적으로 가져오거나 오류가 발생하여 데이터 또는 오류가 전달될 때 실행됩니다.
  - Promise가 반환되면 계속 진행하기 전에 기다렸다가 해결됩니다.
- `retry: boolean | number | (failureCount: number, error: TError) => boolean`
  - 기본값은 `0`입니다.
  - `false`인 경우, 실패한 mutations는 ​​재시도하지 않습니다.
  - `true`, 실패한 mutations의 경우 무한 재시도합니다.
  - `number`로 설정된 경우, 예: `3`, 실패 mutations는 ​​실패한 mutations 수가 해당 숫자를 충족할 때까지 재시도합니다.
- `retryDelay: number | (retryAttempt: number, error: TError) => number`
  - 이 함수는 `retryAttempt` 정수와 실제 오류를 수신하고 다음 시도 전에 적용할 지연을 밀리초 단위로 반환합니다.
  - `attempt => Math.min(attempt > 1 ? 2 ** attempt * 1000 : 1000, 30 * 1000)`와 같은 기능은 지수 백오프를 적용합니다.
  - `attempt => attempt * 1000`와 같은 기능은 선형 백오프를 적용합니다.
- `scope: { id: string }`
  - 선택사항
  - 기본값은 고유 ID입니다(모든 mutations가 병렬로 실행되도록).- 동일한 범위 ID를 가진 Mutations는 직렬로 실행됩니다.
- `throwOnError: undefined | boolean | (error: TError) => boolean`
  - mutation 오류가 렌더링 단계에서 발생하고 가장 가까운 오류 경계로 전파되도록 하려면 이를 `true`로 설정합니다.
  - 오류 경계에 오류를 던지는 동작을 비활성화하려면 이를 `false`로 설정합니다.
  - 함수로 설정하면 오류가 전달되고 오류 경계에 오류를 표시할지(`true`) 또는 오류를 상태로 반환할지(`false`) 여부를 나타내는 boolean을 반환해야 합니다.
- `meta: Record<string, unknown>`
  - 선택사항
  - 설정된 경우 필요에 따라 사용할 수 있는 mutation 캐시 항목에 대한 추가 정보를 저장합니다. `mutation`를 사용할 수 있는 모든 곳에서 액세스할 수 있습니다(예: `onError`, `MutationCache`의 `onSuccess` 기능).

**매개변수2(QueryClient)**

- `queryClient?: QueryClient`
  - 사용자 정의 QueryClient를 사용하려면 이를 사용합니다. 그렇지 않으면 가장 가까운 컨텍스트의 컨텍스트가 사용됩니다.

**보고**

- `mutate: (variables: TVariables, { onSuccess, onSettled, onError }) => void`
  - mutation 함수는 변수를 사용하여 호출하여 mutation를 트리거하고 선택적으로 추가 콜백 옵션을 연결할 수 있습니다.
  - `variables: TVariables`
    - 선택사항
    - `mutationFn`에 전달할 변수 개체입니다.
  - `onSuccess: (data: TData, variables: TVariables, onMutateResult: TOnMutateResult | undefined, context: MutationFunctionContext) => void`
    - 선택사항
    - 이 함수는 mutation가 성공하면 실행되고 mutation의 결과가 전달됩니다.
    - Void 함수, 반환된 값은 무시됩니다.
  - `onError: (err: TError, variables: TVariables, onMutateResult: TOnMutateResult | undefined, context: MutationFunctionContext) => void`
    - 선택사항
    - mutation에 오류가 발생하면 이 함수가 실행되고 오류가 전달됩니다.
    - Void 함수, 반환된 값은 무시됩니다.
  - `onSettled: (data: TData | undefined, error: TError | null, variables: TVariables, onMutateResult: TOnMutateResult | undefined, context: MutationFunctionContext) => void`
    - 선택사항
    - 이 함수는 mutation가 성공적으로 가져오거나 오류가 발생하여 데이터 또는 오류가 전달될 때 실행됩니다.
    - Void 함수, 반환된 값은 무시됩니다.
  - 여러 번 요청하는 경우 `onSuccess`는 가장 최근에 호출한 후에만 실행됩니다.
- `mutateAsync: (variables: TVariables, { onSuccess, onSettled, onError }) => Promise<TData>`
  - `mutate`와 유사하지만 기다릴 수 있는 Promise을 반환합니다.
- `status: MutationStatus`
  - 될 것입니다 :
    - mutation 기능이 실행되기 전의 `idle` 초기 상태입니다.
    - mutation가 현재 실행 중인 경우 `pending`입니다.
    - 마지막 mutation 시도에서 오류가 발생한 경우 `error`입니다.
    - 마지막 mutation 시도가 성공한 경우 `success`입니다.
- `isIdle`, `isPending`, `isSuccess`, `isError`: `status`에서 파생된 boolean 변수
- `isPaused: boolean`
  - mutation가 `paused`인 경우 `true`가 됩니다.
  - 자세한 내용은 [네트워크 모드](../../react/guides/network-mode.md)를 참조하세요.
- `data: undefined | unknown`
  - 기본값은 `undefined`입니다.
  - mutation에 대한 마지막으로 성공적으로 해결된 데이터입니다.
- `error: null | TError`
  - 오류가 발생한 경우 query에 대한 오류 개체입니다.
- `reset: () => void`
  - mutation 내부 상태를 정리하는 기능입니다(즉, mutation를 초기 상태로 재설정합니다).
- `failureCount: number`
  - mutation의 실패 횟수입니다.
  - mutation가 실패할 때마다 증가합니다.
  - mutation가 성공하면 `0`로 재설정됩니다.
- `failureReason: null | TError`
  - mutation 재시도 실패 이유입니다.
  - mutation가 성공하면 `null`로 재설정됩니다.
- `submittedAt: number`
  - mutation가 제출된 시점의 타임스탬프입니다.
  - 기본값은 `0`입니다.
- `variables: undefined | TVariables`
  - `variables` 개체가 `mutationFn`에 전달되었습니다.
  - 기본값은 `undefined`입니다.