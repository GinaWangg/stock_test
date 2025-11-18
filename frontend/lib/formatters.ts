/**
 * Format revenue in 元 to 億元 with 2 decimal places and thousand separators
 * @param revenue Revenue in 元 (NTD)
 * @returns Formatted string like "1,234.56"
 */
export function formatRevenue(revenue: number | null): string {
  if (revenue === null || revenue === undefined) {
    return '—';
  }
  
  // Convert to 億元
  const revenueInBillion = revenue / 100_000_000;
  
  // Format with 2 decimal places and thousand separators
  return revenueInBillion.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

/**
 * Format percentage with + or - sign
 * @param pct Percentage value
 * @returns Formatted string like "+5.12%" or "-2.34%"
 */
export function formatPercentage(pct: number | null): string {
  if (pct === null || pct === undefined) {
    return '—';
  }
  
  const sign = pct > 0 ? '+' : pct < 0 ? '' : '';
  return `${sign}${pct.toFixed(2)}%`;
}

/**
 * Get color class for percentage value
 * @param pct Percentage value
 * @returns Tailwind color class
 */
export function getPercentageColor(pct: number | null): string {
  if (pct === null || pct === undefined) {
    return 'text-gray-500';
  }
  
  if (pct > 0) {
    return 'text-red-600'; // Red for positive (up) in Taiwan stock market
  } else if (pct < 0) {
    return 'text-green-600'; // Green for negative (down) in Taiwan stock market
  }
  
  return 'text-gray-500';
}

/**
 * Format price with thousand separators
 * @param price Price value
 * @returns Formatted string
 */
export function formatPrice(price: number | null): string {
  if (price === null || price === undefined) {
    return '—';
  }
  
  return price.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}
