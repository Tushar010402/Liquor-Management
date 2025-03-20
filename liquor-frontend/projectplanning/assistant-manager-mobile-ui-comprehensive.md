# Assistant Manager Mobile UI - Comprehensive Screens

## 1. Dashboard & Navigation

### Assistant Manager Dashboard
```
┌─────────────────────────────────┐
│ Dashboard               🔔 5    │
├─────────────────────────────────┤
│ 🏪 Downtown Shop            ▼   │
├─────────────────────────────────┤
│ PENDING APPROVALS               │
│ ┌───────────────────────────┐   │
│ │ 12 items need review      │   │
│ │ ┌────┐ ┌────┐ ┌────┐ ┌────┐   │
│ │ │Sale│ │Stock│ │Cash│ │More│   │
│ │ │ 5  │ │ 3  │ │ 2  │ │ 2  │   │
│ │ └────┘ └────┘ └────┘ └────┘   │
│ │ [View All Approvals]      │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ TODAY'S SUMMARY                 │
│ ┌─────────┐ ┌─────────┐         │
│ │ SALES   │ │ ITEMS   │         │
│ │ ₹38,500 │ │ 248     │         │
│ │ +10%    │ │ Sold    │         │
│ └─────────┘ └─────────┘         │
│ ┌─────────┐ ┌─────────┐         │
│ │ NEW POs │ │ LOW STOCK│         │
│ │ 2       │ │ 5        │         │
│ │ Orders  │ │ Items    │         │
│ └─────────┘ └─────────┘         │
├─────────────────────────────────┤
│ QUICK ACTIONS                   │
│ ┌────────┐┌────────┐┌────────┐  │
│ │   ✅   ││   📦   ││   🛒   │  │
│ │Approve ││ Stock  ││Purchase│  │
│ └────────┘└────────┘└────────┘  │
├─────────────────────────────────┤
│ URGENT APPROVALS                │
│ ┌───────────────────────────┐   │
│ │ Sale #1052  -  ₹15,400    │   │
│ │ Executive: Rahul          │   │
│ │ Waiting: 2h 15m  ⏱️        │   │
│ │ [Review Now]              │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Stock #483  -  5 Items    │   │
│ │ Executive: Rahul          │   │
│ │ Waiting: 3h 40m  ⏱️        │   │
│ │ [Review Now]              │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ INVENTORY ALERTS                │
│ ┌───────────────────────────┐   │
│ │ ⚠️ Low Stock: 5 Items     │   │
│ │ [View Details]            │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ ⚠️ Expiring Soon: 3 Items │   │
│ │ [View Details]            │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ RECENT ACTIVITY                 │
│ • Sale #1051 approved by Manager│
│ • PO #287 delivered & received  │
│ • Stock transfer #52 completed  │
│ [View All Activity]             │
├─────────────────────────────────┤
│ 🏠 Home │ ✅ Approve │ 📊 Reports │
└─────────────────────────────────┘
```



### Assistant Manager Menu / Navigation
```
┌─────────────────────────────────┐
│ ← Menu                          │
├─────────────────────────────────┤
│                                 │
│ [👤 User Profile Picture]       │
│ Vikram Singh                    │
│ Assistant Manager               │
│ Last Login: Today, 9:10 AM      │
│                                 │
├─────────────────────────────────┤
│ ▶ Dashboard                     │
├─────────────────────────────────┤
│ ▶ Shop Selection                │
├─────────────────────────────────┤
│ APPROVALS                       │
│  ▶ All Pending Approvals        │
│  ▶ Sales Approvals              │
│  ▶ Stock Adjustments            │
│  ▶ Return Approvals             │
│  ▶ Deposit Verifications        │
├─────────────────────────────────┤
│ INVENTORY                       │
│  ▶ Stock Levels                 │
│  ▶ Stock Transfers              │
│  ▶ Expiry Management            │
│  ▶ Brand Management             │
├─────────────────────────────────┤
│ PURCHASING                      │
│  ▶ Create Purchase Orders       │
│  ▶ Track Purchase Orders        │
│  ▶ Receive Inventory            │
├─────────────────────────────────┤
│ ANALYTICS                       │
│  ▶ Sales Analytics              │
│  ▶ Inventory Analytics          │
│  ▶ Executive Performance        │
├─────────────────────────────────┤
│ REPORTS                         │
│  ▶ Generate Reports             │
│  ▶ Report History               │
├─────────────────────────────────┤
│ ▶ Settings                      │
│ ▶ Help & Support                │
│ ▶ Logout                        │
└─────────────────────────────────┘
```

