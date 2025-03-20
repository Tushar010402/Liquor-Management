# Comprehensive API Specification for Liquor Shop Management System

Below is a detailed breakdown of the API endpoints required for each page in the Liquor Shop Management System. This will serve as a guide for both frontend and backend development.

## Authentication APIs

### Authentication Endpoints
1. `POST /api/auth/login` - User login
2. `POST /api/auth/verify-2fa` - Verify two-factor authentication code
3. `POST /api/auth/forgot-password` - Request password reset
4. `POST /api/auth/reset-password` - Reset password with token
5. `POST /api/auth/verify-account` - Verify new account
6. `GET /api/auth/user` - Get current user profile
7. `POST /api/auth/logout` - User logout

## SaaS Admin APIs

### Dashboard & Overview
8. `GET /api/admin/dashboard` - Get admin dashboard data
9. `GET /api/admin/system-overview` - Get system overview metrics

### Tenant Management
10. `GET /api/admin/tenants` - Get list of all tenants with pagination
11. `POST /api/admin/tenants` - Create new tenant
12. `GET /api/admin/tenants/{id}` - Get tenant details
13. `PUT /api/admin/tenants/{id}` - Update tenant information
14. `DELETE /api/admin/tenants/{id}` - Deactivate tenant
15. `PATCH /api/admin/tenants/{id}/activate` - Activate tenant
16. `GET /api/admin/tenants/{id}/activity` - Get tenant activity logs
17. `GET /api/admin/tenants/{id}/users` - Get tenant users
18. `POST /api/admin/tenants/{id}/review` - Review tenant registration

### Billing & Plans
19. `GET /api/admin/billing/plans` - Get all billing plans
20. `POST /api/admin/billing/plans` - Create new billing plan
21. `GET /api/admin/billing/plans/{id}` - Get plan details
22. `PUT /api/admin/billing/plans/{id}` - Update billing plan
23. `DELETE /api/admin/billing/plans/{id}` - Delete billing plan
24. `GET /api/admin/tenants/{id}/billing` - Get tenant billing history
25. `GET /api/admin/billing/analytics` - Get revenue analytics data

### Team Management
26. `GET /api/admin/team` - Get all team members
27. `POST /api/admin/team` - Add new team member
28. `GET /api/admin/team/{id}` - Get team member details
29. `PUT /api/admin/team/{id}` - Update team member
30. `DELETE /api/admin/team/{id}` - Deactivate team member
31. `GET /api/admin/roles` - Get all roles
32. `POST /api/admin/roles` - Create new role
33. `GET /api/admin/roles/{id}` - Get role details
34. `PUT /api/admin/roles/{id}` - Update role
35. `DELETE /api/admin/roles/{id}` - Delete role
36. `GET /api/admin/permissions` - Get all permissions
37. `POST /api/admin/roles/{id}/permissions` - Assign permissions to role

### System Administration
38. `GET /api/admin/system/health` - Get system health metrics
39. `GET /api/admin/system/server-metrics` - Get server metrics
40. `GET /api/admin/system/database-metrics` - Get database metrics
41. `GET /api/admin/system/services` - Get services status
42. `GET /api/admin/system/api-usage` - Get API usage statistics
43. `GET /api/admin/system/error-logs` - Get system error logs
44. `GET /api/admin/system/config` - Get system configuration
45. `PUT /api/admin/system/config` - Update system configuration
46. `GET /api/admin/email-templates` - Get all email templates
47. `GET /api/admin/email-templates/{id}` - Get email template details
48. `PUT /api/admin/email-templates/{id}` - Update email template
49. `POST /api/admin/email-templates/test` - Test email template

### Backup & Restore
50. `GET /api/admin/backups` - Get backup history
51. `GET /api/admin/backups/schedule` - Get backup schedule
52. `PUT /api/admin/backups/schedule` - Update backup schedule
53. `POST /api/admin/backups` - Create manual backup
54. `POST /api/admin/restore` - Restore from backup
55. `GET /api/admin/backups/{id}` - Get backup details
56. `DELETE /api/admin/backups/{id}` - Delete backup

