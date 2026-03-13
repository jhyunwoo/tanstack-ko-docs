---
id: zoneless
title: 영역 없는 각도
---




TanStack Query용 Angular 어댑터는 신호를 기반으로 구축되었으므로 Zoneless를 완벽하게 지원합니다!

Zoneless의 이점 중에는 향상된 성능과 디버깅 경험이 있습니다. 자세한 내용은 [Angular 문서](https://angular.dev/guide/zoneless)를 참조하세요.

> Zoneless 외에도 ZoneJS 변경 감지도 완벽하게 지원됩니다.

> Zoneless를 사용하는 경우 `ApplicationRef.whenStable()`를 진행 중인 queries 및 mutations와 동기화를 유지하는 `PendingTasks` 통합을 활용하려면 Angular v19 이상을 사용 중인지 확인하세요.