### Shop Selector Screen
```
┌─────────────────────────────────┐
│ ← Shop Selection            🔍  │
├─────────────────────────────────┤
│ SHOP OVERVIEW                   │
│ ┌───────────────────────────┐   │
│ │ Total Shops: 3            │   │
│ │ Assigned to me: 2         │   │
│ │ Pending Approvals: 12     │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ SHOP LIST                       │
│ ┌───────────────────────────┐   │
│ │ ⭐ DOWNTOWN SHOP          │   │
│ │ Status: Active            │   │
│ │ Pending: 8 approvals      │   │
│ │ Today's Sales: ₹38,500    │   │
│ │ Last Update: 5 min ago    │   │
│ │ [Set Active] [View Details]│  │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ ┌───────────────────────────┐   │
│ │ MALL BRANCH               │   │
│ │ Status: Active            │   │
│ │ Pending: 4 approvals      │   │
│ │ Today's Sales: ₹28,700    │   │
│ │ Last Update: 22 min ago   │   │
│ │ [Set Active] [View Details]│  │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ ┌───────────────────────────┐   │
│ │ HIGHWAY OUTLET            │   │
│ │ Status: Not assigned      │   │
│ │ [Request Access]          │   │
│ └───────────────────────────┘   │
└─────────────────────────────────┘
```

## 2. Approval Management

### Pending Approvals Screen
```
┌─────────────────────────────────┐
│ ← Pending Approvals         All▼│
├─────────────────────────────────┤
│ 🏪 Downtown Shop                │
├─────────────────────────────────┤
│ FILTER BY TYPE                  │
│ ┌────┐ ┌────┐ ┌────┐ ┌────┐     │
│ │Sale│ │Stock│ │Cash│ │More│     │
│ │ 5  │ │ 3  │ │ 2  │ │ 2  │     │
│ └────┘ └────┘ └────┘ └────┘     │
├─────────────────────────────────┤
│ HIGH PRIORITY                   │
│ ┌───────────────────────────┐   │
│ │ Sale #1052  -  ₹15,400    │   │
│ │ Executive: Rahul          │   │
│ │ Waiting: 2h 15m  ⏱️        │   │
│ │ [View Details]            │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Stock #483  -  5 Items    │   │
│ │ Executive: Rahul          │   │
│ │ Waiting: 3h 40m  ⏱️        │   │
│ │ [View Details]            │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ SALES APPROVALS                 │
│ ┌───────────────────────────┐   │
│ │ Sale #1053  -  ₹8,720     │   │
│ │ Executive: Priya          │   │
│ │ Waiting: 50m  ⏱️           │   │
│ │ [View Details]            │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Sale #1054  -  ₹4,380     │   │
│ │ Executive: Rahul          │   │
│ │ Waiting: 15m  ⏱️           │   │
│ │ [View Details]            │   │
│ └───────────────────────────┘   │
│ [View All Sales Approvals]      │
├─────────────────────────────────┤
│ STOCK ADJUSTMENTS               │
│ ┌───────────────────────────┐   │
│ │ Stock #484  -  3 Items    │   │
│ │ Executive: Priya          │   │
│ │ Waiting: 1h 20m  ⏱️        │   │
│ │ [View Details]            │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Stock #485  -  2 Items    │   │
│ │ Executive: Sanjay         │   │
│ │ Waiting: 45m  ⏱️           │   │
│ │ [View Details]            │   │
│ └───────────────────────────┘   │
│ [View All Stock Adjustments]    │
├─────────────────────────────────┤
│ DEPOSIT VERIFICATIONS           │
│ ┌───────────────────────────┐   │
│ │ Deposit #135  -  ₹25,000  │   │
│ │ Executive: Rahul          │   │
│ │ Waiting: 1h 55m  ⏱️        │   │
│ │ [View Details]            │   │
│ └───────────────────────────┘   │
│ [View All Deposits]             │
└─────────────────────────────────┘
```

### Sale Approval Screen
```
┌─────────────────────────────────┐
│ ← Sale Details                  │
├─────────────────────────────────┤
│ SALE #1052                      │
│ Submitted: Today, 14:35         │
│ Executive: Rahul                │
│ Shop: Downtown                  │
├─────────────────────────────────┤
│ ITEMS SOLD                      │
│ ┌───────────────────────────┐   │
│ │ Royal Stag Premium        │   │
│ │ 10 units × ₹650 = ₹6,500  │   │
│ │ ✓ Price verified          │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Old Monk                  │   │
│ │ 12 units × ₹380 = ₹4,560  │   │
│ │ ✓ Price verified          │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Kingfisher Strong         │   │
│ │ Regular: 18 × ₹160 = ₹2,880│  │
│ │ Discount: 6 × ₹140 = ₹840 │   │
│ │ Remark: "Loyal Customer"  │   │
│ │ ✓ Discount policy applied │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Bira White                │   │
│ │ 8 units × ₹160 = ₹1,280   │   │
│ │ ✓ Price verified          │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ SALES SUMMARY                   │
│ Subtotal: ₹16,060               │
│ Tax (9%): ₹1,445.40             │
│ Total: ₹15,400                  │
├─────────────────────────────────┤
│ INVENTORY IMPACT                │
│ All products in stock           │
│ No low stock alerts after sale  │
├─────────────────────────────────┤
│ ASSISTANT MANAGER REVIEW        │
│ ┌───────────────────────────┐   │
│ │ Verification:             │   │
│ │ ✓ All prices verified     │   │
│ │ ✓ Quantities available    │   │
│ │ ✓ Discount policy applied │   │
│ │ ✓ Math calculations OK    │   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ Comment:                  │   │
│ │ Discount properly applied │   │
│ │ for loyal customer.       │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ ACTION OPTIONS                  │
│ ◉ Approve                       │
│ ○ Forward to Manager            │
│ ○ Reject                        │
├─────────────────────────────────┤
│ [ Submit Review ]               │
└─────────────────────────────────┘
```

