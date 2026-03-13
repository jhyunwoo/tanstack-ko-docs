---
id: QueryErrorResetBoundary
title: QueryErrorResetBoundary
---




queries에서 **suspense** 또는 **throwOnError**를 사용할 때 오류가 발생한 후 다시 렌더링할 때 다시 시도하고 싶다는 것을 queries에 알릴 수 있는 방법이 필요합니다. `QueryErrorResetBoundary` 구성 요소를 사용하면 구성 요소 경계 내의 모든 query 오류를 재설정할 수 있습니다.

```tsx
import { QueryErrorResetBoundary } from '@tanstack/react-query'
import { ErrorBoundary } from 'react-error-boundary'

const App = () => (
  <QueryErrorResetBoundary>
    {({ reset }) => (
      <ErrorBoundary
        onReset={reset}
        fallbackRender={({ resetErrorBoundary }) => (
          <div>
            There was an error!
            <Button onClick={() => resetErrorBoundary()}>Try again</Button>
          </div>
        )}
      >
        <Page />
      </ErrorBoundary>
    )}
  </QueryErrorResetBoundary>
)
```