### Analytics & Monitoring
57. `GET /api/admin/analytics/platform` - Get platform analytics
58. `GET /api/admin/analytics/tenant-growth` - Get tenant growth metrics
59. `GET /api/admin/analytics/usage` - Get usage statistics
60. `GET /api/admin/monitoring/activity` - Get activity monitoring data
61. `GET /api/admin/monitoring/registrations` - Get user registrations

### Security & Compliance
62. `GET /api/admin/security/dashboard` - Get security dashboard data
63. `GET /api/admin/security/policies` - Get security policies
64. `PUT /api/admin/security/policies` - Update security policies
65. `GET /api/admin/audit-logs` - Get audit logs
66. `GET /api/admin/audit-logs/{id}` - Get audit log details
67. `GET /api/admin/compliance/reports` - Get compliance reports

### Implementation & Support
68. `GET /api/admin/implementation/dashboard` - Get implementation dashboard
69. `GET /api/admin/implementation/tenants/{id}/onboarding` - Get tenant onboarding checklist
70. `PUT /api/admin/implementation/tenants/{id}/onboarding` - Update onboarding status
71. `GET /api/admin/documentation` - Get documentation list
72. `GET /api/admin/documentation/{id}` - Get specific documentation

## Tenant Admin APIs

### Dashboard & Overview
73. `GET /api/tenant/dashboard` - Get tenant admin dashboard data

### Shop Management
74. `GET /api/tenant/shops` - Get all shops
75. `POST /api/tenant/shops` - Create new shop
76. `GET /api/tenant/shops/{id}` - Get shop details
77. `PUT /api/tenant/shops/{id}` - Update shop
78. `DELETE /api/tenant/shops/{id}` - Deactivate shop
79. `GET /api/tenant/shops/{id}/performance` - Get shop performance metrics

### Team Management
80. `GET /api/tenant/team` - Get all team members
81. `POST /api/tenant/team` - Add new team member
82. `GET /api/tenant/team/{id}` - Get team member details
83. `PUT /api/tenant/team/{id}` - Update team member
84. `DELETE /api/tenant/team/{id}` - Deactivate team member
85. `POST /api/tenant/team/{id}/shops` - Assign shops to team member
86. `GET /api/tenant/team/{id}/performance` - Get team member performance

### Brand Management
87. `GET /api/tenant/brands` - Get all brands
88. `POST /api/tenant/brands` - Create new brand
89. `GET /api/tenant/brands/{id}` - Get brand details
90. `PUT /api/tenant/brands/{id}` - Update brand
91. `DELETE /api/tenant/brands/{id}` - Deactivate brand
92. `GET /api/tenant/brand-categories` - Get all brand categories
93. `POST /api/tenant/brand-categories` - Create brand category
94. `PUT /api/tenant/brand-categories/{id}` - Update brand category
95. `DELETE /api/tenant/brand-categories/{id}` - Delete brand category
96. `POST /api/tenant/brands/bulk-update` - Bulk update brand prices

### Supplier Management
97. `GET /api/tenant/suppliers` - Get all suppliers
98. `POST /api/tenant/suppliers` - Create new supplier
99. `GET /api/tenant/suppliers/{id}` - Get supplier details
100. `PUT /api/tenant/suppliers/{id}` - Update supplier
101. `DELETE /api/tenant/suppliers/{id}` - Deactivate supplier
102. `GET /api/tenant/suppliers/{id}/products` - Get supplier products
103. `GET /api/tenant/suppliers/{id}/history` - Get supplier history
104. `GET /api/tenant/suppliers/{id}/contacts` - Get supplier contacts
105. `POST /api/tenant/suppliers/{id}/contacts` - Add supplier contact

