import React from 'react';
import { WatchlistItem } from '@/lib/api';
import StockRow from './StockRow';

interface WatchlistTableProps {
  items: WatchlistItem[];
  onDelete: (stockId: string) => void;
}

export default function WatchlistTable({ items, onDelete }: WatchlistTableProps) {
  return (
    <div className="overflow-x-auto bg-white rounded-lg shadow">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              股票代碼/名稱
            </th>
            <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              上個月營收 (億) / YoY
            </th>
            <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              上上個月營收 (億) / YoY
            </th>
            <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              上一季營收 (億) / YoY
            </th>
            <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              當前股價 / 漲跌%
            </th>
            <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
              操作
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {items.length === 0 ? (
            <tr>
              <td colSpan={6} className="px-4 py-8 text-center text-gray-500">
                目前追蹤清單為空，請新增股票
              </td>
            </tr>
          ) : (
            items.map((item) => (
              <StockRow key={item.stock_id} item={item} onDelete={onDelete} />
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
