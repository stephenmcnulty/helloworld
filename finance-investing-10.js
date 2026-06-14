FINANCE_ARTICLES.push(
  {
    id: 'target-maturity-bond-etfs',
    title: 'Target Maturity Bond ETFs: Combining Bond ETF Liquidity with Defined Maturity',
    body: `Traditional bond ETFs have no defined maturity date — they continuously roll their holdings to maintain a target maturity profile, meaning investors never get a guaranteed return of principal at a specific date the way they would from an individual bond held to maturity. Target maturity bond ETFs (sometimes called "defined maturity" bond funds) were developed to address this gap, combining some benefits of individual bonds (a defined maturity date) with the diversification, liquidity, and convenience of an ETF structure.

A target maturity bond ETF holds a portfolio of bonds that all mature in (or near) a specific target year — for example, a fund might hold a diversified portfolio of corporate bonds all maturing in 2030. As that year approaches, the fund's bonds mature and proceeds are not reinvested into new long-term bonds (unlike a traditional bond ETF); instead, the portfolio gradually shifts toward cash and short-term instruments, and near the target date, the fund liquidates and distributes proceeds to shareholders — similar to how an individual bond returns principal at maturity, but via a diversified basket rather than a single issuer's credit risk.

This structure offers a middle ground between individual bonds and traditional bond funds. Compared to buying individual bonds directly, target maturity ETFs offer instant diversification across many issuers (reducing single-issuer credit risk), professional credit selection, and the ability to buy and sell throughout the trading day in any dollar amount (rather than being constrained by individual bond minimum denominations, often $1,000 or more, which can make building a diversified bond portfolio with smaller capital difficult). Compared to traditional bond ETFs, target maturity ETFs offer more predictability — an investor buying a 2030 fund today has a reasonable expectation of what happens at maturity: return of the fund's then-current NAV, primarily reflecting face value of remaining bonds, similar to — though not identical to — receiving face value back from individual bonds.

Target maturity bond ETFs are particularly useful for "bond laddering" strategies — building a portfolio of bonds (or bond funds) maturing in different years to match anticipated future cash flow needs, such as funding tuition payments, or structuring a retirement income stream where each "rung" matures in the year the investor expects to need that money. Using target maturity ETFs for laddering provides diversification (each rung holds many bonds rather than a concentration in a few issuers) while still matching maturity to anticipated cash need.

An important caveat: while these ETFs are designed to return approximately their NAV at the target date, this is not a guarantee the way holding an individual investment-grade bond to maturity (absent default) provides a known return of face value — the NAV depends on remaining holdings, and if the fund holds corporate or high-yield bonds, defaults prior to the target date would reduce the final distribution, just as a default would impair an individual bond investor's principal. For Treasury-focused funds, this credit risk is minimal, but for corporate or high-yield target maturity funds, "target maturity" describes the fund's structure and intended behavior, not a guarantee of principal return.`,
    quiz: [
      {
        q: 'How does a target maturity bond ETF differ from a traditional bond ETF as its target year approaches?',
        choices: [
          'It continues to roll its holdings into new long-term bonds indefinitely, just like a traditional bond ETF',
          'As the target year approaches, the fund\'s bonds mature without reinvestment into new long-term bonds, the portfolio shifts toward cash, and the fund liquidates and distributes proceeds near the target date — providing a defined-maturity-like outcome',
          'It converts entirely to stocks at the target date',
          'It doubles its holdings of long-term bonds as the target date nears'
        ],
        correct: 1,
        explanation: 'Unlike a traditional bond ETF, which continuously rolls holdings to maintain a constant maturity profile, a target maturity ETF lets its bonds mature without reinvesting into new long-term bonds as the target date nears, shifting to cash and ultimately liquidating — providing investors with a maturity-like experience.'
      },
      {
        q: 'Why is the "target maturity" feature not an absolute guarantee of principal return, particularly for corporate or high-yield target maturity funds?',
        choices: [
          'Because target maturity ETFs are not allowed to hold bonds at all',
          'Because defaults among the fund\'s underlying holdings prior to the target date would reduce the NAV the fund ultimately distributes, similar to how a default would impair an individual bond investor\'s return of principal',
          'Because the SEC prohibits these funds from ever distributing proceeds to shareholders',
          'Because target maturity ETFs always mature early without warning'
        ],
        correct: 1,
        explanation: 'A target maturity ETF\'s eventual distribution depends on the value of its remaining holdings at the target date — if underlying bonds default before then (a risk more relevant for corporate or high-yield funds than Treasury-focused funds), the NAV and resulting distribution would be reduced accordingly.'
      }
    ]
  },
  {
    id: 'required-minimum-distributions-rmds',
    title: 'Required Minimum Distributions (RMDs) from Retirement Accounts',
    body: `Traditional retirement accounts — traditional IRAs, 401(k)s, and similar employer-sponsored plans — offer a tax deferral: contributions (and growth) aren't taxed until withdrawal. But this deferral isn't indefinite. Required Minimum Distributions (RMDs) are minimum amounts that account owners must withdraw annually, starting at a specified age, ensuring the government eventually collects tax on these tax-deferred balances.

Under the SECURE 2.0 Act, the RMD starting age increased to 73 for individuals who turn 72 after December 31, 2022 (with a further increase to 75 scheduled for those born in 1960 or later) — a significant change from the historical age 70½, giving account owners more years of continued tax deferral.

The RMD amount for a given year is calculated by dividing the account balance as of December 31 of the prior year by a "distribution period" figure from IRS life expectancy tables (the Uniform Lifetime Table, for most owners). As the owner ages, the distribution period shortens, so the RMD represents a larger percentage of the balance each year — roughly 3.8% at age 73, gradually increasing later. Each traditional IRA has its own RMD calculated separately, but the total can be satisfied from any combination of those IRAs (aggregation is permitted across IRAs, but generally not between IRAs and 401(k)s, each requiring separate calculations).

The consequences of missing an RMD, or withdrawing less than required, used to be severe — historically a 50% excise tax on the shortfall. SECURE 2.0 reduced this to 25%, with a further reduction to 10% if corrected within a specified window — still significant, but meaningfully less punitive, and the IRS has shown willingness to waive the penalty for owners who demonstrate reasonable error and are correcting it.

A special rule applies to Roth IRAs: unlike traditional IRAs, Roth IRAs are not subject to RMDs during the original owner's lifetime (an advantage for those who don't need the funds and want to preserve tax-free growth, or pass the account to heirs). Prior to SECURE 2.0, Roth 401(k)s WERE subject to lifetime RMDs — SECURE 2.0 eliminated this requirement, aligning their treatment with Roth IRAs starting in 2024.

For inherited retirement accounts, RMD rules differ significantly depending on the beneficiary's relationship to the original owner and when the owner died — the SECURE Act (2019) introduced the "10-year rule" for most non-spouse beneficiaries, generally requiring the entire inherited account to be distributed within 10 years of death (with ambiguity, later clarified by the IRS, about whether annual distributions are also required during those years if the owner had already begun RMDs).

For accountants and planners, RMD planning involves coordinating distributions across accounts to satisfy aggregation rules, considering whether Qualified Charitable Distributions (QCDs — direct IRA transfers to charity that count toward the RMD without being taxable income, available starting at age 70½) might help charitably-inclined clients, and ensuring clients meet RMD deadlines (generally December 31, with a special extended deadline for the first RMD year) to avoid penalties.`,
    quiz: [
      {
        q: 'Under SECURE 2.0, what happened to the penalty for missing or under-withdrawing an RMD?',
        choices: [
          'The penalty was eliminated entirely',
          'The penalty increased from 25% to 50% of the shortfall',
          'The penalty was reduced from 50% to 25% of the shortfall, with a further reduction to 10% if corrected within a specified window',
          'The penalty was replaced with a mandatory account closure'
        ],
        correct: 2,
        explanation: 'SECURE 2.0 reduced the historically severe 50% excise tax on a missed RMD shortfall to 25%, with a further reduction to 10% if the shortfall is corrected within a specified correction window — still significant, but less punitive than before.'
      },
      {
        q: 'What is a Qualified Charitable Distribution (QCD), and how does it relate to RMDs?',
        choices: [
          'A penalty charged on RMDs donated to charity',
          'A direct transfer from an IRA to a qualified charity that counts toward satisfying the RMD without being included in the account owner\'s taxable income, available starting at age 70½',
          'A type of RMD that only applies to Roth IRAs',
          'A requirement that all RMDs must be donated to charity'
        ],
        correct: 1,
        explanation: 'A QCD allows an IRA owner (starting at age 70½) to direct funds straight to a qualified charity, satisfying part or all of their RMD for the year without that amount being counted as taxable income — a valuable tax planning tool for charitably-inclined retirees.'
      }
    ]
  },
  {
    id: 'cost-basis-methods-for-tax-reporting',
    title: 'Cost Basis Methods: FIFO, Specific Identification, and Average Cost',
    body: `When an investor sells shares of a stock, mutual fund, or ETF purchased at different times and prices, the difference between the sale price and the "cost basis" of the shares sold determines the taxable gain or loss. But when an investor holds multiple "lots" of the same security purchased at different prices, which lots are considered "sold" first? The cost basis method an investor selects can significantly affect the amount and character (short-term vs. long-term) of the gain or loss reported, making this a meaningful — if often overlooked — tax planning decision.

First-In, First-Out (FIFO) is the default method for most securities if no other is specified: the earliest-purchased shares are considered sold first. In a security that has appreciated over time, FIFO typically results in selling the lowest-cost-basis (and longest-held) shares first — often realizing the largest gains, but also more likely qualifying for long-term capital gains treatment, taxed at preferential rates compared to short-term gains (taxed as ordinary income).

Specific identification (SpecID) allows the investor to choose exactly which lots to sell, regardless of purchase order — for example, selling the highest-cost-basis shares first to minimize the reported gain (or maximize a loss), a technique often used in tax-loss harvesting or to manage gains in a given tax year (to stay within an income bracket, or offset other portfolio losses). To use SpecID, the investor generally must identify the specific lots at the time of sale (typically through the broker's platform) and receive confirmation — deciding "after the fact" which lots were sold doesn't satisfy the requirement.

Average cost is a method historically used primarily for mutual funds, where the cost basis of all shares is averaged together, and each share sold is assumed to have this average basis regardless of when purchased. This method is simpler administratively but offers less flexibility, since the investor can't selectively choose high-basis or low-basis lots — every share has the same basis.

Since 2011, brokers have been required to track and report "covered" securities' cost basis to the IRS on Form 1099-B, using whichever method the investor elected (FIFO by default) — a change from the era when investors tracked their own basis, often imprecisely. For securities purchased before these requirements took effect ("noncovered"), the basis reported to the IRS may be incomplete, and the investor remains responsible for substantiating basis with their own records.

For investors and tax professionals, the practical takeaway is that the cost basis method should be actively chosen rather than left to default — an investor selling part of a long-held, appreciated position might prefer SpecID to select higher-basis lots (reducing the current year's gain) or lower-basis long-term lots (to realize gains at preferential rates during a temporary low-income year). Once elected for a given account/security, changing methods for shares already held may require contacting the broker, and elections generally apply prospectively — worth establishing before significant trading activity occurs.`,
    quiz: [
      {
        q: 'What is the key feature of "specific identification" (SpecID) as a cost basis method?',
        choices: [
          'It automatically selects the lowest-cost shares for every sale',
          'It allows the investor to choose exactly which lots to sell at the time of sale (e.g., to minimize gains or harvest losses), provided the identification is made and confirmed at the time of the transaction',
          'It is only available for mutual funds',
          'It requires selling shares in the exact order they were purchased'
        ],
        correct: 1,
        explanation: 'Specific identification gives investors flexibility to choose which lots to sell — for example, high-basis lots to minimize gains — but the identification must be made at the time of sale (typically through the broker\'s platform), not decided after the fact.'
      },
      {
        q: 'What is the default cost basis method for most securities if an investor does not make an election?',
        choices: [
          'Average cost',
          'LIFO (Last-In, First-Out)',
          'FIFO (First-In, First-Out)',
          'Highest-cost-first'
        ],
        correct: 2,
        explanation: 'FIFO is the default method for most securities absent an election, meaning the earliest-purchased shares are treated as sold first — which, for an appreciated security, often means realizing the longest-held shares (and potentially the largest gains) first.'
      }
    ]
  },
  {
    id: 'collectibles-and-alternative-asset-investing',
    title: 'Collectibles and Alternative Asset Investing: Art, Wine, and Beyond',
    body: `Beyond stocks, bonds, and real estate, a category of "collectible" alternative assets — fine art, wine, classic cars, rare coins, watches, trading cards, and similar items — has attracted growing investor interest, partly driven by new platforms allowing fractional ownership of high-value items, and partly by a broader search for assets that may behave differently from traditional financial markets. Understanding both the unique characteristics and significant limitations of these assets is important before treating them as a meaningful part of an investment strategy.

The appeal often cited for collectibles includes potential diversification (returns on fine art or wine may have low correlation with stock and bond markets in some periods), a tangible, enjoyable asset providing utility beyond financial return (a collector who enjoys displaying art receives a form of "dividend" a stock certificate doesn't provide), and in some cases, scarcity-driven appreciation (a finite supply of a desirable item, such as a renowned artist's limited body of work, can support long-term appreciation if demand grows).

However, collectibles come with substantial challenges that distinguish them from traditional financial assets. Liquidity is a major concern — selling fine art or a rare item typically requires finding a specific buyer (often through an auction house or specialized dealer) willing to pay an acceptable price, a process that can take months and involves significant transaction costs (auction houses commonly charge a "buyer's premium" plus seller's commission, together often totaling 20-25% or more of sale price — a substantial drag compared to trading public securities).

Valuation is similarly challenging — unlike a publicly traded stock with a continuously observable price, collectibles are valued through appraisals, recent comparable sales (which may be infrequent and imperfectly comparable), and ultimately whatever a buyer is actually willing to pay — meaning reported "valuations" (including those used by fractional-ownership platforms) can diverge meaningfully from what an asset would actually sell for.

From a tax perspective, in the U.S., collectibles held more than one year are subject to a maximum federal long-term capital gains rate of 28% — higher than the 15-20% rates typically applying to long-term gains on stocks and most other capital assets — reducing after-tax returns relative to traditional securities, even before considering authentication, insurance, storage, and transaction costs.

Fractional ownership platforms — allowing investors to buy a small percentage interest in a specific high-value item (a painting, a rare wine collection, a vintage car) — have lowered the capital required for exposure to this asset class, but introduce their own considerations: investors typically cannot take possession of or enjoy the underlying asset, returns depend on the platform successfully selling it later (a secondary market for fractional interests may exist but is typically much thinner than for traditional securities), and the platform charges fees that reduce net returns.

For investors and advisors, collectibles are generally best considered — if at all — as a small portion of a diversified portfolio, motivated as much by genuine interest in the underlying items as by financial return expectations, with realistic awareness of liquidity constraints, valuation uncertainty, higher capital gains rates, and meaningful transaction and carrying costs.`,
    quiz: [
      {
        q: 'What is the maximum federal long-term capital gains tax rate that applies to collectibles held more than one year, and how does it compare to most stocks?',
        choices: [
          'Collectibles are tax-exempt, unlike stocks',
          'Collectibles are taxed at a maximum 28% rate, higher than the 15-20% rates typically applicable to long-term gains on stocks and most other capital assets',
          'Collectibles and stocks are taxed at exactly the same rates',
          'Collectibles are taxed at ordinary income rates regardless of holding period'
        ],
        correct: 1,
        explanation: 'Long-term gains on collectibles are subject to a maximum 28% federal rate — notably higher than the 15-20% long-term capital gains rates that typically apply to stocks and most other capital assets, reducing the after-tax appeal of collectibles as investments.'
      },
      {
        q: 'What is a key trade-off of fractional ownership platforms for collectibles compared to owning a collectible directly?',
        choices: [
          'Fractional ownership eliminates all fees and costs',
          'Investors typically cannot take possession of or personally enjoy the underlying asset, and returns depend on the platform eventually selling the asset, with platform fees reducing net returns',
          'Fractional ownership guarantees higher returns than direct ownership',
          'Fractional ownership platforms are not subject to any capital gains tax'
        ],
        correct: 1,
        explanation: 'Fractional ownership lowers the capital needed for exposure to collectibles but removes the ability to personally use or enjoy the asset (one of collectibles\' traditional appeals), and returns depend on a future sale by the platform, which charges its own fees that reduce net investor returns.'
      }
    ]
  },
  {
    id: 'nonqualified-deferred-compensation-plans',
    title: 'Nonqualified Deferred Compensation Plans',
    body: `Qualified retirement plans — like 401(k)s — come with significant tax advantages but also significant restrictions, including annual contribution limits ($23,000 for 401(k) employee deferrals in 2024, plus catch-up contributions for those 50 and older) that can feel limiting for highly compensated executives who want to defer a larger portion of their income. Nonqualified deferred compensation (NQDC) plans offer a way for select groups of employees — typically executives and other highly compensated individuals — to defer a portion of their compensation (salary, bonus, or both) to a future date, often retirement, without the contribution limits that apply to qualified plans.

The fundamental trade-off of NQDC plans is risk versus tax deferral. Because NQDC plans aren't subject to ERISA's funding and protection requirements the way qualified plans are, deferred amounts generally remain assets of the employer (often informally set aside in a "rabbi trust," which remains subject to the claims of the company's general creditors in bankruptcy). This means that if the employer becomes insolvent, employees with NQDC balances are simply unsecured creditors — they could lose some or all of their deferred compensation, a risk that doesn't exist for funds held in a qualified plan's trust, which is protected from the employer's creditors.

Section 409A of the tax code imposes strict rules on NQDC plans, primarily around timing: elections to defer compensation generally must be made before the start of the year in which it's earned (with limited exceptions for new hires), and distribution timing must be specified at the time of the deferral election — generally limited to specific permitted events such as a fixed date, separation from service, death, disability, an unforeseeable emergency, or a change in control. Unlike qualified plans, where participants often have flexibility to choose distribution timing within IRS-permitted ranges, NQDC participants generally must commit to their timing well in advance, with only limited, strictly-regulated ability to change it later. Violating 409A's requirements triggers severe consequences for the employee — immediate taxation of all deferred amounts (even if not yet received), plus a 20% additional tax, plus interest.

A common feature of NQDC plans is allowing participants to choose from a menu of "deemed investment" options — the plan tracks the value of deferred compensation as if invested in selected mutual funds or benchmarks, even though the underlying assets (if held in a rabbi trust) may or may not actually be invested that way. This gives participants investment-like exposure and growth potential, similar to a 401(k)'s investment menu, but the "account value" remains a bookkeeping entry representing an unsecured promise by the employer, not a segregated, protected account.

For executives considering NQDC participation, key considerations include: the employer's creditworthiness (since deferred amounts are at risk if the employer becomes insolvent — more significant the longer the deferral and the larger the amount relative to other assets), the inflexibility of distribution timing once elected, and the tax planning value of deferring income from high-earning years to lower-earning years (such as early retirement) — a benefit weighed against the credit risk and inflexibility inherent in the NQDC structure.`,
    quiz: [
      {
        q: 'Why are amounts deferred under a nonqualified deferred compensation (NQDC) plan considered at risk if the employer becomes insolvent?',
        choices: [
          'Because NQDC amounts are held in a qualified trust protected from creditors, just like a 401(k)',
          'Because NQDC plans aren\'t subject to ERISA\'s protections in the same way as qualified plans — deferred amounts generally remain assets of the employer (even if informally held in a rabbi trust) and are subject to the claims of the employer\'s general creditors',
          'Because the IRS automatically confiscates NQDC balances upon employer bankruptcy',
          'Because NQDC plans are required by law to be invested entirely in the employer\'s own stock'
        ],
        correct: 1,
        explanation: 'Unlike a qualified plan\'s trust, which is protected from the employer\'s creditors, assets informally set aside for NQDC obligations (e.g., in a rabbi trust) remain subject to the claims of the employer\'s general creditors in bankruptcy — making NQDC participants unsecured creditors for their deferred amounts.'
      },
      {
        q: 'What is a key requirement of Section 409A regarding NQDC distribution timing?',
        choices: [
          'Participants can change their distribution timing at any point with no restrictions',
          'The timing of distributions must generally be specified at the time of the deferral election, limited to specific permitted events, with only limited and strictly regulated ability to change the election later',
          'Section 409A has no rules regarding distribution timing',
          'All NQDC balances must be distributed within one year of deferral regardless of the participant\'s wishes'
        ],
        correct: 1,
        explanation: 'Section 409A requires distribution timing to be locked in at the time of the deferral election (limited to specific permitted events like a fixed date, separation from service, or change in control), with only limited, strictly regulated ability to change it later — violations trigger severe tax penalties including immediate taxation plus a 20% additional tax.'
      }
    ]
  },
  {
    id: 'catastrophe-bonds-and-insurance-linked-securities',
    title: 'Catastrophe Bonds and Insurance-Linked Securities',
    body: `Insurance companies that provide property coverage in disaster-prone areas — hurricane-exposed coastal regions, earthquake zones — face the risk that a single major catastrophic event could generate claims large enough to threaten the insurer's solvency. Traditionally, insurers manage this risk by purchasing reinsurance (insurance for insurers) from large reinsurance companies. Catastrophe bonds ("cat bonds") and other insurance-linked securities (ILS) represent an alternative way for insurers to transfer catastrophe risk — not to traditional reinsurers, but directly to capital markets investors, who effectively act as reinsurers in exchange for an attractive yield.

In a typical cat bond structure, an insurer (the "sponsor") sets up a special purpose vehicle that issues bonds to investors. Proceeds are placed in a collateral account, typically invested in safe, short-term securities. Investors receive periodic interest payments, funded by the collateral's return plus premium payments from the sponsor (the cost of the "reinsurance" purchased). If a predefined catastrophic event occurs — say, a hurricane causing insured losses above a specified threshold — some or all of the collateral is paid to the sponsor to cover claims, and investors lose some or all of their principal. If no qualifying event occurs before maturity (typically 1-5 years), investors get their full principal back, having earned attractive yields throughout.

The trigger mechanism for a payout varies by structure. "Indemnity" triggers pay out based on the sponsor's actual incurred losses — closely matching real risk, but requiring investors to trust the sponsor's loss reporting and potentially delaying settlement while losses are assessed. "Parametric" triggers pay out based on objectively measurable physical characteristics of the event itself — a hurricane's wind speed and location, or an earthquake's magnitude and epicenter, as measured by an independent source like the National Hurricane Center or USGS — without reference to the sponsor's actual losses. Parametric triggers offer faster, more transparent settlement but introduce "basis risk" for the sponsor — the possibility the trigger doesn't pay out (or pays too little) despite real losses, because measured parameters didn't cross the defined threshold, or pays out despite lower actual losses.

For investors, cat bonds offer a return stream largely uncorrelated with traditional financial markets — performance depends on whether a hurricane or earthquake occurs, a risk essentially unrelated to stock market movements, interest rates, or corporate credit conditions. This low correlation has made cat bonds attractive to institutional investors (and increasingly, cat bond-focused mutual funds and ETFs accessible to individuals) seeking diversification.

However, cat bonds carry distinct risks that don't map onto traditional credit analysis: "tail risk" is central — most years, no qualifying catastrophe occurs and investors earn their full coupon, but in a year when a major event occurs, investors can lose a substantial portion (or all) of their principal — a profile sometimes likened to selling insurance, where premiums are collected steadily but a large loss can occur suddenly. Additionally, climate change introduces uncertainty into the historical models used to price catastrophe risk, as weather event frequency and severity may not follow historical patterns — a modeling risk affecting both sponsors and investors assessing whether yields compensate for the risk taken.`,
    quiz: [
      {
        q: 'What is the fundamental purpose of a catastrophe bond from the sponsoring insurer\'s perspective?',
        choices: [
          'To raise general corporate funding unrelated to insurance risk',
          'To transfer catastrophe risk (such as hurricane or earthquake losses) directly to capital markets investors, who act effectively as reinsurers in exchange for yield',
          'To guarantee the insurer will never have to pay any claims',
          'To eliminate the need for the insurer to hold any reserves'
        ],
        correct: 1,
        explanation: 'Cat bonds let an insurer transfer catastrophe risk to capital markets investors — investors receive attractive yields in exchange for potentially losing principal if a defined catastrophic event occurs, effectively functioning as an alternative to traditional reinsurance.'
      },
      {
        q: 'What is "basis risk" in the context of a parametric trigger cat bond?',
        choices: [
          'The risk that the bond pays a variable interest rate',
          'The possibility that the parametric trigger (based on objective measures like wind speed or earthquake magnitude) doesn\'t align with the sponsor\'s actual losses — potentially not paying out (or paying too little) despite real losses, or paying out despite lower actual losses',
          'The risk that the bond is denominated in a foreign currency',
          'The risk that the bond has no maturity date'
        ],
        correct: 1,
        explanation: 'Parametric triggers offer fast, objective settlement based on measured event characteristics, but because those measurements may not perfectly correspond to the sponsor\'s actual incurred losses, a mismatch ("basis risk") can occur in either direction — insufficient payout despite real losses, or payout despite limited actual losses.'
      }
    ]
  }
);