### Tax Management
106. `GET /api/tenant/tax/categories` - Get all tax categories
107. `POST /api/tenant/tax/categories` - Create tax category
108. `GET /api/tenant/tax/categories/{id}` - Get tax category details
109. `PUT /api/tenant/tax/categories/{id}` - Update tax category
110. `DELETE /api/tenant/tax/categories/{id}` - Delete tax category
111. `POST /api/tenant/tax/assign` - Assign tax categories to products
112. `GET /api/tenant/tax/reports` - Get tax reports

### Financial Accounting
113. `GET /api/tenant/finance/dashboard` - Get financial dashboard
114. `GET /api/tenant/finance/accounts` - Get chart of accounts
115. `POST /api/tenant/finance/accounts` - Create account
116. `PUT /api/tenant/finance/accounts/{id}` - Update account
117. `GET /api/tenant/finance/ledger` - Get general ledger entries
118. `GET /api/tenant/finance/profit-loss` - Get profit & loss statement
119. `GET /api/tenant/finance/balance-sheet` - Get balance sheet
120. `GET /api/tenant/finance/reconciliation` - Get bank reconciliation data
121. `POST /api/tenant/finance/reconciliation` - Perform reconciliation

### Reports & Analytics
122. `GET /api/tenant/reports/dashboard` - Get reports dashboard
123. `POST /api/tenant/reports/generate` - Generate custom report
124. `GET /api/tenant/reports/{id}` - Get report data
125. `GET /api/tenant/analytics/sales` - Get sales analytics
126. `GET /api/tenant/analytics/inventory` - Get inventory analytics
127. `GET /api/tenant/analytics/staff` - Get staff performance analytics
128. `GET /api/tenant/analytics/finance` - Get financial analytics

### Settings & Configuration
129. `GET /api/tenant/settings/business` - Get business settings
130. `PUT /api/tenant/settings/business` - Update business settings
131. `GET /api/tenant/settings/approvals` - Get approval workflows
132. `PUT /api/tenant/settings/approvals` - Update approval workflows
133. `GET /api/tenant/settings/permissions` - Get role permissions
134. `PUT /api/tenant/settings/permissions` - Update role permissions
135. `GET /api/tenant/settings/notifications` - Get notification settings
136. `PUT /api/tenant/settings/notifications` - Update notification settings
137. `POST /api/tenant/data/import` - Import data
138. `POST /api/tenant/data/export` - Export data

## Manager APIs

### Dashboard & Overview
139. `GET /api/manager/dashboard` - Get manager dashboard data
140. `GET /api/manager/shops` - Get assigned shops

### Approvals
141. `GET /api/manager/approvals` - Get all pending approvals
142. `GET /api/manager/approvals/sales` - Get pending sales approvals
143. `GET /api/manager/approvals/sales/{id}` - Get sale approval details
144. `POST /api/manager/approvals/sales/{id}` - Process sale approval
145. `GET /api/manager/approvals/stock` - Get pending stock adjustments
146. `GET /api/manager/approvals/stock/{id}` - Get stock adjustment details
147. `POST /api/manager/approvals/stock/{id}` - Process stock adjustment
148. `GET /api/manager/approvals/returns` - Get pending returns
149. `GET /api/manager/approvals/returns/{id}` - Get return details
150. `POST /api/manager/approvals/returns/{id}` - Process return
151. `GET /api/manager/approvals/deposits` - Get pending deposits
152. `GET /api/manager/approvals/deposits/{id}` - Get deposit details
153. `POST /api/manager/approvals/deposits/{id}` - Verify deposit
154. `POST /api/manager/approvals/batch` - Process batch approvals

### Inventory Management
155. `GET /api/manager/inventory/stock` - Get stock levels
156. `POST /api/manager/inventory/transfer` - Create stock transfer
157. `GET /api/manager/inventory/expiry` - Get expiring products
158. `POST /api/manager/inventory/expiry/{id}/action` - Take action on expiring product

### Purchase Management
159. `GET /api/manager/purchase/orders` - Get purchase orders
160. `POST /api/manager/purchase/orders` - Create purchase order
161. `GET /api/manager/purchase/orders/{id}` - Get purchase order details
162. `PUT /api/manager/purchase/orders/{id}` - Update purchase order
163. `POST /api/manager/purchase/receive` - Receive inventory

