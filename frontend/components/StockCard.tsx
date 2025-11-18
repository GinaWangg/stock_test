import React from 'react';
import { WatchlistItem } from '@/lib/api';
import { formatRevenue, formatPercentage, getPercentageColor, formatPrice } from '@/lib/formatters';

interface StockCardProps {
  item: WatchlistItem;
  onDelete: (stockId: string) => void;
}

export default function StockCard({ item, onDelete }: StockCardProps) {
  return (
    <div className="bg-white border rounded-lg shadow-sm p-4 mb-3">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-bold text-gray-900">{item.stock_id}</h3>
            {item.is_new && (
              <span className="px-2 py-0.5 text-xs font-semibold text-white bg-blue-500 rounded">
                NEW
              </span>
            )}
          </div>
          <p className="text-sm text-gray-600">{item.name_zh}</p>
        </div>
        <button
          onClick={() => onDelete(item.stock_id)}
          className="px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded transition-colors"
        >
          刪除
        </button>
      </div>

      {/* Data Grid */}
      <div className="space-y-3">
        {/* Last Month Revenue */}
        <div className="flex justify-between items-start">
          <span className="text-sm text-gray-600">上個月營收</span>
          <div className="text-right">
            <div className="font-semibold">{formatRevenue(item.last_month_revenue)} 億</div>
            <div className={`text-sm ${getPercentageColor(item.last_month_yoy)}`}>
              {formatPercentage(item.last_month_yoy)}
            </div>
          </div>
        </div>

        {/* Previous Month Revenue */}
        <div className="flex justify-between items-start">
          <span className="text-sm text-gray-600">上上個月營收</span>
          <div className="text-right">
            <div className="font-semibold">{formatRevenue(item.prev_month_revenue)} 億</div>
            <div className={`text-sm ${getPercentageColor(item.prev_month_yoy)}`}>
              {formatPercentage(item.prev_month_yoy)}
            </div>
          </div>
        </div>

        {/* Last Quarter Revenue */}
        <div className="flex justify-between items-start">
          <span className="text-sm text-gray-600">上一季營收</span>
          <div className="text-right">
            <div className="font-semibold">{formatRevenue(item.last_quarter_revenue)} 億</div>
            <div className={`text-sm ${getPercentageColor(item.last_quarter_yoy)}`}>
              {formatPercentage(item.last_quarter_yoy)}
            </div>
          </div>
        </div>

        {/* Current Price */}
        <div className="flex justify-between items-start pt-2 border-t">
          <span className="text-sm text-gray-600">當前股價</span>
          {item.current_price ? (
            <div className="text-right">
              <div className="font-semibold">{formatPrice(item.current_price.price)}</div>
              <div className={`text-sm ${getPercentageColor(item.current_price.pct)}`}>
                {formatPercentage(item.current_price.pct)}
              </div>
              <div className="text-xs text-gray-500">{item.current_price.time || '—'}</div>
            </div>
          ) : (
            <div className="text-gray-400">—</div>
          )}
        </div>
      </div>
    </div>
  );
}
