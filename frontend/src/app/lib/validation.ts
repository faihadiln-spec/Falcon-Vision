const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const SAUDI_MOBILE_PATTERN = /^05\d{8}$/;

export function isValidEmail(email: string) {
  return EMAIL_PATTERN.test(email.trim());
}

export function isValidSaudiMobile(phone: string) {
  return SAUDI_MOBILE_PATTERN.test(phone.trim());
}

export function validateRequiredFields(fields: Array<{ label: string; value: string }>) {
  const missingFields = fields
    .filter((field) => !field.value.trim())
    .map((field) => field.label);

  if (missingFields.length === 0) {
    return null;
  }

  return `Please fill in: ${missingFields.join(', ')}.`;
}
