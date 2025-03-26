import * as Yup from 'yup';

/**
 * Common validation schemas for forms
 */

// Email validation
export const emailSchema = Yup.string()
  .email('Enter a valid email')
  .required('Email is required');

// Password validation
export const passwordSchema = Yup.string()
  .min(8, 'Password should be of minimum 8 characters length')
  .matches(
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
    'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character'
  )
  .required('Password is required');

// Confirm password validation
export const confirmPasswordSchema = (passwordField: string) =>
  Yup.string()
    .oneOf([Yup.ref(passwordField)], 'Passwords must match')
    .required('Confirm password is required');

// Name validation
export const nameSchema = Yup.string()
  .min(2, 'Name should be of minimum 2 characters length')
  .max(50, 'Name should be of maximum 50 characters length')
  .required('Name is required');

// Phone validation
export const phoneSchema = Yup.string()
  .matches(
    /^[0-9]{10}$/,
    'Phone number must be 10 digits'
  )
  .required('Phone number is required');

// Amount validation
export const amountSchema = Yup.number()
  .positive('Amount must be positive')
  .required('Amount is required');

// Quantity validation
export const quantitySchema = Yup.number()
  .integer('Quantity must be an integer')
  .min(1, 'Quantity must be at least 1')
  .required('Quantity is required');

// Date validation
export const dateSchema = Yup.date()
  .required('Date is required');

// Required string validation
export const requiredStringSchema = Yup.string()
  .required('This field is required');

// Optional string validation
export const optionalStringSchema = Yup.string()
  .nullable();

// Required select validation
export const requiredSelectSchema = Yup.mixed()
  .required('Please select an option');

// Required array validation
export const requiredArraySchema = Yup.array()
  .min(1, 'Please select at least one option')
  .required('This field is required');

/**
 * Create a validation schema for a login form
 * @returns Yup validation schema
 */
export const createLoginValidationSchema = () => {
  return Yup.object({
    email: emailSchema,
    password: passwordSchema,
  });
};

/**
 * Create a validation schema for a registration form
 * @returns Yup validation schema
 */
export const createRegistrationValidationSchema = () => {
  return Yup.object({
    name: nameSchema,
    email: emailSchema,
    password: passwordSchema,
    confirmPassword: confirmPasswordSchema('password'),
    phone: phoneSchema,
  });
};

/**
 * Create a validation schema for a forgot password form
 * @returns Yup validation schema
 */
export const createForgotPasswordValidationSchema = () => {
  return Yup.object({
    email: emailSchema,
  });
};

/**
 * Create a validation schema for a reset password form
 * @returns Yup validation schema
 */
export const createResetPasswordValidationSchema = () => {
  return Yup.object({
    password: passwordSchema,
    confirmPassword: confirmPasswordSchema('password'),
  });
};

/**
 * Create a validation schema for a product form
 * @returns Yup validation schema
 */
export const createProductValidationSchema = () => {
  return Yup.object({
    name: nameSchema,
    category: requiredStringSchema,
    price: amountSchema,
    stock: quantitySchema,
    brand: optionalStringSchema,
    description: optionalStringSchema,
    barcode: optionalStringSchema,
  });
};

/**
 * Create a validation schema for a customer form
 * @returns Yup validation schema
 */
export const createCustomerValidationSchema = () => {
  return Yup.object({
    name: nameSchema,
    phone: phoneSchema,
    email: emailSchema.notRequired(),
    address: optionalStringSchema,
  });
};

/**
 * Create a validation schema for a supplier form
 * @returns Yup validation schema
 */
export const createSupplierValidationSchema = () => {
  return Yup.object({
    name: nameSchema,
    contact_person: nameSchema,
    phone: phoneSchema,
    email: emailSchema.notRequired(),
    address: optionalStringSchema,
  });
};

/**
 * Create a validation schema for a sale form
 * @returns Yup validation schema
 */
