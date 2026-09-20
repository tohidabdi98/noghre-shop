# Information architecture — Example SaaS (abridged)

## 1. Navigation model
| Aspect | Decision |
|---|---|
| Primary navigation | left sidebar (desktop), bottom bar ≤ 5 items (mobile) |
| Max depth | 3 (`/app` → section → detail) |
| Global actions | header: search, unread count, create |
| Contextual actions | page header + row actions |
| Deep linking | every view has a URL, including filter state |

## 2. Site map
```text
/
├── /signin  /signup  /reset
└── /app
    ├── /app                     dashboard (attention + activity)
    ├── /app/projects            project list
    ├── /app/projects/:id        project detail (+ collaborators)
    ├── /app/notifications       notification centre
    └── /app/settings/profile
```

## 3. Hierarchy and ownership
| Level | Contains | Owner module | Rule |
|---|---|---|---|
| Shell | nav, header, token file | `APP-001` (shared zone) | additive changes requested from the owner |
| Section | dashboard, projects, notifications | `DASH-001`, `PROJECT-001`, `NOTIFY-001` | one module per section |
| Screen | detail views | one module | new screens require an IA change here first |
| Dialog | one focused decision | its screen's module | ≤ 3 fields, otherwise a page |

## 4. Naming rules
| Concern | Rule | Example |
|---|---|---|
| Navigation labels | user vocabulary, ≤ 2 words | "Projects" |
| URLs | plural nouns, kebab-case | `/app/projects/42` |
| Actions | verb + object, sentence case | "Create project" |
| Synonyms | one word per concept: "project" (never "workspace") | — |
| Empty copy | second person, states the next action | "No projects yet. Create your first one." |

## 5. Visibility
| Area | Visitor | User | Owner | Enforced in |
|---|---|---|---|---|
| `/app/*` | redirect to `/signin` | own + collaborating projects | all their projects | server (`requireSession`, `requireProjectAccess`) |
| `/app/settings/profile` | — | self | self | server |

The UI hides what a user cannot use; the server still enforces it (`NFR-SEC-2`).

## 6. Search, filtering, sorting
Search is scoped to the current section in v1. Project list supports status and owner filters with the
filter state in the URL. Default sort: attention urgency on the dashboard, last-updated on the list.
Empty filter results say which filter excluded everything.

## 7. Responsive IA
| Area | Desktop | Tablet | Mobile |
|---|---|---|---|
| primary nav | sidebar | collapsible sidebar | bottom bar |
| dashboard | 2 columns | stacked | attention first |
| project list | table | reduced columns | card list |
| create | header action | header action | floating action |
