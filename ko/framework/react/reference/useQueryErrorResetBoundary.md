---
id: useQueryErrorResetBoundary
title: useQueryErrorResetBoundary
---




이 후크는 가장 가까운 `QueryErrorResetBoundary` 내의 모든 query 오류를 재설정합니다. 정의된 경계가 없으면 전역적으로 재설정됩니다.

```tsx
import { useQueryErrorResetBoundary } from '@tanstack/react-query'
import { ErrorBoundary } from 'react-error-boundary'

const App = () => {
  const { reset } = useQueryErrorResetBoundary()
  return (
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
  )
}
```