### Stock Adjustment Review
```
┌─────────────────────────────────┐
│ ← Stock Adjustment Review       │
├─────────────────────────────────┤
│ ADJUSTMENT #483                 │
│ Submitted: Today, 13:20         │
│ Executive: Rahul                │
│ Shop: Downtown                  │
├─────────────────────────────────┤
│ ITEMS ADJUSTED                  │
│ ┌───────────────────────────┐   │
│ │ Kingfisher Premium        │   │
│ │ Previous: 42   New: 38    │   │
│ │ Change: -4                │   │
│ │ • Regular Sale: 2         │   │
│ │ • Discount: 1 (₹140)      │   │
│ │ • Breakage: 1             │   │
│ │ ✓ Quantities match system │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Kingfisher Strong         │   │
│ │ Previous: 36   New: 30    │   │
│ │ Change: -6                │   │
│ │ • Regular Sale: 4         │   │
│ │ • Discount: 2 (₹140)      │   │
│ │ ✓ Quantities match system │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Royal Stag Premium        │   │
│ │ Previous: 28   New: 25    │   │
│ │ Change: -3                │   │
│ │ • Regular Sale: 3         │   │
│ │ ✓ Quantities match system │   │
│ └───────────────────────────┘   │
│ [View All Items (2 more)]       │
├─────────────────────────────────┤
│ ADJUSTMENT REASON               │
│ Daily closing stock count       │
├─────────────────────────────────┤
│ ASSISTANT MANAGER REVIEW        │
│ ┌───────────────────────────┐   │
│ │ Verification:             │   │
│ │ ✓ All quantities verified │   │
│ │ ✓ Discount prices correct │   │
│ │ ✓ Reason appropriate      │   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ Comment:                  │   │
│ │ All adjustments verified  │   │
│ │ against sales records.    │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ ACTION OPTIONS                  │
│ ◉ Approve                       │
│ ○ Forward to Manager            │
│ ○ Reject                        │
├─────────────────────────────────┤
│ [ Submit Review ]               │
└─────────────────────────────────┘
```

### Deposit Verification Screen
```
┌─────────────────────────────────┐
│ ← Deposit Verification          │
├─────────────────────────────────┤
│ DEPOSIT #135                    │
│ Status: Pending Verification    │
│ Submitted: Today, 16:05         │
│ Executive: Rahul                │
│ Shop: Downtown                  │
├─────────────────────────────────┤
│ DEPOSIT DETAILS                 │
│ ┌───────────────────────────┐   │
│ │ Amount: ₹25,000           │   │
│ │ Date: 20/03/2025          │   │
│ │ Bank: SBI                 │   │
│ │ Account: XXXXXXX7842      │   │
│ │ Reference: DEP78652341    │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ DEPOSIT RECEIPT                 │
│ ┌───────────────────────────┐   │
│ │ [📷 RECEIPT IMAGE]        │   │
│ │                           │   │
│ │ [View Full Image]         │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ CASH RECONCILIATION             │
│ ┌───────────────────────────┐   │
│ │ Opening Balance: ₹8,200   │   │
│ │ + Cash Sales:    ₹24,500  │   │
│ │ - Expenses:      ₹1,200   │   │
│ │ - This Deposit:  ₹25,000  │   │
│ │ = Remaining:     ₹6,500   │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ VERIFICATION CHECKS             │
│ ✓ Receipt date matches          │
│ ✓ Receipt amount matches        │
│ ✓ Bank details match            │
│ ✓ Reference number valid        │
├─────────────────────────────────┤
│ ASSISTANT MANAGER REVIEW        │
│ ┌───────────────────────────┐   │
│ │ Comment:                  │   │
│ │ Receipt verified and      │   │
│ │ matches system records.   │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ ACTION OPTIONS                  │
│ ◉ Forward to Manager            │
│ ○ Approve (if authorized)       │
│ ○ Reject                        │
├─────────────────────────────────┤
│ [ Submit Review ]               │
└─────────────────────────────────┘
```

