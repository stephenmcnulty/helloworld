// ---------- GAAP Accounting (batch 3) ----------
FINANCE_ARTICLES.push(
  {
    id: 'property-plant-equipment',
    title: 'Accounting for Property, Plant, and Equipment',
    body: `Property, plant, and equipment (PP&E) — sometimes called fixed assets or capital assets — represents the long-lived tangible resources a company uses to operate its business: land, buildings, machinery, vehicles, and equipment. Accounting for PP&E involves several distinct steps over the life of the asset: initial recognition and measurement, depreciation over its useful life, subsequent expenditures, and eventual disposal.

When an asset is acquired, it's recorded at its historical cost — not just the purchase price, but all costs necessary to get the asset ready for its intended use. For a piece of manufacturing equipment, this includes the purchase price, sales taxes, shipping and delivery costs, installation costs, and any costs of testing the equipment before it's placed into service. For land, historical cost includes the purchase price plus costs like legal fees, title insurance, and any costs to prepare the land for use, such as grading or demolition of existing structures (though demolition costs for a building being removed to make way for new construction are sometimes treated differently depending on whether the building was acquired with the intent to demolish it).

Once in service, most PP&E (except land, which is not depreciated because it doesn't have a determinable useful life) is depreciated — its cost is systematically allocated as an expense over its estimated useful life, as discussed in the depreciation article. Management must estimate both the useful life and the salvage value (estimated residual value at the end of useful life), and these estimates can be revised if circumstances change, with the revision applied prospectively (affecting depreciation in current and future periods, not retroactively restating prior periods).

A key distinction in PP&E accounting is between capital expenditures and repairs/maintenance expenses. Costs that extend an asset's useful life, increase its capacity, or improve its efficiency are capitalized — added to the asset's cost and depreciated over time. Costs that simply maintain the asset in its normal operating condition — routine repairs, oil changes, minor part replacements — are expensed immediately as incurred. This distinction matters significantly for reported earnings: capitalizing a cost that should have been expensed inflates current-period income (by deferring the expense to future periods through depreciation) while expensing a cost that should have been capitalized understates current income but overstates future income — both represent departures from proper accounting that can be either innocent errors or, in more troubling cases, deliberate earnings manipulation.

When PP&E is disposed of — sold, scrapped, or exchanged — the company removes the asset's cost and accumulated depreciation from the books, and recognizes a gain or loss equal to the difference between any proceeds received and the asset's net book value (cost minus accumulated depreciation) at the time of disposal. If a fully depreciated asset (net book value of zero) is simply scrapped with no proceeds, no gain or loss is recognized — the asset is just removed from the books.

PP&E also requires ongoing assessment for impairment — situations where an asset's carrying value may no longer be recoverable, a topic covered in more depth in the discussion of impairment of long-lived assets.`,
    quiz: [
      {
        q: 'When a company purchases a piece of equipment, which of the following would typically be included in its capitalized cost?',
        choices: [
          'Only the sticker price of the equipment, with all other costs expensed immediately',
          'The purchase price, sales taxes, shipping, and installation/testing costs necessary to get the asset ready for its intended use',
          'The salaries of unrelated employees in other departments',
          'Future repair costs expected over the asset\'s entire life'
        ],
        correct: 1,
        explanation: 'Historical cost for PP&E includes all costs necessary to acquire the asset and prepare it for its intended use, including purchase price, taxes, delivery, and installation/testing — not just the base purchase price.'
      },
      {
        q: 'What is the key distinction between a capital expenditure and a repair/maintenance expense for PP&E?',
        choices: [
          'There is no distinction; all costs are always expensed immediately',
          'Capital expenditures extend useful life, increase capacity, or improve efficiency and are capitalized; routine repairs that maintain normal operating condition are expensed immediately',
          'Capital expenditures are always larger than $1,000,000',
          'Repair costs are always capitalized and depreciated over 40 years'
        ],
        correct: 1,
        explanation: 'Costs that improve, extend the life of, or increase the capacity of an asset are capitalized and depreciated over time, while costs that simply maintain the asset\'s existing condition are expensed as incurred.'
      }
    ]
  },
  {
    id: 'impairment-of-long-lived-assets',
    title: 'Impairment of Long-Lived Assets',
    body: `Impairment occurs when the carrying value of a long-lived asset on a company's balance sheet exceeds its recoverable amount — essentially, when an asset is "worth less" than the books currently show, and that decline is expected to be permanent rather than temporary. Under U.S. GAAP, the impairment test for long-lived assets held for use (like PP&E and finite-lived intangible assets) follows a specific two-step process.

The first step is a "recoverability test." A company compares the asset's (or asset group's) carrying value to the sum of the undiscounted future cash flows expected to result from its use and eventual disposal. If the carrying value is less than or equal to these undiscounted cash flows, the asset is considered recoverable, and no impairment is recorded — even if the asset's fair value happens to be lower than its carrying value. This step uses undiscounted cash flows specifically as a screening test to avoid requiring impairment for assets that will still generate enough cash over their remaining life to "earn back" their carrying value, even if that's spread over many years.

If the recoverability test fails — meaning the carrying value exceeds the undiscounted future cash flows — the company proceeds to the second step: measuring the impairment loss as the difference between the asset's carrying value and its fair value. Fair value is typically estimated using discounted cash flow analysis (using discounted, not undiscounted, cash flows at this stage) or, where available, market prices for similar assets.

Impairment testing for long-lived assets is generally only required when there are "triggering events" — indicators that an asset's value may have declined, such as a significant decrease in the asset's market price, a significant adverse change in how the asset is used or in the business climate, an accumulation of costs significantly exceeding the amount originally expected for the asset's acquisition or construction, or a current expectation that the asset will be sold or disposed of before the end of its previously estimated useful life. Absent such triggering events, companies are not required to test for impairment routinely.

This differs notably from the impairment testing required for goodwill and indefinite-lived intangible assets (discussed separately), which generally requires at least annual testing regardless of whether a triggering event has occurred, and which doesn't include the same undiscounted cash flow "recoverability" screening step — goodwill impairment is assessed by comparing carrying value directly to fair value.

Once an impairment loss is recognized for a long-lived asset under U.S. GAAP, the new, lower carrying value becomes the asset's new cost basis going forward, and — importantly — this write-down generally cannot be reversed even if the asset's value subsequently recovers. This is a notable contrast with International Financial Reporting Standards (IFRS), which permits reversal of impairment losses (except for goodwill) if conditions that caused the impairment no longer exist, one of several areas where U.S. GAAP and IFRS diverge on impairment accounting.`,
    quiz: [
      {
        q: 'In the first step of the U.S. GAAP long-lived asset impairment test (the recoverability test), what is the carrying value compared to?',
        choices: [
          'The asset\'s original purchase price only',
          'The sum of undiscounted future cash flows expected from the asset\'s use and eventual disposal',
          'The fair value of a completely unrelated asset',
          'The company\'s total revenue for the year'
        ],
        correct: 1,
        explanation: 'The recoverability test compares carrying value to undiscounted future cash flows. If carrying value is less than or equal to these cash flows, the asset is considered recoverable and no impairment is recorded at this stage, even if fair value is lower.'
      },
      {
        q: 'Under U.S. GAAP, once an impairment loss is recognized on a long-lived asset, can it later be reversed if the asset\'s value recovers?',
        choices: [
          'Yes, automatically and immediately',
          'No — under U.S. GAAP, impairment write-downs of long-lived assets generally cannot be reversed, unlike under IFRS',
          'Only if the company changes its auditor',
          'Reversal is required every five years regardless of value changes'
        ],
        correct: 1,
        explanation: 'U.S. GAAP generally prohibits reversing impairment losses on long-lived assets even if their value later recovers, establishing a new (lower) cost basis going forward. IFRS, by contrast, permits reversal (except for goodwill) under certain conditions.'
      }
    ]
  },
  {
    id: 'fair-value-measurement',
    title: 'Fair Value Measurement and the Fair Value Hierarchy',
    body: `Fair value is defined under U.S. GAAP (ASC 820) as "the price that would be received to sell an asset or paid to transfer a liability in an orderly transaction between market participants at the measurement date" — essentially, an exit price based on market participant assumptions, not necessarily what the holder paid or what they personally believe the asset is worth. Fair value measurement has become increasingly central to financial reporting as accounting standards have moved toward greater use of fair value for certain assets and liabilities, including many financial instruments, certain investments, and impairment assessments.

To bring consistency and comparability to fair value estimates — which can range from highly objective (an actively traded stock price) to highly subjective (an estimate of a private company's worth) — ASC 820 establishes a three-level fair value hierarchy based on the inputs used in the valuation.

Level 1 inputs are quoted prices in active markets for identical assets or liabilities that the company can access at the measurement date — the most reliable category. A share of stock in a large, publicly traded company, valued at its closing market price, is a Level 1 measurement.

Level 2 inputs are observable inputs other than quoted prices for identical assets, such as quoted prices for similar assets in active markets, quoted prices for identical or similar assets in markets that are not active, or other observable market data like interest rates, yield curves, and credit spreads that can be used in a valuation model. A corporate bond that doesn't trade frequently but can be valued using a model based on observable interest rate and credit spread data would typically be Level 2.

Level 3 inputs are unobservable inputs — used when relevant observable data isn't available, requiring the company to develop its own assumptions about what market participants would use, often based on the best information available in the circumstances, including the company's own data. Examples include valuations of private equity investments, certain complex derivatives, and goodwill or other assets measured using discounted cash flow models with significant unobservable assumptions about future growth rates or discount rates.

The hierarchy isn't a choice — companies must use the highest level of inputs available and reasonably obtainable; Level 3 isn't an option to be selected for convenience but reflects the reality that some assets simply lack observable market data. Companies are required to disclose which level each fair-valued item falls into, and for Level 3 items, additional disclosures about the valuation techniques and significant unobservable inputs used, along with a reconciliation of changes in Level 3 balances during the period.

For financial statement users, the fair value hierarchy serves as an important signal of measurement reliability — a balance sheet with significant Level 3 assets carries more estimation uncertainty than one dominated by Level 1 and Level 2 measurements, even though both are reported as "fair value" under the same accounting framework.`,
    quiz: [
      {
        q: 'A company holds shares of a large public company, valued at the stock\'s current closing market price. What level of the fair value hierarchy does this represent?',
        choices: [
          'Level 1, since it uses quoted prices in active markets for identical assets',
          'Level 2',
          'Level 3, since stock prices are always unobservable',
          'The fair value hierarchy does not apply to publicly traded stocks'
        ],
        correct: 0,
        explanation: 'Level 1 represents the highest-quality fair value inputs: quoted prices in active markets for identical assets, such as a publicly traded stock valued at its closing market price.'
      },
      {
        q: 'What characterizes Level 3 fair value measurements?',
        choices: [
          'They are always more accurate than Level 1 measurements',
          'They rely on unobservable inputs and the company\'s own assumptions, used when relevant observable market data is not available',
          'They can only be used for cash and cash equivalents',
          'They require no disclosure of valuation methods'
        ],
        correct: 1,
        explanation: 'Level 3 measurements rely on unobservable inputs developed by the company itself, used when observable market data isn\'t available — examples include certain private investments and assets valued using discounted cash flow models with significant unobservable assumptions.'
      }
    ]
  },
  {
    id: 'stock-based-compensation',
    title: 'Accounting for Stock-Based Compensation',
    body: `Stock-based compensation (SBC) refers to non-cash compensation that companies give employees in the form of equity — most commonly stock options and restricted stock units (RSUs) — and has become a major component of total compensation, particularly in the technology sector. Accounting for SBC under U.S. GAAP (ASC 718) requires companies to recognize the cost of these awards as compensation expense, based on their fair value at the time of grant.

For stock options, fair value is typically estimated using an option-pricing model such as Black-Scholes or a binomial/lattice model, which requires inputs including the current stock price, exercise price, expected volatility, expected term (how long employees are expected to hold the option before exercising), risk-free interest rate, and expected dividend yield. For restricted stock units, fair value is generally simply the stock price on the grant date (since RSUs, unlike options, have no exercise price — they convert to actual shares upon vesting).

Once fair value is determined at grant date, the total cost is recognized as compensation expense over the "requisite service period" — typically the vesting period, which is the time an employee must remain employed for the award to vest. For an award that vests over four years, the company would recognize roughly one-quarter of the total grant-date fair value as expense each year (using straight-line or graded-vesting attribution methods), regardless of how the stock price actually moves after the grant date — a key point: the fair value is "locked in" at grant date and is not subsequently adjusted for stock price changes (with certain narrow exceptions for awards with performance or market conditions).

If an employee leaves before their awards vest, the unvested awards are typically forfeited, and the company reverses any previously recognized compensation expense related to those forfeited awards (under the most common accounting policy election) — though companies can also elect to estimate forfeitures upfront and not true up later, an accounting policy choice that affects the timing but not the ultimate total expense recognized for awards that actually vest.

SBC expense is recorded on the income statement, typically allocated across expense categories based on where the recipient employees work (cost of revenue, research and development, sales and marketing, general and administrative) — meaning it reduces reported net income just like cash compensation. However, because it's a non-cash expense, it's added back in the cash flow statement's operating activities section when reconciling net income to cash flow from operations.

A frequent point of debate among investors and analysts is whether to exclude SBC when evaluating a company's profitability — some argue SBC should be added back because it's "non-cash," similar to how depreciation is sometimes added back, while others argue SBC represents a real economic cost (it dilutes existing shareholders, who bear the cost of new shares being issued to employees) and excluding it from profitability metrics like "adjusted EBITDA" can present an overly rosy picture of a company's true economics, particularly for companies that rely heavily on equity compensation to attract talent while reporting large net losses on a GAAP basis.`,
    quiz: [
      {
        q: 'When is the fair value of a stock option grant determined for expense recognition purposes under ASC 718?',
        choices: [
          'At the grant date, using an option-pricing model, and this value is generally not subsequently adjusted for later stock price changes',
          'At the date the option is exercised, based on the stock price at that time',
          'Every day until the option expires, with daily revaluation',
          'Fair value is never used for stock options'
        ],
        correct: 0,
        explanation: 'Stock option fair value is estimated at grant date using a model like Black-Scholes, and this grant-date fair value is generally "locked in" and recognized as expense over the vesting period without subsequent adjustment for stock price movements.'
      },
      {
        q: 'Why do some analysts argue against excluding stock-based compensation when evaluating a company\'s "adjusted" profitability?',
        choices: [
          'Because SBC has no effect on shareholders whatsoever',
          'Because SBC represents a real economic cost to existing shareholders through dilution, even though it is a non-cash expense',
          'Because SBC is illegal under GAAP',
          'Because companies are required to pay SBC in cash within 30 days'
        ],
        correct: 1,
        explanation: 'While SBC doesn\'t require a cash outlay, issuing new shares to employees dilutes existing shareholders\' ownership. Critics argue that excluding SBC from adjusted profitability metrics can overstate a company\'s true economic performance.'
      }
    ]
  },
  {
    id: 'pension-accounting',
    title: 'Pension Accounting: Defined Benefit vs. Defined Contribution',
    body: `Employer-sponsored retirement plans generally fall into two categories with very different accounting implications: defined contribution plans and defined benefit plans.

Defined contribution (DC) plans, such as 401(k) plans, are the simpler case from an accounting perspective. The employer commits to contributing a specified amount — often a percentage of employee salary or a matching contribution based on the employee's own contributions — into individual employee accounts. Once the contribution is made, the employer's obligation is satisfied; the employee bears the investment risk and reward for whatever happens to the account balance afterward. Accounting for DC plans is straightforward: the employer simply recognizes an expense equal to the contributions made (or owed) for the period.

Defined benefit (DB) plans, more common in older industries and the public sector (and increasingly rare for new hires in the private sector), promise employees a specified benefit at retirement — often based on a formula involving years of service and final or average salary — regardless of how the underlying pension plan assets perform. This shifts investment risk to the employer, who must ensure the plan has sufficient assets to pay promised benefits, potentially for decades after an employee retires.

Accounting for DB plans (ASC 715) is considerably more complex, requiring actuarial estimates of the present value of future benefit obligations (the "projected benefit obligation" or PBO), which depend on assumptions about discount rates, expected salary increases, employee turnover, mortality rates, and more. The plan's funded status — the difference between the fair value of plan assets and the PBO — is reported on the employer's balance sheet as either a net pension asset (if overfunded) or net pension liability (if underfunded).

Pension expense recognized in the income statement includes several components: service cost (the present value of benefits earned by employees during the current period), interest cost (the increase in the PBO due to the passage of time, since the obligation is a present value that grows as the payment date approaches), expected return on plan assets (a reduction to expense, reflecting the assumed investment earnings on plan assets), and amortization of certain deferred items, including actuarial gains/losses (differences between actual experience and previous assumptions) and prior service costs (the effect of plan amendments on the benefit obligation for past service).

A significant feature of DB pension accounting is that actuarial gains and losses — which can be substantial when actual investment returns or actuarial assumptions differ from expectations — are typically recorded initially in "other comprehensive income" rather than immediately flowing through net income, then gradually amortized into net income over time (often using a method that "corridors" small gains/losses to avoid excessive volatility in reported earnings from year-to-year market fluctuations).

The shift away from DB plans toward DC plans over recent decades reflects employers' desire to shed the long-term investment risk, funding volatility, and accounting complexity associated with DB plans, transferring that risk to employees in exchange for the simplicity and predictability of fixed periodic contributions.`,
    quiz: [
      {
        q: 'What is the key difference in risk allocation between defined contribution and defined benefit plans?',
        choices: [
          'In DC plans, the employee bears investment risk for their account; in DB plans, the employer bears investment risk because it must fund a promised benefit regardless of investment performance',
          'There is no difference; both shift all risk to the government',
          'In DB plans, employees choose their own promised benefit amount each year',
          'DC plans guarantee a fixed retirement income regardless of contributions'
        ],
        correct: 0,
        explanation: 'Defined contribution plans shift investment risk to employees, whose retirement income depends on account performance. Defined benefit plans place investment risk on the employer, who must ensure sufficient assets exist to pay a promised benefit formula regardless of how plan investments perform.'
      },
      {
        q: 'What is the "funded status" of a defined benefit pension plan, as reported on the employer\'s balance sheet?',
        choices: [
          'The total amount employees have personally contributed',
          'The difference between the fair value of plan assets and the projected benefit obligation (PBO), reported as a net pension asset or liability',
          'The number of employees enrolled in the plan',
          'The plan\'s expected return on assets for the next fiscal year only'
        ],
        correct: 1,
        explanation: 'Funded status equals plan assets (at fair value) minus the projected benefit obligation. A positive funded status (assets exceed PBO) is reported as a net pension asset, while a negative funded status (PBO exceeds assets) is reported as a net pension liability.'
      }
    ]
  },
  {
    id: 'foreign-currency-translation',
    title: 'Foreign Currency Translation in Financial Statements',
    body: `Many companies operate subsidiaries in countries that use currencies other than the parent company's reporting currency. To prepare consolidated financial statements, the financial statements of these foreign subsidiaries — originally prepared in their local currency — must be translated into the parent's reporting currency. U.S. GAAP (ASC 830) governs this process, distinguishing between a subsidiary's "functional currency" and the parent's "reporting currency."

The functional currency is the currency of the primary economic environment in which a subsidiary operates — generally the currency in which it primarily generates and spends cash. For a foreign subsidiary that operates largely independently, selling products and incurring costs in the local currency, the functional currency is typically the local currency. For a subsidiary that is essentially an extension of the parent's operations — for instance, a sales office that's financially integrated with the parent and conducts most transactions in the parent's currency — the functional currency might actually be the parent's currency.

When a subsidiary's functional currency is its local currency (the more common case), the "current rate method" is used to translate its financial statements: balance sheet items (assets and liabilities) are translated at the exchange rate in effect at the balance sheet date (the "current rate"), while income statement items are translated at the exchange rate in effect when the transactions occurred — often approximated using a weighted-average rate for the period for practical purposes. Equity accounts are generally translated at historical rates (the rates in effect when the equity was originally recorded).

This mixing of exchange rates at different dates creates an imbalance — the translated balance sheet won't automatically balance using these different rates. The "plug" that resolves this is the cumulative translation adjustment (CTA), recorded within accumulated other comprehensive income (a component of equity), not flowing through net income. This means that, under the current rate method, currency translation effects on a subsidiary's net assets bypass the income statement entirely — they only affect equity (through OCI) until the subsidiary is sold or substantially liquidated, at which point the cumulative translation adjustment is "released" and recognized in net income as part of any gain or loss on the sale.

If a subsidiary's functional currency is determined to be the parent's reporting currency (the less common "remeasurement" scenario), a different method — the "temporal method" — is used, where monetary assets and liabilities are remeasured at current rates, non-monetary items at historical rates, and the resulting gains/losses flow directly through net income rather than OCI, creating more income statement volatility from currency movements.

This distinction matters a great deal to financial statement users: a company with subsidiaries whose functional currency is local will show currency effects mainly in OCI and the cumulative translation adjustment within equity, with relatively muted income statement impact from currency swings, while a company using the temporal method will show more direct currency-related volatility in reported net income.`,
    quiz: [
      {
        q: 'Under the current rate method, how are balance sheet items (assets and liabilities) of a foreign subsidiary typically translated?',
        choices: [
          'At the exchange rate in effect when the company was first founded, never updated',
          'At the exchange rate in effect on the balance sheet date (the current rate)',
          'At a rate fixed by the parent company\'s board of directors regardless of actual exchange rates',
          'Balance sheet items are never translated, only income statement items'
        ],
        correct: 1,
        explanation: 'Under the current rate method, balance sheet items are translated at the exchange rate in effect at the balance sheet date, while income statement items use rates approximating those in effect when transactions occurred (often a period average).'
      },
      {
        q: 'Where does the cumulative translation adjustment (CTA) generally appear under the current rate method, and when does it affect net income?',
        choices: [
          'It immediately flows through net income every period',
          'It is recorded in accumulated other comprehensive income (within equity) and only affects net income when the subsidiary is sold or substantially liquidated',
          'It has no impact on the financial statements at all',
          'It is recorded as a liability that must be paid in cash annually'
        ],
        correct: 1,
        explanation: 'The CTA, which "balances" the translated financial statements due to using different exchange rates for different items, sits in accumulated other comprehensive income within equity and is only recognized in net income upon sale or substantial liquidation of the foreign subsidiary.'
      }
    ]
  },
  {
    id: 'segment-reporting',
    title: 'Segment Reporting Requirements',
    body: `Large, diversified companies often operate multiple distinct businesses — different product lines, geographic regions, or customer bases — that may have very different growth rates, margins, and risk profiles. Segment reporting (ASC 280 under U.S. GAAP) requires public companies to disclose certain financial information separately for significant operating segments, giving investors a more granular view than the consolidated totals alone would provide.

The foundational concept is the "operating segment" — a component of a company that engages in business activities from which it earns revenues and incurs expenses, whose operating results are regularly reviewed by the company's "chief operating decision maker" (CODM) — a role, not necessarily a specific job title, referring to whoever is responsible for allocating resources and assessing performance — and for which discrete financial information is available. This "management approach" is a deliberate design choice: rather than imposing a standardized definition of segments from the outside, GAAP requires companies to report segments based on how management itself actually organizes and evaluates the business internally, on the theory that this internal view is most relevant to investors trying to understand how the company is run.

Not every operating segment must be separately reported — only those meeting quantitative thresholds, generally: the segment's revenue (including intersegment sales) is 10% or more of combined revenue of all operating segments, the segment's profit or loss is 10% or more (in absolute value) of the greater of combined profits of profitable segments or combined losses of loss segments, or the segment's assets are 10% or more of combined assets of all segments. Segments not meeting these thresholds may still be reported if management believes the information would be useful, and there's an overall requirement that reportable segments must constitute at least 75% of total consolidated revenue — if they don't, additional segments must be identified as reportable even if they don't individually meet the 10% thresholds.

For each reportable segment, companies must disclose information about revenues (from external customers and intersegment), a measure of profit or loss (as reviewed by the CODM — which may not be a GAAP measure like operating income, but whatever profitability measure management actually uses internally), total assets, and several other items if included in the measure reviewed by the CODM, such as interest revenue/expense, depreciation and amortization, and significant non-cash items. A reconciliation of total segment revenues, profits, and assets to the corresponding consolidated totals must also be provided, along with certain geographic information (revenues and long-lived assets by country) and information about major customers (if a single customer represents 10% or more of total revenue).

Segment reporting has become an area of increased SEC scrutiny in recent years, particularly regarding whether companies are appropriately identifying their CODM and operating segments, and whether segment profit measures and the related expense categories disclosed provide investors with sufficient detail about how the CODM actually evaluates segment performance and allocates resources — recent updates to ASC 280 have specifically expanded required disclosures about significant segment expenses.`,
    quiz: [
      {
        q: 'What is the "management approach" underlying segment reporting requirements?',
        choices: [
          'Segments are defined entirely by government regulators with no input from the company',
          'Companies report segments based on how management itself organizes and internally evaluates the business, since this internal view is considered most relevant to investors',
          'All companies must use exactly the same three segments regardless of their business',
          'Segment reporting is entirely optional and voluntary'
        ],
        correct: 1,
        explanation: 'The management approach requires companies to define and report operating segments based on the internal structure used by the chief operating decision maker (CODM) to allocate resources and assess performance, rather than an externally imposed standard definition.'
      },
      {
        q: 'Which of the following is one of the quantitative thresholds that can trigger separate reporting of an operating segment?',
        choices: [
          'The segment has fewer than 5 employees',
          'The segment\'s revenue (including intersegment sales) is 10% or more of the combined revenue of all operating segments',
          'The segment was created more than 50 years ago',
          'The segment operates only in the company\'s home country'
        ],
        correct: 1,
        explanation: 'One of the 10% quantitative thresholds requires separate reporting if a segment\'s revenue (including intersegment sales) is 10% or more of the combined revenue of all operating segments; similar thresholds apply to profit/loss and assets.'
      }
    ]
  },
  {
    id: 'interim-financial-reporting',
    title: 'Interim Financial Reporting',
    body: `While annual financial statements (10-K filings for public companies) provide a comprehensive view of a company's financial position and performance for a full fiscal year, interim financial statements — most commonly quarterly reports (10-Q filings in the U.S.) — provide more timely, though less complete, financial information throughout the year. ASC 270 governs interim financial reporting under U.S. GAAP.

A central question in interim reporting is how to treat costs and revenues that don't align neatly with a single quarter. GAAP generally takes an "integral view" of interim periods — treating each interim period as an integral part of the annual period, rather than as a discrete standalone period. This means certain costs that benefit the entire year may be allocated across interim periods based on estimates of annual amounts, rather than recognized entirely in the quarter incurred. For example, if a company expects to pay an annual property tax bill in the fourth quarter but the tax relates to the use of the property throughout the year, an estimated portion of that expense might be recognized in each of the first three quarters, with the remainder in the fourth, so that each quarter bears its proportional share of the annual cost.

Income tax expense in interim periods presents particular complexity. Rather than calculating tax expense based solely on year-to-date income using the actual tax rate that would apply if the year ended at that point, companies generally estimate an "annual effective tax rate" — their best estimate of the tax rate that will apply to the full year's pretax income, considering all anticipated permanent differences, credits, and other items — and apply this estimated rate to year-to-date pretax income to determine year-to-date tax expense. As the year progresses and the estimate is refined, the annual effective tax rate may change, with the cumulative effect of any change recognized in the quarter the estimate changes — meaning interim tax expense for a single quarter can sometimes look unusual due to "catch-up" effects from revising the annual estimate.

Interim financial statements are typically unaudited (reviewed by auditors under a more limited set of procedures than a full audit), and they're permitted to omit certain disclosures that would be required in annual statements, on the theory that users have access to the most recent annual report and don't need every disclosure repeated each quarter — though significant changes since the last annual report must still be disclosed.

Seasonality is a particularly important consideration for users of interim financial statements. Many businesses have predictable seasonal patterns — a retailer's fourth quarter (including the holiday season) might represent a disproportionate share of annual revenue and profit, while a landscaping company might show losses in winter quarters. Comparing a seasonal company's results to the immediately preceding quarter can be highly misleading; year-over-year comparisons (comparing Q3 of this year to Q3 of last year) are generally more meaningful for seasonal businesses, and companies are encouraged (and for certain seasonal businesses, may be required) to disclose the seasonal nature of their operations.`,
    quiz: [
      {
        q: 'Under the "integral view" of interim reporting, how are certain annual costs sometimes treated?',
        choices: [
          'They must always be recognized entirely in the quarter the cash payment is made, regardless of when the cost is incurred',
          'They may be allocated across interim periods based on estimates of the annual amount, so each quarter bears its proportional share',
          'They are never recognized in any interim period, only in the annual report',
          'They must be recognized entirely in the first quarter of the year'
        ],
        correct: 1,
        explanation: 'The integral view treats interim periods as part of the annual period, allowing certain costs that benefit the full year to be allocated proportionally across quarters based on estimates, rather than recognized only when paid or incurred in a single quarter.'
      },
      {
        q: 'How is income tax expense generally determined for an interim period under U.S. GAAP?',
        choices: [
          'By applying an estimated annual effective tax rate to year-to-date pretax income, with adjustments in later quarters as the estimate is refined',
          'By assuming a 0% tax rate for all interim periods',
          'By using a randomly assigned tax rate each quarter',
          'Interim periods are never subject to income tax expense'
        ],
        correct: 0,
        explanation: 'Companies estimate an annual effective tax rate reflecting their best estimate for the full year and apply it to year-to-date pretax income. Revisions to this estimate during the year can create catch-up effects in later quarters\' reported tax expense.'
      }
    ]
  },
  {
    id: 'research-development-costs',
    title: 'Accounting for Research and Development Costs',
    body: `Research and development (R&D) costs present a unique accounting challenge: they represent investments intended to generate future economic benefits — new products, technologies, or processes — but the uncertainty surrounding whether those future benefits will actually materialize is often very high, especially in early research stages. U.S. GAAP (ASC 730) takes a notably conservative approach: with limited exceptions, all R&D costs are expensed as incurred, rather than capitalized as an asset.

This includes costs of materials, equipment, and facilities used in R&D activities (unless they have alternative future uses, in which case they may be capitalized as PP&E and depreciated, with the depreciation itself charged to R&D expense), salaries and related costs of personnel engaged in R&D, costs of services performed by others in connection with R&D (such as contract research), and a reasonable allocation of indirect costs related to R&D activities.

The rationale for immediate expensing is rooted in conservatism and the difficulty of reliably measuring future benefits at the time R&D costs are incurred — at the point a pharmaceutical company begins testing a new drug compound, for instance, it's highly uncertain whether that compound will ever become an approved, revenue-generating product, given the famously high failure rates in drug development. Rather than attempt to capitalize costs based on highly speculative future benefit assessments (which would be vulnerable to manipulation and inconsistency across companies), GAAP requires expensing, providing consistency and removing management discretion from this determination.

This treatment creates a notable divergence from software development costs, which (under separate guidance, ASC 985-20 for software to be sold and ASC 350-40 for internal-use software) can require capitalization of certain costs once "technological feasibility" (for software to be sold) or specific development-stage criteria (for internal-use software) are reached — recognizing that once a software product has reached a point where successful completion is reasonably assured, the remaining development costs more closely resemble an investment in an asset than ongoing research.

It's also worth noting the contrast with International Financial Reporting Standards (IFRS), which takes a different approach: IAS 38 requires research costs to be expensed (similar to U.S. GAAP), but development costs must be capitalized once specific criteria are met — including technical feasibility, intention and ability to complete and use or sell the asset, and ability to reliably measure the costs attributable to the asset during development. This means a company reporting under IFRS might capitalize costs that an otherwise-identical company reporting under U.S. GAAP would expense, leading to different reported R&D expense, total assets, and net income for economically similar activities — an important consideration when comparing financial statements prepared under the two frameworks.

The conservative U.S. GAAP treatment means that companies with significant R&D investment — biotech, pharmaceutical, and technology companies — often show reduced current-period profitability (or losses) reflecting the full cost of R&D investment, even though the hoped-for benefits of that R&D may not materialize as revenue for years, if ever, creating a potential mismatch between when costs are recognized and when (if ever) related benefits are recognized.`,
    quiz: [
      {
        q: 'Under U.S. GAAP (ASC 730), how are most research and development costs treated?',
        choices: [
          'They are capitalized as an intangible asset and amortized over 20 years',
          'They are expensed as incurred, with limited exceptions',
          'They are deducted directly from retained earnings without affecting net income',
          'They are recorded as a reduction to revenue'
        ],
        correct: 1,
        explanation: 'U.S. GAAP requires R&D costs to be expensed as incurred in nearly all cases, reflecting the conservative view that future benefits from R&D are too uncertain to reliably support capitalization as an asset.'
      },
      {
        q: 'How does IFRS (IAS 38) differ from U.S. GAAP in its treatment of R&D costs?',
        choices: [
          'IFRS prohibits any R&D spending entirely',
          'IFRS requires research costs to be expensed (similar to U.S. GAAP), but requires development costs to be capitalized once specific feasibility and other criteria are met',
          'IFRS requires all R&D costs, including basic research, to be capitalized immediately',
          'There is no difference between IFRS and U.S. GAAP for R&D costs'
        ],
        correct: 1,
        explanation: 'IFRS expenses research costs similar to U.S. GAAP, but requires capitalization of development costs once criteria such as technical feasibility and intent/ability to complete and use or sell the resulting asset are met — a notable divergence from U.S. GAAP\'s blanket expensing approach.'
      }
    ]
  }
);
