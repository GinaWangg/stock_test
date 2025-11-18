import React from 'react';
import { WatchlistItem } from '@/lib/api';
import StockCard from './StockCard';

interface WatchlistCardsProps {
  items: WatchlistItem[];
  onDelete: (stockId: string) => void;
}

export default function WatchlistCards({ items, onDelete }: WatchlistCardsProps) {
  if (items.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        目前追蹤清單為空，請新增股票
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {items.map((item) => (
        <StockCard key={item.stock_id} item={item} onDelete={onDelete} />
      ))}
    </div>
  );
}
