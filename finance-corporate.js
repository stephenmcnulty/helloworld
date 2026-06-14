// ---------- Corporate Finance (batch 1) ----------
FINANCE_ARTICLES.push(
  {
    id: 'wacc',
    title: 'The Weighted Average Cost of Capital',
    body: `Every company funds itself with a mix of debt and equity, and each source has a cost. The Weighted Average Cost of Capital, or WACC, blends those costs into a single rate that represents the minimum return a company must earn on its investments to satisfy everyone who provided capital.

The formula weights the cost of equity and the after-tax cost of debt by their proportion in the capital structure: WACC = (E/V × Re) + (D/V × Rd × (1 - Tc)), where E and D are the market values of equity and debt, V is their sum, Re is the cost of equity, Rd is the cost of debt, and Tc is the corporate tax rate.

Debt is multiplied by (1 - Tc) because interest payments are tax-deductible, creating a "tax shield" that lowers the effective cost of borrowing. Equity gets no such shield, since dividends are paid from after-tax profits. This is one reason debt is often cheaper than equity on paper, even though it carries the risk of fixed obligations.

WACC matters most as a discount rate. When a company evaluates a new project using net present value, it discounts future cash flows at the WACC. If the project's expected return exceeds the WACC, it should create value for shareholders; if not, it likely destroys value, even if it looks "profitable" on a simple income statement basis.

For an accountant, WACC also shows up in goodwill impairment testing, where the discount rate used to estimate a reporting unit's fair value is often derived from its WACC. A higher WACC means future cash flows are worth less today, which can trigger impairment charges even if a business's operations haven't changed.

Estimating the cost of equity usually relies on the Capital Asset Pricing Model, while the cost of debt can be approximated from a company's current bond yields or borrowing rate. Because market values of equity fluctuate daily, WACC is not a fixed number — it shifts with stock prices, interest rates, and capital structure decisions, which is why companies typically recalculate it periodically rather than treating it as a constant.`,
    quiz: [
      {
        q: 'Why is the cost of debt multiplied by (1 - tax rate) in the WACC formula?',
        choices: [
          'Because debt is always riskier than equity',
          'Because interest expense is tax-deductible, lowering its effective cost',
          'Because lenders require a discount for early repayment',
          'Because GAAP requires debt to be understated'
        ],
        correct: 1,
        explanation: 'Interest payments reduce taxable income, creating a "tax shield." The after-tax cost of debt reflects the true net cost to the company after accounting for the tax savings from deducting interest.'
      },
      {
        q: 'A company is evaluating a new project using NPV. What discount rate is most commonly used?',
        choices: [
          'The risk-free rate',
          'The company\'s WACC',
          'The prime lending rate',
          'The prior year\'s net profit margin'
        ],
        correct: 1,
        explanation: 'WACC represents the blended return required by all capital providers, so it serves as the hurdle rate: projects earning above WACC tend to create shareholder value, while those below it tend to destroy it.'
      }
    ]
  },
  {
    id: 'capital-structure',
    title: 'Capital Structure: Balancing Debt and Equity',
    body: `Capital structure refers to how a company finances its assets and operations — the mix of debt (loans, bonds) and equity (common stock, retained earnings) on the right side of the balance sheet. The choice between the two has major implications for risk, cost of capital, and control.

Debt has advantages: interest is tax-deductible, lenders don't get a vote in company decisions, and debt is typically cheaper than equity because lenders take less risk than shareholders (they get paid first in a liquidation and receive fixed payments). But debt also creates fixed obligations — interest and principal payments must be made regardless of how the business performs. Too much debt increases financial risk and can lead to default, bankruptcy, or restrictive loan covenants that limit management's flexibility.

Equity carries no mandatory repayment schedule, which gives a company breathing room during downturns. However, issuing new shares dilutes existing owners' stakes and can signal to the market that management believes the stock is overvalued. Equity is also more expensive than debt because shareholders demand higher returns to compensate for being last in line if the company fails.

The theoretical sweet spot is often discussed through the lens of the Modigliani-Miller theorem, which (under simplifying assumptions like no taxes or bankruptcy costs) argues that capital structure shouldn't affect firm value. In the real world, taxes and bankruptcy risk matter a great deal, so most finance theory points toward an "optimal" capital structure that balances the tax benefits of debt against the rising costs of financial distress as leverage increases.

Industries with stable, predictable cash flows — utilities, for example — can typically support more debt than industries with volatile revenues, like technology startups. An accountant analyzing a company's capital structure should look at the debt-to-equity ratio, interest coverage ratio, and how those compare to industry peers, since "too much" or "too little" debt is always relative to the nature of the business and its cash flow stability.`,
    quiz: [
      {
        q: 'Why is debt generally cheaper than equity as a source of financing?',
        choices: [
          'Because debt never has to be repaid',
          'Because lenders take on less risk than shareholders and interest is tax-deductible',
          'Because equity investors are guaranteed a fixed return',
          'Because debt does not appear on the balance sheet'
        ],
        correct: 1,
        explanation: 'Lenders are paid before shareholders in a liquidation and receive fixed, contractual payments, so they demand lower returns. The tax-deductibility of interest further lowers debt\'s effective cost compared to equity.'
      },
      {
        q: 'Which type of company can typically support a higher proportion of debt in its capital structure?',
        choices: [
          'A volatile early-stage technology startup',
          'A company with stable, predictable cash flows like a utility',
          'A company with no fixed assets',
          'A company that has never earned a profit'
        ],
        correct: 1,
        explanation: 'Stable cash flows make it easier to reliably cover fixed interest and principal payments, so companies like utilities can sustain higher leverage than businesses with unpredictable revenue.'
      }
    ]
  },
  {
    id: 'npv-capital-budgeting',
    title: 'Net Present Value and Capital Budgeting',
    body: `Capital budgeting is the process companies use to decide which long-term investments — new equipment, factories, product lines — are worth pursuing. The most widely respected tool for this is Net Present Value, or NPV.

NPV works by translating all future cash flows from a project into today's dollars, using a discount rate (often the WACC), and then subtracting the initial investment. The formula is: NPV = Σ [CFt / (1 + r)^t] - Initial Investment, where CFt is the cash flow in period t, r is the discount rate, and t is the time period.

The logic behind discounting is simple: a dollar received in five years is worth less than a dollar received today, because today's dollar can be invested and grow. By discounting future cash flows back to present value, NPV puts cash received at different times on a level, comparable footing.

The decision rule is straightforward: if NPV is positive, the project is expected to add value beyond the cost of capital and should generally be accepted. If NPV is negative, the project would destroy value and should be rejected. When comparing mutually exclusive projects, the one with the higher NPV is generally preferred, even if it has a lower percentage return, because NPV measures value created in dollar terms.

NPV's biggest strength is also its biggest challenge: it depends heavily on the accuracy of projected cash flows and the chosen discount rate. Small changes in assumptions — especially the discount rate, which is raised to a power in the denominator — can swing the result significantly for long-lived projects. This is why sensitivity analysis, where key assumptions are varied to see how much the NPV changes, is a standard part of any serious capital budgeting exercise.

Compared to alternatives like payback period (which ignores the time value of money and cash flows beyond the payback point) or accounting rate of return (which uses accounting profits rather than cash flows), NPV is considered theoretically superior because it directly measures the dollar impact on shareholder wealth, properly accounting for both timing and risk.`,
    quiz: [
      {
        q: 'What does a positive NPV indicate about a proposed project?',
        choices: [
          'The project will pay back its initial cost within one year',
          'The project is expected to generate returns exceeding the cost of capital, adding value',
          'The project has no risk',
          'The project will increase the company\'s tax liability'
        ],
        correct: 1,
        explanation: 'A positive NPV means the present value of future cash inflows exceeds the initial investment after discounting at the cost of capital — meaning the project is expected to create value beyond what investors require.'
      },
      {
        q: 'Why does NPV discount future cash flows back to today\'s value?',
        choices: [
          'To adjust for inflation only',
          'Because a dollar received in the future is worth less than a dollar today due to the time value of money',
          'Because accounting rules require all cash flows to be reported at historical cost',
          'To make the numbers easier to round'
        ],
        correct: 1,
        explanation: 'Money available today can be invested and grow, so future cash flows are worth less in present terms. Discounting converts all cash flows to a common point in time so they can be compared fairly.'
      }
    ]
  },
  {
    id: 'irr',
    title: 'Internal Rate of Return',
    body: `The Internal Rate of Return, or IRR, is the discount rate at which a project's Net Present Value equals exactly zero. In other words, it's the "break-even" rate of return — the percentage yield a project is expected to generate over its life.

Mathematically, IRR is found by solving for r in the equation: 0 = Σ [CFt / (1 + r)^t] - Initial Investment. Unlike NPV, which produces a dollar figure, IRR produces a percentage, which many managers find intuitive because it can be directly compared to a "hurdle rate" — often the company's WACC or required return.

The decision rule: if a project's IRR exceeds the hurdle rate, it's expected to add value and is generally accepted; if IRR is below the hurdle rate, it should be rejected. For a single conventional project (one initial outflow followed by inflows), IRR and NPV usually agree on accept/reject decisions.

However, IRR has well-known limitations. First, when comparing mutually exclusive projects of different sizes, IRR can rank a smaller project with a higher percentage return above a larger project that actually creates more dollar value — NPV is the more reliable measure in these cases. Second, projects with unconventional cash flows (cash outflows occurring more than once, such as a project requiring a large cleanup cost at the end of its life) can produce multiple IRRs or no real IRR at all, making the metric unreliable.

Third, IRR implicitly assumes that interim cash flows are reinvested at the IRR itself, which can be unrealistic for very high IRRs. The Modified Internal Rate of Return (MIRR) addresses this by assuming reinvestment at a more realistic rate, such as the WACC.

Despite these issues, IRR remains popular in practice because it's easy to communicate — "this project returns 18%" is more intuitive to a non-financial audience than "this project has an NPV of $2.3 million." A well-rounded capital budgeting analysis typically presents both metrics together, using NPV as the primary decision tool and IRR as a supplementary, more communicable figure.`,
    quiz: [
      {
        q: 'By definition, what does the Internal Rate of Return represent?',
        choices: [
          'The discount rate at which a project\'s NPV equals zero',
          'The company\'s tax rate on project income',
          'The average annual cash flow divided by the initial investment',
          'The interest rate charged by the company\'s bank'
        ],
        correct: 0,
        explanation: 'IRR is the break-even discount rate — the rate at which the present value of future cash inflows exactly equals the initial investment, making NPV zero.'
      },
      {
        q: 'When comparing two mutually exclusive projects of very different sizes, why might NPV and IRR give conflicting rankings?',
        choices: [
          'IRR always favors larger projects',
          'IRR is a percentage and can favor a smaller project with a higher rate even though a larger project creates more total dollar value',
          'NPV cannot be calculated for large projects',
          'IRR ignores the initial investment entirely'
        ],
        correct: 1,
        explanation: 'A small project might have a very high percentage return but generate little total value, while a larger project with a lower percentage return could generate far more dollars of value. NPV captures total value created, which is why it\'s generally preferred for ranking.'
      }
    ]
  },
  {
    id: 'working-capital-management',
    title: 'Working Capital Management',
    body: `Working capital is the difference between a company's current assets and current liabilities — essentially, the resources available to fund day-to-day operations. Managing it well is critical: too little working capital can leave a company unable to pay its bills, while too much can mean cash is sitting idle instead of being invested productively.

The core components of working capital management are accounts receivable, inventory, and accounts payable — often analyzed together through the "cash conversion cycle" (CCC). The CCC measures how many days it takes for a dollar spent on inventory to come back as cash from a customer. It's calculated as: Days Inventory Outstanding + Days Sales Outstanding - Days Payable Outstanding.

Days Inventory Outstanding (DIO) measures how long inventory sits before being sold. Days Sales Outstanding (DSO) measures how long it takes to collect cash after a sale is made on credit. Days Payable Outstanding (DPO) measures how long the company takes to pay its own suppliers. A shorter CCC means cash returns to the company faster, reducing the need for external financing to bridge the gap.

Companies manage these levers in different ways. To reduce DIO, they might adopt just-in-time inventory systems or improve demand forecasting to avoid overstocking. To reduce DSO, they might tighten credit terms, offer early-payment discounts, or invest in more aggressive collections. To increase DPO — without damaging supplier relationships — they might negotiate longer payment terms.

There's a balancing act here. Stretching payables too far can strain supplier relationships and lead to worse pricing or terms over time. Squeezing customers too hard on collections can hurt sales and customer goodwill. Cutting inventory too aggressively risks stockouts that lose sales.

For accountants, working capital metrics are also early warning signals. A rising DSO might indicate customers are struggling to pay or that credit policies have loosened too much — both potential signs of future bad debt. A rising DIO might indicate slowing sales or obsolete inventory that may need to be written down. Because of this, working capital ratios are a key part of both financial analysis and audit risk assessment.`,
    quiz: [
      {
        q: 'What does the Cash Conversion Cycle (CCC) measure?',
        choices: [
          'The total revenue earned in a fiscal year',
          'The number of days it takes for cash spent on inventory to be converted back into cash from customers',
          'The interest rate on short-term loans',
          'The company\'s total market capitalization'
        ],
        correct: 1,
        explanation: 'CCC = Days Inventory Outstanding + Days Sales Outstanding - Days Payable Outstanding. It captures how long cash is tied up in operations before it returns to the company.'
      },
      {
        q: 'A company\'s Days Sales Outstanding (DSO) has been steadily increasing for several quarters. What might this signal to an accountant reviewing the financials?',
        choices: [
          'The company is paying its suppliers faster',
          'Customers may be struggling to pay, or credit policies have loosened — a potential bad debt risk',
          'The company has reduced its inventory levels',
          'The company\'s tax rate has increased'
        ],
        correct: 1,
        explanation: 'Rising DSO means it\'s taking longer to collect cash from customers, which can indicate looser credit terms, collection problems, or customers in financial distress — all of which raise the risk of future write-offs.'
      }
    ]
  },
  {
    id: 'financial-leverage',
    title: 'Financial Leverage and the Debt-to-Equity Ratio',
    body: `Financial leverage refers to the use of borrowed money to finance a company's assets, with the goal of magnifying returns to shareholders. The most common measure of leverage is the debt-to-equity (D/E) ratio: total liabilities divided by total shareholders' equity.

Leverage works like a lever in physics — it amplifies outcomes in both directions. If a company borrows money at 5% interest and invests it in a project earning 12%, the spread (7%) accrues entirely to shareholders, boosting return on equity (ROE) above what it would be with all-equity financing. This is sometimes called "positive leverage" or a favorable use of "other people's money."

But leverage cuts both ways. If that same project earns only 3% — below the cost of debt — the company still owes the full interest payment, and the shortfall comes directly out of shareholders' returns, magnifying losses. This is why highly leveraged companies see far more volatile equity returns than unleveraged ones, even if their underlying operating performance is similar.

The DuPont analysis formalizes this relationship by breaking ROE into three components: Net Profit Margin × Asset Turnover × Equity Multiplier (where the equity multiplier is Total Assets / Total Equity, a measure of leverage). This decomposition shows that ROE can be increased either by genuinely improving operations (margin and turnover) or simply by taking on more debt (the multiplier) — and the second path doesn't necessarily reflect a healthier business.

From a credit perspective, lenders and rating agencies focus heavily on leverage ratios because higher leverage means less cushion to absorb losses before a company becomes insolvent. Covenants in loan agreements frequently set maximum D/E ratios or minimum interest coverage ratios (EBIT divided by interest expense) precisely to limit how much additional risk a borrower can take on.

For an accountant, it's important to remember that operating leases, pension obligations, and other off-balance-sheet or quasi-debt items can understate true leverage if not properly considered — which is part of why accounting standards like ASC 842 brought most leases onto the balance sheet, giving a more complete picture of a company's financial obligations.`,
    quiz: [
      {
        q: 'How does financial leverage affect a company\'s return on equity (ROE) when a leveraged investment earns more than the cost of debt?',
        choices: [
          'It has no effect on ROE',
          'It amplifies ROE upward, since the spread between the investment return and the cost of debt accrues to shareholders',
          'It always reduces ROE',
          'It eliminates the company\'s tax liability'
        ],
        correct: 1,
        explanation: 'When borrowed funds earn more than their cost, the excess return flows to equity holders without requiring additional equity investment, increasing ROE. This same mechanism amplifies losses when returns fall short of the cost of debt.'
      },
      {
        q: 'In the DuPont analysis, which component of ROE specifically reflects the impact of leverage?',
        choices: [
          'Net Profit Margin',
          'Asset Turnover',
          'The Equity Multiplier (Total Assets / Total Equity)',
          'The effective tax rate'
        ],
        correct: 2,
        explanation: 'The equity multiplier captures how much of the company\'s assets are financed by equity versus debt. A higher multiplier means more leverage, which can boost ROE without any change in operating performance.'
      }
    ]
  },
  {
    id: 'dividend-policy',
    title: 'Dividend Policy: How Companies Decide What to Pay Out',
    body: `Dividend policy is a company's approach to deciding how much of its earnings to distribute to shareholders versus retain for reinvestment. It's one of the most closely watched signals a company sends to the market, because changes in dividends are often interpreted as changes in management's confidence about future earnings.

There are several common approaches. A stable dividend policy aims to pay a consistent or steadily growing dividend per share regardless of short-term earnings fluctuations, smoothing out volatility for income-focused investors. A constant payout ratio policy ties the dividend to a fixed percentage of earnings, meaning the dollar amount fluctuates with profitability. A residual dividend policy treats dividends as whatever is "left over" after funding all positive-NPV investment opportunities — prioritizing growth over consistent payouts.

The "dividend irrelevance" theory, associated with Modigliani and Miller, argues that in a perfect market with no taxes or transaction costs, dividend policy shouldn't affect firm value — shareholders can create their own "dividends" by selling shares, and a dollar paid out is a dollar the company no longer has to invest. In practice, though, taxes, transaction costs, and signaling effects mean dividend policy does matter to many investors.

The "signaling" effect is significant: because managers have more information about a company's prospects than outside investors, a dividend increase is often read as a signal of confidence in sustainable future earnings, while a cut is read as a warning sign — even if the stated reason is unrelated. This is why companies are often very reluctant to cut dividends once established, preferring to maintain them even through difficult years if at all possible.

Share buybacks have become an increasingly popular alternative to dividends. Buybacks return cash to shareholders by reducing the number of outstanding shares, which can increase earnings per share and offer more flexibility than dividends (a buyback program can be paused without the negative signal a dividend cut sends). Buybacks can also be more tax-efficient for shareholders in jurisdictions where dividends are taxed as ordinary income but capital gains are taxed at a lower rate.

For accountants, dividends declared but not yet paid are recorded as a liability (dividends payable), and the cumulative effect of dividends reduces retained earnings on the balance sheet — a direct link between dividend policy and the equity section of the financial statements.`,
    quiz: [
      {
        q: 'Why do companies tend to be very reluctant to cut a dividend once it has been established?',
        choices: [
          'Because dividends are legally required once declared',
          'Because a dividend cut is often interpreted by the market as a negative signal about future earnings',
          'Because cutting a dividend increases the company\'s tax liability',
          'Because dividends cannot be changed under GAAP'
        ],
        correct: 1,
        explanation: 'Due to information asymmetry, investors often read dividend changes as signals about management\'s view of future prospects. A cut can trigger a sharp negative reaction even if unrelated factors caused it.'
      },
      {
        q: 'How are dividends declared but not yet paid typically recorded on the balance sheet?',
        choices: [
          'As an asset called "dividends receivable"',
          'As a reduction to revenue',
          'As a current liability called "dividends payable"',
          'They are not recorded until paid'
        ],
        correct: 2,
        explanation: 'Once a dividend is declared, the company has a legal obligation to pay it, so it is recorded as a current liability (dividends payable) until the cash is actually distributed, at which point both the liability and cash are reduced.'
      }
    ]
  },
  {
    id: 'free-cash-flow',
    title: 'Free Cash Flow: FCFF vs. FCFE',
    body: `Free cash flow (FCF) measures the cash a company generates after accounting for the expenditures needed to maintain or expand its asset base. Unlike net income, which includes non-cash items like depreciation and can be influenced by accounting choices, free cash flow focuses on actual cash available to be distributed to capital providers — making it a favorite metric for valuation.

There are two main versions. Free Cash Flow to the Firm (FCFF) represents cash available to all capital providers — both debt and equity holders — before any financing costs. A common formula is: FCFF = Net Income + Non-Cash Charges (like depreciation and amortization) + Interest Expense × (1 - Tax Rate) - Capital Expenditures - Changes in Net Working Capital.

Free Cash Flow to Equity (FCFE) represents cash available specifically to equity holders, after debt obligations have been satisfied. It's calculated as: FCFE = FCFF - Interest Expense × (1 - Tax Rate) + Net Borrowing (new debt issued minus debt repaid). Alternatively, FCFE can be calculated more directly starting from net income.

The choice between FCFF and FCFE matters for valuation. FCFF is discounted at the WACC to arrive at the total enterprise value (the value of the whole firm, debt and equity combined); subtracting net debt from enterprise value gives equity value. FCFE, on the other hand, is discounted at the cost of equity directly to arrive at equity value. Both approaches should, in theory, arrive at similar equity values if applied consistently — but FCFF is often preferred for companies with changing or unstable capital structures, since the cost of equity (and thus FCFE) can be distorted by leverage changes.

A critical input in both calculations is capital expenditures (CapEx) — the cash spent on property, plant, and equipment to maintain or grow the business. A company can show strong net income while consuming large amounts of cash on CapEx, resulting in weak or negative free cash flow. This divergence is a red flag analysts watch closely, since a business that consistently can't convert profits into cash may struggle to fund dividends, pay down debt, or survive a downturn without external financing.

Free cash flow is also central to leveraged buyout analysis and credit assessments, where the key question is often simply: does this business generate enough cash to service its debt?`,
    quiz: [
      {
        q: 'What is the key difference between Free Cash Flow to the Firm (FCFF) and Free Cash Flow to Equity (FCFE)?',
        choices: [
          'FCFF includes taxes while FCFE does not',
          'FCFF represents cash available to all capital providers (debt and equity), while FCFE represents cash available only to equity holders after debt obligations',
          'FCFE is always larger than FCFF',
          'There is no difference; the terms are interchangeable'
        ],
        correct: 1,
        explanation: 'FCFF is a pre-financing measure available to both debtholders and shareholders, discounted at WACC to find enterprise value. FCFE is what remains for shareholders after debt payments and is discounted at the cost of equity.'
      },
      {
        q: 'A company reports strong net income but consistently negative free cash flow. What is the most likely explanation?',
        choices: [
          'The company is paying too much in dividends',
          'The company is spending heavily on capital expenditures relative to its operating cash generation',
          'The company has no debt',
          'The company\'s tax rate is too low'
        ],
        correct: 1,
        explanation: 'High capital expenditures consume cash even when net income (which includes non-cash depreciation) looks healthy. Persistent negative free cash flow despite reported profits is a common warning sign analysts investigate further.'
      }
    ]
  },
  {
    id: 'capm',
    title: 'The Capital Asset Pricing Model',
    body: `The Capital Asset Pricing Model, or CAPM, is one of the most widely used tools for estimating the cost of equity — the return shareholders require for investing in a company's stock. It provides the theoretical foundation for the "Re" term in the WACC calculation.

The CAPM formula is: Re = Rf + β × (Rm - Rf), where Rf is the risk-free rate (typically the yield on long-term government bonds), β (beta) measures a stock's sensitivity to overall market movements, and (Rm - Rf) is the "market risk premium" — the extra return investors expect for holding the risky market portfolio instead of a risk-free asset.

The intuition is that investors should be compensated only for risk that can't be diversified away — known as systematic or market risk. Company-specific risk (a factory fire, a product recall) can theoretically be eliminated by holding a diversified portfolio of many stocks, so CAPM argues the market doesn't reward investors for bearing it. Beta is the measure of how much of that undiversifiable, market-wide risk a particular stock carries.

A beta of 1.0 means a stock tends to move in line with the overall market. A beta above 1.0 indicates a stock that amplifies market moves (more volatile than the market — common for high-growth or cyclical companies), while a beta below 1.0 indicates a stock that's less volatile than the market (common for utilities or consumer staples). A negative beta, while rare, would indicate a stock that tends to move opposite to the market.

CAPM has well-documented limitations. It relies on historical data to estimate beta, which may not predict future risk. It assumes a single risk factor (the market) drives returns, while real-world research (such as the Fama-French models) shows that factors like company size and value characteristics also help explain returns. And the model's assumptions — frictionless markets, rational investors, unlimited borrowing/lending at the risk-free rate — don't hold perfectly in reality.

Despite these critiques, CAPM remains the standard starting point in corporate finance for estimating the cost of equity, largely because of its simplicity, intuitive logic, and the widespread availability of the inputs needed to apply it.`,
    quiz: [
      {
        q: 'According to CAPM, what type of risk should investors be compensated for bearing?',
        choices: [
          'All risk, including company-specific events like factory fires',
          'Only systematic (market-wide) risk that cannot be eliminated through diversification',
          'Only the risk of inflation',
          'Only currency risk'
        ],
        correct: 1,
        explanation: 'CAPM assumes investors hold diversified portfolios, which eliminate company-specific risk. Only market-wide (systematic) risk, measured by beta, remains and is therefore the risk the market compensates investors for.'
      },
      {
        q: 'A stock has a beta of 1.5. What does this suggest about the stock relative to the overall market?',
        choices: [
          'It is expected to move with about 1.5 times the volatility of the overall market',
          'It is guaranteed to return 1.5% more than the market every year',
          'It has no systematic risk',
          'Its price never changes'
        ],
        correct: 0,
        explanation: 'A beta of 1.5 means the stock tends to amplify market movements — if the market rises or falls by 1%, the stock would be expected, on average, to move by about 1.5% in the same direction.'
      }
    ]
  },
  {
    id: 'break-even-analysis',
    title: 'Break-Even Analysis and Operating Leverage',
    body: `Break-even analysis examines the relationship between costs, sales volume, and profit to determine the point at which a business neither makes nor loses money — total revenue exactly equals total costs. It's a foundational tool for pricing decisions, cost management, and understanding business risk.

The core concept relies on separating costs into fixed costs (which don't change with production volume, like rent and salaried staff) and variable costs (which scale with each unit produced, like materials and per-unit labor or shipping). The break-even point in units is calculated as: Fixed Costs / (Price per Unit - Variable Cost per Unit). The denominator — price minus variable cost — is called the "contribution margin per unit," representing how much each additional unit sold contributes toward covering fixed costs and, beyond that, profit.

Once a business passes its break-even point, every additional unit sold contributes its full contribution margin directly to profit (since fixed costs are already covered). This creates "operating leverage" — a business with high fixed costs and low variable costs (like software or airlines) sees profits grow much faster than revenue once past break-even, but also sees losses mount much faster if sales fall short.

Operating leverage is conceptually similar to financial leverage but relates to the cost structure of operations rather than financing. The degree of operating leverage (DOL) measures the percentage change in operating income relative to a percentage change in sales — a high DOL means small sales swings translate into large swings in profitability.

Break-even analysis has practical applications well beyond a single product. Companies use it to evaluate whether to launch a new product line, whether to automate a process (trading variable labor costs for fixed equipment costs), or how a price change would affect the volume needed to maintain profitability. It also informs decisions about outsourcing — shifting costs from fixed (an in-house department) to variable (a per-unit contractor fee) reduces risk during downturns but may raise costs during high-demand periods.

One limitation is that the simple break-even model assumes costs behave in a strictly linear fashion and that the sales mix (for multi-product companies) remains constant — assumptions that often break down in the real world and require more sophisticated cost-volume-profit models to address.`,
    quiz: [
      {
        q: 'What does the "contribution margin per unit" represent in break-even analysis?',
        choices: [
          'The total fixed costs of the business',
          'The amount each unit sold contributes toward covering fixed costs and, beyond break-even, toward profit',
          'The selling price of the product',
          'The total variable costs for the year'
        ],
        correct: 1,
        explanation: 'Contribution margin per unit equals price minus variable cost per unit. It represents the portion of each sale that goes toward covering fixed costs first, and then toward profit once fixed costs are fully covered.'
      },
      {
        q: 'A company with high fixed costs and low variable costs (high operating leverage) experiences a sales decline. What is the likely impact on operating income?',
        choices: [
          'Operating income will decline by roughly the same percentage as sales',
          'Operating income will decline by a larger percentage than the sales decline',
          'Operating income is unaffected by sales changes',
          'Operating income will increase'
        ],
        correct: 1,
        explanation: 'High operating leverage means fixed costs make up a large share of total costs, so profit is highly sensitive to changes in sales volume — a given percentage drop in sales causes a larger percentage drop in operating income.'
      }
    ]
  }
);
