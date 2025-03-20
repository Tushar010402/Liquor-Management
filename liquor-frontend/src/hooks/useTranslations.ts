import { useTranslation } from 'react-i18next';

/**
 * Custom hook for using translations with type safety
 * @returns Translation functions
 */
function useTranslations() {
  const { t, i18n } = useTranslation();

  /**
   * Translate a key with namespace
   * @param namespace Namespace
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const translate = (namespace: string, key: string, options?: any): string => {
    return t(`${namespace}.${key}`, options);
  };

  /**
   * Translate a common key
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const common = (key: string, options?: any): string => {
    return translate('common', key, options);
  };

  /**
   * Translate an auth key
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const auth = (key: string, options?: any): string => {
    return translate('auth', key, options);
  };

  /**
   * Translate a dashboard key
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const dashboard = (key: string, options?: any): string => {
    return translate('dashboard', key, options);
  };

  /**
   * Translate a sales key
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const sales = (key: string, options?: any): string => {
    return translate('sales', key, options);
  };

  /**
   * Translate a products key
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const products = (key: string, options?: any): string => {
    return translate('products', key, options);
  };

  /**
   * Translate a customers key
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const customers = (key: string, options?: any): string => {
    return translate('customers', key, options);
  };

  /**
   * Translate a suppliers key
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const suppliers = (key: string, options?: any): string => {
    return translate('suppliers', key, options);
  };

  /**
   * Translate a cash key
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const cash = (key: string, options?: any): string => {
    return translate('cash', key, options);
  };

  /**
   * Translate a returns key
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const returns = (key: string, options?: any): string => {
    return translate('returns', key, options);
  };

  /**
   * Translate a settings key
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const settings = (key: string, options?: any): string => {
    return translate('settings', key, options);
  };

  /**
   * Translate a users key
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const users = (key: string, options?: any): string => {
    return translate('users', key, options);
  };

  /**
   * Translate a roles key
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const roles = (key: string, options?: any): string => {
    return translate('roles', key, options);
  };

  /**
   * Translate a shops key
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const shops = (key: string, options?: any): string => {
    return translate('shops', key, options);
  };

  /**
   * Translate a tenants key
   * @param key Translation key
   * @param options Translation options
   * @returns Translated string
   */
  const tenants = (key: string, options?: any): string => {
    return translate('tenants', key, options);
  };

  return {
    t,
    i18n,
    translate,
    common,
    auth,
    dashboard,
    sales,
    products,
    customers,
    suppliers,
    cash,
    returns,
    settings,
    users,
    roles,
    shops,
    tenants,
  };
}

export default useTranslations;