## 3. Inventory Management

### Stock Levels Screen
```
┌─────────────────────────────────┐
│ ← Stock Levels              🔍  │
├─────────────────────────────────┤
│ 🏪 Downtown Shop   🗃️ All Brands▼│
├─────────────────────────────────┤
│ FILTER BY:                      │
│ [Category ▼] [Low Stock ✓]      │
├─────────────────────────────────┤
│ WHISKY                          │
│ ┌───────────────────────────┐   │
│ │ Royal Stag Premium        │   │
│ │ Current: 18   Min: 20 ⚠️  │   │
│ │ 7-day Sales: 84 units     │   │
│ │ [Adjust] [Transfer In]    │   │
│ └───────────────────────────┘   │
│                                 │
│ BEER                           │
│ ┌───────────────────────────┐   │
│ │ Kingfisher Premium        │   │
│ │ Current: 38   Min: 30 ✅  │   │
│ │ 7-day Sales: 68 units     │   │
│ │ [Adjust] [Transfer In]    │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Kingfisher Strong         │   │
│ │ Current: 12   Min: 40 ⚠️  │   │
│ │ 7-day Sales: 120 units    │   │
│ │ [Adjust] [Transfer In]    │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Bira White                │   │
│ │ Current: 35   Min: 30 ✅  │   │
│ │ 7-day Sales: 58 units     │   │
│ │ [Adjust] [Transfer In]    │   │
│ └───────────────────────────┘   │
│                                 │
│ RUM                            │
│ ┌───────────────────────────┐   │
│ │ Old Monk                  │   │
│ │ Current: 8    Min: 15 ⚠️  │   │
│ │ 7-day Sales: 46 units     │   │
│ │ [Adjust] [Transfer In]    │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ ACTIONS                         │
│ [Suggest Purchase Order]        │
│ [Generate Stock Report]         │
└─────────────────────────────────┘
```

### Stock Transfer Initiation
```
┌─────────────────────────────────┐
│ ← Initiate Stock Transfer       │
├─────────────────────────────────┤
│ TRANSFER DETAILS                │
│ ┌───────────────────────────┐   │
│ │ From Shop:                │   │
│ │ [Mall Branch__________] ▼ │   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ To Shop:                  │   │
│ │ [Downtown Shop________] ▼ │   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ Transfer Date:            │   │
│ │ [20/03/2025________] 🗓️   │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ ITEMS TO TRANSFER               │
│ ┌───────────────────────────┐   │
│ │ Kingfisher Strong         │   │
│ │ Source Stock: 68          │   │
│ │ Transfer Qty: [40]        │   │
│ │ Destination Stock: 12     │   │
│ │ After Transfer: 52        │   │
│ │ [Remove]                  │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Old Monk                  │   │
│ │ Source Stock: 22          │   │
│ │ Transfer Qty: [15]        │   │
│ │ Destination Stock: 8      │   │
│ │ After Transfer: 23        │   │
│ │ [Remove]                  │   │
│ └───────────────────────────┘   │
│ [ + Add More Products ]         │
├─────────────────────────────────┤
│ TRANSFER REASON                 │
│ ┌───────────────────────────┐   │
│ │ Addressing low stock at   │   │
│ │ Downtown Shop             │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ TRANSPORT DETAILS               │
│ ┌───────────────────────────┐   │
│ │ Transport Method:         │   │
│ │ [Company Vehicle_______] ▼│   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ Handled By:               │   │
│ │ [Suresh (Driver)________] │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ ACTION OPTIONS                  │
│ ◉ Submit for Approval           │
│ ○ Save as Draft                 │
├─────────────────────────────────┤
│ [ Process Transfer ]            │
└─────────────────────────────────┘
```

