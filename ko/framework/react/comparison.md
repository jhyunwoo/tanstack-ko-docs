---
id: comparison
title: 비교 | React Query vs SWR vs Apollo vs RTK Query vs React Router
---




> 이 비교표는 최대한 정확하고 편견이 없도록 노력하고 있습니다. 이러한 라이브러리 중 하나를 사용하고 정보가 개선될 수 있다고 생각되면 이 페이지 하단에 있는 "Github에서 이 페이지 편집" 링크를 사용하여 변경 사항(주장 또는 주장 증거 포함)을 자유롭게 제안하십시오.

특징/능력 키:

- ✅ 1등급, 내장형, 추가 구성이나 코드 없이 즉시 사용 가능
- 🟡 지원되지만 비공식 제3자 또는 커뮤니티 라이브러리/기여로 지원됩니다.
- 🔶 지원되고 문서화되었지만 구현하려면 추가 사용자 코드가 필요합니다.
- 🛑 공식적으로 지원되거나 문서화되지 않았습니다.

||React Query|SWR [_(웹사이트)_][swr]|Apollo Client [_(웹사이트)_][apollo]|RTK Query [_(웹사이트)_][rtk-query]|React Router [_(웹사이트)_][react-router]|
| -------------------------------------------------- | ---------------------------------------- | ---------------------------------------- | ------------------------------------------ | ------------------------------------ | ------------------------------------------------------------------------- |
|GitHub 레포 / 별|[![][stars-react-query]][gh-react-query]|[![][stars-swr]][gh-swr]|[![][stars-apollo]][gh-apollo]|[![][stars-rtk-query]][gh-rtk-query]|[![][stars-react-router]][gh-react-router]|
|플랫폼 요구 사항|React|React|React, GraphQL|Redux|React|
|자체 비교 문서||(없음)|(없음)|[비교][rtk-query-comparison]|(없음)|
|지원되는 Query 문법|Promise, REST, GraphQL|Promise, REST, GraphQL|GraphQL, Any (Reactive Variables)|Promise, REST, GraphQL|Promise, REST, GraphQL|
|지원되는 프레임워크|React|React|React + 기타|Any|React|
|캐싱 전략|계층적 키 -> 값|고유 키 -> 값|정규화된 스키마|고유 키 -> 값|중첩 라우트 -> 값|
|캐시 키 전략|JSON|JSON|GraphQL Query|JSON|라우트 경로|
|캐시 변경 감지|심층 비교 키(안정적인 직렬화)|심층 비교 키(안정적인 직렬화)|심층 비교 키(불안정한 직렬화)|키 참조 동일성(===)|라우트 변경|
|데이터 변경 감지|심층 비교 + 구조적 공유|심층 비교 (`stable-hash` 사용)|심층 비교(불안정한 직렬화)|키 참조 동일성(===)|로더 실행|
|데이터 메모화|완전한 구조적 공유|동일성(===)|정규화된 동일성|동일성(===)|동일성(===)|
|번들 크기|[![][bp-react-query]][bpl-react-query]|[![][bp-swr]][bpl-swr]|[![][bp-apollo]][bpl-apollo]|[![][bp-rtk-query]][bpl-rtk-query]|[![][bp-react-router]][bpl-react-router] + [![][bp-history]][bpl-history]|
|API 정의 위치|컴포넌트, 외부 설정|컴포넌트|GraphQL 스키마|외부 설정|라우트 트리 설정|
|Queries|✅|✅|✅|✅|✅|
|캐시 지속성|✅|✅|✅|✅|🛑 활성 경로만 <sup>8</sup>|
|개발자 도구|✅|✅|✅|✅|🛑|
|폴링/간격|✅|✅|✅|✅|🛑|
|병렬 Queries|✅|✅|✅|✅|✅|
|종속 Queries|✅|✅|✅|✅|✅|
|페이지가 매겨진 Queries|✅|✅|✅|✅|✅|
|인피니트 Queries|✅|✅|✅|✅|🛑|
|양방향 무한 Queries|✅|🔶|🔶|✅|🛑|
|무한 Query 다시 가져오는 중|✅|✅|🛑|✅|🛑|
|지연된 Query 데이터<sup>1</sup>|✅|✅|✅|✅|✅|
|선택기|✅|🛑|✅|✅|해당 없음|
|초기 데이터|✅|✅|✅|✅|✅|
|스크롤 복구|✅|✅|✅|✅|✅|
|캐시 조작|✅|✅|✅|✅|🛑|
|오래된 Query 해고|✅|✅|✅|✅|✅|
|렌더 배치 및 최적화<sup>2</sup>|✅|✅|🛑|✅|✅|
|자동 쓰레기 수거|✅|🛑|🛑|✅|해당 없음|
|Mutation 후크|✅|✅|✅|✅|✅|
|오프라인 Mutation 지원|✅|🛑|🟡|🛑|🛑|
|API 프리패치|✅|✅|✅|✅|✅|
|Query 취소|✅|🛑|🛑|🛑|✅|
|부분 Query 일치<sup>3</sup>|✅|🔶|✅|✅|해당 없음|
|Stale While Revalidate|✅|✅|✅|✅|🛑|
|staleTime 설정|✅|🛑<sup>7</sup>|🛑|✅|🛑|
|사전 사용 Query/Mutation 구성<sup>4</sup>|✅|🛑|✅|✅|✅|
|윈도우 포커스 시 refetch|✅|✅|🛑|✅|🛑|
|네트워크 상태 변경 시 refetch|✅|✅|✅|✅|🛑|
|일반 캐시 탈수/재수화|✅|🛑|✅|✅|✅|
|오프라인 캐싱|✅|🛑|✅|🔶|🛑|
|React Suspense|✅|✅|✅|🛑|✅|
|추상화/불가지론적 코어|✅|🛑|✅|✅|🛑|
|Mutation<sup>5</sup> 이후 자동 다시 가져오기|🔶|🔶|✅|✅|✅|
|정규화된 캐싱<sup>6</sup>|🛑|🛑|✅|🛑|🛑|

