# MASTER PARAMETER SHEET - B2B TELECOM SALES MODEL

## 0. AGENT STATES

### SELLER STATES
| State       | Description | Next Possible States | Typical Duration |
|------------|-------------|---------------------|------------------|
| PROSPECTING | Looking for opportunities, market scanning | QUALIFYING | 1-4 weeks |
| QUALIFYING  | Evaluating potential of lead | PROPOSING | 1-2 weeks |
| PROPOSING   | Creating and presenting solution | NEGOTIATING | 2-4 weeks |
| NEGOTIATING | Discussion of terms and conditions | CLOSING, PROPOSING | 2-3 weeks |
| CLOSING     | Finalizing the deal | CLOSE LOST, MAINTAINING | 1-2 weeks |
| MAINTAINING | Managing existing customer relationship | PROSPECTING | Ongoing |

### BUYER STATES
| State          | Description | Next Possible States | Typical Duration |
|----------------|-------------|---------------------|------------------|
| NOT_INTERESTED | No active buying process | EVALUATING | Indefinite |
| EVALUATING     | Assessing needs and solutions | BUDGETING, NOT_INTERESTED | 1-3 months |
| BUDGETING      | Securing funding and planning | DECIDING, EVALUATING | 1-2 months |
| DECIDING       | Making final selection | GO_NOGO, EVALUATING | 2-4 weeks |
| GO_NOGO        | Purchase Decision | NOT_INTERESTED, DELIVERED | 2-8 weeks |
| DELIVERED      | Final Delivery | SATISFIED, DISSATISFIED | 1-24 months | 
| SATISFIED      | Happy with the purchase | BUDGETING | 3-12 months |
| DISSATISF      | Not Happy with the purchase | NOT_INTERESTED | Indefinite


### State Transition Probabilities

#### Seller Transition Matrix
| From/To    | PROSP | QUAL | PROP | NEG  | CLOSE | MAINT |
|------------|-------|------|------|------|-------|-------|
| PROSPECTING| 0.6   | 0.4  | 0    | 0    | 0     | 0     |
| QUALIFYING | 0.0   | 0.6  | 0.4  | 0    | 0     | 0     |
| PROPOSING  | 0.0   | 0.1  | 0.3  | 0.4  | 0.2   | 0     |
| NEGOTIATING| 0.0   | 0    | 0.2  | 0.5  | 0.3   | 0     |
| CLOSING    | 0.0   | 0    | 0    | 0.1  | 0.2   | 0.5   |
| MAINTAINING| 0.0   | 0    | 0    | 0    | 0.3   | 0.7   |

#### Buyer Transition Matrix
| From/To    | NOT_INT | EVAL | BUDG | DEC  | GO_NOGO | DELIVERED | SAT  | DISS |
|------------|---------|------|------|------|---------|-----------|------|------|
| NOT_INT    | 0.7     | 0.3  | 0    | 0    | 0       | 0         | 0    |  0   |
| EVALUATING | 0.3     | 0.3  | 0.4  | 0    | 0       | 0         | 0    |  0   |
| BUDGETING  | 0.2     | 0.2  | 0.3  | 0.3  | 0       | 0         | 0    |  0   |
| DECIDING   | 0.1     | 0.2  | 0.1  | 0.3  | 0.3     | 0         | 0    |  0   |
| GO_NOGO    | 0       | 0    | 0    | 0.1  | 0.2     | 0.7       | 0.0  |  0   |
| DELIVERED  | 0       | 0    | 0    | 0    | 0       | 0         | 0.8  |  0.2 |
| SATISFIED  | 0       | 0.0  | 0    | 0    | 0       | 0         | 0.9  |  0.1 |
| DISSATISF  | 0       | 0.0  | 0    | 0    | 0       | 0         | 0.1  |  0.9 |

### State Impact on Success Probability
| Seller State | Buyer State   | Success Modifier |
|--------------|---------------|------------------|
| PROPOSING    | EVALUATING    | +10%            |
| NEGOTIATING  | DECIDING      | +20%            |
| CLOSING      | DECIDING      | +30%            |
| MAINTAINING  | SATISFIED     | +15%            |
| PROSPECTING  | NOT_INTERESTED| -20%            |
| ANY          | DISSATISFIED  | -25%            |

## 1. COMPANY SIZE CLASSIFICATION

| Category | Staff    | Turnover (M€) | Balance Sheet (M€) | Decision Makers |
|----------|----------|---------------|-------------------|-----------------|
| Micro    | ≤ 10     | ≤ 0.7         | ≤ 0.35            | 1               |
| Small    | ≤ 50     | ≤ 12          | ≤ 6               | 1-2             |
| Medium   | ≤ 250    | ≤ 40          | ≤ 20              | 2-4             |
| Large    | > 250    | > 40          | > 20              | 4-8             |

## 2. SELLING EFFORT MULTIPLIERS

| Customer/Product | Old Product | New Product | Decision Time |
|-----------------|-------------|-------------|---------------|
| Old Customer    | 1x          | 2x          | 1x            |
| New Customer    | 4x          | 8-16x       | 2x            |

