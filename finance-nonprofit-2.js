// ---------- Non-Profit Accounting (batch 2) ----------
FINANCE_ARTICLES.push(
  {
    id: 'statement-of-cash-flows-np',
    title: 'The Statement of Cash Flows for Non-Profits',
    body: `Non-profit organizations prepare a statement of cash flows under the same overall framework as for-profit entities — organizing cash flows into operating, investing, and financing activities — but several aspects of the statement reflect the unique features of non-profit accounting.

The operating activities section typically starts with the change in net assets (the non-profit equivalent of net income) and adjusts for non-cash items (such as depreciation and amortization) and changes in working capital accounts (receivables, payables, and similar items), arriving at cash provided by or used in operating activities — conceptually parallel to the for-profit approach.

The investing activities section includes purchases and sales of property and equipment, as well as purchases, sales, and maturities of investments — which can be a particularly significant category for non-profits with substantial endowments or investment portfolios, where investment activity may dwarf operating cash flows in dollar terms.

The financing activities section for non-profits includes items like proceeds from and repayments of debt — but it also includes a distinctive item not found in for-profit statements: cash received from contributions that are restricted by donors for long-term purposes, such as contributions to permanent endowment or for the acquisition of long-lived assets like buildings. This reflects the view that such contributions are more analogous to "financing" the organization's long-term capital needs (similar to how a for-profit might raise capital through debt or equity issuance) than to ongoing operations.

This treatment creates an important nuance: a contribution restricted for the purchase of a building might be reported as operating activity in terms of its effect on the change in net assets (since contribution revenue, even restricted, generally flows through the statement of activities), but the related cash receipt could be classified as a financing activity in the cash flow statement — requiring a reconciling adjustment in the operating activities section to remove the effect of that contribution revenue from operating cash flows, since the cash itself is presented in the financing section.

Non-profits can use either the direct method (showing actual cash receipts and payments for operating activities, such as cash received from contributors and cash paid to employees and suppliers) or the indirect method (starting from the change in net assets and adjusting for non-cash items, as described above) — the indirect method is far more common in practice, similar to for-profit reporting, largely because it can be derived more easily from existing accrual-basis accounting records, while the direct method requires tracking cash flows by category separately.

For an organization heavily reliant on multi-year pledges and grants, the statement of cash flows can tell a very different story than the statement of activities — an organization might report a large increase in net assets (driven by recognizing a multi-year pledge as revenue in full) while generating relatively little actual cash during the same period (since the pledge will be collected over future years) — making the cash flow statement an essential complement for understanding an organization's actual liquidity position.`,
    quiz: [
      {
        q: 'Where would cash received from a donor-restricted contribution for the purchase of a building typically be classified on a non-profit\'s statement of cash flows?',
        choices: [
          'Operating activities only',
          'Financing activities, reflecting that such contributions function similarly to long-term capital financing',
          'It is not reported on the cash flow statement at all',
          'Investing activities only'
        ],
        correct: 1,
        explanation: 'Contributions restricted for long-term purposes like building acquisition or permanent endowment are classified as financing activities, even though the related revenue may flow through the change in net assets reported in operating activities — requiring a reconciling adjustment.'
      },
      {
        q: 'Why might a non-profit show a large increase in net assets on its statement of activities while generating relatively little actual cash during the same period?',
        choices: [
          'Because non-profits are not allowed to hold cash',
          'Because revenue from a multi-year pledge may be recognized in full when promised, even though the related cash will be collected over multiple future years',
          'Because the statement of activities always overstates expenses',
          'Because cash flow statements are optional for non-profits'
        ],
        correct: 1,
        explanation: 'Unconditional multi-year pledges are often recognized as revenue (at present value) when promised, increasing net assets immediately — but the actual cash collection happens over time, creating a timing gap between reported net assets and actual cash generated, which the cash flow statement reveals.'
      }
    ]
  },
  {
    id: 'pledges-receivable',
    title: 'Pledges Receivable and Multi-Year Promises to Give',
    body: `A pledge (or promise to give) is a donor's commitment to make a future contribution to a non-profit organization. Under GAAP, unconditional promises to give are recognized as revenue and as an asset (pledges receivable, also called contributions receivable) at the time the promise is made — not when the cash is actually received — distinguishing non-profit revenue recognition for contributions from typical cash-basis intuitions.

For pledges expected to be collected within one year, the recorded amount is generally the amount expected to be collected (face value, net of an allowance for uncollectible pledges, similar in concept to the allowance for doubtful accounts discussed elsewhere). For multi-year pledges — where a donor promises, say, $500,000 payable in $100,000 installments over five years — GAAP requires the pledge to be recorded at its present value, discounted using an appropriate discount rate (often based on rates for instruments of similar duration and risk at the time the pledge is made).

This present value treatment has an important consequence: in subsequent years, as the pledge moves closer to its payment dates, the discount is "unwound" — recorded as additional contribution revenue (sometimes presented as a separate line, such as "amortization of discount on pledges receivable") representing the time value of money. This means a multi-year pledge generates a small amount of additional revenue each year simply due to the passage of time, separate from any new pledges or payments.

A critical distinction exists between unconditional and conditional promises (discussed more broadly in the grant accounting article). An unconditional pledge — "I will give you $50,000 next year" — is recognized as revenue when made. A conditional pledge — "I will give you $50,000 next year if you raise $200,000 in matching funds from other donors" — is not recognized as revenue until the condition (the matching funds requirement) is substantially met, since the donor's obligation doesn't become unconditional until then.

Pledges also raise measurement challenges around collectibility. Multi-year pledges, by their nature, carry more uncertainty than pledges payable immediately — a donor's circumstances could change significantly over a five-year pledge period. Organizations must estimate an allowance for uncollectible pledges based on factors like historical collection experience, the donor's history of fulfilling past pledges, and general economic conditions — similar in concept to estimating bad debts for accounts receivable, but often with less data available, particularly for large, infrequent pledges from major donors where historical patterns may not be very informative.

Intentions to give — informal indications that a donor "intends" to give in the future, without a sufficiently clear and unconditional promise — are not recognized as pledges receivable or revenue at all; the distinction between an "intention" and a "promise" can require judgment, particularly for verbal commitments or estate-related gifts (such as bequests) where legal enforceability may be uncertain until the donor's death.`,
    quiz: [
      {
        q: 'How is a multi-year unconditional pledge (e.g., $100,000 per year for five years) initially recorded under GAAP?',
        choices: [
          'At its full $500,000 face value, undiscounted',
          'At its present value, discounted to reflect the time value of money over the payment period',
          'Only when each $100,000 installment is actually received',
          'It is not recorded at all until the final payment'
        ],
        correct: 1,
        explanation: 'Multi-year pledges are recorded at present value because the future payments are worth less today. The discount is then unwound over time, generating additional contribution revenue each period as the pledge approaches its payment dates.'
      },
      {
        q: 'What is the difference between an "intention to give" and a "promise to give" for accounting purposes?',
        choices: [
          'There is no difference; both are recorded identically',
          'A promise to give that is sufficiently clear and unconditional is recognized as a pledge receivable and revenue, while a mere intention (without a clear, enforceable commitment) is not recognized at all',
          'Intentions to give are always larger in dollar amount',
          'Promises to give can never be conditional'
        ],
        correct: 1,
        explanation: 'GAAP requires a sufficiently clear and (for unconditional pledges) enforceable commitment before recognizing a pledge receivable and revenue. A vague or informal "intention" that doesn\'t rise to this level isn\'t recorded, which requires judgment particularly for verbal or estate-related commitments.'
      }
    ]
  },
  {
    id: 'single-audit',
    title: 'Non-Profit Audits and the Single Audit',
    body: `Many non-profit organizations are subject to financial statement audits — independent examinations of their financial statements, similar in basic structure to audits of for-profit companies, as discussed in the audit opinions article. However, non-profits that receive significant federal funding face an additional layer of audit requirements: the Single Audit, governed by the Uniform Guidance (2 CFR Part 200) issued by the U.S. Office of Management and Budget.

A Single Audit is required for non-profit organizations (and state/local governments) that expend $750,000 or more in federal awards during a fiscal year (a threshold that has changed over time and should be verified against current regulations). The "single" in Single Audit refers to the idea of having one comprehensive audit that satisfies the audit requirements of multiple federal programs and agencies, rather than requiring separate audits for each federal grant — a significant simplification compared to the alternative of program-by-program audits.

A Single Audit consists of two main components. First, an audit of the organization's financial statements as a whole, similar to a standard financial statement audit. Second, a compliance audit focused on the organization's major federal programs — testing whether the organization complied with specific requirements applicable to each program (such as eligibility requirements for program participants, allowable costs, and reporting requirements) and evaluating the organization's internal controls over compliance with these requirements.

"Major programs" for compliance testing purposes are determined through a risk-based approach that generally focuses audit attention on the largest federal programs (in terms of expenditures) and on programs identified as higher risk, ensuring that audit effort is concentrated where federal dollars are most significant or where compliance risk is greatest, rather than spreading effort evenly across all programs regardless of size.

The output of compliance testing includes identification of "findings" — instances of noncompliance with program requirements or internal control deficiencies over compliance — which are reported in a "Schedule of Findings and Questioned Costs." Significant findings can have serious consequences: they may need to be resolved with the relevant federal awarding agency, could affect an organization's eligibility for future federal funding, and in serious cases (such as findings involving the misuse of federal funds) could result in the organization being required to repay funds or facing other sanctions.

For organizations that receive federal funding through "pass-through" arrangements (federal money that flows through a state agency or another non-profit before reaching the organization), Single Audit requirements still apply based on the total federal awards expended, regardless of whether the funds came directly from a federal agency or were passed through an intermediary — and the pass-through entity has its own responsibilities to monitor the subrecipient's compliance, creating a layered system of accountability for federal funds as they flow through the non-profit sector.`,
    quiz: [
      {
        q: 'What is the general purpose of a "Single Audit" for non-profits receiving significant federal funding?',
        choices: [
          'To eliminate the need for any financial statement audit',
          'To provide one comprehensive audit covering both the organization\'s financial statements and compliance with requirements across its major federal programs, rather than requiring separate audits for each grant',
          'To audit only the organization\'s tax return',
          'To replace the Form 990 entirely'
        ],
        correct: 1,
        explanation: 'The Single Audit combines a financial statement audit with a compliance audit of major federal programs, satisfying the audit requirements of multiple federal awarding agencies through one comprehensive process rather than program-by-program audits.'
      },
      {
        q: 'How are "major programs" selected for compliance testing in a Single Audit?',
        choices: [
          'Every federal program is tested equally, regardless of size',
          'Through a risk-based approach that generally focuses on the largest federal programs by expenditure and those identified as higher risk',
          'Programs are selected alphabetically',
          'Only programs with no federal funding are tested'
        ],
        correct: 1,
        explanation: 'A risk-based major program determination concentrates audit effort on the programs where federal expenditures are largest or where compliance risk is greatest, rather than spreading limited audit resources evenly across all federal programs regardless of significance.'
      }
    ]
  },
  {
    id: 'board-governance-financial',
    title: 'Board Governance and Financial Oversight',
    body: `A non-profit's board of directors (or board of trustees) bears ultimate fiduciary responsibility for the organization, including oversight of its financial health, integrity, and compliance. Unlike a for-profit board, which is primarily accountable to shareholders focused on financial returns, a non-profit board is accountable to a broader set of stakeholders — donors, the community served, regulators, and the public interest in the organization fulfilling its tax-exempt mission — even though it must still attend to financial sustainability.

Core fiduciary duties applicable to non-profit board members are generally described using three concepts borrowed from broader principles of fiduciary law. The duty of care requires board members to exercise reasonable care in making decisions — attending meetings, reviewing financial statements and other materials, and asking informed questions, rather than passively rubber-stamping management's recommendations. The duty of loyalty requires board members to act in the best interest of the organization, not their own personal interests — this is the foundation for conflict-of-interest policies, which require disclosure of potential conflicts and typically require conflicted board members to recuse themselves from related decisions. The duty of obedience requires the organization (and its board) to remain faithful to its mission and comply with applicable laws, regulations, and its own governing documents (articles of incorporation, bylaws).

In terms of specific financial oversight responsibilities, boards typically: approve the annual budget and monitor actual results against it throughout the year; review and approve audited financial statements (often through a designated audit committee, particularly for larger organizations); oversee the organization's investment policies, especially for organizations with significant endowments or reserves; ensure appropriate internal controls are in place, including segregation of duties even in small organizations where this can be challenging given limited staff; and review and approve the Form 990 before it's filed, as the IRS specifically asks whether the board has reviewed the form.

An audit committee — a subset of the board (or, in smaller organizations, the full board acting in this capacity) — typically has direct responsibility for overseeing the external audit process, including selecting and evaluating the external auditor, reviewing the results of the audit (including any identified internal control deficiencies or significant accounting judgments), and serving as a point of direct communication between the auditor and the board, independent of management — this independence is considered important because management is the party whose work is being audited, and a direct line of communication to the board (bypassing management if necessary) helps ensure issues are appropriately escalated.

Whistleblower and document retention policies, while not strictly "financial" in nature, are also commonly recommended (and in some states required) governance practices that intersect with financial oversight — providing channels for concerns about financial improprieties to be raised and ensuring records needed for audits, tax filings, and legal compliance are retained appropriately.

For an accountant working with non-profits, understanding board governance isn't just an abstract good-governance topic — board engagement (or lack thereof) directly affects the control environment, which is the foundation of the COSO internal controls framework, and weak board oversight is frequently cited as a contributing factor in cases of non-profit financial mismanagement or fraud.`,
    quiz: [
      {
        q: 'What is the "duty of loyalty" as it applies to non-profit board members?',
        choices: [
          'A requirement to attend all board meetings',
          'A requirement to act in the best interest of the organization rather than personal interests, forming the basis for conflict-of-interest policies and recusal requirements',
          'A requirement to donate money to the organization',
          'A requirement to approve every staff decision'
        ],
        correct: 1,
        explanation: 'The duty of loyalty requires board members to prioritize the organization\'s interests over their own, which is why conflict-of-interest policies require disclosure of potential conflicts and recusal from related decisions to prevent self-interested influence on governance.'
      },
      {
        q: 'Why is independence important for a non-profit\'s audit committee in its oversight of the external audit?',
        choices: [
          'Independence has no real importance in practice',
          'Because management\'s work is the subject of the audit, an independent line of communication between the auditor and the board helps ensure issues can be escalated without being filtered or suppressed by management',
          'Audit committees are required to be located in a different city than the organization',
          'Independence only matters for for-profit companies'
        ],
        correct: 1,
        explanation: 'Since the audit examines management\'s financial reporting, an independent audit committee provides a channel for the auditor to communicate directly with board-level oversight, helping ensure significant issues (including potential concerns about management) are properly addressed.'
      }
    ]
  },
  {
    id: 'budgeting-nonprofits',
    title: 'Budgeting for Non-Profit Organizations',
    body: `Budgeting serves a different, and in some ways more central, role for non-profit organizations than for many for-profit businesses. While a for-profit budget is primarily an internal planning and performance management tool, a non-profit budget often also functions as a public statement of organizational priorities, a tool for demonstrating accountability to funders, and — particularly for organizations with restricted grants — a mechanism for ensuring compliance with donor and grantor requirements.

Non-profit budgets are often prepared at multiple levels of detail simultaneously. An organization-wide operating budget shows total projected revenue and expenses across the entire organization. Program-level (or grant-level) budgets break this down by individual programs or funding sources — particularly important because many grants require the organization to spend funds only on budgeted line items within that specific grant, and significant deviations from a grant budget may require prior approval from the funder (a "budget modification" request).

Revenue budgeting for non-profits often involves more uncertainty than for many for-profit businesses, since a significant portion of revenue may come from sources outside the organization's direct control — government grants subject to annual appropriations processes, foundation grants with multi-year but not guaranteed renewal, individual donations that can fluctuate with economic conditions and donor relationships, and special events whose success depends on factors like weather, attendance, and the broader fundraising environment. This uncertainty often leads organizations to budget revenue conservatively while planning expenses more precisely, or to build in contingency plans for different revenue scenarios.

A particularly important budgeting concept for non-profits is the difference between a program's "direct costs" (costs specifically attributable to that program — staff salaries, supplies, direct activities) and its "indirect costs" or "overhead" (costs supporting the organization as a whole, allocated across programs, as discussed in the functional expense classification article). Grant budgets often specify how indirect costs are recovered — either through a negotiated "indirect cost rate" applied to direct costs, or a "de minimis rate" (currently 10% of modified total direct costs under federal Uniform Guidance) for organizations that have never negotiated their own rate.

Cash flow budgeting — projecting the timing of cash receipts and disbursements, not just annual totals — is especially important for non-profits because revenue and expenses are often poorly synchronized in time. A government grant might reimburse expenses only after they're incurred and documented, requiring cash on hand before reimbursement arrives, or a major fundraising event might generate a large share of annual revenue in a single month. Organizations without adequate reserves or credit lines to bridge these gaps can face real operational difficulties even when the annual budget balances on paper.

Budget-to-actual variance analysis — comparing actual results to the budget throughout the year and investigating significant variances — is a standard practice that helps boards and management identify problems early (a program running significantly over budget, or revenue significantly behind projections) while there's still time to take corrective action, rather than discovering issues only when annual financial statements are prepared.`,
    quiz: [
      {
        q: 'Why might a non-profit need to request a "budget modification" from a funder?',
        choices: [
          'Because all non-profit budgets must be approved by the IRS',
          'Because many grants restrict spending to budgeted line items within that grant, so significant deviations from the approved grant budget may require prior funder approval',
          'Because budget modifications are required every month regardless of circumstances',
          'Because non-profits are not allowed to create budgets'
        ],
        correct: 1,
        explanation: 'Grant agreements often specify how funds must be spent according to an approved budget. If actual needs diverge significantly from that budget, the organization may need funder approval to reallocate funds between line items — a compliance requirement distinct from internal budget management.'
      },
      {
        q: 'Why is cash flow budgeting (timing of receipts and disbursements) especially important for non-profits?',
        choices: [
          'Because non-profits never have cash',
          'Because revenue (such as reimbursement-based government grants) and expenses are often poorly synchronized in time, so an organization could face cash shortages even if its annual budget balances on paper',
          'Because cash flow budgets replace the need for an operating budget',
          'Because cash flow budgeting is required only for for-profit companies'
        ],
        correct: 1,
        explanation: 'Reimbursement-based funding often pays after expenses are incurred, and revenue from events or grants may arrive in lumps rather than evenly throughout the year. Without adequate cash reserves or credit to bridge these gaps, an organization can face real operational difficulty despite a balanced annual budget.'
      }
    ]
  },
  {
    id: 'capital-campaigns',
    title: 'Capital Campaigns: Accounting Considerations',
    body: `A capital campaign is an intensive, time-limited fundraising effort aimed at raising a large sum of money for a specific major purpose — typically constructing or renovating a building, acquiring property, building an endowment, or some combination of these. Capital campaigns differ from a non-profit's ongoing annual fundraising both in scale and in the accounting considerations they raise.

The most fundamental accounting question for capital campaign contributions is timing of revenue recognition, which depends on whether pledges are conditional or unconditional (as discussed in the grant accounting and pledges receivable articles). Capital campaign pledges are often payable over multiple years (a common structure might be a five-year pledge period), meaning multi-year pledge accounting — recording pledges at present value and unwinding the discount over time — is particularly relevant for capital campaigns, which often involve some of an organization's largest individual pledges.

Capital campaign contributions are typically restricted by donors for the specific campaign purpose (construction of a new building, for example), classifying them as net assets with donor restrictions until the restriction is satisfied — which, for a building campaign, generally occurs as construction costs are incurred (since the donor's restriction is being fulfilled as the building is built) or, depending on the specific donor stipulations and the organization's accounting policy, potentially over the depreciable life of the resulting asset.

A significant accounting question involves the treatment of campaign costs — the expenses of running the campaign itself (campaign staff, consultants, materials, events). These costs are generally expensed as incurred, classified as fundraising expenses under the functional expense classification framework discussed elsewhere — they are not capitalized as part of the cost of the building or other asset being funded, even though the campaign's purpose is directly tied to that asset's acquisition.

Capital campaigns often include a "quiet phase" (sometimes called the "leadership phase") before the public launch, during which the organization seeks commitments from major donors and board members — often securing a significant percentage (sometimes 50% or more) of the total campaign goal before any public announcement. From an accounting perspective, pledges made during the quiet phase are recognized under the same rules as any other pledge — the "phase" of the campaign doesn't change the accounting, though the quiet phase can create a situation where an organization has recognized substantial pledge revenue (and corresponding receivables) before a public campaign total has even been announced.

For organizations undertaking major construction projects funded by capital campaigns, additional accounting considerations include: tracking and capitalizing eligible construction costs (and potentially capitalizing interest on construction-period borrowing, under the rules for capitalized interest), coordinating the timing of restriction releases with the construction timeline and the related depreciation of the completed asset, and managing the cash flow mismatch that can occur if pledge payments (often spread over years) lag behind the actual construction spending (which may need to occur on a compressed timeline) — sometimes requiring bridge financing to cover the gap between when pledges are made and when the cash is actually collected.`,
    quiz: [
      {
        q: 'How are the costs of running a capital campaign (staff, consultants, materials) typically treated for accounting purposes?',
        choices: [
          'Capitalized as part of the cost of the building being funded',
          'Expensed as incurred, classified as fundraising expenses under the functional expense framework',
          'Recorded as a reduction to pledges receivable',
          'Not recorded at all'
        ],
        correct: 1,
        explanation: 'Campaign costs are operating expenses related to fundraising activity and are expensed as incurred and classified as fundraising expenses, even though the campaign\'s purpose is to fund a specific capital asset — the costs of raising the money are distinct from the cost of the asset itself.'
      },
      {
        q: 'Why is multi-year pledge accounting particularly relevant to capital campaigns?',
        choices: [
          'Capital campaigns never involve pledges',
          'Capital campaign pledges are often payable over multiple years and tend to include some of an organization\'s largest individual commitments, making present value recognition and discount amortization especially significant',
          'Capital campaigns are always completed within one year',
          'Multi-year pledges are prohibited for capital campaigns'
        ],
        correct: 1,
        explanation: 'Capital campaigns commonly involve large pledges payable over several years (e.g., a five-year pledge period), so the present value recognition and subsequent discount unwinding discussed in the pledges receivable article are especially material to how campaign revenue is reported over time.'
      }
    ]
  },
  {
    id: 'joint-cost-allocation',
    title: 'Joint Cost Allocations for Fundraising Appeals',
    body: `Many non-profit fundraising materials serve more than one purpose at once — a direct mail piece might both solicit donations (a fundraising activity) and provide information about a public health issue or advocate for a policy position (a program activity). When a single activity combines fundraising with program (or management) components, GAAP provides specific guidance — historically under what's often still referred to as "SOP 98-2" guidance, now codified within ASC 958 — on whether and how the costs of that activity can be allocated between fundraising and program/management categories, rather than being classified entirely as fundraising.

Without this guidance, there would be an incentive to label virtually any communication as having a "program" component (education, advocacy) to avoid classifying its costs as fundraising — potentially making an organization's program expense ratio look more favorable than its actual activities would justify. To prevent this, joint cost allocation is permitted only if three specific criteria are met: purpose, audience, and content.

The "purpose" criterion requires that the activity call for specific action by the recipient that will help accomplish the organization's mission (beyond simply asking for a donation) — for example, asking the recipient to contact their legislator about an issue, or take some other action related to the organization's programmatic goals.

The "audience" criterion requires that the audience for the activity be selected based on their need for the program component of the message (or their ability to take the requested action), not solely based on their likelihood of making a contribution — if the mailing list is simply the organization's list of past donors or prospects identified primarily by their giving capacity, this criterion is generally not met, regardless of the content's substance.

The "content" criterion requires that the activity support the program (or management) function — meaning it must call for specific action intended to fulfill the entity's mission, and must fulfill one or more of the organization's programmatic purposes (not merely mention the existence of a program in passing while the primary content focuses on the fundraising appeal).

If all three criteria are met, the costs of the joint activity can be allocated among fundraising, program, and management/general categories using a reasonable allocation methodology. If any one of the three criteria is not met, the entire cost of the activity must be classified as fundraising expense — even if a portion of the content genuinely relates to program activities.

This is an area where auditors pay particular attention, given the direct impact joint cost allocations can have on an organization's reported program expense ratios — a metric heavily scrutinized by donors and charity watchdogs, as discussed in the overhead ratios article. An organization that allocates significant costs away from fundraising based on joint cost rules should be able to clearly demonstrate, with documented evidence, that all three criteria (purpose, audience, content) were genuinely met for the specific activities in question.`,
    quiz: [
      {
        q: 'What are the three criteria that must ALL be met for a non-profit to allocate the costs of a joint activity (combining fundraising and program elements) between functional categories?',
        choices: [
          'Size, timing, and cost',
          'Purpose, audience, and content',
          'Revenue, expense, and net assets',
          'Donor, grantor, and beneficiary'
        ],
        correct: 1,
        explanation: 'The purpose, audience, and content criteria together determine whether a joint activity genuinely has a program or management component beyond fundraising. All three must be met for any cost allocation away from fundraising to be permitted.'
      },
      {
        q: 'If a fundraising mailing fails to meet the "audience" criterion (e.g., it\'s sent based on donor capacity rather than need for program information), how must its costs be classified?',
        choices: [
          'Allocated proportionally based on content, regardless of the audience issue',
          'Entirely as fundraising expense, since all three criteria must be met for any allocation to program or management',
          'Entirely as program expense',
          'The costs can be excluded from the financial statements entirely'
        ],
        correct: 1,
        explanation: 'If any one of the three criteria (purpose, audience, content) is not met, the entire cost of the joint activity must be classified as fundraising — even if portions of the content relate to program activities, since all three criteria are required for any allocation.'
      }
    ]
  },
  {
    id: 'ubit',
    title: 'Unrelated Business Income Tax (UBIT) in Depth',
    body: `Tax-exempt organizations generally don't pay federal income tax on revenue from activities related to their exempt purpose. However, when a tax-exempt organization generates income from activities that are not substantially related to that exempt purpose, that income may be subject to Unrelated Business Income Tax (UBIT) — taxed at regular corporate income tax rates, even though the organization remains tax-exempt overall.

For income to be subject to UBIT, three conditions generally must all be present. First, the activity must constitute a "trade or business" — an activity carried on for the production of income from the sale of goods or services. Second, the trade or business must be "regularly carried on" — sporadic or one-time activities (like an annual fundraising dinner or occasional bake sale) generally don't meet this threshold, while an activity conducted with a frequency and continuity comparable to a commercial enterprise would. Third, the activity must not be "substantially related" to the organization's exempt purpose — meaning the activity doesn't contribute importantly to accomplishing the organization's exempt mission, aside from the organization's need for the income itself (the need for income, by itself, doesn't make an activity "related").

A classic example illustrating these concepts: a university's cafeteria, which serves students, faculty, and staff, is substantially related to its educational mission (feeding the people who are part of the educational community) and isn't subject to UBIT — even though the cafeteria generates revenue. But if that same university operates a separate commercial parking garage open to the general public for a fee, unrelated to any educational purpose, the income from that activity could be subject to UBIT, even though the proceeds support the university's educational mission generally (since, again, merely using the proceeds for exempt purposes doesn't make the activity itself "related").

Several important exceptions and modifications apply. Income from activities performed substantially by volunteers (the "volunteer labor exception") is generally excluded from UBIT, regardless of how commercial the activity might otherwise appear — this is why many non-profit thrift stores, staffed largely by volunteers, don't generate UBIT despite operating essentially as retail businesses. Income from the sale of donated goods (the "donated goods exception") is similarly excluded. Most forms of passive investment income — dividends, interest, royalties, and certain rents — are generally excluded from UBIT under specific statutory exceptions, on the theory that passive investment activity isn't the kind of active commercial competition UBIT is meant to address — though "debt-financed" investment income (income from property financed with borrowed money) can lose this exception under separate "unrelated debt-financed income" rules.

Organizations with $1,000 or more of gross unrelated business income must file Form 990-T and pay any resulting tax. The underlying policy rationale for UBIT is often described as addressing "unfair competition" — preventing tax-exempt organizations from having a competitive advantage over taxable businesses offering similar commercial goods or services, simply because the exempt organization's profits (if any) wouldn't be taxed while a for-profit competitor's would be.`,
    quiz: [
      {
        q: 'What three general conditions must be present for income to be subject to UBIT?',
        choices: [
          'The organization must be a church, the income must exceed $1 million, and the activity must be illegal',
          'The activity must be a trade or business, regularly carried on, and not substantially related to the organization\'s exempt purpose',
          'The income must come from donations, grants, and investment returns',
          'The organization must have for-profit subsidiaries'
        ],
        correct: 1,
        explanation: 'All three conditions must generally be met: the activity must be a trade or business (conducted for income from goods/services), regularly carried on (with commercial-like frequency), and not substantially related to the organization\'s exempt mission beyond the need for funds.'
      },
      {
        q: 'Why might a non-profit thrift store, which sells donated goods and is largely staffed by volunteers, avoid UBIT despite operating like a commercial retail business?',
        choices: [
          'Because thrift stores are illegal',
          'Because of statutory exceptions for income from activities substantially performed by volunteers and from the sale of donated goods',
          'Because UBIT only applies to organizations with no employees',
          'Because thrift stores never generate any income'
        ],
        correct: 1,
        explanation: 'The volunteer labor exception and the donated goods exception are specific statutory carve-outs that exclude income from these activities from UBIT, regardless of how commercial the activity might otherwise appear — explaining why such operations are common among non-profits without triggering UBIT.'
      }
    ]
  },
  {
    id: 'nonprofit-financial-ratios',
    title: 'Key Financial Ratios for Non-Profit Analysis',
    body: `While overhead ratios (discussed elsewhere) are perhaps the most commonly cited non-profit financial metrics, a more complete financial analysis of a non-profit organization draws on a broader set of ratios, many adapted from for-profit financial analysis but interpreted with non-profit-specific considerations in mind.

The "months of cash" or "months of operating reserve" ratio — unrestricted cash and cash equivalents (or sometimes unrestricted net assets) divided by average monthly operating expenses — provides a simple measure of how long an organization could sustain operations from its liquid reserves alone if revenue stopped entirely. While there's no universal "right" answer, many non-profit financial management resources suggest a target range (often three to six months, though this varies significantly based on the predictability and diversification of an organization's revenue sources) as a reasonable cushion against revenue disruptions.

The "current ratio" (current assets divided by current liabilities) — borrowed directly from for-profit analysis — measures short-term liquidity. For non-profits, it's worth considering whether current assets include amounts that are restricted (and therefore not actually available to meet general current liabilities) — a current ratio that looks healthy on paper might be less reassuring if a large portion of current assets consists of donor-restricted cash or pledges that can't be used for general operating purposes.

The "operating reliance" ratio examines what portion of an organization's revenue comes from its core mission-related activities (program service fees, for example) versus contributions and grants — providing insight into revenue diversification and dependence on fundraising versus earned revenue.

A ratio specific to organizations with significant debt is the "debt service coverage ratio" — a measure of whether operating cash flow is sufficient to cover required debt payments (principal and interest), often a covenant requirement in loan agreements with banks or bond holders financing non-profit facilities.

The "change in unrestricted net assets as a percentage of unrestricted revenue" provides a rough non-profit analog to a for-profit operating margin — though, as discussed in the statement of activities article, a single year's result can be heavily influenced by the timing of large grants or contributions, so trends over multiple years are generally more informative than any single year's figure.

Liquidity and reserve-focused ratios have become increasingly emphasized following the required "liquidity and availability of resources" disclosures under ASU 2016-14, which directly address how much of an organization's resources could be converted to cash within a year to meet general expenditures — a question these ratios attempt to approximate using readily available balance sheet figures, though the disclosure itself often provides more precise and organization-specific information than a generic ratio calculation could.

As with any ratio analysis, context matters enormously: appropriate benchmarks vary by organization size, sector (a hospital's financial ratios look very different from a small community arts organization's), revenue model (heavily grant-dependent organizations face different liquidity dynamics than those with diversified earned revenue), and the specific point in an organization's life cycle (a young, growing organization may have different — and not necessarily worse — financial characteristics than a mature, stable one).`,
    quiz: [
      {
        q: 'What does the "months of cash" (operating reserve) ratio measure?',
        choices: [
          'The total revenue earned over twelve months',
          'How long an organization could sustain operations from its liquid reserves alone if revenue stopped entirely, calculated as unrestricted cash divided by average monthly operating expenses',
          'The number of donors who gave during the year',
          'The percentage of expenses spent on fundraising'
        ],
        correct: 1,
        explanation: 'Months of cash provides a simple gauge of an organization\'s financial cushion against revenue disruptions — dividing available unrestricted liquid resources by typical monthly operating costs to estimate how long operations could continue without new revenue.'
      },
      {
        q: 'Why should a non-profit\'s "current ratio" be interpreted with extra care compared to a similar ratio for a for-profit company?',
        choices: [
          'Non-profits never have current liabilities',
          'Current assets might include donor-restricted cash or pledges that are not actually available to meet general current liabilities, even though they appear in the ratio',
          'The current ratio cannot be calculated for non-profits',
          'Non-profits are required to have a current ratio of exactly 1.0'
        ],
        correct: 1,
        explanation: 'A current ratio that appears healthy could be misleading if a significant portion of current assets is donor-restricted and unavailable for general operating purposes — understanding the composition of current assets is important for accurately assessing true liquidity.'
      }
    ]
  }
);