export const createSaleValidationSchema = () => {
  return Yup.object({
    customer_id: Yup.number().nullable(),
    items: Yup.array()
      .of(
        Yup.object({
          product_id: Yup.number().required('Product is required'),
          quantity: quantitySchema,
          price: amountSchema,
          discount: Yup.number().min(0, 'Discount must be positive or zero').nullable(),
        })
      )
      .min(1, 'At least one item is required'),
    discount: Yup.number().min(0, 'Discount must be positive or zero').nullable(),
    tax: Yup.number().min(0, 'Tax must be positive or zero').nullable(),
    payment_method: requiredStringSchema,
    payment_details: Yup.mixed().when(['payment_method'], {
      is: (payment_method: string) => payment_method !== 'cash',
      then: () => Yup.object().required('Payment details are required'),
      otherwise: () => Yup.mixed().nullable(),
    }),
    status: requiredStringSchema,
    notes: optionalStringSchema,
  });
};

/**
 * Create a validation schema for a stock adjustment form
 * @returns Yup validation schema
 */
export const createStockAdjustmentValidationSchema = () => {
  return Yup.object({
    product_id: Yup.number().required('Product is required'),
    adjustment_type: Yup.string()
      .oneOf(['increase', 'decrease'], 'Invalid adjustment type')
      .required('Adjustment type is required'),
    quantity: quantitySchema,
    reason: requiredStringSchema,
    notes: optionalStringSchema,
  });
};

/**
 * Create a validation schema for a stock return form
 * @returns Yup validation schema
 */
export const createStockReturnValidationSchema = () => {
  return Yup.object({
    supplier_id: Yup.number().required('Supplier is required'),
    reference_number: optionalStringSchema,
    items: Yup.array()
      .of(
        Yup.object({
          product_id: Yup.number().required('Product is required'),
          quantity: quantitySchema,
          price: amountSchema,
          reason: requiredStringSchema,
          notes: optionalStringSchema,
        })
      )
      .min(1, 'At least one item is required'),
    notes: optionalStringSchema,
  });
};

/**
 * Create a validation schema for an expense form
 * @returns Yup validation schema
 */
export const createExpenseValidationSchema = () => {
  return Yup.object({
    category: requiredStringSchema,
    amount: amountSchema,
    payment_method: requiredStringSchema,
    payment_details: Yup.mixed().when('payment_method', ([value]) => {
      return value !== 'cash' 
        ? Yup.object().required('Payment details are required')
        : Yup.mixed().nullable();
    }),
    recipient: requiredStringSchema,
    receipt_number: optionalStringSchema,
    notes: optionalStringSchema,
  });
};

/**
 * Create a validation schema for a deposit form
 * @returns Yup validation schema
 */
export const createDepositValidationSchema = () => {
  return Yup.object({
    amount: amountSchema,
    deposit_method: requiredStringSchema,
    deposit_details: Yup.mixed().required('Deposit details are required'),
    bank_name: requiredStringSchema,
    account_number: requiredStringSchema,
    reference_number: optionalStringSchema,
    notes: optionalStringSchema,
  });
};

// For batch sale validation
export const batchSaleValidationSchema = Yup.object().shape({
  // ... other fields
  payment_method: requiredStringSchema,
  payment_details: Yup.mixed().when('payment_method', ([value]) => {
    return value !== 'cash' 
      ? Yup.object().required('Payment details are required')
      : Yup.mixed().nullable();
  }),
  // ... other fields
});

export default {
  emailSchema,
  passwordSchema,
  confirmPasswordSchema,
  nameSchema,
  phoneSchema,
  amountSchema,
  quantitySchema,
  dateSchema,
  requiredStringSchema,
  optionalStringSchema,
  requiredSelectSchema,
  requiredArraySchema,
  createLoginValidationSchema,
  createRegistrationValidationSchema,
  createForgotPasswordValidationSchema,
  createResetPasswordValidationSchema,
  createProductValidationSchema,
  createCustomerValidationSchema,
  createSupplierValidationSchema,
  createSaleValidationSchema,
  createStockAdjustmentValidationSchema,
  createStockReturnValidationSchema,
  createExpenseValidationSchema,
  createDepositValidationSchema,
  batchSaleValidationSchema,
};