### Financial Verification
164. `GET /api/manager/finance/verification` - Get financial verification dashboard
165. `GET /api/manager/finance/reconciliation` - Get cash reconciliation data
166. `POST /api/manager/finance/reconciliation` - Perform reconciliation
167. `GET /api/manager/finance/tax` - Get tax management data

### Analytics & Reporting
168. `GET /api/manager/analytics/dashboard` - Get analytics dashboard
169. `GET /api/manager/analytics/executive` - Get executive performance
170. `POST /api/manager/reports/generate` - Generate custom report

## Assistant Manager APIs

### Dashboard & Overview
171. `GET /api/assistant/dashboard` - Get assistant manager dashboard

### Approvals
172. `GET /api/assistant/approvals` - Get all pending approvals
173. `GET /api/assistant/approvals/sales/{id}` - Get sale details
174. `POST /api/assistant/approvals/sales/{id}` - Process sale review
175. `GET /api/assistant/approvals/stock/{id}` - Get stock adjustment details
176. `POST /api/assistant/approvals/stock/{id}` - Process stock review
177. `GET /api/assistant/approvals/returns/{id}` - Get return details
178. `POST /api/assistant/approvals/returns/{id}` - Process return review

### Inventory Management
179. `GET /api/assistant/inventory/stock` - Get stock levels
180. `POST /api/assistant/inventory/transfer` - Initiate stock transfer
181. `GET /api/assistant/inventory/expiry` - Get expiring products

### Purchase Management
182. `POST /api/assistant/purchase/orders` - Create purchase order
183. `GET /api/assistant/purchase/orders` - Get purchase orders
184. `POST /api/assistant/purchase/receive` - Receive inventory

### Analytics
185. `GET /api/assistant/analytics/sales` - Get sales analytics
186. `GET /api/assistant/analytics/inventory` - Get inventory analytics
187. `GET /api/assistant/analytics/executive` - Get executive analytics

## Executive APIs

### Dashboard & Overview
188. `GET /api/executive/dashboard` - Get executive dashboard
189. `GET /api/executive/shops` - Get assigned shops

### Sales Management
190. `POST /api/executive/sales` - Create new sale
191. `POST /api/executive/sales/batch` - Create batch sale
192. `GET /api/executive/sales` - Get my sales
193. `GET /api/executive/sales/{id}` - Get sale details
194. `GET /api/executive/sales/drafts` - Get draft sales
195. `POST /api/executive/sales/drafts` - Save draft sale
196. `DELETE /api/executive/sales/drafts/{id}` - Delete draft sale

### Stock Management
197. `POST /api/executive/stock/adjust` - Create single stock adjustment
198. `POST /api/executive/stock/adjust/batch` - Create batch stock adjustment
199. `GET /api/executive/stock/adjustments` - Get my adjustments
200. `GET /api/executive/stock/adjustments/{id}` - Get adjustment details
201. `GET /api/executive/stock/expiry` - Get expiring products
202. `POST /api/executive/stock/expiry/{id}/report` - Report expired product

### Returns Management
203. `POST /api/executive/returns` - Create return
204. `GET /api/executive/returns` - Get my returns
205. `GET /api/executive/returns/{id}` - Get return details

### Cash Management
206. `GET /api/executive/cash/balance` - Get cash balance
207. `POST /api/executive/cash/deposit` - Record bank deposit
208. `POST /api/executive/cash/upi` - Record UPI transaction
209. `POST /api/executive/cash/expense` - Record expense
210. `GET /api/executive/cash/history` - Get cash history

### Daily Summary
211. `GET /api/executive/summary/daily` - Get daily summary
212. `POST /api/executive/summary/payment` - Record payment breakdown
213. `GET /api/executive/summary/brands` - Get brand-wise sales

### My Approvals
214. `GET /api/executive/approvals` - Get my approvals
215. `GET /api/executive/approvals/{id}` - Get approval details
216. `POST /api/executive/approvals/{id}/resubmit` - Resubmit rejected item

