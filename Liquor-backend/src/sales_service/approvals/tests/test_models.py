import uuid
from django.test import TestCase
from django.utils import timezone
from sales_service.approvals.models import Approval, ApprovalHistory, BatchApproval, BatchApprovalItem

class ApprovalModelsTest(TestCase):
    """
    Test the approval models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.shop_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.reference_id = uuid.uuid4()
        
        # Create approval
        self.approval = Approval.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            approval_number="APR-2023-0001",
            approval_type=Approval.TYPE_SALE,
            status=Approval.STATUS_PENDING,
            priority=Approval.PRIORITY_HIGH,
            reference_id=self.reference_id,
            reference_number="INV-2023-0001",
            reference_data={
                "total_amount": "5000.00",
                "discount_amount": "500.00",
                "customer_name": "John Doe"
            },
            notes="Approval needed for high-value sale",
            requested_by=self.user_id,
            requested_by_name="John Smith",
            created_by=self.user_id
        )
        
        # Create approval history
        self.approval_history = ApprovalHistory.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            approval=self.approval,
            action=ApprovalHistory.ACTION_CREATED,
            user_id=self.user_id,
            user_name="John Smith",
            notes="Approval request created",
            created_by=self.user_id
        )
        
        # Create batch approval
        self.batch_approval = BatchApproval.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            batch_number="BATCH-2023-0001",
            status=BatchApproval.STATUS_PENDING,
            total_approvals=2,
            notes="Batch approval for end of day",
            processed_by=self.user_id,
            processed_by_name="John Smith",
            created_by=self.user_id
        )
        
        # Create batch approval item
        self.batch_approval_item = BatchApprovalItem.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            batch=self.batch_approval,
            approval=self.approval,
            action=BatchApprovalItem.ACTION_APPROVE,
            notes="Approve this sale",
            created_by=self.user_id
        )
    
    def test_approval_creation(self):
        """
        Test Approval creation.
        """
        self.assertEqual(self.approval.tenant_id, self.tenant_id)
        self.assertEqual(self.approval.shop_id, self.shop_id)
        self.assertEqual(self.approval.approval_number, "APR-2023-0001")
        self.assertEqual(self.approval.approval_type, Approval.TYPE_SALE)
        self.assertEqual(self.approval.status, Approval.STATUS_PENDING)
        self.assertEqual(self.approval.priority, Approval.PRIORITY_HIGH)
        self.assertEqual(self.approval.reference_id, self.reference_id)
        self.assertEqual(self.approval.reference_number, "INV-2023-0001")
        self.assertEqual(self.approval.reference_data["total_amount"], "5000.00")
        self.assertEqual(self.approval.reference_data["discount_amount"], "500.00")
        self.assertEqual(self.approval.reference_data["customer_name"], "John Doe")
        self.assertEqual(self.approval.notes, "Approval needed for high-value sale")
        self.assertEqual(self.approval.requested_by, self.user_id)
        self.assertEqual(self.approval.requested_by_name, "John Smith")
        self.assertIsNone(self.approval.approved_by)
        self.assertEqual(self.approval.approved_by_name, "")
        self.assertIsNone(self.approval.approved_at)
        self.assertEqual(self.approval.rejection_reason, "")
        self.assertEqual(self.approval.created_by, self.user_id)
    
    def test_approval_str(self):
        """
        Test Approval string representation.
        """
        expected_str = "APR-2023-0001 - sale - pending"
        self.assertEqual(str(self.approval), expected_str)
    
    def test_approval_history_creation(self):
        """
        Test ApprovalHistory creation.
        """
        self.assertEqual(self.approval_history.tenant_id, self.tenant_id)
        self.assertEqual(self.approval_history.shop_id, self.shop_id)
        self.assertEqual(self.approval_history.approval, self.approval)
        self.assertEqual(self.approval_history.action, ApprovalHistory.ACTION_CREATED)
        self.assertEqual(self.approval_history.user_id, self.user_id)
        self.assertEqual(self.approval_history.user_name, "John Smith")
        self.assertEqual(self.approval_history.notes, "Approval request created")
        self.assertEqual(self.approval_history.created_by, self.user_id)
    
    def test_approval_history_str(self):
        """
        Test ApprovalHistory string representation.
        """
        expected_str = f"APR-2023-0001 - created - {self.approval_history.action_date}"
        self.assertEqual(str(self.approval_history), expected_str)
    
    def test_batch_approval_creation(self):
        """
        Test BatchApproval creation.
        """
        self.assertEqual(self.batch_approval.tenant_id, self.tenant_id)
        self.assertEqual(self.batch_approval.shop_id, self.shop_id)
        self.assertEqual(self.batch_approval.batch_number, "BATCH-2023-0001")
        self.assertEqual(self.batch_approval.status, BatchApproval.STATUS_PENDING)
        self.assertEqual(self.batch_approval.total_approvals, 2)
        self.assertEqual(self.batch_approval.approved_count, 0)
        self.assertEqual(self.batch_approval.rejected_count, 0)
        self.assertEqual(self.batch_approval.notes, "Batch approval for end of day")
        self.assertEqual(self.batch_approval.processed_by, self.user_id)
        self.assertEqual(self.batch_approval.processed_by_name, "John Smith")
        self.assertEqual(self.batch_approval.created_by, self.user_id)
    
    def test_batch_approval_str(self):
        """
        Test BatchApproval string representation.
        """
        expected_str = "BATCH-2023-0001 - 2 approvals"
        self.assertEqual(str(self.batch_approval), expected_str)
    
    def test_batch_approval_item_creation(self):
        """
        Test BatchApprovalItem creation.
        """
        self.assertEqual(self.batch_approval_item.tenant_id, self.tenant_id)
        self.assertEqual(self.batch_approval_item.shop_id, self.shop_id)
        self.assertEqual(self.batch_approval_item.batch, self.batch_approval)
        self.assertEqual(self.batch_approval_item.approval, self.approval)
        self.assertEqual(self.batch_approval_item.action, BatchApprovalItem.ACTION_APPROVE)
        self.assertEqual(self.batch_approval_item.notes, "Approve this sale")
        self.assertEqual(self.batch_approval_item.created_by, self.user_id)
    
    def test_batch_approval_item_str(self):
        """
        Test BatchApprovalItem string representation.
        """
        expected_str = "BATCH-2023-0001 - APR-2023-0001 - approve"
        self.assertEqual(str(self.batch_approval_item), expected_str)
    
    def test_approval_approve(self):
        """
        Test approving an approval.
        """
        # Approve the approval
        self.approval.status = Approval.STATUS_APPROVED
        self.approval.approved_by = self.user_id
        self.approval.approved_by_name = "John Smith"
        self.approval.approved_at = timezone.now()
        self.approval.save()
        
        # Create approval history for the approval
        ApprovalHistory.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            approval=self.approval,
            action=ApprovalHistory.ACTION_APPROVED,
            user_id=self.user_id,
            user_name="John Smith",
            notes="Approval request approved",
            created_by=self.user_id
        )
        
        # Refresh from database
        self.approval.refresh_from_db()
        
        # Check that the approval was approved
        self.assertEqual(self.approval.status, Approval.STATUS_APPROVED)
        self.assertEqual(self.approval.approved_by, self.user_id)
        self.assertEqual(self.approval.approved_by_name, "John Smith")
        self.assertIsNotNone(self.approval.approved_at)
        
        # Check that the approval history was created
        approval_history = ApprovalHistory.objects.filter(
            approval=self.approval,
            action=ApprovalHistory.ACTION_APPROVED
        ).first()
        self.assertIsNotNone(approval_history)
        self.assertEqual(approval_history.user_id, self.user_id)
        self.assertEqual(approval_history.notes, "Approval request approved")
    
    def test_approval_reject(self):
        """
        Test rejecting an approval.
        """
        # Reject the approval
        self.approval.status = Approval.STATUS_REJECTED
        self.approval.rejection_reason = "Amount exceeds customer's credit limit"
        self.approval.save()
        
        # Create approval history for the rejection
        ApprovalHistory.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            approval=self.approval,
            action=ApprovalHistory.ACTION_REJECTED,
            user_id=self.user_id,
            user_name="John Smith",
            notes="Amount exceeds customer's credit limit",
            created_by=self.user_id
        )
        
        # Refresh from database
        self.approval.refresh_from_db()
        
        # Check that the approval was rejected
        self.assertEqual(self.approval.status, Approval.STATUS_REJECTED)
        self.assertEqual(self.approval.rejection_reason, "Amount exceeds customer's credit limit")
        
        # Check that the approval history was created
        approval_history = ApprovalHistory.objects.filter(
            approval=self.approval,
            action=ApprovalHistory.ACTION_REJECTED
        ).first()
        self.assertIsNotNone(approval_history)
        self.assertEqual(approval_history.user_id, self.user_id)
        self.assertEqual(approval_history.notes, "Amount exceeds customer's credit limit")
    
    def test_complete_batch_approval(self):
        """
        Test completing a batch approval.
        """
        # Create another approval
        approval2 = Approval.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            approval_number="APR-2023-0002",
            approval_type=Approval.TYPE_RETURN,
            status=Approval.STATUS_PENDING,
            priority=Approval.PRIORITY_MEDIUM,
            reference_id=uuid.uuid4(),
            reference_number="RET-2023-0001",
            reference_data={
                "total_amount": "2000.00",
                "reason": "Damaged product"
            },
            notes="Approval needed for return",
            requested_by=self.user_id,
            requested_by_name="John Smith",
            created_by=self.user_id
        )
        
        # Create batch approval item for the second approval
        BatchApprovalItem.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            batch=self.batch_approval,
            approval=approval2,
            action=BatchApprovalItem.ACTION_REJECT,
            notes="Reject this return",
            created_by=self.user_id
        )
        
        # Process the batch approval
        # First approval - approve
        self.approval.status = Approval.STATUS_APPROVED
        self.approval.approved_by = self.user_id
        self.approval.approved_by_name = "John Smith"
        self.approval.approved_at = timezone.now()
        self.approval.save()
        
        # Second approval - reject
        approval2.status = Approval.STATUS_REJECTED
        approval2.rejection_reason = "Return policy violation"
        approval2.save()
        
        # Update batch approval
        self.batch_approval.status = BatchApproval.STATUS_COMPLETED
        self.batch_approval.approved_count = 1
        self.batch_approval.rejected_count = 1
        self.batch_approval.save()
        
        # Refresh from database
        self.batch_approval.refresh_from_db()
        
        # Check that the batch approval was completed
        self.assertEqual(self.batch_approval.status, BatchApproval.STATUS_COMPLETED)
        self.assertEqual(self.batch_approval.approved_count, 1)
        self.assertEqual(self.batch_approval.rejected_count, 1)
        
        # Check that the approvals were updated
        self.approval.refresh_from_db()
        approval2.refresh_from_db()
        
        self.assertEqual(self.approval.status, Approval.STATUS_APPROVED)
        self.assertEqual(approval2.status, Approval.STATUS_REJECTED)
        self.assertEqual(approval2.rejection_reason, "Return policy violation")