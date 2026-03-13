---
id: important-defaults
title: 중요한 기본값
---




기본적으로 TanStack Query는 **공격적이지만 정상적인** 기본값으로 구성됩니다. **때때로 이러한 기본값은 새로운 사용자를 당황하게 하거나 사용자가 알 수 없는 경우 학습/디버깅을 어렵게 만들 수 있습니다.** TanStack Query를 계속 배우고 사용할 때 염두에 두십시오.

- 기본적으로 `useQuery` 또는 `useInfiniteQuery`를 통한 Query 인스턴스는 **캐시된 데이터를 오래된 것으로 간주합니다**.

> 이 동작을 변경하려면 `staleTime` 옵션을 사용하여 전역적으로 그리고 query별로 queries를 구성할 수 있습니다. 더 긴 `staleTime`를 지정하면 queries가 데이터를 자주 다시 가져오지 않음을 의미합니다.

- `staleTime` 세트가 있는 Query는 `staleTime`가 경과될 때까지 **신선한** 것으로 간주됩니다.
  - `staleTime`를 예를 들어로 설정합니다. `2 * 60 * 1000`는 2분 동안 또는 Query가 [수동으로 무효화](query-invalidation.md)될 때까지 어떤 종류의 다시 가져오기도 트리거하지 않고 캐시에서 데이터를 읽을 수 있도록 합니다.
  - Query가 [수동으로 무효화](query-invalidation.md)될 때까지 다시 가져오기를 트리거하지 않도록 `staleTime`를 `Infinity`로 설정합니다.
  - Query가 [수동으로 무효화](query-invalidation.md)되더라도 다시 가져오기를 **절대** 트리거하지 않으려면 `staleTime`를 `'static'`로 설정합니다.

- 오래된 queries는 다음과 같은 경우 백그라운드에서 자동으로 다시 가져옵니다.
  - query 마운트의 새로운 인스턴스
  - 창의 초점이 다시 맞춰졌습니다.
  - 네트워크가 다시 연결되었습니다

> 과도한 다시 가져오기를 방지하려면 `staleTime`를 설정하는 것이 권장되지만, `refetchOnMount`, `refetchOnWindowFocus` 및 `refetchOnReconnect`와 같은 옵션을 설정하여 다시 가져오기 시점을 사용자 정의할 수도 있습니다.

- Queries는 `refetchInterval`와 함께 선택적으로 구성하여 `staleTime` 설정과 관계없이 주기적으로 다시 가져오기를 트리거할 수 있습니다.

- `useQuery`, `useInfiniteQuery` 또는 query 관찰자의 활성 인스턴스가 더 이상 없는 Query 결과는 "비활성"으로 표시되고 나중에 다시 사용될 경우를 대비해 캐시에 남아 있습니다.
- 기본적으로 "비활성" queries는 **5분** 후에 가비지 수집됩니다.

> 이를 변경하려면 queries의 기본 `gcTime`를 `1000 * 60 * 5` 밀리초가 아닌 다른 값으로 변경할 수 있습니다.

- 실패한 Queries는 캡처하여 UI에 오류를 표시하기 전에 **지수적 백오프 지연을 사용하여 3번 자동으로 재시도됩니다**.

> 이를 변경하려면 queries에 대한 기본 `retry` 및 `retryDelay` 옵션을 `3` 및 기본 지수 백오프 기능 이외의 다른 것으로 변경할 수 있습니다.

[//]: # 'StructuralSharing'

- 기본적으로 Query 결과는 **데이터가 실제로 변경되었는지 감지하기 위해 구조적으로 공유됩니다**. 그렇지 않은 경우 **데이터 참조는 변경되지 않은 상태로 유지**되어 useMemo 및 useCallback과 관련된 값 안정화에 더 도움이 됩니다. 이 개념이 낯설게 들린다면 걱정하지 마세요! 99.9%의 경우 이 기능을 비활성화할 필요가 없으며 이를 통해 무료로 앱 성능을 높일 수 있습니다.

[//]: # 'StructuralSharing'

> 구조적 공유는 JSON 호환 값에서만 작동하며 다른 값 유형은 항상 변경된 것으로 간주됩니다. 예를 들어 큰 응답으로 인해 성능 문제가 발생하는 경우 `config.structuralSharing` 플래그를 사용하여 이 기능을 비활성화할 수 있습니다. query 응답에서 JSON과 호환되지 않는 값을 처리하고 데이터가 변경되었는지 여부를 계속 감지하려는 경우 `config.structuralSharing`로 고유한 사용자 지정 함수를 제공하여 필요에 따라 참조를 유지하면서 이전 응답과 새 응답에서 값을 계산할 수 있습니다.

[//]: # 'Materials'

## 추가 자료

기본값에 대한 자세한 설명은 [커뮤니티 리소스](../../../_source-only/docs/community-resources.md)의 다음 문서를 참조하세요.

- [실용적인 React Query](https://tkdodo.eu/blog/practical-react-query)
- [상태 관리자로서의 React Query](https://tkdodo.eu/blog/react-query-as-a-state-manager)
- [React Query로 생각하기](https://tkdodo.eu/blog/thinking-in-react-query)

[//]: # 'Materials'
