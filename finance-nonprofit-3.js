// ---------- Non-Profit Accounting (batch 3) ----------
FINANCE_ARTICLES.push(
  {
    id: 'donor-restrictions-release',
    title: 'Releasing Donor Restrictions on Net Assets',
    body: `As discussed in the article on net asset restrictions, non-profit organizations classify their net assets into "without donor restrictions" and "with donor restrictions" categories, based on whether donors have placed limits on how or when contributed resources can be used. A critical and recurring accounting process is the "release" of donor restrictions — recognizing when restricted resources have been used in a manner satisfying the donor's stipulations, and reclassifying the related net assets from "with donor restrictions" to "without donor restrictions."

Restrictions are released in two basic situations: when a purpose restriction is satisfied (the organization has incurred expenses for the specific purpose the donor specified — for example, a donor gave $50,000 restricted to funding a job-training program, and the organization spent $50,000 on qualifying job-training program expenses), or when a time restriction expires (the donor specified the funds couldn't be used until a future date or period, and that date has arrived — for example, a pledge restricted for use "in fiscal year 2027" is released once fiscal year 2027 begins).

The mechanics of release appear on the statement of activities as a reclassification — shown as a decrease (an outflow, sometimes called "net assets released from restrictions") within the "with donor restrictions" column and a corresponding increase (an inflow) within the "without donor restrictions" column, with the two amounts netting to zero across the organization as a whole. This reclassification is not itself revenue or expense — the original contribution revenue was already recognized when the gift was received (assuming it was an unconditional promise); the release simply moves the net assets between restriction categories to reflect that the restriction has now been satisfied. The actual expense for the program activity is recognized separately, generally within "without donor restrictions" as the program expenses are incurred, following the normal expense recognition process described in functional expense classification.

A common point of confusion is the timing relationship between recognizing a restricted contribution, recognizing the related expense, and releasing the restriction. If a donor's restricted gift is received in one fiscal year but the qualifying expenses aren't incurred until a later year, the contribution revenue is recognized (within "with donor restrictions") in the year received, while the release — and the corresponding expense — occurs in the later year when the funds are actually spent for the specified purpose. This can create a temporary "imbalance" where an organization shows a surplus within "with donor restrictions" in the year of receipt (revenue recognized, no offsetting release yet) and then a corresponding net decrease in a later year when the restriction is released and the expense is recognized.

For organizations with multiple restricted funds and grants, tracking releases requires careful record-keeping — typically maintained outside the general ledger in supporting schedules tracking each gift's original amount, cumulative releases to date, and remaining restricted balance — particularly important when an organization has many overlapping restricted funds for similar purposes, requiring judgment about which grant's restriction is released by which expenditures.`,
    quiz: [
      {
        q: 'What event triggers the "release" of a purpose restriction on donor-restricted net assets?',
        choices: [
          'The organization receives the gift, before any expenses are incurred',
          'The organization incurs expenses that satisfy the specific purpose the donor specified for the gift',
          'The organization\'s fiscal year ends, regardless of how the funds were used',
          'The donor passes away'
        ],
        correct: 1,
        explanation: 'A purpose restriction is released when the organization incurs qualifying expenses for the specific purpose the donor designated, at which point the related net assets are reclassified from "with donor restrictions" to "without donor restrictions."'
      },
      {
        q: 'On the statement of activities, how does the release of a donor restriction appear?',
        choices: [
          'As new revenue recognized for the first time',
          'As a reclassification — a decrease in "with donor restrictions" and a corresponding increase in "without donor restrictions," netting to zero overall',
          'As an expense reported only once at the end of the organization\'s existence',
          'It does not appear anywhere in the financial statements'
        ],
        correct: 1,
        explanation: 'The release is shown as a reclassification between net asset categories — a decrease in "with donor restrictions" matched by an equal increase in "without donor restrictions" — reflecting that the restriction has been satisfied, not as new revenue.'
      }
    ]
  },
  {
    id: 'program-service-revenue',
    title: 'Program Service Revenue and Exchange Transactions',
    body: `While contributions and grants represent a major revenue source for many non-profits, many organizations also generate "program service revenue" — fees charged for services that further the organization's mission, such as tuition at a non-profit school, ticket sales for a museum or performing arts organization, fees for counseling services at a community health center, or membership-based access to facilities like a YMCA. Understanding how this revenue is accounted for, and how it differs from contributions, is essential to interpreting a non-profit's statement of activities.

The key distinction is whether a transaction is a "contribution" (a nonreciprocal transfer, where the donor receives no direct commensurate benefit in exchange) or an "exchange transaction" (where both parties receive and give up something of approximately equal value — the organization provides a good or service, and the payer receives that good or service in return). Program service revenue from exchange transactions is accounted for under the general revenue recognition framework (ASC 606), the same standard that applies to for-profit companies — recognizing revenue when (or as) the organization satisfies its performance obligations to the customer, such as when tuition revenue is recognized over the academic term as educational services are provided, or ticket revenue is recognized when the performance occurs.

This is a fundamentally different recognition pattern from contributions, which (for unconditional promises) are generally recognized immediately upon the donor's unconditional commitment, regardless of when the related program activities will occur. The distinction matters significantly for understanding the timing of an organization's reported revenue relative to its actual program delivery.

Many transactions sit in a gray area requiring judgment to classify. Government grants and contracts are a particularly important example — a government grant to provide services to a specific population might be structured as a contribution (if the government receives no direct, commensurate benefit and is essentially "donating" to support the organization's mission for the public's benefit) or as an exchange transaction (if the government is effectively "purchasing" services for itself or specified beneficiaries and receiving value directly comparable to the payment, similar to a contract). The classification affects not just the timing of revenue recognition but also which accounting standard applies (ASC 606 for exchanges, ASC 958 contribution guidance for nonreciprocal transfers).

Membership dues present another classification challenge: dues that primarily provide the member with tangible benefits of value roughly commensurate with the dues paid (such as free admission, discounts, or publications with significant value) are more likely exchange transactions, recognized over the membership period as benefits are provided, while dues that are largely symbolic support for the organization's mission, with only nominal benefits to the member, may be treated substantially as contributions.

For financial statement users, distinguishing program service revenue from contribution revenue helps clarify an organization's reliance on "earned" revenue (which the organization controls more directly through its own operations and pricing decisions) versus its reliance on philanthropic support (which depends on donor relationships and fundraising effectiveness) — two very different revenue models with different risk profiles and sustainability considerations.`,
    quiz: [
      {
        q: 'What is the key distinction between a "contribution" and an "exchange transaction" for a non-profit?',
        choices: [
          'Contributions are always larger in dollar amount than exchange transactions',
          'In an exchange transaction, both parties give and receive approximately equal value; a contribution is a nonreciprocal transfer where the donor receives no commensurate benefit',
          'Exchange transactions can only occur with government entities',
          'There is no meaningful distinction between the two for accounting purposes'
        ],
        correct: 1,
        explanation: 'A contribution is a nonreciprocal transfer — the donor gives without receiving commensurate value in return. An exchange transaction involves both parties exchanging approximately equal value, such as a fee paid for a service received, and is accounted for under ASC 606.'
      },
      {
        q: 'How does the revenue recognition pattern for program service revenue (an exchange transaction) typically differ from that of an unconditional contribution?',
        choices: [
          'They are recognized identically in all cases',
          'Program service revenue is generally recognized as the organization satisfies performance obligations (e.g., as services are delivered), while unconditional contributions are generally recognized immediately upon the donor\'s commitment, regardless of when related activities occur',
          'Program service revenue can never be recognized under any circumstances',
          'Contributions are recognized only when the organization spends the money'
        ],
        correct: 1,
        explanation: 'Exchange transaction revenue follows ASC 606, recognized as performance obligations are satisfied (e.g., over the period a service is delivered). Unconditional contributions are generally recognized immediately upon the donor\'s unconditional commitment, which can create a very different timing pattern.'
      }
    ]
  },
  {
    id: 'special-event-revenue',
    title: 'Accounting for Special Event Revenue',
    body: `Special events — galas, auctions, charity walks, golf tournaments — are a common fundraising tool for non-profits, but they present accounting complexities because a single event often generates revenue from multiple sources that must be classified and reported differently.

When a donor pays for a ticket to a special event such as a gala dinner, the payment often contains two components: a portion that represents payment for tangible benefits received (the fair value of the dinner, entertainment, or other goods/services provided) and a portion that represents a contribution (the excess of what the donor paid over the fair value of what they received). For example, if a gala ticket costs $250 and the fair value of the dinner and entertainment provided is estimated at $75, then $75 is treated as exchange-transaction revenue (special event revenue) and $175 is treated as a contribution.

This split matters for both financial reporting and donor communications — organizations are generally required (under IRS rules, for tax-deductibility purposes) to inform donors of the deductible portion of their payment, which corresponds to the amount exceeding the fair value of benefits received (the $175 in the example above would be the donor's tax-deductible amount, while the $75 fair-value portion is not deductible since the donor received something of value in exchange).

Auction proceeds at special events follow similar logic: if a donor successfully bids $500 for an item with a fair market value of $200, $200 is treated as exchange revenue (or in some presentations, as revenue from the sale of donated goods) and $300 as a contribution. Items donated for the auction by businesses or individuals are themselves often recorded as in-kind contributions at their fair value when received, and then as the item is "sold" through the auction, the organization may recognize both the contribution revenue from the item itself and the additional contribution from any amount the winning bidder pays above fair value.

On the statement of activities, special event revenue is sometimes presented on a gross basis (showing total special event revenue, with direct costs of the event — catering, venue rental, entertainment — shown as a separate expense line, often within fundraising expenses) versus a net basis (showing only the net proceeds from the event). Generally accepted practice favors gross presentation for the primary special event revenue and related direct costs, providing more transparency about both the scale of fundraising activity and its associated costs — net presentation can obscure how efficient (or inefficient) an event was at generating net proceeds relative to its costs.

For an organization's board and management, special event accounting also feeds into important management decisions: tracking the direct costs of an event against the gross revenue generated allows calculation of a "cost to raise a dollar" metric for that specific event, which can inform decisions about whether to continue, modify, or discontinue particular fundraising events in future years — some long-running events may generate significant community goodwill and donor engagement even if their direct net financial return is modest, a consideration that pure financial metrics don't fully capture.`,
    quiz: [
      {
        q: 'If a donor pays $300 for a gala ticket and the fair value of the dinner and entertainment they receive is $90, how is this payment typically split for accounting and tax purposes?',
        choices: [
          'The entire $300 is treated as a tax-deductible contribution',
          '$90 is treated as exchange-transaction revenue (payment for value received) and $210 is treated as a contribution (and the tax-deductible portion)',
          'The entire $300 is treated as exchange revenue with no contribution component',
          'The payment cannot be split and must be returned to the donor'
        ],
        correct: 1,
        explanation: 'The portion of the payment equal to the fair value of benefits received ($90) is treated as exchange revenue (and is not tax-deductible), while the excess ($210) is treated as a contribution and is the donor\'s tax-deductible amount.'
      },
      {
        q: 'Why is "gross presentation" of special event revenue and related direct costs generally favored over "net presentation"?',
        choices: [
          'Gross presentation is required to be hidden from donors',
          'Gross presentation provides more transparency about both the scale of fundraising activity and the costs associated with it, which net presentation can obscure',
          'Net presentation always results in higher reported revenue',
          'There is no difference between gross and net presentation'
        ],
        correct: 1,
        explanation: 'Showing total special event revenue separately from its direct costs (gross presentation) gives financial statement users a clearer picture of both the fundraising activity\'s scale and its efficiency, which can be hidden if only net proceeds are shown.'
      }
    ]
  },
  {
    id: 'membership-dues-accounting',
    title: 'Accounting for Membership Dues',
    body: `Many non-profit organizations — professional associations, museums, advocacy groups, religious congregations — rely on membership dues as a significant revenue source. The accounting treatment of membership dues depends heavily on what members receive in exchange for their payment, echoing the contribution-versus-exchange-transaction distinction discussed in the program service revenue article.

When membership provides significant tangible benefits roughly commensurate with the dues paid — for example, a professional association whose annual dues include a subscription to a journal, access to a member directory, discounted conference registration, and other services with meaningful value — the dues are generally treated as an exchange transaction. Under this treatment, dues revenue is recognized over the membership period (typically the year the membership covers), reflecting that the organization is providing ongoing services or access throughout that period — similar to how a magazine subscription is recognized over the subscription term rather than entirely when payment is received.

When membership provides only nominal benefits — a newsletter of minimal value, a member decal, or primarily the satisfaction of supporting the organization's mission — the dues payment is more akin to a contribution, and may be recognized substantially upon receipt (subject to the unconditional promise recognition principles discussed in fund accounting basics), similar to any other unrestricted contribution.

In practice, many membership structures contain elements of both, and organizations must use judgment — sometimes formalized through an analysis of the fair value of member benefits relative to the total dues charged — to determine the appropriate split, similar to the special event revenue analysis. An organization might determine that $40 of a $100 annual membership represents the fair value of a quarterly publication and other tangible benefits (recognized as exchange revenue over the year), while the remaining $60 represents a contribution (recognized upon receipt, assuming no other restrictions apply).

A practical accounting challenge with membership dues is the treatment of "deferred revenue" for the exchange-transaction portion: if dues are collected in advance for a membership period that spans the organization's fiscal year-end (for example, dues collected in October for a membership running through the following September), the portion of dues relating to the upcoming fiscal year must be deferred (recorded as a liability — deferred revenue or unearned revenue) and recognized as revenue only as that future period's services are provided, rather than recognized entirely in the year cash was received.

Lifetime memberships present a particularly interesting case — a single payment intended to cover benefits (however nominal) for the remainder of a member's life. Organizations typically recognize lifetime membership revenue over an estimated average remaining membership period (based on actuarial or historical data about member longevity and retention) rather than immediately, reflecting the ongoing obligation to provide member benefits over an extended, if uncertain, future period — though if the benefits provided are nominal, a contribution-like immediate recognition approach may be more appropriate, again requiring judgment based on the specific facts.`,
    quiz: [
      {
        q: 'When membership dues provide significant tangible benefits roughly commensurate with the amount paid, how is the revenue typically recognized?',
        choices: [
          'Entirely as a contribution upon receipt, regardless of when benefits are provided',
          'As an exchange transaction, recognized over the membership period as services and benefits are provided',
          'Never recognized as revenue under any circumstances',
          'Only recognized if the member attends every event offered'
        ],
        correct: 1,
        explanation: 'When dues correspond to tangible benefits of comparable value, the arrangement is treated as an exchange transaction, with revenue recognized over the membership period as the organization provides the associated services and access.'
      },
      {
        q: 'If a non-profit collects annual membership dues in October for a membership period running through the following September, and its fiscal year ends December 31, what must happen to the portion of dues relating to January through September of the next year?',
        choices: [
          'It must be recognized entirely as revenue in the year cash was received, with no deferral',
          'It must be deferred as a liability (deferred/unearned revenue) and recognized as revenue as that future period\'s services are provided',
          'It must be returned to the member immediately',
          'It has no effect on the financial statements at all'
        ],
        correct: 1,
        explanation: 'The portion of dues relating to the membership period after fiscal year-end represents an obligation to provide future benefits and must be recorded as deferred (unearned) revenue, recognized as revenue in the future period as those benefits are provided.'
      }
    ]
  },
  {
    id: 'related-organizations-np',
    title: 'Related Organizations and Affiliated Entities',
    body: `Non-profit organizations frequently operate alongside related entities — separately incorporated affiliates, supporting organizations, foundations, or chapters — and understanding how these relationships affect financial reporting is important for anyone analyzing a non-profit's complete financial picture, since a single organization's standalone financial statements may not tell the whole story.

A common structure involves a "supporting organization" — frequently a separately incorporated foundation established specifically to raise and manage funds (particularly endowment and major gift funds) for the benefit of an operating non-profit, such as a university foundation that holds and invests endowment funds on behalf of a public university, or a hospital foundation that fundraises for a hospital. These structures are often used for governance, liability, tax, or donor-relations reasons — for example, separating investment management activities from operational activities, or providing donors with a dedicated entity focused specifically on fundraising and stewardship.

Whether a related organization's financial activity should be consolidated into the primary organization's financial statements depends on accounting standards regarding control. For non-profits, ASC 958-810 (and related guidance) addresses when a non-profit must consolidate a related entity — generally requiring consolidation when the reporting organization has both control (typically through a majority voting interest in the related entity's board) and an economic interest in the related entity, though specific rules apply to different types of relationships, including situations involving "financially interrelated" organizations where consolidation may be required even without majority board control, based on the nature of the relationship.

When consolidation isn't required, related organizations are typically disclosed in the notes to financial statements, describing the nature of the relationship, any significant transactions between the organizations (such as the operating organization receiving distributions from the foundation's investment earnings, or shared staff and facilities with cost allocations between the entities), and amounts due to or from the related organization.

For users analyzing a non-profit's financial health — particularly its available resources — understanding the related-organization landscape is crucial. An operating non-profit's own balance sheet might show relatively modest net assets, while a separately incorporated foundation holds a large endowment whose investment earnings are distributed to support the operating organization's programs — in this case, looking only at the operating entity's financial statements without considering the foundation's resources (and the operating entity's economic interest in those resources, even if not consolidated) could significantly understate the overall financial resources supporting the organization's mission.

Chapter and national/local affiliate relationships present similar analytical challenges — a national organization's consolidated financial statements might include or exclude local chapters depending on their legal structure and the degree of control the national organization exercises, and donors or grantors evaluating "the organization" may need to clarify exactly which legal entity (or combination of entities) they're actually examining.`,
    quiz: [
      {
        q: 'Why might a university establish a separately incorporated "foundation" to hold and manage its endowment?',
        choices: [
          'Because endowments are illegal for universities to hold directly under any circumstances',
          'For reasons such as governance, liability separation, donor relations, or focused investment management — a common structural arrangement for fundraising and endowment management',
          'Because foundations are required to have zero assets',
          'Because it eliminates the need for any financial reporting'
        ],
        correct: 1,
        explanation: 'Separately incorporated supporting foundations are commonly used for governance, liability separation, donor stewardship, and dedicated investment management purposes, holding and investing funds on behalf of the related operating organization.'
      },
      {
        q: 'Why is it important for someone analyzing a non-profit\'s financial health to consider related organizations, even if they aren\'t consolidated into the primary entity\'s financial statements?',
        choices: [
          'Related organizations are never relevant to financial analysis',
          'A related foundation might hold significant resources (like an endowment) that support the operating organization\'s mission, and ignoring this could understate the overall financial resources available',
          'Related organizations always have identical financial statements to the primary entity',
          'Consolidation is always required, so this is never an issue in practice'
        ],
        correct: 1,
        explanation: 'If significant resources are held by a related but non-consolidated entity (such as an endowment foundation), looking only at the primary organization\'s standalone financial statements could significantly understate the total financial resources supporting its operations and mission.'
      }
    ]
  },
  {
    id: 'np-mergers-affiliations',
    title: 'Non-Profit Mergers and Affiliations',
    body: `Non-profit organizations, like their for-profit counterparts, sometimes combine through mergers, acquisitions, or affiliations — often driven by financial pressures, a desire for operational efficiencies, mission alignment, or strategic positioning within a sector (mergers among hospitals, social service agencies, and arts organizations have all been common in recent years). U.S. GAAP (ASC 958-805) provides specific guidance for accounting for these combinations, distinguishing between "mergers" and "acquisitions" in ways that differ somewhat from the for-profit business combination framework.

A "merger" under this guidance occurs when two (or more) organizations combine to form a new reporting entity, with neither party identified as the "acquirer" — typically evidenced by a new, unified governing body, and neither organization's management or board dominating the combined entity. Mergers are accounted for using the "carryover method," in which the combined entity's assets and liabilities are recorded at the carrying amounts (book values) from the predecessor organizations' financial statements — no new "fair value" measurements are made, similar in concept to how a pooling-of-interests transaction (no longer permitted for for-profit business combinations) would have been accounted for.

An "acquisition" occurs when one organization (the acquirer) obtains control over another (the acquiree), with the acquirer's identity clearly established — for example, a larger organization absorbing a smaller one, which ceases to exist as a separate entity, with the acquirer's board and management continuing. Acquisitions are accounted for using the "acquisition method," similar to for-profit business combinations: the acquirer recognizes the identifiable assets acquired and liabilities assumed at their fair values as of the acquisition date, and if the fair value of consideration given (if any — many non-profit acquisitions involve no purchase price, as the "acquired" organization simply combines into the acquirer) plus any noncontrolling interest exceeds the fair value of identifiable net assets acquired, the excess is recognized as goodwill. Conversely, if identifiable net assets exceed consideration paid (often the case when no consideration changes hands, often called an "inherent contribution"), the excess is generally recognized as a contribution received (revenue) by the acquirer rather than as a bargain purchase gain.

The distinction between merger and acquisition accounting can produce materially different financial statement outcomes for economically similar combinations — the carryover method (mergers) avoids the complexity and subjectivity of fair value measurements and goodwill recognition, while the acquisition method (acquisitions) can result in significant goodwill or "inherent contribution" revenue depending on the relationship between fair values and carrying values of the combining organizations.

Beyond formal mergers and acquisitions, many non-profits enter into less formal "affiliations" — joint operating agreements, shared services, or governance affiliations — that create varying degrees of operational and financial interdependence, requiring analysis of whether and how these relationships should be reflected in financial statements, including potential consolidation.

For boards considering a combination, accounting treatment is one of many considerations — but it can have real consequences for how the combined entity's financial statements appear to funders, lenders, and rating agencies afterward, making it an important part of due diligence and planning.`,
    quiz: [
      {
        q: 'Under ASC 958-805, what distinguishes a "merger" from an "acquisition" for non-profit organizations?',
        choices: [
          'A merger always involves a cash payment, while an acquisition never does',
          'In a merger, two organizations combine to form a new entity with no acquirer identified (using carryover/book values); in an acquisition, one organization obtains control over another (using fair values, the acquisition method)',
          'There is no distinction; both terms mean exactly the same thing',
          'Mergers can only occur between for-profit companies'
        ],
        correct: 1,
        explanation: 'A merger involves combining into a new entity with neither party as acquirer, accounted for using carryover (book) values. An acquisition involves one organization gaining control of another, accounted for using fair values under the acquisition method.'
      },
      {
        q: 'In a non-profit acquisition where no consideration changes hands and the fair value of identifiable net assets acquired exceeds zero, how is the excess typically treated?',
        choices: [
          'It is ignored and not recorded anywhere',
          'It is generally recognized as a contribution received (revenue) by the acquirer, often called an "inherent contribution"',
          'It must always be recorded as goodwill regardless of the direction of the difference',
          'It is recorded as a reduction to the acquirer\'s retained earnings'
        ],
        correct: 1,
        explanation: 'When identifiable net assets acquired exceed any consideration paid (common in non-profit combinations with no purchase price), the excess is generally recognized as contribution revenue (an "inherent contribution") by the acquiring organization, rather than as a bargain purchase gain.'
      }
    ]
  },
  {
    id: 'lobbying-political-activity',
    title: 'Lobbying, Political Activity, and Tax-Exempt Status',
    body: `Tax-exempt status under Section 501(c)(3) of the Internal Revenue Code — the category covering most charitable, educational, and religious organizations — comes with significant restrictions on lobbying and political activity, and understanding these restrictions (and how related costs are tracked and reported) is important both for compliance and for the financial reporting implications.

Political campaign activity is subject to an absolute prohibition for 501(c)(3) organizations: they may not participate in, or intervene in, any political campaign on behalf of (or in opposition to) any candidate for public office. This is a bright-line rule with essentially no exceptions — violating it can jeopardize an organization's entire tax-exempt status, regardless of the amount of resources involved. This contrasts with lobbying, which is restricted but not entirely prohibited.

Lobbying — attempting to influence specific legislation — is permitted for 501(c)(3) organizations, but only as an "insubstantial" part of their overall activities. What counts as "insubstantial" is determined either under a vague "facts and circumstances" test (the default rule, which provides little certainty) or, for organizations that make a specific election under Section 501(h) (the "h election"), under more objective expenditure-based limits — generally a sliding-scale percentage of the organization's total exempt-purpose expenditures, with separate (lower) limits for "grassroots lobbying" (attempting to influence legislation by encouraging the public to contact legislators) versus "direct lobbying" (direct contact with legislators or their staff).

For organizations that make the 501(h) election, tracking and reporting lobbying expenditures becomes a specific accounting requirement — the organization must track expenditures related to lobbying activities separately, and report them on Form 990 (specifically, organizations making the 501(h) election file Schedule C). This requires an allocation methodology for situations where staff time and other resources are used partly for lobbying and partly for other activities — similar in concept to the functional expense allocation challenges discussed elsewhere, but specifically focused on identifying the lobbying-related portion.

A related but distinct issue involves 501(c)(3) organizations' relationships with affiliated 501(c)(4) organizations (social welfare organizations, which face less restrictive lobbying limits and can engage in limited political activity, though not as their primary purpose). Some organizations establish a 501(c)(4) affiliate specifically to conduct lobbying or advocacy activities that would be problematic for the 501(c)(3) entity, with careful attention to ensuring that 501(c)(3) resources (which are tax-deductible to donors) aren't used to subsidize the 501(c)(4)'s activities — requiring clear cost allocation, separate bank accounts, and often formal cost-sharing agreements between the related entities.

The financial reporting implications of these rules are mostly indirect — lobbying expenditures themselves are generally legitimate program or supporting service expenses for financial statement purposes (assuming they don't violate the substantiality limits) — but the tracking and disclosure requirements on Form 990, and the potential consequences of exceeding limits (which can include excise taxes on excess lobbying expenditures, or in extreme cases, loss of tax-exempt status), make this an area requiring careful internal controls and documentation.`,
    quiz: [
      {
        q: 'How does the rule on political campaign activity differ from the rule on lobbying for 501(c)(3) organizations?',
        choices: [
          'Both are completely prohibited with no exceptions',
          'Both are fully permitted with no restrictions',
          'Political campaign activity is absolutely prohibited with no exceptions, while lobbying is permitted as long as it remains an "insubstantial" part of the organization\'s activities (or stays within limits under a 501(h) election)',
          'Lobbying is absolutely prohibited while political campaign activity is fully allowed'
        ],
        correct: 2,
        explanation: '501(c)(3) organizations face an absolute, bright-line prohibition on political campaign intervention, but lobbying (attempting to influence legislation) is permitted as long as it remains insubstantial relative to overall activities, with more objective limits available under a 501(h) election.'
      },
      {
        q: 'What is the purpose of the Section 501(h) election available to 501(c)(3) organizations?',
        choices: [
          'It allows unlimited lobbying with no restrictions whatsoever',
          'It allows organizations to use more objective, expenditure-based limits on lobbying (rather than the vague "facts and circumstances" test) and requires tracking lobbying expenditures for reporting on Form 990 Schedule C',
          'It permanently revokes the organization\'s tax-exempt status',
          'It applies only to organizations with no employees'
        ],
        correct: 1,
        explanation: 'The 501(h) election replaces the vague "insubstantial" facts-and-circumstances test with more objective, expenditure-based percentage limits on lobbying, requiring organizations to track and report lobbying expenditures (on Schedule C of Form 990).'
      }
    ]
  },
  {
    id: 'nonprofit-investment-policy',
    title: 'Investment Policies and Spending Rules for Non-Profits',
    body: `Many non-profit organizations hold investment portfolios — endowments, reserve funds, or other long-term investments — and the governance and accounting around these investments involves both fiduciary considerations and specific accounting rules that differ in important ways from how individuals or for-profit companies might manage investments.

A foundational governance document is the investment policy statement (IPS), typically approved by the board (or a designated investment committee), which establishes the organization's investment objectives, risk tolerance, asset allocation targets, permissible and prohibited investments, rebalancing guidelines, and performance benchmarks. The IPS provides a framework intended to ensure investment decisions are made consistently and prudently over time, independent of short-term market fluctuations or the preferences of any individual board member, and provides a basis for evaluating investment managers' performance.

For endowment funds specifically, the Uniform Prudent Management of Institutional Funds Act (UPMIFA), adopted in some form by nearly all U.S. states, governs how organizations manage and spend from donor-restricted endowment funds. UPMIFA requires organizations to consider a list of factors when making decisions to spend or accumulate endowment funds, including the duration and preservation of the fund, the purposes of the organization and the fund, general economic conditions, the possible effects of inflation, the expected total return from income and appreciation of investments, other resources of the organization, and the investment policy of the organization. Importantly, UPMIFA generally allows organizations to spend from the appreciation of an endowment (not just traditional "income" like interest and dividends) as long as the spending is prudent — a shift from older "trust law" approaches that sometimes restricted spending to income only, preventing organizations from accessing endowment growth even when prudent.

A common practical implementation of UPMIFA's prudence standard is a "spending rate" policy — for example, an organization might adopt a policy of spending 4-5% of a trailing average (often a 3-year rolling average) of the endowment's fair value each year, regardless of the endowment's actual investment return in any single year. This smooths the impact of market volatility on the amount available for spending, providing more predictable annual support for programs while still preserving the endowment's long-term purchasing power (assuming the long-term average investment return exceeds the spending rate plus inflation).

A significant accounting consequence of UPMIFA relates to net asset classification (discussed in the net asset restrictions article): if an endowment's fair value falls below its original gift value (sometimes called being "underwater"), the deficiency was historically required to be classified within "without donor restrictions" net assets (since the original donor-restricted corpus had effectively been spent down below its required level), even though the underlying funds remained legally donor-restricted endowment funds — current guidance (ASU 2016-14) instead requires underwater endowment funds to remain classified within "with donor restrictions," but with enhanced disclosures about the original endowment gift amount, the current fair value, and the amount of the deficiency, along with the organization's policy on spending from underwater funds.

Boards overseeing non-profit investments must balance several considerations: near-term operational needs for spendable resources, the long-term goal of preserving the endowment's real purchasing power, the organization's overall risk tolerance, and compliance with donor restrictions and UPMIFA.`,
    quiz: [
      {
        q: 'What is a key feature of UPMIFA\'s approach to spending from donor-restricted endowment funds?',
        choices: [
          'It prohibits spending from endowments under any circumstances',
          'It generally allows organizations to spend from the appreciation (not just traditional income) of an endowment, as long as the spending decision is prudent considering specified factors',
          'It requires all endowment funds to be spent within one year of receipt',
          'It applies only to for-profit corporations'
        ],
        correct: 1,
        explanation: 'UPMIFA allows prudent spending from endowment appreciation, not just traditional income (interest and dividends), representing a shift from older trust law approaches and giving organizations more flexibility to access endowment growth when appropriate.'
      },
      {
        q: 'Under current guidance (ASU 2016-14), how should an "underwater" endowment fund (where fair value has fallen below the original gift amount) be classified?',
        choices: [
          'It must be reclassified entirely to "without donor restrictions"',
          'It remains classified within "with donor restrictions," with enhanced disclosures about the original gift amount, current fair value, and the deficiency',
          'It is removed from the financial statements entirely',
          'It must be immediately liquidated and returned to the donor'
        ],
        correct: 1,
        explanation: 'ASU 2016-14 requires underwater endowment funds to remain within "with donor restrictions" net assets (reflecting their continued legal restriction), but requires enhanced disclosures about the original gift amount, current fair value, the size of the deficiency, and the organization\'s spending policy for such funds.'
      }
    ]
  }
);
