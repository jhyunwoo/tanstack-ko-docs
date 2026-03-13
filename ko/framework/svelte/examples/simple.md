# 날씬한 + TS + Vite

이 템플릿은 Vite에서 Svelte 및 TypeScript를 사용하여 개발을 시작하는 데 도움이 됩니다.

## 권장 IDE 설정

[VS 코드](https://code.visualstudio.com/) + [Svelte](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode).

## 공식 Svelte 프레임워크가 필요합니까?

역시 Vite로 구동되는 [SvelteKit](https://github.com/sveltejs/kit#readme)을 확인해 보세요. 서버리스 우선 접근 방식으로 어디에나 배포하고 TypeScript, SCSS, Less에 대한 기본 지원과 mdsvex, GraphQL, PostCSS, Tailwind CSS 등에 대한 쉽게 추가된 지원을 통해 다양한 플랫폼에 적응합니다.

## 기술적인 고려사항

**SvelteKit 대신 이것을 사용하는 이유는 무엇입니까?**

- 일부 사용자에게는 바람직하지 않을 수 있는 자체 라우팅 솔루션을 제공합니다.
- 무엇보다도 Vite 앱이 아닌 내부적으로 Vite를 사용하는 프레임워크입니다.
  예를 들어 `vite dev` 및 `vite build`는 SvelteKit 환경에서 작동하지 않습니다.

이 템플릿에는 HMR 및 intellisense와 관련된 개발자 경험을 고려하면서 Vite + TypeScript + Svelte를 시작하는 데 필요한 내용이 최대한 적게 포함되어 있습니다. 이는 다른 `create-vite` 템플릿과 동등한 기능을 보여 주며 Vite + Svelte 프로젝트에 발을 담그는 초보자에게 좋은 출발점이 됩니다.

나중에 SvelteKit에서 제공하는 확장된 기능과 확장성이 필요한 경우 템플릿은 SvelteKit과 유사하게 구성되어 쉽게 마이그레이션할 수 있습니다.

**`jsconfig.json` 또는 `tsconfig.json` 내부에서 `compilerOptions.types` 대신 `global.d.ts`를 사용하는 이유는 무엇입니까?**

`compilerOptions.types`를 설정하면 구성에 명시적으로 나열되지 않은 다른 모든 유형이 차단됩니다. 삼중 슬래시 참조를 사용하면 전체 작업공간에서 유형 정보를 허용하는 기본 TypeScript 설정을 유지하는 동시에 `svelte` 및 `vite/client` 유형 정보도 추가합니다.

**`.vscode/extensions.json`를 포함하는 이유는 무엇입니까?**

다른 템플릿은 README를 통해 간접적으로 확장을 권장하지만 이 파일을 사용하면 VS Code는 프로젝트를 열 때 사용자에게 권장 확장을 설치하라는 메시지를 표시할 수 있습니다.

**TS 템플릿에서 `allowJs`를 활성화하는 이유는 무엇입니까?**

`allowJs: false`는 실제로 프로젝트에서 `.js` 파일의 사용을 방지하지만 `.svelte` 파일의 JavaScript 구문 사용을 방지하지는 않습니다. 또한 `checkJs: false`를 강제하여 두 세계 모두에서 최악의 결과를 가져옵니다. 전체 코드베이스가 TypeScript임을 보장할 수 없으며 기존 JavaScript에 대한 유형 검사도 더 나빠집니다. 또한 혼합 코드베이스가 관련될 수 있는 유효한 사용 사례가 있습니다.

**HMR이 내 로컬 구성 요소 상태를 유지하지 않는 이유는 무엇입니까?**

HMR 상태 보존에는 여러 문제가 있습니다! 종종 놀라운 동작으로 인해 `svelte-hmr` 및 `@sveltejs/vite-plugin-svelte` 모두에서 기본적으로 비활성화되었습니다. 자세한 내용은 [여기](https://github.com/rixo/svelte-hmr#svelte-hmr)에서 읽어보실 수 있습니다.

구성 요소 내에 유지해야 하는 중요한 상태가 있는 경우 HMR로 대체되지 않는 외부 저장소를 만드는 것이 좋습니다.

```ts
// store.ts
// 매우 간단한 외부 저장소
import { writable } from 'svelte/store'
export default writable(0)
```