### Expiry Tracking
```
┌─────────────────────────────────┐
│ ← Expiry Management         🔍 │
├─────────────────────────────────┤
│ 🏪 Downtown Shop                │
├─────────────────────────────────┤
│ FILTER BY                       │
│ ┌──────────┐ ┌──────────┐       │
│ │ Next 30  │ │  Next 60 │       │
│ │   Days   │ │   Days   │       │
│ └──────────┘ └──────────┘       │
│ ┌──────────┐ ┌──────────┐       │
│ │ Already  │ │All Expiry│       │
│ │ Expired  │ │   Items  │       │
│ └──────────┘ └──────────┘       │
├─────────────────────────────────┤
│ EXPIRING PRODUCTS               │
│ ┌───────────────────────────┐   │
│ │ Carlsberg Elephant        │   │
│ │ Batch: BT45873            │   │
│ │ Expires: 15 days          │   │
│ │ Quantity: 24 bottles      │   │
│ │ [Suggest Action]          │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Corona Extra              │   │
│ │ Batch: BT42190            │   │
│ │ Expires: 22 days          │   │
│ │ Quantity: 18 bottles      │   │
│ │ [Suggest Action]          │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Bacardi White Rum         │   │
│ │ Batch: BT41005            │   │
│ │ Expires: 28 days          │   │
│ │ Quantity: 6 bottles       │   │
│ │ [Suggest Action]          │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ EXPIRED PRODUCTS                │
│ ┌───────────────────────────┐   │
│ │ Budweiser                 │   │
│ │ Batch: BT38721            │   │
│ │ Expired: 2 days ago       │   │
│ │ Quantity: 4 bottles       │   │
│ │ [Suggest Disposal]        │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ ACTIONS                         │
│ [ Suggest Promotion ]           │
│ [ Generate Expiry Report ]      │
└─────────────────────────────────┘
```

## 4. Purchase Management

### Create Purchase Order Screen
```
┌─────────────────────────────────┐
│ ← Create Purchase Order         │
├─────────────────────────────────┤
│ 🏪 Downtown Shop                │
├─────────────────────────────────┤
│ SUPPLIER DETAILS                │
│ ┌───────────────────────────┐   │
│ │ Select Supplier:          │   │
│ │ [United Breweries______] ▼│   │
│ └───────────────────────────┘   │
│ Contact: Ramesh Sharma          │
│ Phone: +91 9876543210           │
│ Email: ramesh.s@ublmail.com     │
├─────────────────────────────────┤
│ ORDER DETAILS                   │
│ ┌───────────────────────────┐   │
│ │ Expected Delivery:        │   │
│ │ [25/03/2025________] 🗓️   │   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ Payment Terms:            │   │
│ │ [Net 30 Days__________] ▼ │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ ORDER ITEMS                     │
│ ┌───────────────────────────┐   │
│ │ Kingfisher Premium        │   │
│ │ Current Stock: 38         │   │
│ │ Suggested: 60             │   │
│ │ Order Qty: [60]           │   │
│ │ Rate: ₹120                │   │
│ │ Amount: ₹7,200            │   │
│ │ [Remove]                  │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Kingfisher Strong         │   │
│ │ Current Stock: 12 ⚠️       │   │
│ │ Suggested: 120            │   │
│ │ Order Qty: [120]          │   │
│ │ Rate: ₹130                │   │
│ │ Amount: ₹15,600           │   │
│ │ [Remove]                  │   │
│ └───────────────────────────┘   │
│ [+ Add More Items]              │
├─────────────────────────────────┤
│ ORDER SUMMARY                   │
│ ┌───────────────────────────┐   │
│ │ Total Items: 2            │   │
│ │ Total Quantity: 180       │   │
│ │ Subtotal: ₹22,800         │   │
│ │ Tax (18%): ₹4,104         │   │
│ │ Total: ₹26,904            │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ NOTES                           │
│ ┌───────────────────────────┐   │
│ │ Priority delivery for     │   │
│ │ Kingfisher Strong         │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ ACTION OPTIONS                  │
│ ◉ Submit for Approval           │
│ ○ Save as Draft                 │
├─────────────────────────────────┤
│ [ Submit Purchase Order ]       │
└─────────────────────────────────┘
```



### Receive Inventory (continued)
```
┌─────────────────────────────────┐
│ ← Receive Inventory             │
├─────────────────────────────────┤
│ PURCHASE ORDER DETAILS          │
│ PO #286 - Radico Khaitan        │
│ Ordered: Yesterday, 14:20       │
│ Expected: 25/03/2025            │
├─────────────────────────────────┤
│ DELIVERY DETAILS                │
│ ┌───────────────────────────┐   │
│ │ Delivery Date:            │   │
│ │ [20/03/2025________] 🗓️   │   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ Invoice Number:           │   │
│ │ [INV-RK-20952___________] │   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ Delivered By:             │   │
│ │ [Sunil Kumar_____________]│   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ RECEIVE ITEMS                   │
│ ┌───────────────────────────┐   │
│ │ 8PM Whisky                │   │
│ │ Ordered: 24 bottles       │   │
│ │ Received: [24]            │   │
│ │ Batch: [BT58921________]  │   │
│ │ Expiry: [05/01/2026___] 🗓️│   │
│ │ [✓ Received in good condition]│
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Rampur Single Malt        │   │
│ │ Ordered: 12 bottles       │   │
│ │ Received: [12]            │   │
│ │ Batch: [BT58922________]  │   │
│ │ Expiry: [15/02/2026___] 🗓️│   │
│ │ [✓ Received in good condition]│
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ Jaisalmer Gin             │   │
│ │ Ordered: 18 bottles       │   │
│ │ Received: [16]            │   │
│ │ Batch: [BT58923________]  │   │
│ │ Expiry: [10/01/2026___] 🗓️│   │
│ │ [✓ Received in good condition]│
│ │ Note: 2 bottles short     │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ RECEIPT PHOTOS                  │
│ ┌───────────────────────────┐   │
│ │ [📷 Take Photo]           │   │
│ │ [📁 Choose from Gallery]  │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ NOTES                           │
│ ┌───────────────────────────┐   │
│ │ 2 bottles of Jaisalmer    │   │
│ │ Gin short delivery.       │   │
│ │ Supplier to adjust in     │   │
│ │ next order.               │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ [ Save Draft ] [ Complete ]     │
└─────────────────────────────────┘
```