### 참고 사항

> **<sup>1</sup> 지연된 Query 데이터** - React Query는 다음 query가 로드되는 동안 기존 query의 데이터를 계속 볼 수 있는 방법을 제공합니다(suspense가 곧 기본적으로 제공할 동일한 UX와 유사). 이는 새 query가 요청될 때마다 하드 로딩 상태를 표시하지 않으려는 페이지 매김 UI 또는 무한 로딩 UI를 작성할 때 매우 중요합니다. 다른 라이브러리에는 이 기능이 없으며 새 query가 로드되는 동안 새 query(프리페치되지 않은 경우)에 대한 하드 로딩 상태를 렌더링합니다.

> **<sup>2</sup> 렌더링 최적화** - React Query는 렌더링 성능이 뛰어납니다. 기본적으로 액세스되는 필드를 자동으로 추적하고 필드 중 하나가 변경되는 경우에만 다시 렌더링합니다. 이 최적화를 선택 해제하려면 `notifyOnChangeProps`를 `'all'`로 설정하면 query가 업데이트될 때마다 구성 요소가 다시 렌더링됩니다. 예를 들어 새 데이터가 있거나 가져오는 중임을 나타냅니다. React Query는 또한 업데이트를 일괄 처리하여 여러 구성 요소가 동일한 query를 사용할 때 애플리케이션이 한 번만 다시 렌더링되도록 합니다. `data` 또는 `error` 속성에만 관심이 있는 경우 `notifyOnChangeProps`를 `['data', 'error']`로 설정하여 렌더링 수를 더욱 줄일 수 있습니다.

> **<sup>3</sup> 부분 query 매칭** - React Query는 결정적 query 키 직렬화를 사용하기 때문에 이를 통해 일치시키려는 각 개별 query 키를 알 필요 없이 queries의 변수 그룹을 조작할 수 있습니다. 변수에 관계없이 키에서 `todos`로 시작하는 모든 query를 다시 가져오거나 변수 또는 중첩 속성이 있거나 없는 특정 queries를 대상으로 지정할 수 있으며 필터 기능을 사용하여 특정 조건을 통과하는 queries만 일치시킬 수도 있습니다.

