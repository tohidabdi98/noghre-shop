# Definition of done — Example SaaS

> Abridged reference: levels 1–4 of `docs/project/definition_of_done.md` in the template, with the
> project's concrete evidence requirements.

## Task
- [ ] change traced to a requirement ID or an acceptance criterion
- [ ] inside the module's `allowed_to_modify`
- [ ] tests cover the behaviour and edge cases
- [ ] `python scripts/verify.py` passes locally (output pasted into the PR)
- [ ] docs updated in the same commit

## Module
- [ ] every acceptance criterion has evidence (test name, command output, or screenshot path)
- [ ] contract test passes for each provided port
- [ ] security duties met (server-side authorization, no plaintext secrets)
- [ ] `NFR-PERF-*` targets measured when the module touches a list query
- [ ] review findings resolved or accepted as non-blocking by the human
- [ ] `state/modules.yaml` → `validated`, `validation: passed`

## Integration / milestone
- [ ] UF-01 and UF-02 pass end to end on the integration branch
- [ ] dashboard screens validated visually at three widths, all states
- [ ] `NFR-A11Y-1` sweep clean on changed screens
- [ ] configuration validated in a clean environment
- [ ] human approval recorded (`gates.release_approved`)

## Not done
Tests passing without exercising a criterion · UI never rendered · validation claimed without a
command · coverage target reached but a requirement unverified.
