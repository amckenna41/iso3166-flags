## Upstream Flag Icons Sync — v7.5.0

A new release of [**lipis/flag-icons**](https://github.com/lipis/flag-icons/releases/tag/v7.5.0) was published on 2025-05-29.

This PR syncs the `iso3166-1-flags` folder with the upstream `flags/4x3/` directory from that release.

### Changes to `iso3166-1-flags/`

| | Count | Flags |
|---|---|---|
| ✅ Added   | 21   | arab.svg, asean.svg, cefta.svg, cp.svg, dg.svg, eac.svg, es-ct.svg, es-ga.svg, es-pv.svg, eu.svg, gb-eng.svg, gb-nir.svg, gb-sct.svg, gb-wls.svg, ic.svg, pc.svg, sh-ac.svg, sh-hl.svg, sh-ta.svg, un.svg, xx.svg |
| 🔄 Updated | 250 | ad.svg, ae.svg, af.svg, ag.svg, ai.svg, al.svg, am.svg, ao.svg, aq.svg, ar.svg, as.svg, at.svg, au.svg, aw.svg, ax.svg, az.svg, ba.svg, bb.svg, bd.svg, be.svg, bf.svg, bg.svg, bh.svg, bi.svg, bj.svg … |
| ❌ Removed | 0 | None |

### Review checklist
- [ ] Spot-check changed SVGs against the [upstream release](https://github.com/lipis/flag-icons/releases/tag/v7.5.0)
- [ ] Confirm no custom / curated flags were accidentally overwritten
- [ ] Verify counts in `repo_metadata.json` are still accurate after merge
- [ ] Run the full test suite (`python -m unittest discover tests -v`)

---
*Automatically created by the [check-upstream-flags](.github/workflows/check_upstream_flags.yml) workflow.*