> **<sup>4</sup> 사전 사용 Query 구성** - 이는 단순히 queries 및 mutations가 사용되기 전에 작동하는 방식을 구성할 수 있는 멋진 이름입니다. 예를 들어, query는 사전에 기본값으로 완전히 구성될 수 있으며, 이를 사용할 때가 되면 사용할 때마다 페처 및/또는 옵션을 전달하는 대신 `useQuery({ queryKey })`만 필요합니다. SWR은 기본 페처를 사전 구성할 수 있도록 하여 이 기능의 부분적인 형태를 가지고 있지만 query 기준이 아닌 글로벌 페처로만 가능하며 mutations에 대해서는 확실히 그렇지 않습니다.

> **<sup>5</sup> Mutation 이후 자동 다시 가져오기** - mutation가 발생한 후 진정한 자동 다시 가져오기가 발생하려면 라이브러리가 해당 스키마에서 개별 엔터티와 엔터티 유형을 식별하는 방법을 알 수 있도록 돕는 경험적 방법과 함께 스키마(graphQL이 제공하는 것과 같은)가 필요합니다.

> **<sup>6</sup> 정규화된 캐싱** - React Query, SWR 및 RTK-Query는 현재 일부 상위 수준 데이터 중복을 피하기 위해 플랫 아키텍처에 엔터티를 저장하는 것을 설명하는 자동 정규화된 캐싱을 지원하지 않습니다.

> **<sup>7</sup> SWR의 불변 모드** - SWR에는 캐시 수명 동안 query를 한 번만 가져올 수 있는 "불변" 모드가 제공되지만 여전히 오래된 시간 또는 조건부 자동 재검증 개념이 없습니다.

> **<sup>8</sup> React Router 캐시 지속성** - React Router는 현재 일치하는 경로를 넘어서는 데이터를 캐시하지 않습니다. 경로를 벗어나면 해당 데이터가 손실됩니다.

[bpl-react-query]: https://bundlephobia.com/result?p=@tanstack/react-query
[bp-react-query]: https://badgen.net/bundlephobia/minzip/@tanstack/react-query?label=💾
[gh-react-query]: https://github.com/tannerlinsley/react-query
[stars-react-query]: https://img.shields.io/github/stars/tannerlinsley/react-query?label=%F0%9F%8C%9F
[swr]: https://github.com/vercel/swr
[bp-swr]: https://badgen.net/bundlephobia/minzip/swr?label=💾
[gh-swr]: https://github.com/vercel/swr
[stars-swr]: https://img.shields.io/github/stars/vercel/swr?label=%F0%9F%8C%9F
[bpl-swr]: https://bundlephobia.com/result?p=swr
[apollo]: https://github.com/apollographql/apollo-client
[bp-apollo]: https://badgen.net/bundlephobia/minzip/@apollo/client?label=💾
[gh-apollo]: https://github.com/apollographql/apollo-client
[stars-apollo]: https://img.shields.io/github/stars/apollographql/apollo-client?label=%F0%9F%8C%9F
[bpl-apollo]: https://bundlephobia.com/result?p=@apollo/client
[rtk-query]: https://redux-toolkit.js.org/rtk-query/overview
[rtk-query-comparison]: https://redux-toolkit.js.org/rtk-query/comparison
[rtk-query-bundle-size]: https://redux-toolkit.js.org/rtk-query/comparison#bundle-size
[bp-rtk]: https://badgen.net/bundlephobia/minzip/@reduxjs/toolkit?label=💾
[bp-rtk-query]: https://badgen.net/bundlephobia/minzip/@reduxjs/toolkit?label=💾
[gh-rtk-query]: https://github.com/reduxjs/redux-toolkit
[stars-rtk-query]: https://img.shields.io/github/stars/reduxjs/redux-toolkit?label=🌟
[bpl-rtk]: https://bundlephobia.com/result?p=@reduxjs/toolkit
[bpl-rtk-query]: https://bundlephobia.com/package/@reduxjs/toolkit
[react-router]: https://github.com/remix-run/react-router
[bp-react-router]: https://badgen.net/bundlephobia/minzip/react-router-dom?label=💾
[gh-react-router]: https://github.com/remix-run/react-router
[stars-react-router]: https://img.shields.io/github/stars/remix-run/react-router?label=%F0%9F%8C%9F
[bpl-react-router]: https://bundlephobia.com/result?p=react-router-dom
[bp-history]: https://badgen.net/bundlephobia/minzip/history?label=💾
[bpl-history]: https://bundlephobia.com/result?p=history
