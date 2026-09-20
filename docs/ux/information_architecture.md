# Information architecture

> Owned by the Frontend/UX Agent. This is the product's map: hierarchy, navigation, naming, URLs
> and who can see what. It prevents the classic agent failure mode of inventing a new page or a
> new navigation entry for every new feature.

## 1. Navigation model

| Aspect | Decision | Rationale |
|---|---|---|
| Primary navigation | e.g. persistent left sidebar on desktop, bottom bar on mobile | |
| Max depth | e.g. 3 levels | deeper levels lose users |
| Where global actions live | e.g. top bar: search, create, notifications, account | |
| Where contextual actions live | e.g. row actions, page header | |
| Back behaviour | browser history respected; no navigation traps | |
| Deep linking | every meaningful view has a URL | |
| Persistence | nav state survives reload and refresh | |

## 2. Site map

```text
/
├── /signin              unauthenticated
├── /signup
├── /onboarding          first-run only, resumable
└── /app                 authenticated shell
    ├── /app/dashboard
    ├── /app/projects
    │   ├── /app/projects/:id
    │   └── /app/projects/:id/settings
    ├── /app/notifications
    └── /app/settings
        ├── /app/settings/profile
        └── /app/settings/team
```

## 3. Hierarchy and ownership

| Level | Contains | Example | Rule |
|---|---|---|---|
| Shell | global chrome: nav, search, notifications | `/app` | owned by the app-shell module |
| Section | a coherent domain area | Projects | one module |
| Screen | one task or view | project detail | one module |
| Panel/dialog | a focused subtask | invite member | belongs to its screen |

**New screens require an IA change first** — the Frontend/UX Agent reviews and records it here,
then the affected module contract is updated. Implementation agents must not add navigation
entries on their own.

## 4. Naming rules

| Concern | Rule | Examples |
|---|---|---|
| Navigation labels | user vocabulary, not system vocabulary, ≤ 2 words | "Projects", not "Project entities" |
| URLs | plural nouns for collections, `kebab-case`, no verbs for GET routes | `/app/projects/42` |
| Actions | verb + object, sentence case | "Create project" |
| Consistent synonyms | one word per concept, everywhere | pick "project" *or* "workspace" — never both |
| Empty/error copy | second person, no blame, states the next action | "No projects yet. Create your first one." |

## 5. Visibility and permissions

| Area | Visitor | User | Admin | Enforced in |
|---|---|---|---|---|
| dashboard | redirect to sign-in | own data | all data | server |

Rule: navigation hides what a user cannot use **and** the server still enforces it — the UI is not
a security boundary.

## 6. Search, filtering and sorting

| Concern | Decision |
|---|---|
| Global search scope | |
| Per-section filters | |
| Sort defaults | |
| Empty search results | |
| Result URL state | filters reflected in the URL so views are shareable |

## 7. Responsive IA

| Area | Desktop | Tablet | Mobile |
|---|---|---|---|
| primary nav | sidebar | collapsible sidebar | bottom bar ≤ 5 items |
| secondary nav | tabs | tabs | segmented control / sheet |
| data-heavy views | table | table (reduced columns) | card list |
| global actions | top bar | top bar | floating action |

## 8. IA change log

| Date | Change | Reason | Affected modules |
|---|---|---|---|
| | initial draft | — | — |