### Purchase Orders Tracking
```
┌─────────────────────────────────┐
│ ← Purchase Orders           🔍 │
├─────────────────────────────────┤
│ 🏪 Downtown Shop                │
├─────────────────────────────────┤
│ FILTER BY STATUS                │
│ ┌────────┐ ┌────────┐ ┌────────┐│
│ │ Draft  │ │Ordered │ │Received││
│ │   2    │ │   3    │ │   5    ││
│ └────────┘ └────────┘ └────────┘│
├─────────────────────────────────┤
│ DRAFT ORDERS                    │
│ ┌───────────────────────────┐   │
│ │ PO #289 - United Breweries│   │
│ │ Created: Today, 15:30     │   │
│ │ Items: 3                  │   │
│ │ Value: ₹45,600            │   │
│ │ Status: Awaiting Approval │   │
│ │ [View] [Edit]             │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ PO #290 - Diageo India    │   │
│ │ Created: Today, 16:45     │   │
│ │ Items: 4                  │   │
│ │ Value: ₹62,800            │   │
│ │ Status: Draft             │   │
│ │ [View] [Edit]             │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ ORDERED                         │
│ ┌───────────────────────────┐   │
│ │ PO #286 - Radico Khaitan  │   │
│ │ Ordered: Yesterday, 14:20 │   │
│ │ Expected: 25/03/2025      │   │
│ │ Items: 5                  │   │
│ │ Value: ₹38,400            │   │
│ │ [View] [Receive]          │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ PO #285 - Pernod Ricard   │   │
│ │ Ordered: Yesterday, 11:30 │   │
│ │ Expected: 24/03/2025      │   │
│ │ Items: 4                  │   │
│ │ Value: ₹72,600            │   │
│ │ [View] [Receive]          │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ RECENTLY RECEIVED               │
│ ┌───────────────────────────┐   │
│ │ PO #283 - United Breweries│   │
│ │ Received: Today, 10:15    │   │
│ │ Items: 3/3 received       │   │
│ │ Value: ₹36,400            │   │
│ │ [View Details]            │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ [ Create New Purchase Order ]   │
└─────────────────────────────────┘
```

## 5. Analytics & Reporting

### Analytics Dashboard
```
┌─────────────────────────────────┐
│ ← Analytics Dashboard       📤  │
├─────────────────────────────────┤
│ 🏪 Downtown Shop   📅 This Week▼ │
├─────────────────────────────────┤
│ SALES PERFORMANCE               │
│ ┌───────────────────────────┐   │
│ │ 📈                         │   │
│ │                           │   │
│ │  [SALES TREND CHART]      │   │
│ │                           │   │
│ │                           │   │
│ └───────────────────────────┘   │
│ Total: ₹245,800                 │
│ Target: ₹240,000 (102%)         │
│ Growth: +8% vs Last Week        │
├─────────────────────────────────┤
│ CATEGORY BREAKDOWN              │
│ ┌───────────────────────────┐   │
│ │ 🍩                         │   │
│ │                           │   │
│ │  [CATEGORY PIE CHART]     │   │
│ │                           │   │
│ │                           │   │
│ └───────────────────────────┘   │
│ Whisky: ₹108,152 (44%)          │
│ Rum: ₹78,656 (32%)              │
│ Beer: ₹58,992 (24%)             │
├─────────────────────────────────┤
│ TOP SELLING BRANDS              │
│ ┌───────────────────────────┐   │
│ │ 📊                         │   │
│ │                           │   │
│ │  [BRANDS BAR CHART]       │   │
│ │                           │   │
│ │                           │   │
│ └───────────────────────────┘   │
│ 1. Royal Stag    - ₹45,400      │
│ 2. Old Monk      - ₹32,800      │
│ 3. Kingfisher    - ₹28,600      │
│ [View All Brands]                │
├─────────────────────────────────┤
│ EXECUTIVE PERFORMANCE           │
│ ┌───────────────────────────┐   │
│ │ 📊                         │   │
│ │                           │   │
│ │  [EXECUTIVE BAR CHART]    │   │
│ │                           │   │
│ │                           │   │
│ └───────────────────────────┘   │
│ Rahul: ₹98,320 (40%)            │
│ Priya: ₹73,740 (30%)            │
│ Sanjay: ₹73,740 (30%)           │
│ [View Detailed Performance]      │
├─────────────────────────────────┤
│ INVENTORY INSIGHTS              │
│ ┌───────────────────────────┐   │
│ │ Low Stock Items: 5        │   │
│ │ Fast Moving: 8 items      │   │
│ │ Slow Moving: 3 items      │   │
│ │ Expiring Soon: 3 items    │   │
│ │ [View Inventory Analytics]│   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ [ Export Analytics ]            │
└─────────────────────────────────┘
```

