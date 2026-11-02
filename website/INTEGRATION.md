# Website integration content

No existing portfolio website is edited. `project.json` contains structured content and evidence boundaries; `case-study.mdx` contains the full long-form case study; `card.md` and `seo.json` supply listing/metadata copy. The offline `../index.html` is a complete accessible presentation that can be reviewed without a framework or deployment.

Suggested route: `/projects/gb10-v2-engineering-validation`. Copy the approved figures to `/images/projects/gb10-v2/` when integrating MDX; those are the exact image paths used there. The field `sections[].body_markdown` in JSON uses publication-root-relative figure paths and needs an asset-base mapping in an existing website. Preserve the numerical load/material context, source IDs, captions and no-hardware-validation boundary. Select framework components from the existing site's architecture; no new stack is required.

Retain one h1, ordered h2 sections, figure alt text/captions and labelled tables. Tables require a local horizontal-scroll wrapper on small screens. The portfolio card should lead with the engineering decision and evidence, not claim an optimized/high-torque actuator or a successfully tested robot. Link the report/limitations and provide accessible downloads.

The owner approved this GitHub distribution under the scoped MIT/CC BY 4.0 licenses; live website integration still requires separate authorization. This package includes no deploy/push/upload command and has not modified the live portfolio.
