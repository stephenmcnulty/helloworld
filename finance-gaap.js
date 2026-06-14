// ---------- GAAP Accounting (batch 1) ----------
FINANCE_ARTICLES.push(
  {
    id: 'revenue-recognition-asc606',
    title: 'Revenue Recognition Under ASC 606',
    body: `ASC 606, "Revenue from Contracts with Customers," is the converged revenue recognition standard adopted by U.S. GAAP (and mirrored internationally by IFRS 15). It replaced a patchwork of industry-specific rules with a single principles-based framework built around a five-step model.

Step one is to identify the contract with a customer — an agreement that creates enforceable rights and obligations. Step two is to identify the performance obligations, which are the distinct promises to transfer goods or services. A single contract can contain multiple performance obligations; for example, a software contract might bundle a license, implementation services, and ongoing support, each potentially recognized differently.

Step three is to determine the transaction price — the amount the company expects to be entitled to in exchange for the goods or services, which can involve estimating variable consideration like discounts, rebates, or performance bonuses. Step four is to allocate that transaction price among the separate performance obligations, typically based on each obligation's standalone selling price. Step five is to recognize revenue as (or when) each performance obligation is satisfied — either over time (as a service is performed) or at a point in time (when control of a good transfers to the customer).

The "over time vs. point in time" distinction is one of the most consequential judgments under ASC 606. A long-term construction contract might recognize revenue over time as work progresses, using a measure of progress like costs incurred to date relative to total estimated costs. A retail sale, by contrast, recognizes revenue at the point in time when the customer takes control of the goods — typically at delivery.

ASC 606 also introduced more rigorous guidance on variable consideration, requiring companies to estimate amounts like returns, refunds, and rebates and include them in the transaction price only to the extent it's "probable" that a significant reversal won't occur later — a constraint designed to prevent companies from recognizing overly optimistic revenue too early.

For accountants, the practical impact has been most significant in industries with complex, multi-element arrangements — software, telecommunications, construction, and licensing — where the timing and pattern of revenue recognition can shift meaningfully compared to prior rules, even when the underlying economics of a contract haven't changed at all.`,
    quiz: [
      {
        q: 'Under the ASC 606 five-step model, what is a "performance obligation"?',
        choices: [
          'The total cash a customer must pay under the contract',
          'A distinct promise within a contract to transfer a good or service to the customer',
          'The tax owed on a transaction',
          'The discount rate used to value the contract'
        ],
        correct: 1,
        explanation: 'A performance obligation is each distinct good or service (or bundle) a company has promised to deliver. Revenue is recognized separately for each performance obligation as it is satisfied, which is why identifying them correctly is step two of the model.'
      },
      {
        q: 'How does ASC 606 determine whether revenue should be recognized "over time" versus "at a point in time"?',
        choices: [
          'Revenue is always recognized at the point of cash collection',
          'It depends on whether control of the good or service transfers to the customer gradually over the contract term or at a single moment',
          'Companies can choose either method freely each year',
          'It depends only on the contract\'s total dollar value'
        ],
        correct: 1,
        explanation: 'If the customer obtains control of the asset as it is created (e.g., a long-term construction project), revenue is recognized over time based on progress. If control transfers all at once (e.g., a retail sale at delivery), revenue is recognized at that point in time.'
      }
    ]
  },
  {
    id: 'lease-accounting-asc842',
    title: 'Lease Accounting Under ASC 842',
    body: `ASC 842 fundamentally changed how leases appear on a company's financial statements. Under the prior standard, operating leases were largely kept off the balance sheet, disclosed only in footnotes — meaning two companies with identical real-world obligations could look very different on paper depending on whether they leased or owned their assets.

Under ASC 842, lessees must recognize a "right-of-use" (ROU) asset and a corresponding lease liability on the balance sheet for nearly all leases with terms longer than 12 months. The lease liability is measured as the present value of future lease payments, discounted using the rate implicit in the lease or, more commonly, the lessee's incremental borrowing rate. The ROU asset is generally initially measured at the same amount as the liability, adjusted for items like prepaid rent or lease incentives.

ASC 842 retains a distinction between finance leases (formerly called capital leases) and operating leases, but the key change is that both now appear on the balance sheet. The difference shows up in the income statement and cash flow presentation. For finance leases, the ROU asset is amortized separately from the lease liability, and interest expense is recognized on the liability — similar to how a purchased asset financed with debt would be treated, resulting in front-loaded expense recognition. For operating leases, the company instead recognizes a single, typically straight-line lease expense over the term, with the ROU asset amortization calculated as a "plug" to achieve that straight-line pattern.

This distinction matters for EBITDA and other metrics: finance lease expense includes interest (often excluded from EBITDA) and amortization (added back to EBITDA), while operating lease expense is typically treated as a single operating cost embedded in EBITDA. As a result, a shift between lease classifications — or a shift in how companies structure new leases — can meaningfully affect reported EBITDA even without any change in actual cash payments.

The standard also affects financial ratios broadly. Because ROU assets and lease liabilities now appear on the balance sheet, metrics like return on assets, debt-to-equity, and various leverage ratios changed for companies with significant operating lease portfolios — retailers, airlines, and restaurant chains were among those most affected — even though the underlying economics of their lease arrangements were unchanged. Analysts and lenders had to adjust historical comparisons and loan covenants to account for this shift.`,
    quiz: [
      {
        q: 'What is the most significant change ASC 842 introduced compared to the prior leases standard?',
        choices: [
          'Leases are no longer allowed under GAAP',
          'Operating leases must now generally be recognized on the balance sheet as a right-of-use asset and lease liability',
          'All leases must now be classified as finance leases',
          'Lease payments are no longer tax-deductible'
        ],
        correct: 1,
        explanation: 'Previously, operating leases were kept off the balance sheet and disclosed only in footnotes. ASC 842 requires lessees to record a right-of-use asset and lease liability for nearly all leases over 12 months, bringing these obligations onto the balance sheet.'
      },
      {
        q: 'How does the expense pattern differ between a finance lease and an operating lease under ASC 842?',
        choices: [
          'There is no difference; both are expensed identically',
          'Finance leases separate interest and amortization (often front-loading expense), while operating leases typically result in a single straight-line expense',
          'Operating leases are never expensed',
          'Finance leases are expensed only at the end of the lease term'
        ],
        correct: 1,
        explanation: 'Finance leases recognize interest expense on the liability plus amortization of the ROU asset, similar to debt-financed asset ownership, which front-loads expense. Operating leases instead produce a single lease expense recognized evenly (straight-line) over the term.'
      }
    ]
  },
  {
    id: 'inventory-valuation-methods',
    title: 'Inventory Valuation: FIFO, LIFO, and Weighted Average',
    body: `When a company buys or produces inventory at different costs over time, it must choose a method to determine which costs flow to the income statement as cost of goods sold (COGS) and which remain on the balance sheet as ending inventory. The three primary methods under U.S. GAAP are First-In, First-Out (FIFO), Last-In, First-Out (LIFO), and weighted-average cost.

FIFO assumes the oldest inventory costs are the first to be recognized as COGS when goods are sold, leaving the most recently incurred costs in ending inventory. During periods of rising prices (inflation), FIFO results in lower COGS (using older, cheaper costs) and therefore higher reported gross profit and net income, while ending inventory on the balance sheet reflects more current, higher costs.

LIFO assumes the most recently incurred costs are the first to be recognized as COGS, leaving older costs in ending inventory. During inflation, LIFO results in higher COGS (using newer, more expensive costs), lower reported gross profit, and lower taxable income — a tax advantage that's the primary reason companies adopt LIFO in the U.S. However, this also means ending inventory on the balance sheet can reflect costs from years or even decades ago, understating its current value. Importantly, LIFO is permitted under U.S. GAAP but is prohibited under IFRS, creating a significant difference for companies that report under both frameworks.

Weighted-average cost calculates a single average cost per unit by dividing total cost of goods available for sale by total units available, applying that average to both COGS and ending inventory. It smooths out price fluctuations and is simpler to apply, especially for businesses with large volumes of similar, interchangeable inventory items (commodities, for example).

A key concept tied to LIFO is the "LIFO reserve" — the difference between what inventory would be valued at under FIFO versus LIFO. Companies using LIFO are required to disclose this reserve, which analysts use to adjust LIFO-based financial statements to a FIFO-equivalent basis for comparison with companies using different methods. The "LIFO conformity rule" also requires that if a company uses LIFO for tax purposes, it must also use LIFO for financial reporting — preventing companies from claiming the tax benefit while reporting higher profits to shareholders.

Choice of method is not just an accounting technicality — it affects tax bills, reported profitability, key ratios like inventory turnover, and comparability between companies, making it one of the most consequential judgment calls a company makes about its financial statements.`,
    quiz: [
      {
        q: 'During a period of rising prices, how does LIFO typically affect a company\'s reported net income and taxes compared to FIFO?',
        choices: [
          'LIFO results in higher net income and higher taxes',
          'LIFO results in higher COGS, lower net income, and lower taxes',
          'LIFO has no effect on net income or taxes',
          'LIFO is not permitted under any accounting framework'
        ],
        correct: 1,
        explanation: 'LIFO matches the most recent (higher, during inflation) costs against revenue, increasing COGS and reducing reported profit and taxable income — which is why companies often adopt LIFO specifically for its tax benefits during inflationary periods.'
      },
      {
        q: 'Which inventory valuation method is permitted under U.S. GAAP but prohibited under IFRS?',
        choices: [
          'FIFO',
          'Weighted-average cost',
          'LIFO',
          'Specific identification'
        ],
        correct: 2,
        explanation: 'LIFO is allowed under U.S. GAAP, subject to the LIFO conformity rule, but IFRS does not permit its use — a key difference companies must address when reconciling financial statements between the two frameworks.'
      }
    ]
  },
  {
    id: 'allowance-doubtful-accounts',
    title: 'Accounts Receivable and the Allowance for Doubtful Accounts',
    body: `When a company sells goods or services on credit, it records an account receivable — an asset representing the right to collect cash in the future. But not every customer pays. GAAP requires companies to estimate and record an "allowance for doubtful accounts" (also called allowance for credit losses) to present receivables at their net realizable value — the amount the company actually expects to collect.

The allowance is a contra-asset account that reduces gross accounts receivable to arrive at "net accounts receivable" on the balance sheet. When a company estimates that some portion of receivables won't be collected, it records bad debt expense (an income statement charge) and increases the allowance (a balance sheet contra-asset) by a corresponding amount. When a specific account is later confirmed uncollectible, the company writes it off by reducing both the allowance and the gross receivable — this write-off doesn't affect the income statement again, since the expense was already recognized when the allowance was established.

Under the current expected credit loss (CECL) model established by ASC 326, companies must estimate expected credit losses over the entire life of a receivable at the time it's recognized, based on historical experience, current conditions, and reasonable, supportable forecasts of future conditions. This is a forward-looking approach, a shift from the prior "incurred loss" model, which generally required a loss event to have already occurred (or be probable) before a reserve could be recorded.

Common estimation techniques include the percentage-of-sales method (applying a historical bad-debt percentage to current credit sales) and the aging-of-receivables method (applying different loss percentages to receivables based on how long they've been outstanding — a 90-day-past-due balance is far more likely to go uncollected than a 10-day balance).

The allowance is inherently an estimate, which makes it an area auditors scrutinize closely — management has some discretion in setting assumptions, and overly conservative or overly optimistic allowances can be used to manage reported earnings. A sudden, unexplained change in the allowance percentage from one period to the next is often a red flag warranting closer examination, since it could indicate either a genuine change in customer credit quality or an attempt to smooth earnings.`,
    quiz: [
      {
        q: 'What is the purpose of the allowance for doubtful accounts?',
        choices: [
          'To increase the reported value of accounts receivable',
          'To present accounts receivable at the net amount the company actually expects to collect',
          'To record cash received from customers',
          'To eliminate the need for bad debt expense'
        ],
        correct: 1,
        explanation: 'The allowance is a contra-asset that reduces gross receivables to their net realizable value, reflecting the reality that some customers will not pay. It ensures the balance sheet doesn\'t overstate the cash a company expects to collect.'
      },
      {
        q: 'When a specific customer account is written off as uncollectible after an allowance has already been established, what is the effect on the income statement?',
        choices: [
          'A new bad debt expense is recognized at the time of write-off',
          'There is no additional income statement impact, since the expense was already recognized when the allowance was set up',
          'Revenue is reversed',
          'The write-off increases net income'
        ],
        correct: 1,
        explanation: 'The write-off simply reduces both the gross receivable and the allowance by the same amount — it\'s a balance sheet reclassification. The expense impact was already captured earlier when the allowance was established through bad debt expense.'
      }
    ]
  },
  {
    id: 'goodwill-impairment',
    title: 'Goodwill and Impairment Testing',
    body: `Goodwill arises in an acquisition when the purchase price paid for a company exceeds the fair value of its identifiable net assets (assets minus liabilities, each measured at fair value). It represents intangible value — things like brand reputation, customer relationships, assembled workforce, and expected synergies — that can't be separately identified and valued on their own.

Unlike most assets, goodwill is not amortized under U.S. GAAP. Instead, it's tested for impairment at least annually (and more frequently if a "triggering event" occurs, such as a significant decline in stock price, loss of a key customer, or an economic downturn affecting the business). This reflects the view that goodwill doesn't necessarily decline in value in a predictable, systematic way the way a piece of equipment wears out.

The impairment test is performed at the "reporting unit" level — a component of the business for which discrete financial information is available and that management regularly reviews. A company compares the fair value of the reporting unit to its carrying value (including goodwill). If the carrying value exceeds fair value, an impairment loss is recognized for the difference, up to the amount of goodwill allocated to that unit. Goodwill impairment losses cannot later be reversed, even if the reporting unit's value recovers — a key asymmetry compared to some other asset impairments.

Determining fair value of a reporting unit typically involves either a market approach (comparing to similar publicly traded companies) or an income approach (a discounted cash flow analysis using a discount rate derived from something like the WACC). Because these inputs involve significant judgment — projected cash flows, discount rates, terminal growth rates — goodwill impairment testing is one of the most subjective and heavily audited areas of financial reporting.

Goodwill impairment charges can be large and sudden, often triggered by macroeconomic shocks, industry disruption, or simply the realization that an acquisition didn't deliver the value originally anticipated. Because impairment is a non-cash charge, it doesn't directly affect cash flow — but it can significantly affect reported net income, and large impairments are sometimes viewed by analysts as a tacit admission that management overpaid for a prior acquisition.

Private companies and certain not-for-profit entities have the option under GAAP to amortize goodwill over a period of up to ten years instead of performing annual impairment testing, a simplification intended to reduce the cost and complexity of compliance for smaller organizations.`,
    quiz: [
      {
        q: 'How is goodwill typically treated under U.S. GAAP for a public company?',
        choices: [
          'It is amortized evenly over 40 years',
          'It is not amortized but is tested at least annually for impairment',
          'It is immediately expensed when an acquisition occurs',
          'It is reclassified as a liability after five years'
        ],
        correct: 1,
        explanation: 'Public companies do not amortize goodwill. Instead, they test it for impairment at least annually, and more often if a triggering event occurs, comparing the reporting unit\'s fair value to its carrying value.'
      },
      {
        q: 'If a reporting unit\'s fair value recovers after a goodwill impairment loss was previously recognized, what happens to the previously recorded impairment?',
        choices: [
          'It is automatically reversed in the next period',
          'It cannot be reversed — goodwill impairment losses are permanent under GAAP',
          'It is moved to a separate "recovered goodwill" account',
          'It offsets future depreciation expense'
        ],
        correct: 1,
        explanation: 'Goodwill impairment losses are not reversible under U.S. GAAP, even if the underlying business later recovers in value — this is a notable asymmetry compared to the treatment of some other long-lived assets.'
      }
    ]
  },
  {
    id: 'deferred-taxes',
    title: 'Deferred Tax Assets and Liabilities',
    body: `Deferred taxes arise because the rules for computing income under GAAP (used for financial reporting) often differ from the rules for computing taxable income under the tax code (used for filing tax returns). These "temporary differences" mean a company's reported book income and taxable income diverge in a given year, but the difference is expected to reverse in future periods — creating deferred tax assets (DTAs) or deferred tax liabilities (DTLs).

A deferred tax liability arises when a company recognizes less tax expense now but more later — typically because it's deducting more for tax purposes today than for book purposes, deferring the tax payment. The classic example is depreciation: many companies use accelerated depreciation methods (like MACRS) for tax purposes, which front-load deductions, while using straight-line depreciation for GAAP, which spreads deductions evenly. In early years, tax depreciation exceeds book depreciation, so taxable income is lower than book income — creating a DTL that will reverse in later years when book depreciation exceeds tax depreciation.

A deferred tax asset arises in the opposite situation — when a company will get a tax benefit in the future for something it has already recognized as an expense for book purposes. Common examples include warranty reserves (expensed for books when estimated, but deductible for tax only when actually paid), net operating loss carryforwards (losses that can offset future taxable income), and the allowance for doubtful accounts (bad debt expense recognized for books before the specific write-off is deductible for tax).

A critical aspect of deferred tax assets is the "valuation allowance." GAAP requires a company to assess whether it's "more likely than not" that a deferred tax asset will actually be realized — meaning the company will generate enough future taxable income to use it. If realization is in doubt (for example, a company with a history of losses and uncertain future profitability), a valuation allowance must be recorded to reduce the DTA to the amount expected to be realized, with the offsetting entry increasing tax expense.

Changes in tax law can also have an immediate and sometimes dramatic effect on deferred tax balances. When a corporate tax rate changes, all existing deferred tax assets and liabilities must be remeasured at the new rate, which can create a one-time gain or loss in the period the law is enacted — even though no cash has changed hands. This is why major tax legislation often produces large, headline-grabbing one-time charges or benefits in companies' quarterly earnings.`,
    quiz: [
      {
        q: 'What causes a company to record a deferred tax liability related to depreciation?',
        choices: [
          'Using accelerated depreciation for tax purposes while using straight-line depreciation for GAAP, which front-loads tax deductions relative to book expense',
          'Paying cash taxes earlier than book taxes',
          'Recording more depreciation for GAAP than allowed for tax purposes',
          'Eliminating depreciation entirely for tax purposes'
        ],
        correct: 0,
        explanation: 'Accelerated tax depreciation reduces taxable income (and current taxes paid) more than book depreciation reduces book income in early years, deferring the tax liability to later years when the relationship reverses.'
      },
      {
        q: 'When is a company required to record a valuation allowance against a deferred tax asset?',
        choices: [
          'Whenever any deferred tax asset exists',
          'When it is more likely than not that the DTA will not be realized due to insufficient expected future taxable income',
          'Only when the company has no deferred tax liabilities',
          'Valuation allowances are never required under GAAP'
        ],
        correct: 1,
        explanation: 'GAAP requires a valuation allowance when it\'s more likely than not (greater than 50% probability) that some or all of a deferred tax asset won\'t be realized, reducing the asset to its expected realizable amount and increasing tax expense.'
      }
    ]
  },
  {
    id: 'contingent-liabilities',
    title: 'Contingent Liabilities and ASC 450',
    body: `A contingent liability is a potential obligation that depends on the outcome of a future event — a lawsuit, a product warranty claim, a government investigation. ASC 450, "Contingencies," provides the GAAP framework for determining how and when these uncertain obligations should be reflected in financial statements.

ASC 450 establishes a three-tier probability framework. If a loss is "probable" (likely to occur) and the amount can be "reasonably estimated," the company must accrue a liability and recognize an expense for the estimated amount. If a loss is "reasonably possible" (more than remote but less than probable) — or if it's probable but the amount can't be reasonably estimated — the company doesn't record a liability but must disclose the nature of the contingency and an estimate of the possible loss (or range) in the footnotes. If a loss is "remote" (slight chance of occurring), generally no accrual or disclosure is required at all.

This framework requires significant judgment, especially in litigation. Companies work closely with legal counsel to assess the likelihood of an unfavorable outcome and estimate potential damages — but disclosing too much detail about a weak legal position could itself be used against the company in court, creating tension between transparency for investors and litigation strategy. As a result, contingency disclosures are often written in carefully calibrated, conservative language.

When a range of loss is reasonably estimable but no single amount within the range is more likely than any other, GAAP requires accruing the minimum amount in the range (while disclosing the full range in the footnotes). This differs from a single best estimate approach and is a frequently tested concept because it's counterintuitive — many people assume the midpoint of a range should be used.

Contingent gains, by contrast, are treated very differently — and far more conservatively. Even if a favorable outcome (such as winning a lawsuit and receiving a settlement) is probable, GAAP generally prohibits recognizing a contingent gain until it is realized or realization is virtually certain. This asymmetry — conservative treatment of potential losses, even more conservative treatment of potential gains — reflects the broader principle of conservatism that has historically influenced GAAP, even as the framework has moved toward more principles-based standards in other areas.

Common examples accountants encounter include pending litigation, product warranty obligations, environmental remediation liabilities, and guarantees of third-party debt — each requiring this same probability-and-estimability analysis.`,
    quiz: [
      {
        q: 'Under ASC 450, when must a company accrue a liability for a contingent loss?',
        choices: [
          'Whenever any lawsuit is filed against the company',
          'When the loss is probable AND the amount can be reasonably estimated',
          'Only after the loss has actually been paid in cash',
          'Whenever the loss is remote'
        ],
        correct: 1,
        explanation: 'Accrual is required only when both conditions are met: the loss must be probable (likely to occur), and the amount must be reasonably estimable. If only one condition is met, disclosure rather than accrual is typically required.'
      },
      {
        q: 'If a loss is probable and reasonably estimable within a range, with no amount in the range more likely than any other, what amount should be accrued?',
        choices: [
          'The maximum amount in the range',
          'The midpoint of the range',
          'The minimum amount in the range, with the full range disclosed in footnotes',
          'No accrual should be made; only disclosure is required'
        ],
        correct: 2,
        explanation: 'When no point estimate within a range is better than any other, GAAP requires accruing the minimum amount of the range while disclosing the nature of the contingency and the full range of possible loss in the footnotes.'
      }
    ]
  },
  {
    id: 'statement-of-stockholders-equity',
    title: 'The Statement of Stockholders\' Equity',
    body: `The statement of stockholders' equity (sometimes called the statement of changes in equity) is one of the core financial statements required under GAAP, even though it often gets less attention than the balance sheet, income statement, and cash flow statement. It explains how each component of equity changed from the beginning to the end of the reporting period.

The statement is typically organized as a grid, with columns for each major equity component — common stock (at par value), additional paid-in capital, retained earnings, treasury stock, and accumulated other comprehensive income (AOCI) — and rows representing the events that changed each balance during the period.

Net income for the period flows into retained earnings, increasing it (a net loss decreases it). Dividends declared reduce retained earnings, regardless of whether they've been paid in cash yet. Stock issuances increase common stock and additional paid-in capital — common stock increases by the par value of shares issued, while the excess of the issuance price over par value goes to additional paid-in capital. Stock buybacks increase treasury stock, a contra-equity account that reduces total equity, recorded at the cost the company paid to repurchase its own shares.

Other comprehensive income (OCI) items — such as unrealized gains and losses on certain investment securities, foreign currency translation adjustments, and certain pension plan adjustments — bypass the income statement and flow directly into AOCI, a component of equity. This is an important distinction: these items affect equity and are part of "comprehensive income," but they don't appear in net income or affect retained earnings (until realized, in some cases).

Stock-based compensation expense also flows through this statement: as employees earn stock options or restricted stock units, the company recognizes compensation expense (reducing net income and thus retained earnings indirectly) while simultaneously increasing additional paid-in capital — recognizing that the company is, in effect, paying employees with equity rather than cash.

For an accountant or analyst, the statement of stockholders' equity is often the best place to spot unusual activity that might not be obvious elsewhere — large buyback programs, significant new share issuances (which dilute existing shareholders), or swings in AOCI that hint at foreign currency exposure or investment portfolio volatility that hasn't yet hit the income statement.`,
    quiz: [
      {
        q: 'When a company declares a cash dividend, what is the immediate effect on the statement of stockholders\' equity?',
        choices: [
          'Common stock increases',
          'Retained earnings decreases, even before the dividend is paid in cash',
          'Treasury stock decreases',
          'There is no effect until the dividend is paid'
        ],
        correct: 1,
        explanation: 'Declaring a dividend creates an obligation that immediately reduces retained earnings, with a corresponding increase in dividends payable (a liability). The cash effect occurs later when the dividend is actually paid.'
      },
      {
        q: 'How do unrealized gains on certain investment securities typically affect the financial statements?',
        choices: [
          'They increase net income directly',
          'They flow into accumulated other comprehensive income (AOCI), affecting equity without passing through net income',
          'They have no impact on any financial statement',
          'They are recorded as a liability'
        ],
        correct: 1,
        explanation: 'Certain unrealized gains and losses bypass the income statement and are recorded in other comprehensive income, accumulating in AOCI — a component of equity — rather than directly affecting net income or retained earnings.'
      }
    ]
  },
  {
    id: 'intangible-assets',
    title: 'Intangible Assets: Recognition and Amortization',
    body: `Intangible assets are non-physical assets that provide future economic benefit — patents, trademarks, copyrights, customer lists, licensing agreements, and proprietary technology, among others. GAAP draws an important distinction in how intangibles are treated based on whether they're internally developed or acquired, and whether they have a finite or indefinite useful life.

Internally developed intangibles present one of the more counterintuitive areas of GAAP: most costs to internally develop intangible assets — including nearly all research and development costs — must be expensed as incurred rather than capitalized. The rationale is that the future benefit of R&D is too uncertain at the time costs are incurred to justify recording an asset. This means a company that spends heavily on R&D to build valuable technology may show that technology nowhere on its balance sheet, even though it could be the company's most valuable resource.

Acquired intangibles are treated very differently. When a company acquires another business, GAAP requires identifying and separately valuing intangible assets acquired — customer relationships, brand names, technology, non-compete agreements — at fair value as of the acquisition date, with any residual recorded as goodwill. This is why two companies with economically similar internally-developed technology can show vastly different balance sheets simply because one built its technology in-house while the other acquired it.

For intangibles with a finite useful life (like a patent with a fixed legal term, or a customer relationship expected to generate benefits for a defined period), the asset is amortized — its cost is systematically allocated to expense over its useful life, similar to depreciation for tangible assets. The amortization method should reflect the pattern in which the asset's economic benefits are consumed; straight-line is common when no better pattern can be determined.

Intangibles with an indefinite useful life — most notably goodwill, but also certain trademarks or licenses that can be renewed indefinitely at minimal cost — are not amortized. Instead, like goodwill, they're tested for impairment at least annually. If at some point an indefinite-lived intangible is determined to have a finite life after all (say, a trademark the company decides to discontinue), it would then begin being amortized over its remaining useful life going forward.

One narrow exception to the "expense R&D" rule involves certain costs for internally developed software intended for sale or internal use, which can be capitalized once the project reaches "technological feasibility" — though even this carve-out is applied conservatively and only to costs incurred after that milestone.`,
    quiz: [
      {
        q: 'How does GAAP generally treat costs for internally developed research and development?',
        choices: [
          'Capitalized and amortized over 20 years',
          'Expensed as incurred, because future benefits are too uncertain to justify capitalization',
          'Recorded directly as goodwill',
          'Treated as a reduction to revenue'
        ],
        correct: 1,
        explanation: 'Nearly all R&D costs must be expensed as incurred under GAAP, reflecting the uncertainty of future economic benefit at the time the costs are spent — even though successful R&D can create substantial real economic value.'
      },
      {
        q: 'How are intangible assets with an indefinite useful life, such as certain trademarks, typically accounted for?',
        choices: [
          'Amortized over 40 years',
          'Expensed immediately upon acquisition',
          'Not amortized, but tested at least annually for impairment, similar to goodwill',
          'Reclassified as inventory'
        ],
        correct: 2,
        explanation: 'Indefinite-lived intangibles are not systematically amortized because there is no foreseeable limit to the period over which they are expected to generate benefits. Instead, they are subject to periodic impairment testing.'
      }
    ]
  },
  {
    id: 'accrual-vs-cash-basis',
    title: 'Accrual Accounting vs. Cash-Basis Accounting',
    body: `The choice between accrual-basis and cash-basis accounting determines when revenues and expenses are recognized in the financial records — and it's one of the most fundamental distinctions in all of accounting.

Under cash-basis accounting, revenue is recorded only when cash is received, and expenses are recorded only when cash is paid. It's simple and intuitive — the books mirror the bank account — which is why many very small businesses and individuals use it. But it can paint a misleading picture of financial performance: a company could look highly profitable in a month simply because it collected a large payment for work done over the prior six months, or look unprofitable because it prepaid a year's worth of insurance in a single month.

Under accrual-basis accounting, revenue is recorded when it's earned (regardless of when cash is received) and expenses are recorded when they're incurred (regardless of when cash is paid) — this is the "matching principle" in action, pairing revenues with the expenses incurred to generate them in the same period. GAAP requires accrual-basis accounting for all but the smallest entities, because it's considered to provide a much more accurate picture of a company's economic performance during a period.

Accrual accounting introduces several balance sheet accounts that don't exist under pure cash accounting: accounts receivable (revenue earned but not yet collected), accounts payable (expenses incurred but not yet paid), accrued expenses (like wages earned by employees but not yet paid as of period-end), prepaid expenses (cash paid in advance for future benefits, like insurance), and unearned/deferred revenue (cash received for goods or services not yet delivered).

The difference between accrual-basis net income and cash flow is precisely what the statement of cash flows reconciles, particularly in the operating activities section, which starts with net income and adjusts for non-cash items and changes in working capital accounts to arrive at cash flow from operations.

For tax purposes, many small businesses are permitted to use cash-basis accounting (subject to revenue thresholds and entity type restrictions under the tax code), even while larger or public companies must use accrual accounting for both tax and financial reporting. This divergence is itself a source of some of the book-tax differences that create deferred tax assets and liabilities discussed elsewhere — a business might report income on an accrual basis for GAAP purposes while using a different method for its tax return, subject to the specific rules governing each.`,
    quiz: [
      {
        q: 'Under accrual-basis accounting, when is revenue recorded?',
        choices: [
          'Only when cash is received from the customer',
          'When it is earned, regardless of when cash is received',
          'At the end of the fiscal year only',
          'Only when the customer\'s invoice is paid in full'
        ],
        correct: 1,
        explanation: 'Accrual accounting records revenue when it is earned (typically when goods or services are delivered), creating an account receivable if cash hasn\'t yet been collected — this better matches revenue to the period in which the related work was performed.'
      },
      {
        q: 'Which balance sheet account arises specifically because a company received cash before delivering the related goods or services?',
        choices: [
          'Accounts receivable',
          'Prepaid expenses',
          'Unearned (deferred) revenue',
          'Accumulated depreciation'
        ],
        correct: 2,
        explanation: 'Unearned revenue is a liability representing an obligation to deliver goods or services in the future in exchange for cash already received. It is reduced and converted to revenue as the company fulfills that obligation.'
      }
    ]
  }
);