### Generate Reports Screen
```
┌─────────────────────────────────┐
│ ← Generate Reports              │
├─────────────────────────────────┤
│ 🏪 Downtown Shop                │
├─────────────────────────────────┤
│ REPORT TYPE                     │
│ ┌───────────────────────────┐   │
│ │ Select Report Type:       │   │
│ │ [Sales Report__________] ▼│   │
│ └───────────────────────────┘   │
│                                 │
│ Available Report Types:         │
│ • Sales Report                  │
│ • Inventory Report              │
│ • Stock Adjustment Report       │
│ • Executive Performance         │
│ • Brand Performance             │
│ • Expiry Report                 │
├─────────────────────────────────┤
│ DATE RANGE                      │
│ ┌───────────────────────────┐   │
│ │ Date Range:               │   │
│ │ [Last 7 Days___________] ▼│   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ Start Date:               │   │
│ │ [14/03/2025________] 🗓️   │   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ End Date:                 │   │
│ │ [20/03/2025________] 🗓️   │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ REPORT FILTERS                  │
│ ┌───────────────────────────┐   │
│ │ Group By:                 │   │
│ │ [Brand________________] ▼ │   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ Executive:                │   │
│ │ [All Executives________] ▼│   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ Brand Category:           │   │
│ │ [All Categories________] ▼│   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ REPORT OPTIONS                  │
│ ☑️ Include Charts               │
│ ☑️ Include Brand Breakdown      │
│ ☑️ Include Payment Methods      │
│ ☑️ Include Executive Details    │
│ ☐ Include Tax Details           │
├─────────────────────────────────┤
│ DELIVERY METHOD                 │
│ ◉ View Online                   │
│ ○ Download PDF                  │
│ ○ Download Excel                │
│ ○ Email Report                  │
├─────────────────────────────────┤
│ [ Generate Report ]             │
└─────────────────────────────────┘
```

## 6. Settings & Account

### Profile Settings
```
┌─────────────────────────────────┐
│ ← Profile Settings              │
├─────────────────────────────────┤
│                                 │
│ [👤 User Profile Picture]       │
│ [ Change Photo ]                │
├─────────────────────────────────┤
│ PERSONAL INFORMATION            │
│ ┌───────────────────────────┐   │
│ │ Full Name:                │   │
│ │ [Vikram Singh___________] │   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ Email:                    │   │
│ │ [vikram.s@example.com____]│   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ Mobile Number:            │   │
│ │ [+91 9876543212_________] │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ ACCOUNT SETTINGS                │
│ [ Change Password ]             │
│ [ Enable Biometric Login ]      │
├─────────────────────────────────┤
│ NOTIFICATION PREFERENCES        │
│ ☑️ Push Notifications           │
│ ☑️ New Approval Requests        │
│ ☑️ Low Stock Alerts             │
│ ☑️ Expiry Alerts                │
│ ☑️ Purchase Order Updates       │
│ ☐ Marketing Communications      │
├─────────────────────────────────┤
│ DISPLAY PREFERENCES             │
│ ┌───────────────────────────┐   │
│ │ Default Shop:             │   │
│ │ [Downtown Shop_________] ▼ │   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ Default Currency:         │   │
│ │ [Indian Rupee (₹)______] ▼│   │
│ └───────────────────────────┘   │
│                                 │
│ Theme:                          │
│ ○ Light  ● Dark  ○ System       │
├─────────────────────────────────┤
│ APPROVAL SETTINGS               │
│ ┌───────────────────────────┐   │
│ │ My approval limits:       │   │
│ │ • Sales up to ₹10,000     │   │
│ │ • Stock adjustments       │   │
│ │ • Cannot approve deposits │   │
│ │ [Request Change]          │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ APP INFORMATION                 │
│ Version: 1.2.0                  │
│ [ Check for Updates ]           │
│ [ Terms of Service ]            │
│ [ Privacy Policy ]              │
├─────────────────────────────────┤
│ [ Save Changes ]                │
└─────────────────────────────────┘
```

## 7. Notifications & Alerts

