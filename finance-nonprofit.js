// ---------- Non-Profit Accounting (batch 1) ----------
FINANCE_ARTICLES.push(
  {
    id: 'fund-accounting-basics',
    title: 'Fund Accounting Basics',
    body: `Fund accounting is a system used primarily by non-profit organizations and governments to track resources according to restrictions on their use, rather than purely by department or activity as a for-profit business might. The central idea is accountability: donors, grantors, and boards want assurance that money given for a specific purpose is actually spent on that purpose.

A "fund" in this context is a self-balancing set of accounts — its own mini set of assets, liabilities, and net assets (or fund balance) — established for a particular purpose or activity. A non-profit might maintain an unrestricted operating fund for general activities, a restricted fund for a specific grant, a building fund for a capital campaign, and an endowment fund for long-term investments, each tracked separately even though they appear together in the organization's overall financial statements.

This contrasts with for-profit accounting, where all resources are typically pooled and tracked through a single set of books focused on overall profitability. A non-profit, by contrast, must be able to demonstrate that restricted funds were used only for their intended purposes — spending restricted grant money on general overhead, for instance, could constitute a breach of the organization's obligations to the donor and, in some cases, legal violations.

Modern GAAP for non-profits (under ASC 958) doesn't require literal segregated "funds" in the bookkeeping sense for external financial reporting — instead, net assets are classified into two categories: net assets without donor restrictions and net assets with donor restrictions. However, many non-profits still maintain fund-based bookkeeping internally, both for historical reasons and because it helps program managers and boards track restricted resources at a granular level, even though the external financial statements aggregate this information into the two required net asset classifications.

Fund accounting also plays a major role in governmental accounting (governed by GASB rather than FASB), where funds are categorized into governmental funds, proprietary funds, and fiduciary funds — each with different measurement focuses and bases of accounting. While the specific rules differ from non-profit GAAP, the underlying philosophy is the same: resources are tracked according to the restrictions and purposes for which they were provided, not just pooled together as a single undifferentiated pot of money.

For an accountant moving from for-profit to non-profit work, the biggest mental shift is usually this: the question isn't just "did we make money?" but "did we use the resources we were given the way we promised to?"`,
    quiz: [
      {
        q: 'What is the primary purpose of fund accounting in a non-profit organization?',
        choices: [
          'To maximize reported net income',
          'To track resources according to restrictions on their use, providing accountability to donors and grantors',
          'To avoid filing tax returns',
          'To eliminate the need for a balance sheet'
        ],
        correct: 1,
        explanation: 'Fund accounting separates resources by purpose and restriction so an organization can demonstrate that donor-restricted funds were used as intended — a core accountability requirement that differs from the profit-focused tracking typical of for-profit businesses.'
      },
      {
        q: 'Under current GAAP (ASC 958), how are a non-profit\'s net assets classified on its statement of financial position?',
        choices: [
          'Permanently restricted, temporarily restricted, and unrestricted (three categories)',
          'Net assets without donor restrictions and net assets with donor restrictions (two categories)',
          'Only as "total equity" with no further breakdown',
          'By department or program only'
        ],
        correct: 1,
        explanation: 'ASC 958 simplified the prior three-category system into two: net assets without donor restrictions and net assets with donor restrictions, while many organizations continue to use internal fund accounting to track more granular detail.'
      }
    ]
  },
  {
    id: 'statement-of-activities',
    title: 'The Statement of Activities',
    body: `The statement of activities is the non-profit equivalent of a for-profit company's income statement, but its structure reflects the unique way non-profits report revenue and the restrictions that come with it. Rather than showing "net income," it shows the "change in net assets" — the non-profit equivalent of profit or loss for the period.

The statement is typically organized into columns (or sections) for net assets without donor restrictions and net assets with donor restrictions, with a total column combining both. Revenue and support — including contributions, grants, program service fees, and investment income — are reported in the column corresponding to any restrictions placed on them by the donor. Expenses, by contrast, are almost always reported only in the unrestricted column, because incurring an expense is, by definition, an unrestricted use of resources (even if the cash that funded it came from a restricted source).

This creates one of the most distinctive features of non-profit reporting: "net assets released from restrictions." When a donor-restricted contribution is used for its intended purpose (or a time restriction expires), the organization reclassifies that amount — showing it as a decrease in the "with restrictions" column and a corresponding increase in the "without restrictions" column. This reclassification has no effect on total net assets; it simply reflects that the restriction has now been satisfied and the resources have moved into the unrestricted pool where the related expense will be recorded.

Expenses on the statement of activities are typically reported by functional classification — program services, management and general, and fundraising — rather than by natural classification (salaries, rent, supplies) alone, although many organizations present both views, either on the face of the statement or in a separate statement of functional expenses.

A non-profit can have a "surplus" (increase in net assets) or "deficit" (decrease in net assets) in a given period, and unlike a for-profit company, a surplus isn't necessarily "good" in isolation, nor is a deficit necessarily "bad" — a non-profit might run a planned deficit by drawing down reserves to fund an unusually large program need, or might show a large surplus simply because it received a major multi-year grant upfront that will be spent over several future years. Understanding the statement of activities requires looking beyond the bottom line to understand the restrictions and timing behind the numbers.`,
    quiz: [
      {
        q: 'On the statement of activities, why are expenses almost always reported in the "without donor restrictions" column, even if the cash used came from a restricted gift?',
        choices: [
          'Because GAAP prohibits non-profits from spending restricted funds',
          'Because incurring an expense is considered an unrestricted use of resources, and a "release from restriction" reclassification moves the related resources to the unrestricted column first',
          'Because expenses are never reported on the statement of activities',
          'Because all donor restrictions automatically expire after one year'
        ],
        correct: 1,
        explanation: 'When restricted funds are spent for their intended purpose, the organization records a "net assets released from restrictions" reclassification, moving the amount from the restricted to the unrestricted column — expenses are then recorded against the unrestricted column.'
      },
      {
        q: 'Why might a non-profit show a large "surplus" (increase in net assets) in a given year without it necessarily indicating strong operational performance?',
        choices: [
          'Surpluses are always a sign of mismanagement',
          'A large multi-year grant received upfront could be recorded as revenue in the year received, even though it will be spent over several future years',
          'Non-profits are not allowed to have surpluses',
          'Surpluses only occur due to accounting errors'
        ],
        correct: 1,
        explanation: 'Revenue recognition timing for grants and contributions can create a mismatch between when resources are received/recognized and when they are actually spent, so a surplus in one year may simply reflect timing rather than improved operations.'
      }
    ]
  },
  {
    id: 'net-assets-restrictions',
    title: 'Net Assets: With and Without Donor Restrictions',
    body: `Under ASC 958, a non-profit's net assets — the non-profit equivalent of equity — are classified into exactly two categories based on donor-imposed restrictions: net assets without donor restrictions, and net assets with donor restrictions. This two-category structure replaced the older three-category system (unrestricted, temporarily restricted, permanently restricted) in 2018, simplifying presentation while preserving the underlying distinctions in the footnotes.

Net assets without donor restrictions represent resources the organization can use for any purpose consistent with its mission, at the discretion of its board. This includes the bulk of typical operating revenue — program fees, unrestricted contributions, and most government contract revenue for services already rendered. The board can designate portions of unrestricted net assets for specific future purposes (a "board-designated" reserve, for example), but — critically — board designations are internal and can be changed by the board itself; they don't carry the same legal weight as donor restrictions.

Net assets with donor restrictions represent resources subject to restrictions imposed by donors (not the organization itself) that haven't yet been met. These restrictions generally fall into two types: purpose restrictions (the money must be used for a specific program, like "scholarships" or "the new building") and time restrictions (the money can't be used until a future date, or must be maintained in perpetuity, as with many endowments).

Donor-restricted endowments — where the donor specifies that the principal must be maintained permanently, with only investment earnings available for spending — represent a special case. The original gift amount typically remains classified "with donor restrictions" indefinitely (since the purpose/time restriction on the corpus never expires), while earnings may be either restricted (if the donor also restricted how earnings can be used) or released to the unrestricted column as they're appropriated for spending under the organization's spending policy.

A critical compliance issue is "underwater endowments" — funds where the current fair value has fallen below the original gift amount due to investment losses. Accounting standards require specific disclosures about underwater endowments, and many states' adoption of the Uniform Prudent Management of Institutional Funds Act (UPMIFA) affects whether and how an organization can continue spending from an underwater fund.

For accountants and auditors, correctly classifying net assets — and tracking the often-detailed, donor-by-donor and restriction-by-restriction records behind the summary numbers — is one of the most labor-intensive but legally significant aspects of non-profit financial reporting.`,
    quiz: [
      {
        q: 'What is the key difference between a "board-designated" reserve and donor-restricted net assets?',
        choices: [
          'There is no difference; both are reported identically',
          'Board designations are internal decisions that the board itself can change, while donor restrictions are externally imposed and cannot be removed by the organization alone',
          'Board-designated funds must always be classified as donor-restricted',
          'Donor restrictions can be removed by the organization at any time'
        ],
        correct: 1,
        explanation: 'Board designations remain part of net assets without donor restrictions because the board retains the authority to redirect those resources. Donor restrictions are externally imposed and remain in the "with donor restrictions" category until the donor\'s conditions are satisfied.'
      },
      {
        q: 'For a donor-restricted endowment requiring the principal to be maintained in perpetuity, how is the original gift typically classified over time?',
        choices: [
          'It moves to "without donor restrictions" after one year',
          'It generally remains classified "with donor restrictions" indefinitely, since the restriction on the corpus never expires',
          'It is recorded as a liability rather than net assets',
          'It is expensed immediately upon receipt'
        ],
        correct: 1,
        explanation: 'Because the donor\'s restriction on maintaining the principal in perpetuity never lapses, the original corpus remains "with donor restrictions" indefinitely, while investment earnings may be released for spending depending on the donor\'s terms and the organization\'s spending policy.'
      }
    ]
  },
  {
    id: 'statement-of-financial-position-np',
    title: 'The Non-Profit Statement of Financial Position',
    body: `The statement of financial position is the non-profit equivalent of a balance sheet — a snapshot, as of a specific date, of an organization's assets, liabilities, and net assets. The fundamental accounting equation still holds: Assets = Liabilities + Net Assets, mirroring the for-profit Assets = Liabilities + Equity.

On the asset side, non-profits report many of the same categories a for-profit would: cash and cash equivalents, investments, accounts and pledges receivable, prepaid expenses, and property and equipment. One distinctive item is "contributions receivable" (also called pledges receivable) — amounts donors have promised to give but haven't yet paid, which are recorded as an asset (and corresponding revenue) when the promise becomes unconditional, often at a present value if payments will be received over multiple years.

A particularly important non-profit-specific concept is the distinction between assets that are available for general use versus those that are restricted or otherwise limited in their availability — for example, cash held in a donor-restricted endowment, or property that must be used for a specific purpose under the terms of a grant. While these restricted assets still appear within the relevant asset categories (cash, investments, etc.), the corresponding net asset classification (with donor restrictions) signals that they aren't freely available for general operations — and many organizations provide additional disclosures or a "liquidity and availability" note specifically addressing how much of their assets could be converted to cash within a year to meet general expenditures.

On the liabilities side, non-profits report typical items like accounts payable, accrued expenses, and debt — but also some unique items, such as "refundable advances" (cash received under a grant or contract that's conditional, meaning the organization hasn't yet earned the right to keep it, so it's recorded as a liability rather than revenue until conditions are met) and amounts held for others (resources the organization is holding on behalf of another entity, such as in an agency transaction).

The bottom section — net assets — is where the statement of financial position connects directly to the statement of activities: the change in net assets for the period (from the statement of activities) flows into the ending net assets balance reported here, split between the with- and without-donor-restriction categories.

The "liquidity and availability of resources" disclosure, required under ASU 2016-14, has become one of the most useful additions for readers of non-profit financial statements — it directly addresses a question that's often hard to answer from the raw numbers alone: if this organization needed cash to cover unexpected expenses in the next twelve months, how much could it actually access?`,
    quiz: [
      {
        q: 'What does "contributions receivable" (pledges receivable) represent on a non-profit\'s statement of financial position?',
        choices: [
          'Cash the organization owes to vendors',
          'Amounts donors have unconditionally promised to give but have not yet paid',
          'Government grants that have already been spent',
          'The market value of the organization\'s building'
        ],
        correct: 1,
        explanation: 'Once a donor makes an unconditional promise to give, the non-profit records an asset (contributions receivable) and corresponding revenue, even though cash hasn\'t yet been received — often discounted to present value for multi-year pledges.'
      },
      {
        q: 'Why might cash received under a conditional grant be recorded as a liability ("refundable advance") rather than revenue?',
        choices: [
          'Because the organization has not yet met the conditions required to earn and keep the funds',
          'Because all government funding is automatically classified as debt',
          'Because the cash belongs to the organization\'s employees',
          'Because non-profits cannot recognize grant revenue under any circumstances'
        ],
        correct: 0,
        explanation: 'If a grant is conditional (requiring specific actions or outcomes before the recipient is entitled to the funds), cash received before those conditions are met is recorded as a refundable advance — a liability — until the conditions are substantially met and revenue can be recognized.'
      }
    ]
  },
  {
    id: 'in-kind-donations',
    title: 'Accounting for In-Kind Donations',
    body: `In-kind donations — also called gifts-in-kind or non-cash contributions — are donations of goods, services, or use of facilities rather than cash. Common examples include donated food for a food bank, donated professional services (legal, accounting, or medical), donated use of office space, and donated equipment or supplies. GAAP requires these contributions to be recognized in the financial statements at fair value, ensuring the full economic resources an organization receives and uses are reflected, not just its cash transactions.

For donated goods, fair value is generally based on what the organization would have to pay to acquire similar goods in the market in which it normally would obtain them — which might be a wholesale market rather than retail, particularly for items like donated pharmaceuticals or bulk food, where the distinction can produce dramatically different valuations.

Donated services are subject to a more restrictive recognition test. Under ASC 958, contributed services are recognized only if they either (a) create or enhance a nonfinancial asset (for example, a contractor donating labor to renovate a building owned by the non-profit), or (b) require specialized skills, are provided by individuals possessing those skills, and would typically need to be purchased if not donated (for example, a licensed attorney providing pro bono legal services, or a licensed nurse providing medical care at a clinic). Services that don't meet this test — such as general volunteer labor for things like serving meals or staffing a fundraising event — are not recognized in the financial statements at all, even though they're often critical to an organization's operations and may be discussed extensively in non-financial reporting.

Since 2020, ASU 2020-07 has required non-profits to present contributed nonfinancial assets (in-kind donations of goods, services, and use of facilities) as a separate line item in the statement of activities, distinct from cash contributions, and to provide expanded footnote disclosures describing the types of contributed nonfinancial assets received, the valuation techniques used, and any donor-imposed restrictions on their use. This change was driven partly by concerns that in-kind contributions — particularly large gifts of pharmaceuticals or other goods with debatable market valuations — were not being presented with enough transparency for readers to understand their nature and significance relative to cash operations.

When recorded, an in-kind donation typically results in both revenue (contribution revenue at fair value) and a corresponding expense or asset — for example, donated food recognized as both revenue and, often immediately, as a program expense if distributed promptly, or as inventory if held for later distribution.`,
    quiz: [
      {
        q: 'Under ASC 958, when must a non-profit recognize donated (contributed) services in its financial statements?',
        choices: [
          'Whenever any volunteer provides any service, regardless of type',
          'Only when the services create or enhance a nonfinancial asset, or require specialized skills that would otherwise need to be purchased',
          'Never — donated services are never recognized under GAAP',
          'Only if the volunteer requests recognition'
        ],
        correct: 1,
        explanation: 'GAAP sets a deliberately narrow test: contributed services are recognized only if they create/enhance a nonfinancial asset or require specialized skills typically performed by paid professionals. General volunteer labor that doesn\'t meet this test goes unrecorded in the financial statements.'
      },
      {
        q: 'What change did ASU 2020-07 require regarding contributed nonfinancial assets (in-kind donations)?',
        choices: [
          'In-kind donations no longer need to be recorded at all',
          'They must be presented as a separate line item from cash contributions, with expanded footnote disclosures about valuation and restrictions',
          'They must be valued at the donor\'s original purchase price only',
          'They can only be recorded if received from government entities'
        ],
        correct: 1,
        explanation: 'ASU 2020-07 increased transparency by requiring non-profits to separately present contributed nonfinancial assets in the statement of activities and disclose additional detail about the nature, valuation methods, and any restrictions on these contributions.'
      }
    ]
  },
  {
    id: 'form-990',
    title: 'The Form 990 and Tax-Exempt Reporting',
    body: `Form 990 is the annual information return that most tax-exempt organizations — including 501(c)(3) public charities — must file with the IRS. Unlike a typical corporate tax return, the Form 990 isn't primarily about calculating taxes owed (most tax-exempt organizations owe little or no income tax on their exempt-purpose activities). Instead, it's a public disclosure document designed to demonstrate that an organization continues to operate consistently with its tax-exempt purpose.

Because Form 990 is a public document — available to anyone through the IRS or third-party databases like GuideStar/Candid and ProPublica's Nonprofit Explorer — it serves as a primary source of information for donors, watchdog groups, journalists, and researchers evaluating a non-profit's finances, governance, and programs. This public visibility creates pressure on organizations to present their numbers carefully and consistently, since a poorly explained financial result can attract unwanted scrutiny.

The form requires extensive disclosures beyond basic financial statements: compensation of officers, directors, key employees, and highest-paid contractors; governance practices (such as whether the organization has a conflict-of-interest policy and whether the board reviews the Form 990 before filing); a detailed breakdown of revenue and expenses by program activity; and a description of the organization's mission and most significant program accomplishments during the year.

One area that receives particular attention is the calculation of program service expense ratios — the percentage of total expenses spent on program activities versus management/general and fundraising. While these ratios are popular with donors and watchdog organizations as a quick efficiency measure, they can be misleading: legitimate differences in organizational size, life cycle stage (a young organization may need to invest heavily in fundraising infrastructure), and how costs are allocated to functional categories can all affect these ratios without reflecting actual differences in effectiveness.

Organizations with unrelated business income — income from a trade or business not substantially related to their exempt purpose — must also file Form 990-T and may owe Unrelated Business Income Tax (UBIT) on that income, even though their primary activities remain tax-exempt.

Smaller organizations (generally those with gross receipts under certain thresholds) may be eligible to file simplified versions — Form 990-EZ or the even simpler Form 990-N ("e-Postcard") — though many choose to file the full Form 990 anyway for the credibility and transparency it provides to donors and grantors evaluating the organization.`,
    quiz: [
      {
        q: 'What is the primary purpose of Form 990, as distinct from a typical corporate income tax return?',
        choices: [
          'To calculate and pay income tax on all of the organization\'s revenue',
          'To serve as a public disclosure document demonstrating the organization continues to operate consistently with its tax-exempt purpose',
          'To register the organization as a corporation',
          'To apply for tax-exempt status for the first time'
        ],
        correct: 1,
        explanation: 'Most tax-exempt organizations owe little or no tax on exempt-purpose activities, so Form 990 functions primarily as a transparency and accountability tool — a publicly available document detailing finances, governance, and program activities.'
      },
      {
        q: 'When would a tax-exempt organization owe Unrelated Business Income Tax (UBIT) and need to file Form 990-T?',
        choices: [
          'Whenever it receives any donations',
          'When it has income from a trade or business not substantially related to its exempt purpose',
          'Whenever its program expenses exceed its revenue',
          'UBIT applies to all non-profit revenue automatically'
        ],
        correct: 1,
        explanation: 'Income from activities unrelated to an organization\'s exempt mission can be subject to UBIT, even though the organization\'s core charitable activities remain tax-exempt — this prevents exempt organizations from gaining an unfair competitive advantage in unrelated commercial activities.'
      }
    ]
  },
  {
    id: 'functional-expense-classification',
    title: 'Functional Expense Classification',
    body: `Non-profit accounting requires expenses to be classified not only by their natural type (salaries, rent, utilities, supplies) but also by their function — what the expense was for. GAAP identifies three functional categories: program services, management and general, and fundraising.

Program services represent the activities for which the organization exists — the direct delivery of services or goods that fulfill its mission. A food bank's program expenses would include the cost of food distributed and the staff who run distribution operations. A large organization may have multiple program categories (for example, "education programs" and "advocacy programs" reported separately) if that breakdown is meaningful to how the organization is managed and evaluated.

Management and general (sometimes called "administrative" or "overhead") expenses are the costs of overall direction and oversight that aren't identifiable with a specific program, fundraising activity, or membership development — things like the executive director's general oversight time, accounting and HR functions, board governance costs, and general legal expenses.

Fundraising expenses are costs incurred to induce potential donors to contribute — direct mail campaigns, special events (net of any direct costs that benefit donors, which may be classified differently), grant-writing staff time, and donor cultivation activities.

Many costs benefit more than one function simultaneously — a classic example is an executive director's salary, where some portion of their time is spent on program oversight, some on general management, and some on donor relations and fundraising. GAAP requires these "joint costs" to be allocated among functions using a reasonable, consistently applied methodology — often based on time studies, square footage, or other objective measures — rather than assigned entirely to one category.

The required "statement of functional expenses" (mandatory for voluntary health and welfare organizations, and increasingly common practice for all non-profits under ASU 2016-14) presents expenses in a matrix — natural classification down the rows, functional classification across the columns — giving readers a two-dimensional view: both what the organization spent money on, and what it was for.

Functional expense allocation is an area where management has genuine discretion, and reasonable people can disagree about appropriate allocation methodologies. Because program expense ratios derived from this classification are heavily used by donors and watchdogs to judge "efficiency," there's an inherent (if usually unconscious) incentive to allocate costs toward programs and away from administration and fundraising — something auditors specifically watch for when reviewing allocation methodologies for reasonableness and consistency year over year.`,
    quiz: [
      {
        q: 'What are the three functional expense categories required under non-profit GAAP?',
        choices: [
          'Revenue, expenses, and net assets',
          'Program services, management and general, and fundraising',
          'Cash, investments, and fixed assets',
          'Restricted, unrestricted, and endowment'
        ],
        correct: 1,
        explanation: 'Non-profit GAAP requires expenses to be classified by function into program services (mission delivery), management and general (overhead/administration), and fundraising — in addition to their natural classification by type.'
      },
      {
        q: 'How should a cost that benefits multiple functions — such as an executive director\'s salary covering program oversight, administration, and fundraising — be handled?',
        choices: [
          'It must be allocated entirely to program services to improve efficiency ratios',
          'It must be allocated entirely to management and general',
          'It should be allocated among the relevant functions using a reasonable, consistently applied methodology',
          'It should be excluded from the statement of functional expenses entirely'
        ],
        correct: 2,
        explanation: 'GAAP requires joint costs that benefit multiple functions to be allocated using a reasonable basis (such as time studies), applied consistently — allocating such costs entirely to one category, especially to improve reported ratios, would not be appropriate.'
      }
    ]
  },
  {
    id: 'endowments-accounting',
    title: 'Endowments and Their Accounting Treatment',
    body: `An endowment is a fund established to provide ongoing financial support for an organization, typically structured so that the original gift (the "corpus" or "principal") is invested and only a portion of the investment returns is spent each year, allowing the fund to support the organization indefinitely. Endowments are common at universities, hospitals, museums, and foundations, where donors want to create a lasting legacy of support.

Endowments come in three general types from an accounting perspective. A "true" or donor-restricted endowment is created by a donor's explicit instruction that the principal be maintained permanently (or for a specified term), with only earnings available for spending — this is classified as net assets with donor restrictions, often permanently so for true perpetual endowments. A "term endowment" is similar but the restriction on principal expires after a specified period or event, after which the funds become unrestricted. A "quasi-endowment" (sometimes called a "board-designated endowment") is created when the organization's own board, rather than a donor, decides to set aside unrestricted funds and invest them as if they were an endowment — because this restriction comes from the board rather than a donor, quasi-endowments remain classified as net assets without donor restrictions, and the board retains the authority to "un-designate" them if needed.

Most states have adopted some version of the Uniform Prudent Management of Institutional Funds Act (UPMIFA), which provides a framework for how much an organization can prudently spend from a donor-restricted endowment each year, considering factors like the fund's purpose, duration, expected total return, and the effects of inflation. Many organizations adopt a formal spending policy — often a percentage (commonly 4-5%) of a moving average of the fund's fair value over several years — designed to provide a predictable stream of support while preserving purchasing power over time.

A significant accounting and disclosure issue arises when an endowment's fair value falls below its original gift amount (or the amount required to be maintained by donor stipulation or law) — a situation called being "underwater." GAAP requires disclosure of the aggregate amount by which funds are underwater, the aggregate original gift amounts, and the organization's policy regarding spending from underwater funds. Under UPMIFA, organizations generally retain the ability to prudently spend from an underwater endowment (rather than being absolutely prohibited), but must document that any such spending decision is consistent with the duty of prudence.

For accountants, endowment accounting combines investment accounting (tracking fair value, realized and unrealized gains, and investment income) with donor restriction tracking (determining what's available to spend under both legal requirements and donor-specific terms) — making it one of the more technically demanding areas of non-profit financial reporting.`,
    quiz: [
      {
        q: 'What distinguishes a "quasi-endowment" (board-designated endowment) from a donor-restricted endowment?',
        choices: [
          'Quasi-endowments are larger in size',
          'Quasi-endowments are created by the organization\'s own board from unrestricted funds, so the board retains authority to remove the designation, unlike a donor restriction',
          'Quasi-endowments cannot be invested',
          'There is no difference in accounting treatment'
        ],
        correct: 1,
        explanation: 'Because a quasi-endowment\'s restriction originates from the board itself rather than a donor, it remains classified as net assets without donor restrictions, and the board can change its designation — unlike a true donor-restricted endowment, which the organization cannot unilaterally modify.'
      },
      {
        q: 'What does it mean for an endowment fund to be "underwater," and what does GAAP require in that situation?',
        choices: [
          'The fund has more cash than required, and no disclosure is needed',
          'The fund\'s current fair value has fallen below its original gift amount, requiring specific disclosures about the underwater amount and the organization\'s spending policy',
          'The fund must be immediately liquidated',
          'The organization must return the funds to the donor'
        ],
        correct: 1,
        explanation: 'An underwater endowment has lost value relative to its original gift (or required maintained amount). GAAP requires disclosure of the aggregate underwater amounts, original gift values, and the organization\'s policy on spending from such funds, since UPMIFA generally permits continued prudent spending rather than an outright prohibition.'
      }
    ]
  },
  {
    id: 'grant-accounting-np',
    title: 'Grant Accounting and Revenue Recognition for Non-Profits',
    body: `Grants are a major revenue source for many non-profits, but accounting for them requires answering a deceptively tricky question: is this grant a "contribution" or an "exchange transaction"? The answer determines which accounting framework applies — ASC 958-605 (not-for-profit revenue recognition for contributions) or ASC 606 (the general revenue recognition standard used for exchange transactions, discussed elsewhere).

A contribution is a transfer of assets where the donor receives no direct commensurate value in return — the donor is providing resources to support the organization's mission, not purchasing a good or service for their own benefit. An exchange transaction, by contrast, involves each party receiving and giving up something of approximately equal value — for example, a government contract to provide specific services to a defined population, where the government is essentially "purchasing" services, may be considered an exchange transaction even if it's structured as a "grant."

Once a transaction is determined to be a contribution, the next question is whether it's "conditional" or "unconditional." A conditional contribution includes a "barrier" the recipient must overcome to be entitled to the funds — specific performance requirements, measurable outcomes, or matching fund requirements — combined with a right of return (or release from obligation) for the donor if the barrier isn't met. Conditional contributions are not recognized as revenue until the conditions are substantially met; cash received before that point is recorded as a refundable advance (a liability).

An unconditional contribution, by contrast, is recognized as revenue immediately upon the unconditional promise to give — even if payment will occur over multiple future years (in which case it's typically recorded at present value, with the discount unwound as interest income over time) — though it may still carry donor-imposed restrictions on how or when the funds can be used, which affects net asset classification (with vs. without donor restrictions) but not the timing of revenue recognition itself.

Multi-year grants are particularly important to get right. A common error is recognizing a multi-year grant entirely as revenue in the year it's awarded — if the grant is unconditional, this might actually be correct (with the funds simply classified as restricted until used in future years), but if the grant includes conditions tied to future performance periods, only the portion related to conditions already met should be recognized, with the remainder still treated as a liability.

The distinction between conditional and unconditional, and between contribution and exchange, requires careful reading of the actual grant agreement's terms — the label a funder puts on a grant ("grant," "contract," "award") doesn't determine its accounting treatment; the substance of the terms does.`,
    quiz: [
      {
        q: 'What is the key difference between a "contribution" and an "exchange transaction" for a non-profit?',
        choices: [
          'Contributions are always larger in dollar amount',
          'In a contribution, the donor receives no direct commensurate value in return; in an exchange transaction, each party gives and receives something of approximately equal value',
          'Exchange transactions can only occur with government entities',
          'There is no accounting difference between the two'
        ],
        correct: 1,
        explanation: 'This distinction determines which revenue recognition framework applies — ASC 958-605 for contributions or ASC 606 for exchange transactions — and the label a funder uses (e.g., "grant") doesn\'t determine the answer; the substance of the agreement does.'
      },
      {
        q: 'How should cash received under a conditional contribution be recorded before the conditions are met?',
        choices: [
          'As revenue immediately',
          'As a refundable advance (a liability) until the conditions are substantially met',
          'As an increase to net assets with donor restrictions only, with no liability',
          'It should not be recorded at all until spent'
        ],
        correct: 1,
        explanation: 'Conditional contributions are not recognized as revenue until the specified barriers are substantially overcome. Cash received in advance of meeting those conditions is recorded as a refundable advance — a liability — reflecting the possibility the funds could need to be returned.'
      }
    ]
  },
  {
    id: 'overhead-ratios',
    title: 'Overhead Ratios and Charity Watchdogs',
    body: `Donors, charity rating agencies, and the media frequently use "overhead ratios" — most commonly the percentage of total expenses spent on management and general plus fundraising, versus the percentage spent on program services — as a shorthand measure of a non-profit's efficiency or quality. A common rule of thumb circulated by some watchdogs suggests organizations should spend 75% or more of their budget on programs, keeping overhead below 25%.

While these ratios are easy to calculate from the Form 990 or audited financial statements and provide some signal, the non-profit sector has increasingly pushed back against treating them as a primary measure of organizational effectiveness — a movement sometimes called the "overhead myth." Several major charity evaluators, including some that historically emphasized these ratios heavily, have shifted toward incorporating measures of actual impact and outcomes alongside, or instead of, pure financial ratios.

There are several legitimate reasons overhead ratios can be misleading. First, organizations vary enormously in how they allocate joint costs across functional categories — an organization with aggressive (but defensible) allocation methodologies might report a lower overhead ratio than an otherwise-identical organization with more conservative allocations, without any real difference in how resources are actually used. Second, organizations at different life-cycle stages have different needs — a young organization building infrastructure, technology, or fundraising capacity may need to invest more heavily in "overhead" in the short term to build long-term program capacity and sustainability. Third, certain types of programs are inherently more "overhead-light" or "overhead-heavy" — a direct cash-transfer program will show a very different ratio than a research-intensive or advocacy-focused organization, even if both are highly effective at their respective missions.

There's also a documented risk of a "starvation cycle": pressure to keep overhead ratios artificially low can lead organizations to underinvest in things like financial systems, staff training, technology, and fundraising capacity — all of which can ultimately undermine the organization's ability to deliver on its mission effectively and sustainably, even though it might look more "efficient" on paper in the short term.

For accountants working with non-profits, understanding overhead ratios means understanding both how they're calculated (and the judgment involved in functional expense allocation that feeds into them) and their limitations as a standalone measure — useful as one data point among many, but a poor substitute for evaluating whether an organization is actually achieving its mission.`,
    quiz: [
      {
        q: 'What is the "overhead myth" that some non-profit sector advocates have pushed back against?',
        choices: [
          'The idea that non-profits have any overhead costs at all',
          'The idea that a low overhead ratio (spending on admin/fundraising vs. programs) is a reliable, standalone measure of an organization\'s effectiveness',
          'The idea that donors should never look at financial statements',
          'The idea that the Form 990 is required'
        ],
        correct: 1,
        explanation: 'The "overhead myth" refers to the oversimplified belief that low overhead ratios equal high effectiveness. In reality, ratios can be affected by cost allocation judgments, organizational life cycle, and program type, and underinvestment in "overhead" can actually undermine mission delivery.'
      },
      {
        q: 'What is the "starvation cycle" concern related to overhead ratios?',
        choices: [
          'Non-profits running out of food to distribute',
          'Pressure to minimize reported overhead can lead organizations to underinvest in systems, training, and fundraising capacity, ultimately undermining long-term effectiveness',
          'Donors stopping all contributions to an organization',
          'A requirement that all non-profits spend exactly 25% on overhead'
        ],
        correct: 1,
        explanation: 'When organizations chronically underinvest in administrative and fundraising infrastructure to keep reported overhead ratios low, they can become less capable over time — a self-reinforcing cycle that can ultimately harm program delivery despite appearing "efficient" on paper.'
      }
    ]
  }
);