## Mobile App Specific APIs

217. `GET /api/mobile/sync/status` - Get sync status
218. `POST /api/mobile/sync` - Synchronize offline data
219. `GET /api/mobile/offline-queue` - Get offline queue
220. `GET /api/mobile/dashboard` - Get lightweight mobile dashboard
221. `POST /api/mobile/sales/quick` - Create quick sale
222. `POST /api/mobile/inventory/scan` - Scan inventory barcode

## System Integration APIs

223. `GET /api/integration/webhooks` - Get webhook configurations
224. `POST /api/integration/webhooks` - Create webhook
225. `PUT /api/integration/webhooks/{id}` - Update webhook
226. `DELETE /api/integration/webhooks/{id}` - Delete webhook
227. `GET /api/integration/payment-gateways` - Get payment gateway settings
228. `PUT /api/integration/payment-gateways` - Update payment gateway settings
229. `GET /api/integration/sms` - Get SMS integration settings
230. `PUT /api/integration/sms` - Update SMS integration settings
231. `GET /api/integration/third-party` - Get third-party integrations
232. `POST /api/integration/third-party` - Configure third-party integration

## Additional APIs Required for Complete Functionality

### Inventory & Product Management
233. `GET /api/tenant/inventory/stock` - Get complete inventory stock
234. `GET /api/tenant/inventory/stock/{id}` - Get product stock details
235. `GET /api/tenant/inventory/transactions` - Get inventory transactions
236. `GET /api/tenant/inventory/transfers` - Get stock transfers
237. `GET /api/tenant/inventory/adjustments` - Get all stock adjustments

### Sales & Transactions
238. `GET /api/tenant/sales` - Get all sales
239. `GET /api/tenant/sales/{id}` - Get sale details
240. `GET /api/tenant/returns` - Get all returns
241. `GET /api/tenant/transactions` - Get all financial transactions

### Common Lookup APIs
242. `GET /api/common/countries` - Get countries list
243. `GET /api/common/states` - Get states list
244. `GET /api/common/cities` - Get cities list
245. `GET /api/common/currencies` - Get currencies list
246. `GET /api/common/timezones` - Get timezones list

### File Management
247. `POST /api/files/upload` - Upload file
248. `GET /api/files/{id}` - Get file
249. `DELETE /api/files/{id}` - Delete file

## API Response Structure Recommendations

For consistency across all APIs, I recommend the following standard response structure:

### Success Response
```json
{
  "success": true,
  "data": {
    // Response data specific to the API endpoint
  },
  "message": "Operation completed successfully",
  "timestamp": "2025-03-20T10:15:30Z"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Description of the error",
    "details": [] // Optional array with detailed error information
  },
  "timestamp": "2025-03-20T10:15:30Z"
}
```

## Implementation Recommendations

To efficiently implement this large system, consider the following approach:

1. **API Grouping and Prioritization**:
   - Group APIs by functionality and user role
   - Prioritize core features first (authentication, basic CRUD operations)
   - Implement advanced features in later phases

2. **Use API Gateway Pattern**:
   - Implement a central API gateway to handle routing, authentication, and logging
   - This simplifies security and monitoring across all endpoints

3. **Module-Based Development**:
   - Divide backend into microservices or modules (Auth, Tenant, Inventory, Sales, etc.)
   - Allows parallel development by different teams

4. **Generate API Documentation**:
   - Use tools like Swagger/OpenAPI to document all endpoints
   - This helps frontend and backend teams stay in sync

5. **Implement Versioning**:
   - Use API versioning (e.g., `/api/v1/...`) to allow for future changes
   - This enables smoother updates without breaking existing clients

6. **Testing Strategy**:
   - Create automated tests for all API endpoints
   - Implement integration tests for critical workflows

This comprehensive API specification covers all the functionality needed for the Liquor Shop Management System. By implementing these endpoints, you'll have a complete backend that supports all the features across different user roles.

Would you like me to provide more detailed specifications for any particular API group or suggestions for technology stack selection?