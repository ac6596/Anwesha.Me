---
title: "Data Foundations: Because Regulators Don't Accept 'It Worked on My Machine'!"
date: 2025-11-08
excerpt: Why mastering data governance, lineage, and quality matters more than chasing the latest tech — especially in regulated banking environments.
author: Anwesha Chakraborty
---

It all started on a Friday afternoon — the kind where the office smells like reheated coffee, everyone's staring at the clock, waiting for the weekend miracle. I was tidying up my week's to-do list, locked in a battle with a stubborn dbt model build.

Then, out of nowhere, a business requirement doc — **FINAL\_BRD** flashed onto my monitor. Right on cue, whispers of yet another **"slight change"** floated around. (Seriously, why is **"FINAL"** apparently negotiable?) "We need this ASAP," they said — apparently the regulators want **some data**. Somewhere between a sigh and a mild panic attack, it hit me: all the fancy tools in the world won't save you from vague requirements and messy data — especially when every system claims to be the **"source of truth,"** and none actually are.

If you asked me 11 years ago, when I first started my career, whether I cared about regulatory requirements, I'd probably have said — ***"Regula-what?"*** Back then, I was all about the flashy tools — new tech stacks, automation tricks, the joy of writing queries and code that actually ran on the first try (rare, but glorious). Big data, the cloud… everyone said that's where the real money and prestige were. I wanted in. I chased every shiny new platform, every buzzword that promised to make me **"a data wizard overnight."**

Fast forward a decade, and here I am — deep in conversations with Legal about ASIC and APRA reports, throwing around words like ***lineage***, ***controls***, and ***reconciliation*** with the same excitement I once had for shiny new tech. Who knew my thrill for **"next-gen tools"** would one day be replaced by chasing why a number doesn't tie out? (Don't get me wrong — new tech still makes my heart race!) Turns out, understanding how a bank *really* runs makes you appreciate why regulators exist — and why a strong data foundation isn't a **"nice-to-have,"** it's **non-negotiable.**

In banking, data isn't just information — it's evidence. Every field, every transaction, every number that shows up in a report needs to tell a defensible story.

## 🏦 Why Data Quality Is the Bank's Lifeline?

When preparing ASIC reports or APRA submissions, you can't rely on best guesses or manual reconciliations. Frameworks like **BCOP** and **Basel III** aren't just checklists — they're the unsung rulebooks that keep banks from turning into financial thrill rides. **Basel III** keeps our risk-taking in check, while **BCOP** ensures operational controls are airtight.

Because let's be honest — when a regulator asks, "Where did this number come from?", replying with *"I think it's from the old system… maybe?"* doesn't quite inspire confidence.

## ⚙️ What I've Learned (and Laughed About) Along the Way

Here's the thing I've realised — you can have all the fancy tools in the world (Databricks, Fabric, Synapse, Glue, Starburst — pick your fighter). Believe me, I've dated most of them. But no matter how shiny the tech, your data won't behave unless you actually *know* it, *love* it, and occasionally *discipline* it. But unless you *know* your data, it'll still ghost you at the worst possible time. If your foundation's shaky, compliance turns into an endless game of data Jenga — one wrong move and the whole thing collapses.

I've seen projects struggle not because of bad tech — but because no one knew what their own data was trying to say.

No tool can fix a relationship problem between you and your data — you've got to spend time together, learn its quirks, and stop pretending that **"Final\_v3\_\*\*\*.xlsx"** is a stable version.

A strong data foundation saves you from:

- The eternal Excel chaos: ***"Final\_v3\_\*\*\*.xlsx"***
- Late-night **"quick fixes"** that break 10 other reports
- The sinking feeling when Legal says, **"Can you trace that back to source?"**

No tool, CI/CD pipeline, or fancy framework can rescue you from that — only **truly knowing, loving, and taming your data** does. Once you've lived through that, you never underestimate the power of **clean, governed, and traceable data** — or the peace of mind that comes with it.

## 📊 Why Good Data Foundations Make Compliance (Almost) Enjoyable

1. **Single Source of Truth** – One consistent view across reporting, risk, finance, and legal teams. No more ***"my dashboard says something else."***

2. **Lineage & Transparency** – When every transformation is mapped and auditable, you can answer *"where did this come from?"* without a week's worth of Teams archaeology.

3. **Automation & Accuracy** – With modern data frameworks, checks and validations run automatically — making compliance reports almost *self-healing*.

4. **Speed & Sanity** – Clean data = faster reporting cycles = fewer caffeine-fueled all-nighters before submission deadlines.

5. **Data Modelling & Layered Checks** – Build your data in layers with validations at each stage, from raw ingestion to final reporting.

6. **WAP (Write, Audit, Publish)** – Ensure every metric is written correctly, audited for accuracy, and published only when validated. No surprises, no last-minute firefighting.

## ⚖️ Lessons from the Legal Side

Working closely with Legal has been an eye-opener. You realise the stress isn't just about missing a deadline — it's about ***data accountability.***
When something doesn't reconcile, it's not just a "data issue" — it's a *regulatory exposure*.

**What helps:**

- Establishing clear data ownership — who's accountable for each metric.
- Building traceability from raw source to submission.
- Documenting transformations and assumptions — because undocumented logic is the silent killer of compliance.
- Adding automated **tests** in your data pipelines — because prevention is cheaper than a 2 AM fix.
- Maintaining a **data catalog** — so everyone knows what exists, where it lives, and how it behaves.
- Being **proactive** — spotting issues early, raising them, and owning the resolution.

## 🧪 Testing — The Unsung Hero of Compliance

When designing a data pipeline, **never skip testing** — it's NOT optional; it's INTEGRAL.

**DQ Checks** – Ensure accuracy, completeness, and consistency (nulls, duplicates, types).
**File Validation** – Confirm files meet schema, record count, and naming expectations.
**Business Rules** – Verify data aligns with operational and business logic.

Modern cloud and open-source tools make testing part of your data DNA:

- **dbt tests** – Quick, declarative tests for schema, relationships, and business rules right inside your transformation layer.
- **Great Expectations** – Framework-agnostic, great for validating data at every stage and generating human-readable validation reports.
- **AWS Deequ** – Scalable data quality checks built on Spark, ideal for large datasets in S3, Glue, or EMR.
- **Azure Data Factory Data Flow Tests** – Add assertions and monitor rule outcomes directly within Azure pipelines.
- **Google Cloud Data Quality (Dataplex)** – Manage quality rules across BigQuery and GCS with central governance.
- **Soda Core / Soda Cloud** – Cloud-native testing and monitoring, perfect for continuous validation across environments.

Integrate these into your CI/CD pipelines (Codefresh, GitHub Actions, or Azure DevOps) so every deployment automatically runs validation checks.

Because when your tests catch the issue before Legal does — compliance suddenly feels a lot less like chaos and a lot more like control.

## 💡 Final Thoughts

A solid data foundation is like a bank vault — quiet when it's strong, headline-worthy when it cracks.

If you're still surviving on last-minute Excel fixes and mystery SQL scripts held together by caffeine and hope — I've been there. But the real magic begins when **data, governance, and tech actually talk to each other**. That's when compliance stops being a checkbox exercise and starts becoming your secret weapon.

Because at the end of the day, good data doesn't just keep regulators calm — it earns **trust**, **builds resilience, and lets your bank sleep well at night (and maybe, finally, you too).**
