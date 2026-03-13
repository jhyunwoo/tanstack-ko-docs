---
id: streamedQuery
title: streamedQuery
---




`streamedQuery`는 [AsyncIterable](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/AsyncIterator)에서 데이터를 스트리밍하는 query 함수를 생성하는 도우미 함수입니다. 데이터는 수신된 모든 청크의 배열이 됩니다. query는 첫 번째 데이터 청크가 수신될 때까지 `pending` 상태에 있지만 그 이후에는 `success`로 이동합니다. query는 스트림이 끝날 때까지 fetchStatus `fetching`에 유지됩니다.

`streamedQuery`의 실제 작동 모습을 보려면 [GitHub의 examples/react/chat 디렉터리](https://github.com/TanStack/query/tree/489359a569fd865f3afd7aac8fa43dfc429309e3/examples/react/chat)에서 채팅 예시를 살펴보세요.

```tsx
import { experimental_streamedQuery as streamedQuery } from '@tanstack/react-query'

const query = queryOptions({
  queryKey: ['data'],
  queryFn: streamedQuery({
    streamFn: fetchDataInChunks,
  }),
})
```
> 참고: `streamedQuery`는 커뮤니티로부터 피드백을 수집하기 위해 현재 `experimental`로 표시되어 있습니다. API를 사용해 보고 피드백이 있으면 이 [GitHub 토론](https://github.com/TanStack/query/discussions/9065)에 제공해 주세요.

**옵션**

- `streamFn: (context: QueryFunctionContext) => Promise<AsyncIterable<TData>>`
  - **필수**
  - 스트리밍할 데이터가 포함된 AsyncIterable의 Promise을 반환하는 함수입니다.
  - [QueryFunctionContext](../framework/react/guides/query-functions.md#queryfunctioncontext)를 수신합니다.
- `refetchMode?: 'append' | 'reset' | 'replace'`
  - 선택사항
  - 다시 가져오기를 처리하는 방법을 정의합니다.
  - 기본값은 `'reset'`입니다.
  - `'reset'`로 설정하면 query가 모든 데이터를 지우고 `pending` 상태로 돌아갑니다.
  - `'append'`로 설정하면 기존 데이터에 데이터가 추가됩니다.
  - `'replace'`로 설정하면 스트림이 끝나면 모든 데이터가 캐시에 기록됩니다.
- `reducer?: (accumulator: TData, chunk: TQueryFnData) => TData`
  - 선택사항
  - 스트리밍된 청크(`TQueryFnData`)를 최종 데이터 형태(`TData`)로 줄입니다.
  - 기본값: `TData`가 배열인 경우 각 청크를 누산기 끝에 추가합니다.
  - `TData`가 어레이가 아닌 경우 사용자 지정 `reducer`를 제공해야 합니다.
- `initialValue?: TData = TQueryFnData`
  - 선택사항
  - 첫 번째 청크를 가져오는 동안 사용할 초기 데이터를 정의하고, 스트림에서 값이 생성되지 않는 경우에도 반환됩니다.
  - 맞춤형 `reducer` 제공 시 필수입니다.
  - 기본값은 빈 배열입니다.