## 3. SALES PIPELINE CONVERSION RATES (NEW SALES)

| Stage           | Rate    | Duration  | Effort Level |
|-----------------|---------|-----------|--------------|
| Lead → MQL      | 1-3%    | 5-10d     | 1x           |
| MQL → SQL       | 10-15%  | 10-15d    | 2x           |
| SQL → Proposal  | 50-60%  | 15-30d    | 3x           |
| Proposal → Won  | 25-30%  | 30-60d    | 4x           |
| Proposal → Lost | 70-75%  | 15-30d    | 1x           |

## 4. BUDGET CYCLES

| Size    | Cycle Length | Planning Time | Flexibility |
|---------|--------------|---------------|-------------|
| Micro   | 1 month     | 1 week       | High        |
| Small   | 3 months    | 2 weeks      | Medium      |
| Medium  | 6 months    | 1 month      | Low         |
| Large   | 12 months   | 2 months     | Very Low    |

## 5. VALUE ELEMENT WEIGHTS

| Element             | Weight | Sub-Components                    |
|--------------------|--------|-----------------------------------|
| Functional Value   | 40%    | Technical (50%), Reliability (30%), Scalability (20%) |
| Economic Value     | 30%    | Price (40%), ROI (40%), Cost Reduction (20%) |
| Relationship Value | 30%    | Trust (40%), Support (30%), Ease of Business (30%) |

## 6. SELLER PARAMETERS

### Experience Levels
| Level | Success Modifier | Relationship Growth | Max Accounts |
|-------|-----------------|---------------------|--------------|
| 1     | +20%           | 10%                | 5            |
| 2     | +30%           | 15%                | 8            |
| 3     | +40%           | 20%                | 12           |
| 4     | +50%           | 25%                | 15           |
| 5     | +60%           | 30%                | 20           |

### Target Customer Matrix
| Experience | Target Segments | Base Success Rate |
|------------|----------------|-------------------|
| 1          | Micro          | 40%              |
| 2          | Micro, Small   | 50%              |
| 3          | Small, Medium  | 60%              |
| 4          | Medium, Large  | 70%              |
| 5          | Large          | 80%              |

## 7. RELATIONSHIP SCORES

| Factor                | Impact | Duration |
|----------------------|--------|----------|
| Initial Score        | 0.3    | -        |
| Successful Meeting   | +0.1   | 30 days  |
| Failed Meeting       | -0.15  | 30 days  |
| Monthly Decay        | -0.05  | 30 days  |

## 8. TIME REQUIREMENTS (HOURS)

### New Customer, New Product
| Role           | Lead-MQL | MQL-SQL | SQL-Proposal | Proposal-Win |
|----------------|----------|---------|--------------|--------------|
| Sales Rep      | 4-8      | 8-16    | 16-24       | 24-32        |
| Sales Engineer | 2-4      | 4-8     | 8-16        | 16-24        |
| Management     | 1-2      | 2-4     | 4-8         | 8-16         |

### Existing Customer, Existing Product
| Role           | Lead-MQL | MQL-SQL | SQL-Proposal | Proposal-Win |
|----------------|----------|---------|--------------|--------------|
| Sales Rep      | 1-2      | 2-4     | 4-6         | 6-8          |
| Sales Engineer | 0-1      | 1-2     | 2-4         | 4-6          |
| Management     | 0-0.5    | 0.5-1   | 1-2         | 2-4          |

## 9. SUCCESS PROBABILITY MODIFIERS

### Base Modifiers
| Factor              | Impact |
|--------------------|--------|
| Experience Level   | ±20%   |
| Company Size Match | ±15%   |
| Budget Available   | ±25%   |
| Technical Fit      | ±20%   |
| Competition       | -10%   |

### Market Condition Impacts
| Condition          | Impact |
|--------------------|--------|
| Growth Market      | +15%   |
| Stable Market      | +5%    |
| Declining Market   | -10%   |
| High Competition   | -15%   |

## 10. SEASONAL ADJUSTMENTS

| Quarter | Modifier | Primary Driver              |
|---------|----------|-----------------------------|
| Q1      | 0.8     | New budget year starting    |
| Q2      | 1.0     | Normal business conditions  |
| Q3      | 0.7     | Summer holiday season       |
| Q4      | 1.2     | Year-end budget utilization |

## 11. RISK ASSESSMENT FACTORS

| Factor Type        | Weight | Impact on Success Rate |
|-------------------|---------|----------------------|
| Technical Risk    | 30%     | ±15%                 |
| Financial Risk    | 25%     | ±20%                 |
| Implementation    | 25%     | ±15%                 |
| Organizational    | 20%     | ±10%                 |

## 12. FORMULA EXAMPLES

### Final Success Probability
```python
success_rate = base_rate * experience_modifier * size_match_modifier * 
               relationship_modifier * market_modifier * seasonal_modifier
```

### Total Selling Effort
```python
total_effort = base_effort * customer_type_multiplier * product_type_multiplier * 
               company_size_modifier * complexity_modifier
```

### Relationship Score
```python
new_score = current_score + interaction_impact + time_decay
```