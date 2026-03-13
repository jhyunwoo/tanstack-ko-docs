---
id: devtools
title: 개발자 도구
---




> Chrome, Firefox 및 Edge 사용자의 경우: 브라우저 DevTools에서 TanStack Query를 직접 디버깅하기 위해 타사 브라우저 확장 프로그램을 사용할 수 있습니다. 이는 프레임워크별 devtools 패키지와 동일한 기능을 제공합니다.
>
> - <img alt="Chrome 로고" src="https://www.google.com/chrome/static/images/chrome-logo.svg" width="16" height="16" class="inline mr-1 not-prose" /> [Devtools for 크롬](https://chromewebstore.google.com/detail/tanstack-query-devtools/annajfchloimdhceglpgglpeepfghfai)
> - <img alt="Firefox 로고" src="https://upload.wikimedia.org/wikipedia/commons/a/a0/Firefox_logo%2C_2019.svg" width="16" height="16" class="inline mr-1 not-prose" /> [Devtools for Firefox](https://addons.mozilla.org/en-US/firefox/addon/tanstack-query-devtools/)
> - <img alt="Edge logo" src="https://upload.wikimedia.org/wikipedia/commons/9/98/Microsoft_Edge_logo_%282019%29.svg" width="16" height="16" class="inline mr-1 not-prose" /> [Devtools for 엣지](https://microsoftedge.microsoft.com/addons/detail/tanstack-query-devtools/edmdpkgkacmjopodhfolmphdenmddobj)

## 개발자 도구 활성화

devtools는 queries 및 mutations를 디버깅하고 검사하는 데 도움이 됩니다. `provideTanStackQuery`에 `withDevtools`를 추가하여 devtools를 활성화할 수 있습니다.

기본적으로 Angular Query Devtools는 개발 모드 번들에만 포함되어 있으므로 프로덕션 빌드 중에 제외하는 것에 대해 걱정할 필요가 없습니다.

```ts
import {
  QueryClient,
  provideTanStackQuery,
} from '@tanstack/angular-query-experimental'

import { withDevtools } from '@tanstack/angular-query-experimental/devtools'

export const appConfig: ApplicationConfig = {
  providers: [provideTanStackQuery(new QueryClient(), withDevtools())],
}
```
## 프로덕션 중인 Devtools

Devtools는 프로덕션 빌드에서 자동으로 제외됩니다. 그러나 프로덕션에서는 devtools를 지연 로드하는 것이 바람직할 수 있습니다.

프로덕션 빌드에서 `withDevtools`를 사용하려면 `production` 하위 경로를 사용하여 가져옵니다. 프로덕션 하위 경로에서 내보낸 함수는 기본 하위 경로와 동일하지만 프로덕션 빌드에서 제외되지 않습니다.

```ts
import { withDevtools } from '@tanstack/angular-query-experimental/devtools/production'
```
devtools가 로드되는 시기를 제어하려면 `loadDevtools` 옵션을 사용할 수 있습니다.

옵션을 설정하지 않거나 'auto'로 설정하면 Angular가 개발 모드에서 실행될 때만 devtools가 자동으로 로드됩니다.

```ts
import { withDevtools } from '@tanstack/angular-query-experimental/devtools'

provideTanStackQuery(new QueryClient(), withDevtools())

// 이는 다음과 같습니다.
provideTanStackQuery(
  new QueryClient(),
  withDevtools(() => ({ loadDevtools: 'auto' })),
)
```
옵션을 true로 설정하면 devtools가 개발 모드와 프로덕션 모드 모두에 로드됩니다.

이는 [Angular 환경 구성](https://angular.dev/tools/cli/environments)을 기반으로 devtool을 로드하려는 경우 유용합니다. 예: 애플리케이션이 프로덕션 빌드 준비 환경에서 실행 중인 경우 이를 true로 설정할 수 있습니다.

```ts
import { environment } from './environments/environment'
// 프로덕션 빌드에서 devtool을 로드하려면 프로덕션 하위 경로를 사용해야 합니다.
import { withDevtools } from '@tanstack/angular-query-experimental/devtools/production'

provideTanStackQuery(
  new QueryClient(),
  withDevtools(() => ({ loadDevtools: environment.loadDevtools })),
)
```
옵션을 false로 설정하면 devtools가 로드되지 않습니다.

```ts
provideTanStackQuery(
  new QueryClient(),
  withDevtools(() => ({ loadDevtools: false })),
)
```
## 반응성을 통해 옵션 도출

옵션은 신호를 통한 반응성을 지원하기 위해 콜백 함수에서 `withDevtools`로 전달됩니다. 다음 예에서는
키보드 단축키를 통해 방출되는 RxJS Observable에서 신호가 생성됩니다. 파생된 신호가 true로 설정되면 devtools가 느리게 로드됩니다.

아래 예제에서는 항상 개발 모드에서 devtools를 로드하고 키보드 단축키를 누를 때 프로덕션 모드에서 요청 시 로드합니다.

```ts
import { Injectable, isDevMode } from '@angular/core'
import { fromEvent, map, scan } from 'rxjs'
import { toSignal } from '@angular/core/rxjs-interop'

@Injectable({ providedIn: 'root' })
export class DevtoolsOptionsManager {
  loadDevtools = toSignal(
    fromEvent<KeyboardEvent>(document, 'keydown').pipe(
      map(
        (event): boolean =>
          event.metaKey && event.ctrlKey && event.shiftKey && event.key === 'D',
      ),
      scan((acc, curr) => acc || curr, isDevMode()),
    ),
    {
      initialValue: isDevMode(),
    },
  )
}
```
콜백에서 서비스와 같은 주입 가능 항목을 사용하려면 `deps`를 사용할 수 있습니다. 주입된 값은 콜백 함수에 매개변수로 전달됩니다.

이는 Angular의 [`useFactory`](https://angular.dev/guide/di/dependent-injection-providers#factory-providers-usefactory) 공급자의 `deps`와 유사합니다.

```ts
// ...
// 👇 프로덕션 빌드에서 devtools 지연 로딩을 활성화하기 위해 프로덕션 하위 경로에서 가져옵니다.
import { withDevtools } from '@tanstack/angular-query-experimental/devtools/production'

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(),
    provideTanStackQuery(
      new QueryClient(),
      withDevtools(
        (devToolsOptionsManager: DevtoolsOptionsManager) => ({
          loadDevtools: devToolsOptionsManager.loadDevtools(),
        }),
        {
          // `deps`는 `DevtoolsOptionsManager`를 `withDevtools` 콜백에 삽입하고 전달하는 데 사용됩니다.
          deps: [DevtoolsOptionsManager],
        },
      ),
    ),
  ],
}
```
### 콜백에서 반환된 옵션

이러한 옵션 중 `loadDevtools`, `client`, `position`, `errorTypes`, `buttonPosition` 및 `initialIsOpen`는 신호를 통한 반응성을 지원합니다.

- `loadDevtools?: 'auto' | boolean`
  - 기본값은 `auto`입니다. 개발 모드에 있을 때 개발자 도구를 느리게 로드합니다. 프로덕션 모드에서는 로딩을 건너뜁니다.
  - 이를 사용하여 devtools가 로드되는지 제어합니다.
- `initialIsOpen?: Boolean`
  - 도구가 기본적으로 열려 있도록 하려면 이를 `true`로 설정하십시오.
- `buttonPosition?: "top-left" | "top-right" | "bottom-left" | "bottom-right" | "relative"`
  - 기본값은 `bottom-right`입니다.
  - devtools 패널을 열고 닫는 TanStack 로고의 위치
  - `relative`인 경우 버튼은 개발자 도구를 렌더링하는 위치에 배치됩니다.
- `position?: "top" | "bottom" | "left" | "right"`
  - 기본값은 `bottom`입니다.
  - Angular Query devtools 패널의 위치
-`client?: QueryClient`,
  - 사용자 정의 QueryClient를 사용하려면 이를 사용합니다. 그렇지 않으면 `provideTanStackQuery`를 통해 제공되는 QueryClient가 주입됩니다.
- `errorTypes?: { name: string; initializer: (query: Query) => TError}[]`
  - 이를 사용하여 queries에서 발생할 수 있는 일부 오류를 미리 정의합니다. UI에서 해당 오류가 전환되면 초기화 프로그램이 특정 query와 함께 호출됩니다. 오류를 반환해야 합니다.
- `styleNonce?: string`
  - 문서 헤드에 추가된 스타일 태그에 nonce를 전달하는 데 사용합니다. 이는 인라인 스타일을 허용하기 위해 CSP(콘텐츠 보안 정책) nonce를 사용하는 경우 유용합니다.
- `shadowDOMTarget?: ShadowRoot`
  - 기본 동작은 devtool의 스타일을 DOM 내의 head 태그에 적용합니다.
  - 스타일이 light DOM의 head 태그 내에서 대신 Shadow DOM 내에서 적용되도록 Shadow DOM 대상을 devtools에 전달하는 데 사용합니다.
- `hideDisabledQueries?: boolean`
  - devtools 패널에서 비활성화된 queries를 숨기려면 이를 true로 설정합니다.