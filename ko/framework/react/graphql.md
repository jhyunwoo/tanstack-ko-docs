---
id: graphql
title: GraphQL
---




React Query의 가져오기 메커니즘은 Promise를 기반으로 구축되었으므로 GraphQL을 포함한 문자 그대로 모든 비동기 데이터 가져오기 클라이언트와 함께 React Query를 사용할 수 있습니다!

> React Query는 정규화된 캐싱을 지원하지 않는다는 점에 유의하세요. 대다수의 사용자는 실제로 정규화된 캐시가 필요하지 않거나 생각만큼 많은 혜택을 누리지 못하지만, 이를 보증할 수 있는 매우 드문 상황이 있을 수 있으므로 먼저 당사에 문의하여 실제로 필요한 것인지 확인하십시오!

[//]: # 'Codegen'

## 유형 안전성 및 코드 생성

`graphql-request^5` 및 [GraphQL 코드 생성기](https://graphql-code-generator.com/)와 함께 사용되는 React Query는 전체 유형의 GraphQL 작업을 제공합니다.

```tsx
import request from 'graphql-request'
import { useQuery } from '@tanstack/react-query'

import { graphql } from './gql/gql'

const allFilmsWithVariablesQueryDocument = graphql(/* GraphQL */ `
  query allFilmsWithVariablesQuery($first: Int!) {
    allFilms(first: $first) {
      edges {
        node {
          id
          title
        }
      }
    }
  }
`)

function App() {
  // `data`가 완전히 입력되었습니다!
  const { data } = useQuery({
    queryKey: ['films'],
    queryFn: async () =>
      request(
        'https://swapi-graphql.netlify.app/.netlify/functions/index',
        allFilmsWithVariablesQueryDocument,
        // 변수도 유형 검사됩니다!
        { first: 10 },
      ),
  })
  // ...
}
```
_[저장소에서 전체 예제]를 찾을 수 있습니다(https://github.com/dotansimha/graphql-code-generator/tree/7c25c4eeb77f88677fd79da557b7b5326e3f3950/examples/front-end/react/tanstack-react-query)_

[GraphQL 코드 생성기 문서 전용 가이드](https://www.the-guild.dev/graphql/codegen/docs/guides/react-vue)를 시작해보세요.

[//]: # 'Codegen'