### Notifications Screen
```
┌─────────────────────────────────┐
│ ← Notifications                 │
├─────────────────────────────────┤
│ TODAY                           │
│ ┌───────────────────────────┐   │
│ │ ⚠️ Low Stock Alert        │   │
│ │ 5 products below minimum  │   │
│ │ stock levels.             │   │
│ │ Just now                  │   │
│ │ [View Products]           │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ 📦 New Approval Request   │   │
│ │ Sale #1052 for ₹15,400    │   │
│ │ from Rahul needs review.  │   │
│ │ 1 hour ago                │   │
│ │ [Review Now]              │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ 🛒 PO Delivery Update     │   │
│ │ PO #286 from Radico       │   │
│ │ Khaitan delivered early.  │   │
│ │ 2 hours ago               │   │
│ │ [Receive Inventory]       │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ 📊 Sales Target Update    │   │
│ │ Downtown Shop at 102% of  │   │
│ │ daily sales target.       │   │
│ │ 3 hours ago               │   │
│ │ [View Analytics]          │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ YESTERDAY                       │
│ ┌───────────────────────────┐   │
│ │ 🛒 Purchase Order Received│   │
│ │ PO #283 from United       │   │
│ │ Breweries delivered.      │   │
│ │ Yesterday, 10:15          │   │
│ │ [View Details]            │   │
│ └───────────────────────────┘   │
│ ┌───────────────────────────┐   │
│ │ 📦 Expiry Alert           │   │
│ │ 3 products will expire in │   │
│ │ the next 30 days.         │   │
│ │ Yesterday, 9:30           │   │
│ │ [View Products]           │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ [ Mark All as Read ]            │
└─────────────────────────────────┘
```

## 8. Help & Support

### Help & Support Screen
```
┌─────────────────────────────────┐
│ ← Help & Support                │
├─────────────────────────────────┤
│ SUPPORT OPTIONS                 │
│ ┌───────────────────────────┐   │
│ │ 📞 Contact Support        │   │
│ │ Call: +91 1800-123-4567   │   │
│ │ [Call Now]                │   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ 📧 Email Support          │   │
│ │ support@liquorshop.com    │   │
│ │ [Send Email]              │   │
│ └───────────────────────────┘   │
│                                 │
│ ┌───────────────────────────┐   │
│ │ 💬 Live Chat              │   │
│ │ Available: 9 AM - 6 PM    │   │
│ │ [Start Chat]              │   │
│ └───────────────────────────┘   │
├─────────────────────────────────┤
│ ASSISTANT MANAGER RESOURCES     │
│ [ Assistant Manager Guide ]     │
│ [ Training Videos ]             │
│ [ FAQs ]                        │
├─────────────────────────────────┤
│ QUICK HELP TOPICS               │
│ [ Review & Approval Process ]   │
│ [ Inventory Management ]        │
│ [ Purchase Orders ]             │
│ [ Reports & Analytics ]         │
├─────────────────────────────────┤
│ TROUBLESHOOTING                 │
│ [ Common Issues ]               │
│ [ System Diagnostics ]          │
│ [ Data Sync Troubleshooting ]   │
├─────────────────────────────────┤
│ GIVE FEEDBACK                   │
│ [ Report a Bug ]                │
│ [ Suggest a Feature ]           │
│ [ Rate the App ]                │
└─────────────────────────────────┘
```

## 9. Error & Status Screens

### No Internet Connection
```
┌─────────────────────────────────┐
│ Dashboard                       │
├─────────────────────────────────┤
│                                 │
│                                 │
│                                 │
│       [NO CONNECTION ICON]      │
│                                 │
│     No Internet Connection      │
│                                 │
│    Please check your network    │
│      settings and try again     │
│                                 │
│                                 │
│          [ Try Again ]          │
│                                 │
│                                 │
└─────────────────────────────────┘
```

### Loading State
```
┌─────────────────────────────────┐
│ ← Stock Levels                  │
├─────────────────────────────────┤
│ 🏪 Downtown Shop                │
├─────────────────────────────────┤
│                                 │
│                                 │
│                                 │
│           [LOADING SPINNER]     │
│                                 │
│          Loading Stock          │
│           Please wait           │
│                                 │
│                                 │
│                                 │
└─────────────────────────────────┘
```

### No Data Screen
```
┌─────────────────────────────────┐
│ ← Pending Approvals             │
├─────────────────────────────────┤
│ 🏪 Downtown Shop                │
├─────────────────────────────────┤
│                                 │
│                                 │
│                                 │
│       [EMPTY STATE ICON]        │
│                                 │
│      No Pending Approvals       │
│                                 │
│    All items have been          │
│    reviewed and processed       │
│                                 │
│                                 │
│                                 │
│     [ Refresh ] [ Go Back ]     │
│                                 │
│                                 │
└─────────────────────────────────┘
```