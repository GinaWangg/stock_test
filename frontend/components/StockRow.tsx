import React from 'react';
import { WatchlistItem } from '@/lib/api';
import { formatRevenue, formatPercentage, getPercentageColor, formatPrice } from '@/lib/formatters';

interface StockRowProps {
  item: WatchlistItem;
  onDelete: (stockId: string) => void;
}

export default function StockRow({ item, onDelete }: StockRowProps) {
  return (
    <tr className="border-b hover:bg-gray-50">
      <td className="px-4 py-3">
        <div className="flex items-center gap-2">
          {item.is_new && (
            <span className="px-2 py-0.5 text-xs font-semibold text-white bg-blue-500 rounded">
              NEW
            </span>
          )}
          <div>
            <div className="font-semibold text-gray-900">{item.stock_id}</div>
            <div className="text-sm text-gray-600">{item.name_zh}</div>
          </div>
        </div>
      </td>
      
      <td className="px-4 py-3 text-right">
        <div className="font-medium">{formatRevenue(item.last_month_revenue)}</div>
        <div className={`text-sm ${getPercentageColor(item.last_month_yoy)}`}>
          {formatPercentage(item.last_month_yoy)}
        </div>
      </td>
      
      <td className="px-4 py-3 text-right">
        <div className="font-medium">{formatRevenue(item.prev_month_revenue)}</div>
        <div className={`text-sm ${getPercentageColor(item.prev_month_yoy)}`}>
          {formatPercentage(item.prev_month_yoy)}
        </div>
      </td>
      
      <td className="px-4 py-3 text-right">
        <div className="font-medium">{formatRevenue(item.last_quarter_revenue)}</div>
        <div className={`text-sm ${getPercentageColor(item.last_quarter_yoy)}`}>
          {formatPercentage(item.last_quarter_yoy)}
        </div>
      </td>
      
      <td className="px-4 py-3 text-right">
        {item.current_price ? (
          <>
            <div className="font-medium">{formatPrice(item.current_price.price)}</div>
            <div className={`text-sm ${getPercentageColor(item.current_price.pct)}`}>
              {formatPercentage(item.current_price.pct)}
            </div>
            <div className="text-xs text-gray-500">{item.current_price.time || '—'}</div>
          </>
        ) : (
          <div className="text-gray-400">—</div>
        )}
      </td>
      
      <td className="px-4 py-3 text-center">
        <button
          onClick={() => onDelete(item.stock_id)}
          className="px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded transition-colors"
        >
          刪除
        </button>
      </td>
    </tr>
  );
}
