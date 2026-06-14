FINANCE_ARTICLES.push(
  {
    id: 'nonprofit-public-support-test-schedule-a',
    title: 'The Public Support Test and Form 990 Schedule A',
    body: `Most public charities organized under Section 501(c)(3) must demonstrate, on an ongoing basis, that they are genuinely "publicly supported" — meaning a meaningful portion of their funding comes from a broad base of the general public, government, and other public charities, rather than being heavily dependent on a small number of large donors. This matters because organizations that fail the public support test risk reclassification as "private foundations," subject to significantly more restrictive rules, including an excise tax on net investment income, mandatory minimum annual distributions, and burdensome restrictions on grant-making and certain investments.

The public support test is calculated and reported annually on Schedule A of Form 990, using a five-year rolling average (the current year plus the four preceding years) to smooth out year-to-year fluctuations — an organization that has an unusually large single-year gift, for example, won't necessarily fail the test in that one year, because the calculation looks at the aggregate of five years.

There are two common versions of the test, and an organization generally must pass at least one. Under Section 170(b)(1)(A)(vi) (most relevant for organizations primarily funded by contributions and grants), public support generally includes contributions from individuals, corporations, and other public charities, plus government grants — but contributions from any single donor are only counted toward the numerator up to 2% of total support for the five-year period. The organization generally needs public support to equal at least 33⅓% of total support, or to meet a "facts and circumstances" test if support falls between 10% and 33⅓%, considering factors like a broad-based fundraising program and a representative board.

Under Section 509(a)(2) (more relevant for organizations with significant program service revenue or membership fees — such as a museum with admission revenue, or an association with membership dues), both contributions/grants AND gross receipts from admissions, sales, and services related to the organization's exempt purpose count as public support — but gross receipts from any single source above the greater of $5,000 or 1% of total support for the year are excluded from the numerator. This test requires both that public support exceed 33⅓% of total support AND that "investment income" not exceed 33⅓% of total support.

The 2% (or 1%/$5,000) limitation creates a practical planning consideration: an organization receiving a single very large grant — say, a $5 million gift to an organization with $10 million in total five-year support — could only count $200,000 toward public support under the 170(b)(1)(A)(vi) test (2% of $10 million), with the remaining $4.8 million excluded from the numerator, potentially pushing the percentage below the required threshold even though the gift is entirely legitimate.

For nonprofit accountants, monitoring the public support test isn't just an annual compliance exercise — it has strategic implications. An organization approaching a major capital campaign or anticipating a very large gift should model the effect on its public support percentage in advance, since failing the test (even temporarily) can trigger private foundation status, though organizations have options including requesting an advance ruling or demonstrating they meet the facts-and-circumstances test.`,
    quiz: [
      {
        q: 'Why does the public support test matter for a 501(c)(3) organization?',
        choices: [
          'It determines how much the organization can pay its CEO',
          'Failing the public support test risks reclassification as a private foundation, which is subject to more restrictive rules including excise taxes on investment income and mandatory minimum distributions',
          'It determines whether the organization must pay sales tax',
          'It only affects organizations with fewer than 10 employees'
        ],
        correct: 1,
        explanation: 'Public charities must demonstrate broad public support to maintain their status; failing the test can result in reclassification as a private foundation, which carries significantly more restrictive operating rules, including excise taxes and mandatory distribution requirements.'
      },
      {
        q: 'Under the Section 170(b)(1)(A)(vi) public support test, how is a very large single gift treated in the numerator of the calculation?',
        choices: [
          'The entire gift counts toward public support with no limitation',
          'The gift is excluded from the calculation entirely',
          'Contributions from any single donor are counted toward public support only up to 2% of total support for the five-year period, with amounts above that excluded from the numerator (but still in the denominator)',
          'Large gifts automatically disqualify an organization from being a public charity'
        ],
        correct: 2,
        explanation: 'The 2% limitation means a very large gift can only contribute up to 2% of total five-year support toward the public support numerator, with the excess excluded from the numerator while remaining in the denominator — potentially reducing the calculated public support percentage even though the gift is legitimate.'
      }
    ]
  },
  {
    id: 'nonprofit-program-related-investments-mission-investing',
    title: 'Program-Related Investments and Mission Investing',
    body: `Most nonprofit investment activity falls into two traditional categories: operating funds invested conservatively for liquidity, and endowment funds invested for long-term growth to support the organization's mission indirectly through investment returns. Program-related investments (PRIs) and broader "mission investing" represent a third category — using an organization's financial assets directly in service of its charitable mission, blurring the traditional line between "grant-making" and "investing."

A program-related investment, a term most directly relevant to private foundations (where PRIs receive specific favorable treatment under the tax code), is an investment whose primary purpose is to accomplish a charitable purpose (rather than to generate investment income or appreciation), and which would not have been made but for that charitable purpose. Common forms include below-market-rate loans to nonprofit organizations or social enterprises (for example, a loan to a community development financial institution that in turn lends to small businesses in underserved areas), equity investments in mission-aligned businesses (such as an affordable housing developer), and loan guarantees that enable a mission-aligned organization to access financing it couldn't obtain otherwise.

For private foundations, PRIs are significant because they count toward the foundation's annual minimum distribution requirement (5% of net investment assets) the same way a grant would — meaning a foundation can satisfy part of its required distributions through PRIs rather than only outright grants, while potentially having the loan or investment repaid (and available for re-deployment) over time, unlike a grant. Additionally, PRIs are generally not counted as "jeopardizing investments" under the rules that otherwise restrict how foundations can invest their assets, since their charitable purpose — not financial return — is the primary consideration.

Beyond PRIs specifically, "mission investing" or "impact investing" more broadly refers to nonprofits (including public charities, not just private foundations) deploying a portion of their endowment or investment portfolio toward investments that generate both financial return and positive social/environmental impact aligned with the organization's mission — for example, an environmental nonprofit investing a portion of its endowment in renewable energy projects, or a community foundation investing in local affordable housing funds. Unlike PRIs (where charitable purpose is primary and financial return is secondary), mission investing within an endowment context often seeks market-rate or near-market-rate returns alongside mission alignment — sometimes described as occupying a spectrum from PRIs (impact-first) through various shades of "impact investing" (balancing impact and return) to traditional investments with ESG screens overlaid (return-first, with impact as a secondary consideration).

For nonprofit finance staff and boards considering PRIs or mission investing, key considerations include: the organization's fiduciary duty to manage investments prudently (which generally permits — and under some state UPMIFA-based laws explicitly allows — considering an investment's relationship to the organization's charitable purposes as one factor among many, not just financial return); the need for due diligence capabilities to evaluate PRI-type risk (often smaller, less liquid, less-rated counterparties than typical fixed-income investments); accounting for PRIs (typically as investments, with consideration of collectability for loan-type PRIs, similar to receivables); and governance processes for approving and monitoring these investments, which often differ from those for the traditional investment portfolio.`,
    quiz: [
      {
        q: 'What is the defining characteristic of a program-related investment (PRI)?',
        choices: [
          'It must generate returns higher than the stock market',
          'Its primary purpose is to accomplish a charitable purpose rather than to generate investment income, and it would not have been made but for that charitable purpose',
          'It must be made only to government entities',
          'It must have a guaranteed return of principal with no risk'
        ],
        correct: 1,
        explanation: 'A PRI is defined by its primary charitable purpose — financial return is secondary. This is what distinguishes PRIs from traditional investments and from "impact investing" more broadly, which often seeks to balance impact with market-rate or near-market-rate returns.'
      },
      {
        q: 'Why are PRIs significant for private foundations specifically?',
        choices: [
          'PRIs are illegal for private foundations',
          'PRIs count toward a private foundation\'s annual minimum distribution requirement (similar to grants) while potentially being repaid over time, and are generally not treated as "jeopardizing investments" under foundation investment restrictions',
          'PRIs eliminate a foundation\'s need to file any tax returns',
          'PRIs can only be made to other private foundations'
        ],
        correct: 1,
        explanation: 'PRIs satisfy part of a foundation\'s required 5% annual distribution (like a grant would) but, unlike a grant, may be repaid and redeployed — and they\'re generally exempt from the rules restricting how foundations can invest, since their charitable purpose is primary.'
      }
    ]
  },
  {
    id: 'nonprofit-disaster-relief-and-emergency-grant-accounting',
    title: 'Accounting for Disaster Relief and Emergency Grant Funding',
    body: `When a disaster strikes — a hurricane, wildfire, pandemic, or other emergency — nonprofits often experience a surge of restricted contributions and emergency grants earmarked for disaster response, frequently arriving in compressed timeframes and sometimes with less formal documentation than typical grant agreements (donors and funders moving quickly to provide urgently needed resources may not execute detailed agreements before funds are transferred). This creates specific accounting and stewardship challenges beyond typical restricted funding.

The first challenge is properly classifying incoming disaster funds. A contribution explicitly designated by the donor for "hurricane relief" or a specific disaster is donor-restricted, and must be tracked separately from general operating funds and other restricted purposes. If the organization receives funds before a formal agreement is executed (common in disaster response, where speed matters), the accountant needs to determine the restriction based on the donor's communicated intent — an email, a designation on a donation form, or other contemporaneous evidence — even in the absence of a signed agreement, and should obtain documentation as soon as practical to support the restriction classification.

A second challenge involves government disaster assistance, which often comes through complex, multi-layered funding streams — federal emergency funds passed through state or local governments, FEMA public assistance reimbursements, and Community Development Block Grant Disaster Recovery (CDBG-DR) funds, among others — each with its own eligibility rules, documentation requirements, and deadlines. Nonprofits receiving these funds, especially as subrecipients, are subject to Uniform Guidance (2 CFR 200) requirements, but disaster funding often involves additional complexity: retroactive eligibility periods, requirements to document that costs weren't covered by insurance (avoiding "duplication of benefits," a major focus of disaster recovery audits), and compressed timeframes that can create pressure to disburse quickly without adequate documentation.

A third challenge is timing — disaster relief often involves the organization spending its own funds first and seeking reimbursement later from government sources or designated donor funds, creating a working capital strain if reimbursement is delayed (common, sometimes by many months). Organizations need to track which expenses are eligible for reimbursement under which funding source, since the same costs might be partially reimbursable from multiple sources (requiring careful allocation to avoid duplication of benefits) or might exceed what any available source will cover.

A fourth challenge involves in-kind donations, which often surge during disaster response — donated supplies, volunteer labor, donated use of facilities or transportation — all needing recognition under the in-kind contribution rules, appropriate valuation, and tracking for financial reporting and, where relevant, documenting matching requirements or cost-sharing under government grants.

For nonprofit accountants, the practical discipline during disaster response is to set up dedicated tracking (often a separate fund or project code) for each disaster as soon as response begins, document funding sources and restrictions as they're identified (even if formal agreements lag behind), maintain detailed expense documentation specifically organized to support reimbursement claims and duplication-of-benefits analysis, and build in additional review of disaster-related transactions given the elevated risk of error or even fraud that can accompany the urgency and volume of disaster response activity.`,
    quiz: [
      {
        q: 'What is "duplication of benefits," and why is it a major focus in disaster recovery accounting?',
        choices: [
          'A bonus payment given to donors who give multiple times',
          'The situation where the same disaster-related costs are reimbursed from multiple sources (e.g., insurance plus government funds), which disaster recovery audits specifically scrutinize to prevent',
          'A requirement that all disaster funds be spent twice',
          'A type of accounting error that only affects for-profit companies'
        ],
        correct: 1,
        explanation: 'Duplication of benefits occurs when the same costs are reimbursed from more than one source (such as insurance proceeds plus government disaster assistance) — disaster recovery audits focus heavily on this issue, requiring organizations to carefully track which funding source covers which costs.'
      },
      {
        q: 'How should a nonprofit classify a contribution received via informal communication (e.g., an email) designating it for a specific disaster, before any formal agreement is signed?',
        choices: [
          'It should be treated as unrestricted until a formal agreement is signed',
          'It should be treated as donor-restricted based on the donor\'s communicated intent, with documentation obtained as soon as practical, even in the absence of a signed agreement',
          'It cannot be recorded as revenue until the disaster is officially declared over',
          'It must be returned to the donor if no formal agreement exists'
        ],
        correct: 1,
        explanation: 'In disaster response, funds often arrive before formal agreements are executed. The restriction classification should be based on the donor\'s communicated intent (even informal evidence like an email or donation form designation), with the organization obtaining formal documentation as soon as practical.'
      }
    ]
  },
  {
    id: 'nonprofit-planned-giving-and-bequest-administration',
    title: 'Planned Giving and Bequest Administration',
    body: `Planned giving refers to charitable gifts arranged during a donor's lifetime but typically realized — in whole or in part — at a future date, often through the donor's estate. While split-interest agreements (like charitable remainder trusts and gift annuities) involve specific actuarial and present-value accounting, bequests — gifts made through a donor's will or living trust, designating the nonprofit as a beneficiary — represent a distinct category of planned gift with their own accounting and stewardship considerations.

The most fundamental accounting question for bequests is timing: when should a bequest be recognized as revenue? An organization may learn it has been named in a donor's will or as a beneficiary of a retirement account or life insurance policy years (sometimes decades) before the donor's death — and the donor can change their will or beneficiary designations at any time before death, meaning the "gift" isn't legally enforceable until death (and even then, until the estate is settled and the amount is determinable). Generally, a bequest is recognized as a contribution receivable and revenue only when the organization has an "unconditional right" to it — typically after the donor's death, when the designation becomes irrevocable and the amount can be reasonably estimated, even if the estate hasn't fully settled.

In practice, this means: learning you're named in a living donor's will is not, by itself, a basis for recognizing revenue (the donor could change the will), but once the donor has died and the organization is notified it's a named beneficiary (often via a letter from the estate's executor, or being named in a probated will), the organization should recognize a receivable and revenue for its best estimate — even if final distribution is months or years away due to estate administration, will contests, or asset sales.

Estimating the amount can be challenging, particularly for "residuary" bequests (where the nonprofit receives a percentage of whatever remains in the estate after specific bequests, debts, taxes, and expenses are paid, rather than a fixed dollar amount) — the organization may need to work with the estate's executor or attorney to obtain estimates based on asset values and anticipated expenses, updating the estimate as better information becomes available, with adjustments recognized as estimates change.

From a stewardship perspective, planned giving programs require long-term relationship management — a donor who notifies an organization of a bequest intention today might not pass away for 20 or 30 years, during which the organization should maintain the relationship and ensure the intention remains current as the donor's circumstances or the organization's structure may change. Many organizations maintain a "legacy society" recognizing donors with documented bequest intentions, even though no revenue is recognized until much later.

For accountants, the practical work includes tracking known bequest intentions for stewardship purposes (though no entry is made until the donor's death), promptly recognizing receivables and revenue upon notification of an actual bequest (working with legal counsel as needed to support the estimate), and periodically reviewing bequest receivable estimates as estates are administered — including assessing collectability if an estate's value declines significantly before final distribution.`,
    quiz: [
      {
        q: 'When should a nonprofit generally recognize a bequest as a contribution receivable and revenue?',
        choices: [
          'As soon as the organization learns it has been named in a living donor\'s will',
          'Only after the donor has died and the bequest has become irrevocable, with the amount reasonably estimable — even if the estate hasn\'t fully settled',
          'Only when the full amount is received in cash',
          'Bequests are never recognized as revenue under GAAP'
        ],
        correct: 1,
        explanation: 'Because a living donor can change their will at any time, a bequest is not recognized until the donor\'s death makes it irrevocable and the amount can be reasonably estimated — at which point a receivable and revenue are recorded, even though final settlement may take much longer.'
      },
      {
        q: 'Why can estimating the amount of a "residuary" bequest be particularly challenging?',
        choices: [
          'Residuary bequests are always a fixed, predetermined dollar amount',
          'A residuary bequest represents a percentage of whatever remains in the estate after specific bequests, debts, taxes, and expenses — requiring estimates based on estate asset values and anticipated expenses, which may change as the estate is administered',
          'Residuary bequests are illegal in most states',
          'Residuary bequests can only be made by for-profit corporations'
        ],
        correct: 1,
        explanation: 'Because a residuary bequest depends on what remains after other claims on the estate are satisfied, the organization must work with the estate\'s executor to estimate the amount based on asset values and expenses — an estimate that may need to be revised as the estate administration progresses.'
      }
    ]
  },
  {
    id: 'nonprofit-grant-budget-modifications-and-no-cost-extensions',
    title: 'Grant Budget Modifications and No-Cost Extensions',
    body: `Grant budgets — whether from foundations, corporations, or government agencies — represent a plan for how grant funds will be spent, typically broken down by category (personnel, supplies, travel, indirect costs, etc.) and often by time period. But real program implementation rarely goes exactly according to plan: a planned hire takes longer than expected (leaving personnel funds unspent while other costs run higher), a program component is delayed, or unexpected opportunities shift the best use of remaining funds. Grant budget modifications and no-cost extensions are the mechanisms organizations use to adapt while maintaining compliance.

A budget modification (or revision/reallocation) involves shifting funds between budget categories from what was originally approved — for example, moving funds from an under-budget personnel line to an over-budget supplies line. Many funders, particularly government funders operating under the Uniform Guidance (2 CFR 200), establish a threshold (often a percentage of total budget, such as 10%) below which reallocations don't require prior approval — the organization can simply make the change and report it routinely. Reallocations exceeding that threshold, or involving categories called out in the award terms (commonly, any reallocation into or out of indirect costs, equipment, or contractual lines often requires prior approval regardless of percentage), require formally requesting approval before making the change — spending inconsistent with the approved budget, without required approval, can result in disallowed costs during audit, even if the spending was reasonable and mission-aligned.

A no-cost extension (NCE) extends a grant's period of performance — allowing additional time to spend already-awarded funds — without providing additional funding. NCEs are commonly used when a program has experienced delays (a hiring delay, supply chain issues affecting a capital project) and unspent funds remain as the original period approaches its end. Most funders allow at least one NCE, often up to 12 months, through a relatively straightforward request process (sometimes automatic for the first extension under federal awards, requiring only notification) — but the request typically must be submitted before the current period ends, with a clear justification of the delay's cause and what will be accomplished during the extension.

A critical point: organizations should not wait until the very end of a grant period to identify the need for a modification or NCE. Budget-to-actual variance should be reviewed regularly (monthly or quarterly) — identifying significant variances early gives time to adjust spending plans or request a modification with adequate lead time, rather than discovering at final reporting that funds were spent inconsistently with no opportunity to seek approval retroactively.

For nonprofit finance staff, the needed infrastructure includes: a tracking system comparing actual spending to approved budgets by category and grant period, documentation of each funder's specific thresholds and approval requirements (these vary significantly), and a calendar of grant end dates with lead time built in to request NCEs before deadlines — turning a potential year-end compliance crisis into routine grant management.`,
    quiz: [
      {
        q: 'What is a "no-cost extension" (NCE) in grant management?',
        choices: [
          'Additional grant funding provided at no cost to the organization',
          'An extension of the period of performance for a grant, allowing more time to spend already-awarded funds, without providing additional funding',
          'A penalty imposed on organizations that overspend their grant budget',
          'A requirement that the organization return unspent funds immediately'
        ],
        correct: 1,
        explanation: 'A no-cost extension gives an organization more time to spend funds already awarded under a grant — commonly used when delays have left unspent funds as the original grant period nears its end — without providing any additional money.'
      },
      {
        q: 'Why is regularly reviewing budget-to-actual variance throughout a grant period important, rather than waiting until the end?',
        choices: [
          'It has no real importance; funders never check spending until the final report',
          'Identifying significant variances early gives the organization time to adjust spending or request a budget modification/extension with proper lead time, rather than discovering noncompliant spending only at final reporting with no opportunity to seek approval',
          'Regular review is only required for grants under $1,000',
          'It eliminates the need for any final financial report to the funder'
        ],
        correct: 1,
        explanation: 'Waiting until the end of a grant period to review spending risks discovering that funds were spent inconsistently with the approved budget without having obtained required prior approvals — regular review allows timely correction, modification requests, or extension requests before deadlines pass.'
      }
    ]
  }
);
